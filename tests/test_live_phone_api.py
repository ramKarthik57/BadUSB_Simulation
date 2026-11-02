import sys
import json
import urllib.request
import pytest
from tests.cdp_client import get_target, MinimalCDP

def is_cdp_available():
    try:
        data = urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=0.5).read()
        tabs = json.loads(data)
        return any("10.85.248.29" in t.get("url", "") for t in tabs)
    except Exception:
        return False

pytestmark = pytest.mark.skipif(
    not is_cdp_available(),
    reason="Chrome CDP debugger on 127.0.0.1:9222 not reachable or BadUSB tab not found (requires live device)"
)

@pytest.fixture(scope="module")
def cdp():
    target = get_target()
    client = MinimalCDP(target["webSocketDebuggerUrl"])
    yield client
    client.close()

def test_page_metadata(cdp):
    title = cdp.evaluate("document.title")
    assert title == "BadUSB Remote Controller"

def test_no_horizontal_overflow(cdp):
    overflow = cdp.evaluate("""
        ({
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth,
            hasOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
        })
    """)
    assert not overflow["hasOverflow"], f"Horizontal overflow detected: {overflow}"

def test_tab_structure(cdp):
    tabs = cdp.evaluate("""
        Array.from(document.querySelectorAll('.tab-pane')).map(p => p.id)
    """)
    assert "tabScenarios" in tabs
    assert "tabKeyboard" in tabs
    assert "tabMouse" in tabs
    assert "tabSettings" in tabs

def test_api_status_endpoint(cdp):
    res = cdp.evaluate("""
        (async () => {
            const r = await fetch('/api/status');
            return { ok: r.ok, status: r.status, data: await r.json() };
        })()
    """)
    assert res["ok"]
    assert res["status"] == 200
    assert res["data"]["device"] == "ESP32-S3 BadUSB"
    assert res["data"]["usb_ready"] is True
    assert res["data"]["sta_ip"] == "10.85.248.29"

def test_auth_login_endpoint(cdp):
    # Invalid PIN
    res_bad = cdp.evaluate("""
        (async () => {
            const r = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pin: 'wrongpin999' })
            });
            return { ok: r.ok, status: r.status, data: await r.json() };
        })()
    """)
    assert res_bad["status"] == 401
    assert res_bad["data"]["success"] is False

    # Valid PIN
    res_good = cdp.evaluate("""
        (async () => {
            const r = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pin: 'badusb123' })
            });
            return { ok: r.ok, status: r.status, data: await r.json() };
        })()
    """)
    assert res_good["status"] == 200
    assert res_good["data"]["success"] is True
    assert res_good["data"]["token"] == "badusb123"

def test_unauthorized_rejection(cdp):
    res = cdp.evaluate("""
        (async () => {
            const r = await fetch('/api/keyboard/release', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pin: 'invalid' })
            });
            return { ok: r.ok, status: r.status, data: await r.json() };
        })()
    """)
    assert res["status"] == 401
    assert "Unauthorized" in res["data"]["error"]

def test_keyboard_release_api(cdp):
    res = cdp.evaluate("""
        (async () => {
            const r = await fetch('/api/keyboard/release', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-Auth-Token': 'badusb123' },
                body: JSON.stringify({ token: 'badusb123' })
            });
            return { ok: r.ok, status: r.status, data: await r.json() };
        })()
    """)
    assert res["status"] == 200
    assert res["data"]["success"] is True

def test_scenario_stop_api(cdp):
    res = cdp.evaluate("""
        (async () => {
            const r = await fetch('/api/scenario/stop', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-Auth-Token': 'badusb123' },
                body: JSON.stringify({ token: 'badusb123' })
            });
            return { ok: r.ok, status: r.status, data: await r.json() };
        })()
    """)
    assert res["status"] == 200
    assert res["data"]["success"] is True

def test_mouse_move_api(cdp):
    res = cdp.evaluate("""
        (async () => {
            const r = await fetch('/api/mouse/move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-Auth-Token': 'badusb123' },
                body: JSON.stringify({ x: 0, y: 0, wheel: 0, token: 'badusb123' })
            });
            return { ok: r.ok, status: r.status, data: await r.json() };
        })()
    """)
    assert res["status"] == 200
    assert res["data"]["success"] is True

def test_mouse_release_api(cdp):
    res = cdp.evaluate("""
        (async () => {
            const r = await fetch('/api/mouse/release', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-Auth-Token': 'badusb123' },
                body: JSON.stringify({ button: 'all', token: 'badusb123' })
            });
            return { ok: r.ok, status: r.status, data: await r.json() };
        })()
    """)
    assert res["status"] == 200
    assert res["data"]["success"] is True
