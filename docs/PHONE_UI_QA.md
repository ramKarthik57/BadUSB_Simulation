# ESP32-S3 Phone Controller: Live Device QA & End-to-End Verification Checklist

## 1. Baseline System Information
- **Target Device**: ESP32-S3 DevKit (Dual-Core LX7, Native USB OTG + UART Bridge CP2102)
- **Serial / Upload Port**: COM5 (`USB\VID_10C4&PID_EA60\0001`)
- **Firmware Path**: `badusb_firmware/`
- **Phone Model**: Vivo V50e (`model: V2428`, `release: Android 16`)
- **ADB Executable**: `C:\Users\Ram\AppData\Local\Android\Sdk\platform-tools\adb.exe`
- **Hotspot SSID**: `AndroidAP_4786` (2.4 GHz WPA2)
- **Verified Target URL**: `http://10.85.248.29` (Station Mode) / `http://192.168.4.1` (SoftAP Mode)
- **Security PIN**: `badusb123`

---

## 2. QA Test Plan & Verification Matrix

### Phase 1: ADB Device Connection
- [x] Locate `adb.exe` on host (`C:\Users\Ram\AppData\Local\Android\Sdk\platform-tools\adb.exe`)
- [x] Detect connected Android phone (`10BF4821CL0024T device product:V2428i model:V2428`)
- [x] Confirm device authorization state (Authorized via USB Debugging prompt)
- [x] Retrieve Android OS version & product model (`release 16`, `model V2428`)

### Phase 2: ESP32 Target Discovery & Connectivity
- [x] Read serial logs on `COM5` to verify current IP address (`*** CONNECTED TO HOTSPOT! IP: 10.85.248.29 ***`)
- [x] Verify network connectivity to `http://10.85.248.29` via phone ICMP (`0% packet loss, 85ms avg latency`)
- [x] Confirm fallback connectivity on SoftAP `http://192.168.4.1`

### Phase 3: Baseline Screenshots on Phone
- [x] Open controller URL on Android phone via ADB intent (`am start -a android.intent.action.VIEW -d "http://10.85.248.29"`)
- [x] Capture baseline screenshot: Dashboard / Scenarios (`artifacts/phone-ui/baseline/01_scenarios.png`)
- [x] Capture baseline screenshot: Keyboard Full Layout (`artifacts/phone-ui/baseline/02_keyboard_full.png`)
- [x] Capture baseline screenshot: Keyboard Shortcuts (`artifacts/phone-ui/baseline/03_keyboard_shortcuts.png`)
- [x] Capture baseline screenshot: Keyboard Live Text (`artifacts/phone-ui/baseline/04_keyboard_livetext.png`)
- [x] Capture baseline screenshot: Keyboard Numpad (`artifacts/phone-ui/baseline/05_keyboard_numpad.png`)
- [x] Capture baseline screenshot: Mouse Trackpad & Buttons (`artifacts/phone-ui/baseline/06_mouse.png`)
- [x] Capture baseline screenshot: Settings Tab (`artifacts/phone-ui/baseline/07_settings.png`)

### Phase 4: UI / UX & Mobile Layout Inspection
- [x] Verify tab switching reliability on mobile touch (All 4 primary tabs switch cleanly)
- [x] Inspect horizontal overflow on narrow viewports (`scrollWidth: 392, clientWidth: 392, hasOverflow: false`)
- [x] Verify touchpad drag vs page scroll (`touch-action: none` verified on `#trackpadSurface`)
- [x] Check button touch targets (Primary buttons are 52px height)
- [x] Check contrast, font legibility, and card alignment (Dark theme `#0b0f19` / `#151e32` with high-contrast text)
- [x] Check sticky modifier key visual indication (Ctrl, Alt, Shift, Win state toggle correctly)

### Phase 5: Browser & JavaScript Debugging
- [x] Inspect DOM structure and closing tags (Fixed previous unclosed `<div>` in `tabKeyboard`)
- [x] Verify absence of unhandled exceptions in event handlers (Live CDP inspection confirmed clean DOM and events)
- [x] Check API fetch error handling and toast alerts (Added `.toast.error` CSS styling)
- [x] Validate periodic status polling loop (`refreshStatus()` runs every 1500ms)

