"""Runtime de plugins: Event Bus + Plugin Engine singletons."""
from pathlib import Path

from ..config import settings
from .engine import PluginEngine
from .eventbus import AOSEvent, EventBus, build_event_bus
from .loader import PluginContext, load_plugins as _load
from .manifest import PluginManifest

event_bus: EventBus = build_event_bus(settings.EVENT_BUS_BACKEND, settings.REDIS_URL, settings.KAFKA_BOOTSTRAP_SERVERS)
plugin_engine = PluginEngine(event_bus)


def load_plugins(app):
    plugins_dir = (Path(__file__).resolve().parents[2] / settings.PLUGINS_DIR).resolve()
    return _load(app, plugin_engine, plugins_dir, settings.API_PREFIX)


__all__ = ["AOSEvent", "EventBus", "PluginContext", "PluginEngine", "PluginManifest", "event_bus", "plugin_engine", "load_plugins"]
