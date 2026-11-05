from __future__ import annotations

import os
from typing import Any, Dict, Optional

import httpx

try:
    from agent.secret_scope import get_secret
except Exception:
    try:
        from secret_scope import get_secret
    except Exception:
        def get_secret(name, default=None):
            import os
            return os.environ.get(name, default)


DEFAULT_BASE_URL = "https://developers.hostinger.com/api"


def get_base_url() -> str:
    return os.environ.get("HOSTINGER_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def get_token() -> Optional[str]:
    return get_secret("HOSTINGER_API_TOKEN")


def _headers() -> Dict[str, str]:
    token = get_token()
    h = {"Accept": "application/json", "Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def request(method: str, path: str, *, params=None, json=None, timeout: int = 30) -> Dict[str, Any]:
    url = get_base_url() + "/" + path.lstrip("/")
    try:
        with httpx.Client(timeout=timeout) as client:
            resp = client.request(method, url, params=params, json=json, headers=_headers())
        try:
            data = resp.json()
        except Exception:
            data = resp.text
        return {"success": resp.is_success, "status": resp.status_code, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}
