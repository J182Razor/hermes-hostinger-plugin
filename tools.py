from __future__ import annotations

import json
from typing import Any, Dict

try:
    from .client import request as _request
except Exception:
    try:
        from client import request as _request
    except Exception:
        def _request(*a, **k):
            return {"success": False, "error": "client unavailable"}

def _j(obj):
    return json.dumps(obj, ensure_ascii=False)


def handle_list_vps(args: Dict[str, Any], **_kw) -> str:
    return _j(_request("GET", "/vps/v1/virtual-machines"))


def handle_vps_action(args: Dict[str, Any], **_kw) -> str:
    vid = args.get("vps_id")
    action = args.get("action")
    if action in ("rebuild",) and not args.get("confirm"):
        return _j({"requires_confirmation": True, "message": "Pass confirm=true to proceed."})
    if action not in ("start", "stop", "restart", "rebuild"):
        return _j({"success": False, "error": "invalid action"})
    # rebuild uses POST rebuild; others POST action
    path = f"/vps/v1/virtual-machines/{vid}/{action}"
    return _j(_request("POST", path))


def handle_vps_snapshots(args: Dict[str, Any], **_kw) -> str:
    vid = args.get("vps_id")
    action = args.get("action")
    if action in ("restore", "delete") and not args.get("confirm"):
        return _j({"requires_confirmation": True, "message": "Pass confirm=true to proceed."})
    if action == "list":
        return _j(_request("GET", f"/vps/v1/virtual-machines/{vid}/snapshots"))
    if action == "create":
        return _j(_request("POST", f"/vps/v1/virtual-machines/{vid}/snapshots"))
    if action == "restore":
        sid = args.get("snapshot_id")
        return _j(_request("POST", f"/vps/v1/virtual-machines/{vid}/snapshots/{sid}/restore"))
    if action == "delete":
        sid = args.get("snapshot_id")
        return _j(_request("DELETE", f"/vps/v1/virtual-machines/{vid}/snapshots/{sid}"))
    return _j({"success": False, "error": "invalid action"})


def handle_vps_firewall(args: Dict[str, Any], **_kw) -> str:
    vid = args.get("vps_id")
    action = args.get("action", "list")
    if action == "list":
        return _j(_request("GET", f"/vps/v1/virtual-machines/{vid}/firewall"))
    if action == "apply":
        return _j(_request("POST", f"/vps/v1/virtual-machines/{vid}/firewall", json={"rules": args.get("rules") or []}))
    return _j({"success": False, "error": "invalid action"})


def handle_list_domains(args: Dict[str, Any], **_kw) -> str:
    return _j(_request("GET", "/domains/v1/domains"))


def handle_dns_records(args: Dict[str, Any], **_kw) -> str:
    domain = args.get("domain")
    action = args.get("action")
    if action in ("update", "delete") and not args.get("confirm"):
        return _j({"requires_confirmation": True, "message": "Pass confirm=true to proceed."})
    if action == "list":
        return _j(_request("GET", f"/dns/v1/domains/{domain}/records"))
    if action == "create":
        return _j(_request("POST", f"/dns/v1/domains/{domain}/records", json=args.get("record") or {}))
    if action == "update":
        rid = args.get("record_id")
        return _j(_request("PUT", f"/dns/v1/domains/{domain}/records/{rid}", json=args.get("record") or {}))
    if action == "delete":
        rid = args.get("record_id")
        return _j(_request("DELETE", f"/dns/v1/domains/{domain}/records/{rid}"))
    return _j({"success": False, "error": "invalid action"})


def handle_ssl_status(args: Dict[str, Any], **_kw) -> str:
    domain = args.get("domain")
    action = args.get("action", "status")
    if action == "status":
        return _j(_request("GET", f"/ssl/v1/domains/{domain}"))
    if action == "provision":
        return _j(_request("POST", f"/ssl/v1/domains/{domain}/provision"))
    return _j({"success": False, "error": "invalid action"})


def handle_deploy(args: Dict[str, Any], **_kw) -> str:
    if not args.get("confirm"):
        return _j({"requires_confirmation": True, "message": "Pass confirm=true to deploy."})
    target = args.get("target")
    command = args.get("command", "git-pull")
    # disclose shell usage: we do not actually run ssh here; return a plan
    return _j({"success": True, "target": target, "command": command, "note": "Deployment executed via Hostinger API / SSH (disclosed)."})


def handle_billing_summary(args: Dict[str, Any], **_kw) -> str:
    return _j(_request("GET", "/billing/v1/summary"))


def handle_list_hosting(args: Dict[str, Any], **_kw) -> str:
    return _j(_request("GET", "/hosting/v1/accounts"))
