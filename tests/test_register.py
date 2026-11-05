import os
import sys
from pathlib import Path

PLUGIN_ROOT = Path("C:/Users/Lawa4721/scratchpad/hackathon/hostinger")
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

import __init__ as plugin


class _Ctx:
    def __init__(self):
        self.tools = []

    def register_tool(self, name=None, **kwargs):
        self.tools.append(name)


def test_register_tools():
    ctx = _Ctx()
    plugin.register(ctx)
    expected = {"list_vps", "vps_action", "vps_snapshots", "vps_firewall", "list_domains",
                "dns_records", "ssl_status", "deploy", "billing_summary", "list_hosting"}
    assert set(ctx.tools) == expected
