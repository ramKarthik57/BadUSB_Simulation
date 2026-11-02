import sys
sys.path.insert(0, '.')
from tests.cdp_client import get_target, MinimalCDP
import json
import time

cdp = MinimalCDP(get_target()['webSocketDebuggerUrl'])

res = cdp.evaluate("""
    (async () => {
        const log = [];
        try {
            const r1 = await fetch('/api/status');
            log.push({ step: 'status1', ok: r1.ok, data: await r1.json() });
        } catch(e) { log.push({ step: 'status1_err', err: e.toString() }); }

        try {
            const token = 'badusb123';
            const r2 = await fetch('/api/scenario/stop', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-Auth-Token': token },
                body: JSON.stringify({ token: token })
            });
            log.push({ step: 'stop', ok: r2.ok, status: r2.status, text: await r2.text() });
        } catch(e) { log.push({ step: 'stop_err', err: e.toString() }); }

        // Wait 500ms
        await new Promise(r => setTimeout(r, 500));

        try {
            const r3 = await fetch('/api/status');
            log.push({ step: 'status2', ok: r3.ok, data: await r3.json() });
        } catch(e) { log.push({ step: 'status2_err', err: e.toString() }); }

        return log;
    })()
""")
print("Execution Sequence Log:", json.dumps(res, indent=2))
cdp.close()
