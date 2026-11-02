import sys
sys.path.insert(0, '.')
from tests.cdp_client import get_target, MinimalCDP
import json

cdp = MinimalCDP(get_target()['webSocketDebuggerUrl'])

res = cdp.evaluate("""
    (async () => {
        try {
            const token = authToken || 'badusb123';
            const res = await fetch('/api/scenario/stop', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Auth-Token': token
                },
                body: JSON.stringify({ token: token, pin: token })
            });
            const text = await res.text();
            return {
                ok: res.ok,
                status: res.status,
                statusText: res.statusText,
                headers: Array.from(res.headers.entries()),
                bodyText: text
            };
        } catch(e) {
            return { exception: e.name, message: e.message, stack: e.stack };
        }
    })()
""")
print("Detailed Fetch Result:", json.dumps(res, indent=2))
cdp.close()
