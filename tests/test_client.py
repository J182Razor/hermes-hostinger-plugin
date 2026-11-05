import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

PLUGIN_ROOT = Path("C:/Users/Lawa4721/scratchpad/hackathon/hostinger")
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

import client


def test_request_success():
    mock_resp = MagicMock()
    mock_resp.is_success = True
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"ok": True}
    with patch("httpx.Client") as mc:
        instance = mc.return_value.__enter__.return_value
        instance.request.return_value = mock_resp
        res = client.request("GET", "/test")
    assert res["success"] is True
    assert res["data"] == {"ok": True}
