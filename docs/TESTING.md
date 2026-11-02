# Testing & Verification Guide

This document describes the automated unit test suite, firmware compilation validation, and hardware testing procedures for the **ESP32-S3 BadUSB Remote Control Platform**.

---

## 1. Automated Host-Side Test Suite

The project includes an automated `pytest` suite validating both defensive keystroke suppression and offensive scenario state machine simulations.

### Running the Tests
Activate the Python virtual environment and run `pytest`:

```powershell
.venv\Scripts\python -m pytest -v
```

### Test Cases Covered

| Test Name | File | Description | Status |
| :--- | :--- | :--- | :---: |
| `test_startup_executes_payload_1_once` | `test_controller_simulation.py` | Verifies Scenario 1 runs once on USB enumeration and does not duplicate on re-entry. | **PASSED** |
| `test_sequential_boot_button_advance` | `test_controller_simulation.py` | Verifies sequential cycling: `1 -> 2 -> 3 -> 4 -> 1`. | **PASSED** |
| `test_direct_scenario_selection` | `test_controller_simulation.py` | Verifies direct jump from Scenario 1 to Scenario 4 without executing 2 and 3. | **PASSED** |
| `test_invalid_scenario_rejection` | `test_controller_simulation.py` | Verifies rejection of out-of-range scenario IDs (`0`, `5`). | **PASSED** |
| `test_emergency_stop` | `test_controller_simulation.py` | Verifies immediate transition to `STOPPED` and clearing of held keys. | **PASSED** |
| `test_keyboard_text_bounds` | `test_controller_simulation.py` | Verifies 256-character maximum boundary and empty string rejection. | **PASSED** |
| `test_keyboard_key_mapping` | `test_controller_simulation.py` | Verifies mapping of `ENTER`, `BACKSPACE`, `F1-F12`, and standard ASCII characters. | **PASSED** |
| `test_keyboard_modifier_parsing` | `test_controller_simulation.py` | Verifies bitmask parsing for `CTRL`, `SHIFT`, `ALT`, and `GUI/WIN`. | **PASSED** |
| `test_firewall_initial_state` | `test_firewall.py` | Verifies initial state of the Python defense application is disabled and unhooked. | **PASSED** |
| `test_firewall_enable_disable` | `test_firewall.py` | Verifies hook registration with `suppress=True` and clean unhooking. | **PASSED** |
| `test_toggle` | `test_firewall.py` | Verifies state toggling between ALLOW and BLOCKING. | **PASSED** |
| `test_auto_disarm_timer` | `test_firewall.py` | Verifies watchdog auto-disarm timer automatically unhooks after timeout. | **PASSED** |

---

## 2. Firmware Compilation Verification

Firmware compilation was verified using the official Espressif ESP32 Arduino Core (`v2.0.17`) via `arduino-cli`:

```powershell
& "C:\Users\Ram\AppData\Local\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe" compile `
  --fqbn esp32:esp32:esp32s3:USBMode=default `
  "c:\Users\Ram\Desktop\BadUSB_Using_ESP32\badusb_firmware"
```

### Compilation Results
- **Exit Code**: `0` (Success)
- **Flash Utilization**: `809,261 bytes (61%)` of 1,310,720 bytes maximum.
- **RAM Utilization**: `59,480 bytes (18%)` of 327,680 bytes maximum.
- **Status**: Zero compilation errors or missing dependencies.

---

## 3. Physical Hardware Verification Checklist

When demonstrating or testing on physical hardware with the ESP32-S3 DevKit:

1. [x] **UART Connectivity Check**: Verified `COM5` CP210x serial communication and chip identification (ESP32-S3 rev 0.2).
2. [ ] **Manual Flash Execution**: User runs upload command to flash firmware to `COM5`.
3. [ ] **USB OTG Enumeration**: Connect USB OTG cable to laptop. Verify Device Manager shows `"TinyUSB BadUSB Demo"`.
4. [ ] **Startup Demonstration**: Verify Scenario 1 types `"BadUSB Simulation using ESP32 S3 Devkit"` in Notepad within 3.5 seconds.
5. [ ] **BOOT Button Advance**: Press the physical BOOT button. Verify advancement to Scenario 2 (opens CMD and browser).
6. [ ] **Phone Wi-Fi Connection**: Open phone browser to `http://badusb.local` (or `http://192.168.4.1`).
7. [ ] **Authentication**: Enter PIN `badusb123` in Settings tab.
8. [ ] **Remote Payload Selection**: Tap **Launch** on Scenario 4. Verify Wi-Fi reconnaissance command runs immediately.
9. [ ] **Live Typing**: Type `"Hi i am ram"` in Keyboard tab and tap **Send**. Verify text appears in active window.
10. [ ] **Keystroke Firewall Test**: Launch `python firewall.py`, click **TOGGLE** to BLOCKING, and verify injected keystrokes are suppressed.
