import sys
sys.path.insert(0, '.')
from tests.cdp_client import get_target, MinimalCDP
import json

cdp = MinimalCDP(get_target()['webSocketDebuggerUrl'])

res = cdp.evaluate("""
    (async () => {
        try {
            const token = 'badusb123';
            const r = await fetch('/api/scenario/stop', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token: token, pin: token })
            });
            const text = await r.text();
            return { ok: r.ok, status: r.status, body: text };
        } catch(e) {
            return { err: e.toString() };
        }
    })()
""")
print("Body-Auth Stop Result:", json.dumps(res, indent=2))
cdp.close()
