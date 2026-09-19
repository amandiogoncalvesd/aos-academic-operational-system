"""Descoberta e carregamento dinâmico de plugins a partir de plugins/*/manifest.json."""
from __future__ import annotations

import importlib
import importlib.util
import logging
import sys
from pathlib import Path

from fastapi import FastAPI

from .engine import LoadedPlugin, PluginEngine
from .manifest import PluginManifest

log = logging.getLogger("aos.plugins.loader")


def discover_plugins(plugins_dir: Path) -> list[Path]:
    if not plugins_dir.exists():
        return []
    return sorted(p for p in plugins_dir.iterdir() if (p / "manifest.json").is_file())


def load_plugin_manifest(plugin_path: Path) -> PluginManifest:
    return PluginManifest.from_file(plugin_path / "manifest.json")


def validate_plugin(manifest: PluginManifest, known: set[str]) -> list[str]:
    errors: list[str] = []
    if not manifest.id.startswith("aos-"):
        errors.append("id deve começar por 'aos-'")
    for dep in manifest.dependencies:
        if dep != "core" and dep not in known:
            errors.append(f"dependência em falta: {dep}")
    return errors


def _topo_sort(manifests: list[PluginManifest]) -> list[PluginManifest]:
    by_id = {m.id: m for m in manifests}
    seen: set[str] = set()
    out: list[PluginManifest] = []

    def visit(m: PluginManifest, stack: tuple = ()):
        if m.id in seen:
            return
        if m.id in stack:
            raise RuntimeError(f"dependência circular: {' -> '.join(stack + (m.id,))}")
        for dep in m.dependencies:
            if dep in by_id:
                visit(by_id[dep], stack + (m.id,))
        seen.add(m.id)
        out.append(m)

    for m in manifests:
        visit(m)
    return out


def _import_entrypoint(manifest: PluginManifest):
    mod_name, _, fn_name = manifest.entrypoint.partition(":")
    pkg_name = manifest.id.replace("-", "_")
    root = manifest.path
    if str(root.parent) not in sys.path:
        sys.path.insert(0, str(root.parent))
    # plugin dir pode ter hífens → registar como pacote com nome seguro
    spec = importlib.util.spec_from_file_location(pkg_name, root / "__init__.py", submodule_search_locations=[str(root)])
    if pkg_name not in sys.modules:
        module = importlib.util.module_from_spec(spec)
        sys.modules[pkg_name] = module
        spec.loader.exec_module(module)
    target = importlib.import_module(f"{pkg_name}.{mod_name}")
    return getattr(target, fn_name or "register")


def register_plugin(app: FastAPI, engine: PluginEngine, manifest: PluginManifest, api_prefix: str) -> LoadedPlugin:
    plugin = LoadedPlugin(manifest=manifest)
    try:
        register = _import_entrypoint(manifest)
        ctx = PluginContext(app=app, engine=engine, manifest=manifest, plugin=plugin)
        register(ctx)
        if plugin.router is not None:
            prefix = manifest.api.prefix or f"/{manifest.id.split('-')[-1]}"
            app.include_router(plugin.router, prefix=f"{api_prefix}{prefix}", tags=[manifest.name])
        plugin.status = "active"
        log.info("plugin %s v%s activo", manifest.id, manifest.version)
    except Exception as exc:  # plugin com erro nunca derruba o core
        plugin.status, plugin.error = "error", f"{type(exc).__name__}: {exc}"
        log.exception("falha ao carregar plugin %s", manifest.id)
    engine.register(plugin)
    return plugin


class PluginContext:
    """Objecto entregue ao `register(ctx)` de cada plugin."""

    def __init__(self, app: FastAPI, engine: PluginEngine, manifest: PluginManifest, plugin: LoadedPlugin):
        self.app, self.engine, self.manifest, self._plugin = app, engine, manifest, plugin
        self.bus = engine.bus

    def add_router(self, router) -> None:
        self._plugin.router = router

    def add_models(self, *models) -> None:
        self._plugin.models.extend(models)

    def on_event(self, *event_types: str):
        return self.bus.on(*event_types)

    def action(self, name: str, priority: int = 10):
        return self.engine.action(name, priority, plugin_id=self.manifest.id)

    def filter(self, name: str, priority: int = 10):
        return self.engine.filter(name, priority, plugin_id=self.manifest.id)


def load_plugins(app: FastAPI, engine: PluginEngine, plugins_dir: Path, api_prefix: str) -> list[LoadedPlugin]:
    manifests = []
    for path in discover_plugins(plugins_dir):
        try:
            manifests.append(load_plugin_manifest(path))
        except Exception:
            log.exception("manifest inválido em %s", path)
    known = {m.id for m in manifests}
    valid = []
    for m in manifests:
        errs = validate_plugin(m, known)
        if errs:
            log.error("plugin %s ignorado: %s", m.id, "; ".join(errs))
            engine.register(LoadedPlugin(manifest=m, status="error", error="; ".join(errs)))
        else:
            valid.append(m)
    return [register_plugin(app, engine, m, api_prefix) for m in _topo_sort(valid)]
