# Smartphone Wi-Fi Controller User Guide

The **ESP32-S3 BadUSB Web Controller** provides a responsive touchscreen dashboard for controlling USB HID keyboard attacks, launching specific scenarios, and sending live text from any mobile browser.

---

## 1. Network Connection Methods

### Scenario A: Your Laptop is Connected to Your Phone's Hotspot (Recommended)
When your laptop is using your mobile phone's hotspot for internet connectivity:
1. Ensure the ESP32-S3 firmware has your hotspot SSID and password configured in `badusb_firmware/config.h` (e.g. `DEFAULT_STA_SSID` and `DEFAULT_STA_PASS`).
2. When the ESP32 powers on, it automatically connects to your phone's hotspot.
3. Open your mobile browser (Chrome / Safari) on the same phone.
4. Navigate to:
   ```
   http://badusb.local
   ```
   *(If your phone's browser does not support mDNS, navigate to the ESP32's assigned hotspot IP, visible in your phone's Connected Devices hotspot menu or in the ESP32 Serial Monitor).*

### Scenario B: Direct SoftAP Mode (Standalone / Offline)
If you do not want to use a mobile hotspot:
1. Open Wi-Fi settings on your phone and search for available networks.
2. Connect to the ESP32-S3's access point:
   - **SSID**: `BadUSB-Controller`
   - **Password**: `badusb_control`
3. Once connected, open your mobile browser and navigate to:
   ```
   http://192.168.4.1
   ```

---

## 2. Authentication & Authorization

To prevent unauthorized commands on your local network, all keyboard and scenario endpoints are protected:
- **Default Security PIN**: `badusb123`
- **First Use Setup**:
  1. Click the **Settings** tab in the web interface.
  2. Enter `badusb123` in the **Security PIN** field.
  3. Tap **Set PIN & Authenticate**.
  4. The web application stores this token in your browser's `sessionStorage` and automatically attaches an `X-Auth-Token` header to all subsequent requests.

---

## 3. Web Dashboard Features

### Tab 1: Educational Scenarios
- **Scenario Cards (1 to 4)**:
  - **Launch Button**: Directly executes that specific payload immediately (e.g., launch Scenario 4 without running Scenarios 2 and 3).
  - **Visual Indicator**: Highlights the currently active or last-executed scenario with an emerald border.
- **Physical Sync (`▶ Next`)**:
  - Programmatically advances to the next scenario, identical to pressing the physical on-board **BOOT** button.
- **Emergency Stop (`⏹ Stop / Abort`)**:
  - Immediately stops any ongoing typing sequence, releases all held keyboard keys, and places the controller in a safe `STOPPED` state.

### Tab 2: Remote Keyboard
- **Text Entry Field**:
  - Enter custom text (e.g. `"Hi i am ram"`) up to 256 characters.
  - Live character counter.
  - Tap **Send Text to Laptop**: The ESP32 sends the text over USB HID keystroke-by-keystroke directly into the laptop's focused window.
- **Special Key Pad**:
  - Single-tap buttons for `Enter ↵`, `⌫ Back`, `Tab ⇥`, `Space`, `Esc`, `Delete`, `Home`, `End`, `Page Up`, `Page Down`, and arrow keys (`←`, `↑`, `↓`, `→`).
- **Shortcut Grid**:
  - One-tap triggers for standard Windows combinations:
    - `Win + R` (Opens Run dialog)
    - `Ctrl + C` (Copy)
    - `Ctrl + V` (Paste)
    - `Ctrl + Z` (Undo)
    - `Ctrl + A` (Select All)
    - `Alt + F4` (Close Active Window)
- **Release All**:
  - An emergency failsafe that issues `Keyboard.releaseAll()` to ensure no modifier keys remain stuck on the target computer.

---

## 4. REST API Reference

Developers can also issue direct HTTP requests to the controller:

| Method | Endpoint | Description | Required Header / Body |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/status` | Returns live JSON status of device, scenario, and USB. | None |
| `POST` | `/api/auth/login` | Authenticates PIN and returns session token. | `{"pin": "badusb123"}` |
| `POST` | `/api/scenario/select` | Triggers a specific scenario (1–4). | `X-Auth-Token`, `{"id": 4}` |
| `POST` | `/api/scenario/next` | Advances to the next sequential scenario. | `X-Auth-Token` |
| `POST` | `/api/scenario/stop` | Halts execution and releases keys. | `X-Auth-Token` |
| `POST` | `/api/keyboard/text` | Sends string of text (max 256 chars). | `X-Auth-Token`, `{"text": "..."}` |
| `POST` | `/api/keyboard/key` | Sends single special key. | `X-Auth-Token`, `{"key": "ENTER"}` |
| `POST` | `/api/keyboard/shortcut` | Sends modifier + key combination. | `X-Auth-Token`, `{"modifiers": "CTRL", "key": "c"}` |
| `POST` | `/api/keyboard/release` | Releases all held keys immediately. | `X-Auth-Token` |
