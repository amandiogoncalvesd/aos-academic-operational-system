"""Plugin Engine — hooks tipados (actions & filters) inspirados no WordPress, + registo de plugins."""
from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from fastapi import APIRouter

from .eventbus import EventBus
from .manifest import PluginManifest

log = logging.getLogger("aos.plugins")


@dataclass(order=True)
class _Hook:
    priority: int
    order: int
    fn: Callable = field(compare=False)
    plugin_id: str = field(compare=False, default="core")


@dataclass
class LoadedPlugin:
    manifest: PluginManifest
    router: APIRouter | None = None
    models: list[type] = field(default_factory=list)
    status: str = "loaded"  # loaded | active | error | inactive
    error: str | None = None


class PluginEngine:
    def __init__(self, bus: EventBus) -> None:
        self.bus = bus
        self._actions: dict[str, list[_Hook]] = defaultdict(list)
        self._filters: dict[str, list[_Hook]] = defaultdict(list)
        self._counter = 0
        self.plugins: dict[str, LoadedPlugin] = {}
        self.nav: list[dict] = []  # itens de navegação expostos ao frontend

    # ---- Actions (notificação, sem retorno) ----
    def add_action(self, name: str, fn: Callable, priority: int = 10, plugin_id: str = "core") -> None:
        self._counter += 1
        self._actions[name].append(_Hook(priority, self._counter, fn, plugin_id))
        self._actions[name].sort()

    async def do_action(self, name: str, *args: Any, **kwargs: Any) -> None:
        for h in list(self._actions.get(name, [])):
            try:
                res = h.fn(*args, **kwargs)
                if asyncio.iscoroutine(res):
                    await res
            except Exception:
                log.exception("action %s (%s) falhou", name, h.plugin_id)

    # ---- Filters (transformação, encadeados) ----
    def add_filter(self, name: str, fn: Callable, priority: int = 10, plugin_id: str = "core") -> None:
        self._counter += 1
        self._filters[name].append(_Hook(priority, self._counter, fn, plugin_id))
        self._filters[name].sort()

    async def apply_filters(self, name: str, value: Any, *args: Any, **kwargs: Any) -> Any:
        for h in list(self._filters.get(name, [])):
            res = h.fn(value, *args, **kwargs)
            value = await res if asyncio.iscoroutine(res) else res
        return value

    # ---- Decorators de conveniência ----
    def action(self, name: str, priority: int = 10, plugin_id: str = "core"):
        def deco(fn):
            self.add_action(name, fn, priority, plugin_id)
            return fn
        return deco

    def filter(self, name: str, priority: int = 10, plugin_id: str = "core"):
        def deco(fn):
            self.add_filter(name, fn, priority, plugin_id)
            return fn
        return deco

    # ---- Registo de plugins ----
    def register(self, plugin: LoadedPlugin) -> None:
        self.plugins[plugin.manifest.id] = plugin
        self.nav.extend({**item, "plugin": plugin.manifest.id} for item in plugin.manifest.frontend.nav)

    def remove_plugin_hooks(self, plugin_id: str) -> None:
        for table in (self._actions, self._filters):
            for k in list(table):
                table[k] = [h for h in table[k] if h.plugin_id != plugin_id]
        self.nav = [n for n in self.nav if n.get("plugin") != plugin_id]

    def describe(self) -> dict:
        return {
            "plugins": {k: {"status": v.status, "version": v.manifest.version, "error": v.error}
                        for k, v in self.plugins.items()},
            "actions": {k: [h.plugin_id for h in v] for k, v in self._actions.items()},
            "filters": {k: [h.plugin_id for h in v] for k, v in self._filters.items()},
            "events": self.bus.subscriptions(),
        }
