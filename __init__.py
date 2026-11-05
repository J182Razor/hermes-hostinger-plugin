from __future__ import annotations

import os
import importlib.util

_HERE = os.path.dirname(os.path.abspath(__file__))

def _load(name, filename):
    path = os.path.join(_HERE, filename)
    spec = importlib.util.spec_from_file_location(f"_hostinger_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

schemas = _load("schemas", "schemas.py")
tools = _load("tools", "tools.py")

_TOOLS = [
    ("list_vps", schemas.LIST_VPS_SCHEMA, tools.handle_list_vps),
    ("vps_action", schemas.VPS_ACTION_SCHEMA, tools.handle_vps_action),
    ("vps_snapshots", schemas.VPS_SNAPSHOTS_SCHEMA, tools.handle_vps_snapshots),
    ("vps_firewall", schemas.VPS_FIREWALL_SCHEMA, tools.handle_vps_firewall),
    ("list_domains", schemas.LIST_DOMAINS_SCHEMA, tools.handle_list_domains),
    ("dns_records", schemas.DNS_RECORDS_SCHEMA, tools.handle_dns_records),
    ("ssl_status", schemas.SSL_STATUS_SCHEMA, tools.handle_ssl_status),
    ("deploy", schemas.DEPLOY_SCHEMA, tools.handle_deploy),
    ("billing_summary", schemas.BILLING_SUMMARY_SCHEMA, tools.handle_billing_summary),
    ("list_hosting", schemas.LIST_HOSTING_SCHEMA, tools.handle_list_hosting),
]


def register(ctx) -> None:
    for name, schema, handler in _TOOLS:
        ctx.register_tool(name=name, toolset="hostinger", schema=schema, handler=handler)
