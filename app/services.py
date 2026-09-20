import json
import logging
from pathlib import Path
from typing import Any

from config import DEFAULT_ACCENT, SERVICES_FILE

logger = logging.getLogger(__name__)

_services_cache: dict[str, dict[str, Any]] | None = None
_services_cache_key: tuple[str, float] | None = None


def _normalize_service(service_id: str, raw: dict[str, Any]) -> dict[str, Any]:
    name = raw.get("name")
    url = raw.get("url")
    if not name or not url:
        raise ValueError(
            f"Service '{service_id}' must include non-empty 'name' and 'url'"
        )

    color = (raw.get("color") or "").strip() or DEFAULT_ACCENT

    normalized: dict[str, Any] = {
        "name": str(name),
        "url": str(url),
        "description": str(raw.get("description") or ""),
        "color": color,
        "icon": (raw.get("icon") or "").strip() or None,
    }
    return normalized


def load_services(path: Path | None = None) -> dict[str, dict[str, Any]]:
    global _services_cache, _services_cache_key

    services_path = path or SERVICES_FILE
    if not services_path.is_file():
        raise FileNotFoundError(f"Services file not found: {services_path}")

    resolved = str(services_path.resolve())
    mtime = services_path.stat().st_mtime
    cache_key = (resolved, mtime)
    if _services_cache is not None and _services_cache_key == cache_key:
        return _services_cache

    with services_path.open(encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("services.json must be a JSON object")

    services: dict[str, dict[str, Any]] = {}
    for service_id, raw in data.items():
        if not isinstance(raw, dict):
            logger.warning("Skipping service '%s': expected object", service_id)
            continue
        try:
            services[service_id] = _normalize_service(service_id, raw)
        except ValueError as exc:
            logger.warning("%s", exc)

    _services_cache = services
    _services_cache_key = cache_key
    return services
