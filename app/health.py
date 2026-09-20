import ssl
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from config import HEALTH_CHECK_TIMEOUT, HEALTH_CHECK_TTL, HEALTH_STRICT

_cache: dict[str, Any] = {
    "at": 0.0,
    "services": {},
}

_AUTH_PROTECTED_CODES = frozenset({401, 403})


def _status_ok(status_code: int, *, strict: bool) -> bool:
    if 200 <= status_code < 400:
        return True
    if not strict and status_code in _AUTH_PROTECTED_CODES:
        return True
    return False


def _probe_url(url: str, *, strict: bool = HEALTH_STRICT) -> bool:
    ctx = ssl.create_default_context()
    request = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "krivoruchko-dev-dashboard/1.0"},
    )
    try:
        with urllib.request.urlopen(
            request, timeout=HEALTH_CHECK_TIMEOUT, context=ctx
        ) as response:
            return _status_ok(response.status, strict=strict)
    except urllib.error.HTTPError as exc:
        if exc.code in (405, 501):
            return _probe_url_get(url, ctx, strict=strict)
        return _status_ok(exc.code, strict=strict)
    except (urllib.error.URLError, TimeoutError, OSError):
        return _probe_url_get(url, ctx, strict=strict)


def _probe_url_get(url: str, ctx: ssl.SSLContext, *, strict: bool) -> bool:
    request = urllib.request.Request(
        url,
        method="GET",
        headers={"User-Agent": "krivoruchko-dev-dashboard/1.0"},
    )
    try:
        with urllib.request.urlopen(
            request, timeout=HEALTH_CHECK_TIMEOUT, context=ctx
        ) as response:
            return _status_ok(response.status, strict=strict)
    except urllib.error.HTTPError as exc:
        return _status_ok(exc.code, strict=strict)
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def check_services(
    services: dict[str, dict[str, Any]], force: bool = False
) -> dict[str, bool]:
    now = time.monotonic()
    if (
        not force
        and _cache["at"]
        and now - _cache["at"] < HEALTH_CHECK_TTL
        and _cache["services"]
    ):
        return dict(_cache["services"])

    statuses: dict[str, bool] = {}
    if not services:
        _cache.update(at=now, services=statuses)
        return statuses

    with ThreadPoolExecutor(max_workers=min(8, len(services))) as executor:
        futures = {
            executor.submit(
                _probe_url,
                svc["url"],
                strict=False
            ): service_id
            for service_id, svc in services.items()
        }
        for future in as_completed(futures):
            service_id = futures[future]
            try:
                statuses[service_id] = future.result()
            except Exception:
                statuses[service_id] = False

    _cache.update(at=now, services=statuses)
    return statuses
