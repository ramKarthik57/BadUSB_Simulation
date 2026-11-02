import sys
sys.path.insert(0, '.')
from tests.cdp_client import get_target, MinimalCDP
import json

cdp = MinimalCDP(get_target()['webSocketDebuggerUrl'])

# Test fetch without custom header X-Auth-Token (simple request: Content-Type: text/plain or urlencoded, or json)
# With Content-Type: application/json, browser triggers preflight if cross-origin or if custom header present
res = cdp.evaluate("""
    (async () => {
        try {
            // Case 1: Standard POST with X-Auth-Token
            const r1 = await fetch('/api/scenario/stop', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-Auth-Token': 'badusb123' },
                body: JSON.stringify({ token: 'badusb123' })
            }).then(r => ({ status: r.status })).catch(e => ({ err: e.toString() }));

            // Case 2: POST without custom header (body only token)
            const r2 = await fetch('/api/scenario/stop', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'plain=' + encodeURIComponent(JSON.stringify({ token: 'badusb123' }))
            }).then(r => ({ status: r.status })).catch(e => ({ err: e.toString() }));

            // Case 3: OPTIONS request directly
            const r3 = await fetch('/api/scenario/stop', {
                method: 'OPTIONS'
            }).then(r => ({ status: r.status })).catch(e => ({ err: e.toString() }));

            return { withHeader: r1, formUrlEncoded: r2, options: r3 };
        } catch(e) {
            return { error: e.toString() };
        }
    })()
""")
print("Preflight Analysis:", json.dumps(res, indent=2))
cdp.close()
