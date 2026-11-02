import sys
import socket
import json
import base64
import os
import urllib.request
import struct

def get_target():
    data = urllib.request.urlopen("http://127.0.0.1:9222/json").read()
    tabs = json.loads(data)
    for t in tabs:
        if "10.85.248.29" in t.get("url", ""):
            return t
    raise RuntimeError("BadUSB tab not found in Chrome")

class MinimalCDP:
    def __init__(self, ws_url):
        # ws_url: ws://127.0.0.1:9222/devtools/page/5810
        parts = ws_url.replace("ws://", "").split("/", 1)
        host, port = parts[0].split(":")
        path = "/" + parts[1]
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, int(port)))
        
        key = base64.b64encode(os.urandom(16)).decode('ascii')
        req = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(req.encode('utf-8'))
        resp = b""
        while b"\r\n\r\n" not in resp:
            resp += self.sock.recv(4096)
        
        self.msg_id = 1

    def send_cmd(self, method, params=None):
        mid = self.msg_id
        self.msg_id += 1
        payload = json.dumps({"id": mid, "method": method, "params": params or {}}).encode('utf-8')
        
        # Build masked WS frame
        header = bytearray()
        header.append(0x81) # text frame, fin
        length = len(payload)
        mask_key = os.urandom(4)
        if length <= 125:
            header.append(0x80 | length)
        elif length <= 65535:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", length))
        
        header.extend(mask_key)
        masked_payload = bytearray(b ^ mask_key[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(header + masked_payload)
        
        # Read response
        while True:
            b1, b2 = self.sock.recv(2)
            length = b2 & 0x7F
            if length == 126:
                length = struct.unpack("!H", self.sock.recv(2))[0]
            elif length == 127:
                length = struct.unpack("!Q", self.sock.recv(8))[0]
            
            data = b""
            while len(data) < length:
                data += self.sock.recv(length - len(data))
            
            try:
                msg = json.loads(data.decode('utf-8'))
                if msg.get("id") == mid:
                    return msg.get("result", {})
            except Exception:
                pass

    def evaluate(self, expr, await_promise=True):
        res = self.send_cmd("Runtime.evaluate", {
            "expression": expr,
            "returnByValue": True,
            "awaitPromise": await_promise
        })
        if "result" in res and "value" in res["result"]:
            return res["result"]["value"]
        return res

    def close(self):
        self.sock.close()

if __name__ == "__main__":
    target = get_target()
    print("Found Target:", target["title"], target["url"])
    cdp = MinimalCDP(target["webSocketDebuggerUrl"])
    
    # 1. Check title
    title = cdp.evaluate("document.title")
    print("Document Title:", title)
    
    # 2. Check for Horizontal Overflow
    overflow = cdp.evaluate("""
        ({
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth,
            hasOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
            bodyWidth: document.body.clientWidth,
            viewportWidth: window.innerWidth
        })
    """)
    print("Overflow Check:", json.dumps(overflow, indent=2))
    
    # 3. Check Active Tab & Visibility
    tabs_state = cdp.evaluate("""
        Array.from(document.querySelectorAll('.tab-pane')).map(p => ({
            id: p.id,
            active: p.classList.contains('active'),
            display: getComputedStyle(p).display,
            rect: { width: p.offsetWidth, height: p.offsetHeight }
        }))
    """)
    print("Tabs Visibility:", json.dumps(tabs_state, indent=2))
    
    # 4. Check API status from browser context
    api_status = cdp.evaluate("""
        (async () => {
            try {
                const res = await fetch('/api/status');
                return await res.json();
            } catch(e) {
                return { error: e.toString() };
            }
        })()
    """)
    print("API /api/status from Phone Browser:", json.dumps(api_status, indent=2))
    
    cdp.close()
