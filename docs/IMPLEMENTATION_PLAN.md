# ESP32-S3 BadUSB Remote Control Platform — Implementation Plan

## 1. Project Baseline & Workspace Inspection

### Hardware & Environment
- **Target Device**: ESP32-S3 DevKit (revision v0.2, MAC `b8:f8:62:fa:c5:4c`) connected on `COM5`.
- **Framework**: Arduino ESP32 Core v2.0.17 (`esp32:esp32:esp32s3:USBMode=default`) with Native USB-OTG TinyUSB stack.
- **Tools**: Arduino IDE 2.x CLI (`arduino-cli.exe`), Python 3.14 with virtual environment (`.venv`).
- **Network Context**: Laptop is connected to the phone's mobile Wi-Fi hotspot. ESP32-S3 operates in dual `WIFI_AP_STA` mode, connecting to the phone's hotspot while simultaneously maintaining a standalone SoftAP (`BadUSB-Controller`) with fallback.

### Historical Assets (Preserved)
- `tusb_hid_example_main.c`: Original ESP-IDF TinyUSB C implementation from prior semester.
- `docs/BadUSB_Report_Final.docx` & `docs/BadUSB_Report_Final.pdf`: Academic project reports.
- `docs/usage.md`, `docs/architecture.md`: Project reference documents.

---

## 2. Implementation Checklist & Phase Tracking

### [X] Phase 0: Discovery & Baseline
- [x] Inspect directory tree, source files, Git status, and hardware configuration.
- [x] Discover tools, Arduino CLI path, board FQBN, and Python dependencies.
- [x] Create `docs/IMPLEMENTATION_PLAN.md`.

### [x] Phase 1 & 2: Firmware Architecture, Scenario Controller & State Machine
- [x] Define formal Finite State Machine: `BOOTING`, `USB_WAIT`, `STARTUP_PAYLOAD`, `IDLE`, `RUNNING_SCENARIO`, `STOPPING`, `ERROR`.
- [x] Implement central, non-blocking FreeRTOS `ScenarioController` task so typing sequences do not block the Wi-Fi web server.
- [x] Replicate all 4 educational scenarios:
  - Scenario 1: Notepad awareness simulation
  - Scenario 2: Educational portal redirection (`my.amrita.edu`)
  - Scenario 3: Self-contained ransomware awareness simulation
  - Scenario 4: Non-sensitive Wi-Fi configuration reconnaissance
- [x] Enforce automatic once-only execution of Scenario 1 on USB enumeration.
- [x] Enforce robust GPIO 0 (BOOT button) debouncing, edge-detection, and scenario advancement.
- [x] Implement instant Stop / cancellation with `Keyboard.releaseAll()`.

### [x] Phase 3, 4 & 5: Wi-Fi, Web Server, Remote Selection & Remote Keyboard
- [x] Implement dual Wi-Fi (`WIFI_AP_STA`) mode with configurable Hotspot STA credentials and fallback SoftAP (`192.168.4.1`).
- [x] Implement local HTTP Web Server (`WebServer.h`) and mDNS responder (`badusb.local`).
- [x] Implement PIN-based session authentication (`/api/auth/login`) and secure token validation for protected endpoints.
- [x] Implement REST API:
  - `GET /api/status`
  - `POST /api/scenario/select`
  - `POST /api/scenario/next`
  - `POST /api/scenario/stop`
  - `POST /api/keyboard/text`
  - `POST /api/keyboard/key`
  - `POST /api/keyboard/shortcut`
  - `POST /api/keyboard/release`
- [x] Build mobile-responsive HTML/CSS/JavaScript single-page application served from ESP32 PROGMEM flash:
  - Dashboard tab: Live status, connection state, USB status, scenario state.
  - Scenario tab: Direct selection of Scenarios 1-4, Next button, Stop button.
  - Keyboard tab: Real-time text transmission, special keys, modifiers, shortcuts, emergency release.
  - Settings tab: Wi-Fi setup, credentials, PIN configuration.

### [x] Phase 6: Host-Side Controller Simulation & Verification Suite
- [x] Build Python host-side controller and API mock test suite to verify state transitions, queue limits, validation, and auth rules without physical hardware dependencies.

### [x] Phase 7: Defensive Keystroke Firewall Enhancement
- [x] Improve `src/firewall.py`:
  - Configurable maximum suppression timeout to prevent permanent lockouts.
  - Safe shutdown unhooking and emergency escape sequence.
  - Clear documentation of global vs device-aware filtering limits.
- [x] Update and expand `tests/test_firewall.py`.

### [x] Phase 8: Compilation, Regression Testing & Documentation
- [x] Compile firmware with `arduino-cli` using `esp32:esp32:esp32s3:USBMode=default`.
- [x] Run full test suite with `pytest` (12/12 passing).
- [x] Produce complete documentation:
  - `README.md`
  - `docs/architecture.md`
  - `docs/SETUP_ESP32.md`
  - `docs/PHONE_CONTROLLER.md`
  - `docs/TESTING.md`
  - `docs/KNOWN_LIMITATIONS.md`
- [x] Prepare manual flash commands for user execution (do not flash automatically).