### Phase 6: Live API & HID Functional Verification
- [x] `GET /api/status` - Returns valid JSON (`state: IDLE, usb_ready: true, sta_ip: 10.85.248.29`)
- [x] `POST /api/auth/login` - Accepts PIN `badusb123` (HTTP 200), rejects invalid PIN (HTTP 401)
- [x] `POST /api/keyboard/release` - Verified HTTP 200 via phone Chrome CDP
- [x] `POST /api/mouse/move` - Verified HTTP 200 via phone Chrome CDP
- [x] `POST /api/mouse/release` - Verified HTTP 200 via phone Chrome CDP
- [x] Identified and fixed FreeRTOS concurrency issue in `ScenarioController::requestStop` where USB transfers occurred inside `portENTER_CRITICAL`
- [x] Added `HTTP_OPTIONS` CORS preflight handler in `WebServerHandler::handleNotFound`

### Phase 7: Automated Regression Testing
- [x] Run pytest simulation suite (`.\.venv\Scripts\python.exe -m pytest tests/test_controller_simulation.py tests/test_firewall.py -v`) -> 12 passed in 0.41s
- [x] Verified full compilation of firmware (`Sketch uses 851157 bytes (64%)`)

---

## 3. Defect & Resolution Log
1. **Defect**: Blank Mouse and Settings tabs.
   - **Root Cause**: Unclosed `<div>` on `#tabKeyboard` caused subsequent tabs to be nested children that hid when `#tabKeyboard` was inactive.
   - **Fix**: Closed `#tabKeyboard` cleanly in `badusb_firmware/web_assets.h`.
2. **Defect**: Fragile `switchTab` using `event.currentTarget`.
   - **Root Cause**: Mobile browsers evaluate `event.currentTarget` to `undefined` during certain inline event dispatches.
   - **Fix**: Explicitly passed `this` in HTML and added fallback detection in `web_assets.h`.
3. **Defect**: FreeRTOS nested critical section stall on Stop.
   - **Root Cause**: `KeyController.releaseAll()` called inside `portENTER_CRITICAL(&stateMux)` disabled interrupts during TinyUSB HID transfer.
   - **Fix**: Moved `KeyController.releaseAll()` outside of `portENTER_CRITICAL(&stateMux)` in `scenario_controller.cpp`.
4. **Defect**: Missing CORS preflight handling for custom headers.
   - **Root Cause**: `HTTP_OPTIONS` requests from mobile Chrome for authenticated POST requests fell into 404 without CORS headers.
   - **Fix**: Added `HTTP_OPTIONS` check in `WebServerHandler::handleNotFound` returning HTTP 204 with CORS allow headers.
5. **Defect**: Sub-tab label wrapping and emoji inconsistency.
   - **Root Cause**: Mobile narrow viewport caused 4-column sub-tab labels with emojis to wrap into two lines.
   - **Fix**: Cleaned labels to concise text (`Full Layout`, `Shortcuts`, `Text & Live`, `Numpad`) and updated `Mouse 🖱` to `Mouse`.

---

## 4. Phase 8: Final Verification & Flash Log
- **Hardware Flashing**: Flashed over `COM5` via `arduino-cli` upon user authorization (Exit code: 0).
- **Post-Flash Network**: ESP32 automatically rejoined `AndroidAP_4786` on `10.85.248.29` (0% packet loss).
- **Final Screenshots**:
  - `artifacts/phone-ui/final/01_scenarios.png`
  - `artifacts/phone-ui/final/02_keyboard.png`
  - `artifacts/phone-ui/final/03_mouse.png`
  - `artifacts/phone-ui/final/04_settings.png`
- **End-to-End Live Phone Test Suite**: `tests/test_live_phone_api.py` ran 10 integration tests via Chrome DevTools Protocol against the physical ESP32 web server -> **10 passed in 0.95s (100% pass rate)**.
- **Unit & Simulation Suite**: `tests/test_controller_simulation.py` & `tests/test_firewall.py` -> **12 passed in 0.41s**.
- **Overall QA Status**: **VERIFIED & PRODUCTION READY**.
