from __future__ import annotations

def _schema(name, description, properties=None, required=None):
    params = {"type": "object", "properties": properties or {}}
    if required:
        params["required"] = required
    params["additionalProperties"] = False
    return {"name": name, "description": description, "parameters": params}

def _str(d):
    return {"type": "string", "description": d}

LIST_VPS_SCHEMA = _schema("list_vps", "List VPS instances.")
VPS_ACTION_SCHEMA = _schema("vps_action", "Start/stop/restart/rebuild a VPS.", {
    "vps_id": _str("VPS id."),
    "action": _str("start|stop|restart|rebuild"),
    "confirm": {"type": "boolean", "description": "Confirm destructive action."},
}, required=["vps_id", "action"])
VPS_SNAPSHOTS_SCHEMA = _schema("vps_snapshots", "List/create/restore/delete snapshots.", {
    "vps_id": _str("VPS id."),
    "action": _str("list|create|restore|delete"),
    "snapshot_id": _str("Snapshot id for restore/delete."),
    "confirm": {"type": "boolean", "description": "Confirm destructive action."},
}, required=["vps_id", "action"])
VPS_FIREWALL_SCHEMA = _schema("vps_firewall", "List or apply firewall rules.", {
    "vps_id": _str("VPS id."),
    "action": _str("list|apply"),
    "rules": {"type": "array", "items": {"type": "object"}, "description": "Rules for apply."},
})
LIST_DOMAINS_SCHEMA = _schema("list_domains", "List domains.")
DNS_RECORDS_SCHEMA = _schema("dns_records", "List/create/update/delete DNS records.", {
    "domain": _str("Domain name."),
    "action": _str("list|create|update|delete"),
    "record": {"type": "object", "description": "Record payload."},
    "record_id": _str("Record id for update/delete."),
    "confirm": {"type": "boolean", "description": "Confirm destructive action."},
}, required=["domain", "action"])
SSL_STATUS_SCHEMA = _schema("ssl_status", "Check or provision SSL.", {
    "domain": _str("Domain name."),
    "action": _str("status|provision"),
})
DEPLOY_SCHEMA = _schema("deploy", "Deploy via ssh/rsync/git-pull (requires confirm).", {
    "target": _str("Deploy target host or vps id."),
    "command": _str("git-pull|rsync"),
    "confirm": {"type": "boolean", "description": "Confirm deployment."},
}, required=["target"])
BILLING_SUMMARY_SCHEMA = _schema("billing_summary", "Billing/usage summary.")
LIST_HOSTING_SCHEMA = _schema("list_hosting", "List shared hosting accounts.")
