"""Contrato do manifest.json de um plugin AOS."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


@dataclass
class PluginHooks:
    actions: list[str] = field(default_factory=list)
    filters: list[str] = field(default_factory=list)


@dataclass
class PluginEvents:
    publishes: list[str] = field(default_factory=list)
    subscribes: list[str] = field(default_factory=list)


@dataclass
class PluginDatabase:
    tables: list[str] = field(default_factory=list)
    migrations: str | None = None


@dataclass
class PluginApi:
    prefix: str | None = None
    module: str | None = None  # ex: "src.routes:router"


@dataclass
class PluginFrontend:
    entry: str | None = None
    mount_point: str | None = None
    routes: list[str] = field(default_factory=list)
    nav: list[dict] = field(default_factory=list)


@dataclass
class PluginManifest:
    id: str
    name: str
    version: str
    author: str = "AOS Core Team"
    description: str = ""
    license: str = "MIT"
    type: Literal["core", "domain", "extension"] = "domain"
    dependencies: dict[str, str] = field(default_factory=dict)
    optional_dependencies: dict[str, str] = field(default_factory=dict)
    hooks: PluginHooks = field(default_factory=PluginHooks)
    events: PluginEvents = field(default_factory=PluginEvents)
    permissions: list[str] = field(default_factory=list)
    database: PluginDatabase = field(default_factory=PluginDatabase)
    api: PluginApi = field(default_factory=PluginApi)
    frontend: PluginFrontend = field(default_factory=PluginFrontend)
    entrypoint: str = "src.plugin:register"  # função chamada no load
    path: Path | None = None

    @classmethod
    def from_dict(cls, d: dict, path: Path | None = None) -> PluginManifest:
        return cls(
            id=d["id"], name=d["name"], version=d.get("version", "0.0.1"),
            author=d.get("author", "AOS Core Team"), description=d.get("description", ""),
            license=d.get("license", "MIT"), type=d.get("type", "domain"),
            dependencies=d.get("dependencies", {}), optional_dependencies=d.get("optional_dependencies", {}),
            hooks=PluginHooks(**d.get("hooks", {})), events=PluginEvents(**d.get("events", {})),
            permissions=d.get("permissions", []), database=PluginDatabase(**d.get("database", {})),
            api=PluginApi(**d.get("api", {})), frontend=PluginFrontend(**d.get("frontend", {})),
            entrypoint=d.get("entrypoint", "src.plugin:register"), path=path,
        )

    @classmethod
    def from_file(cls, file: Path) -> PluginManifest:
        return cls.from_dict(json.loads(file.read_text(encoding="utf-8")), path=file.parent)

    def to_public(self) -> dict:
        return {
            "id": self.id, "name": self.name, "version": self.version, "author": self.author,
            "description": self.description, "type": self.type, "permissions": self.permissions,
            "api_prefix": self.api.prefix, "frontend": self.frontend.__dict__,
            "events": self.events.__dict__,
        }
