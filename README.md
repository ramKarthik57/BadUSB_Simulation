# WHID-Guard: ESP32-S3 BadUSB Hardware Platform & Behavioral Keystroke Dynamics Defense

[![CI Status](https://github.com/ramKarthik57/BadUSB_Simulation/actions/workflows/ci.yml/badge.svg)](https://github.com/ramKarthik57/BadUSB_Simulation/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Firmware](https://img.shields.io/badge/Firmware-ESP32--S3%20Native%20USB--OTG-red.svg)](https://www.espressif.com/en/products/socs/esp32-s3)
[![Tests](https://img.shields.io/badge/pytest-16%20Passed%20%7C%20100%25-brightgreen.svg)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IEEE Publication Ready](https://img.shields.io/badge/Paper-IEEE%20Format-purple.svg)](WHID_GUARD_FINAL_SUBMISSION/)

A dual-mode cyber-physical security platform designed for offensive hardware emulation and host-side defense-in-depth against Human Interface Device (HID) keystroke injection attacks (BadUSB / WHID). 

The platform integrates:
1. **ESP32-S3 Dual-Core Hardware Implant**: Emulates composite USB HID peripherals (Keyboard & Mouse) while hosting a responsive, authenticated Web Controller served from flash memory (`PROGMEM`) over 2.4 GHz Wi-Fi. Features adversarial evasion (human cadence emulation with randomized jitter and cognitive micro-pauses).
2. **WHID-Guard Host Defense Engine**: Real-time behavioral biometric monitoring on Windows using sliding-window Inter-Key Interval (IKI) statistics, combined with per-device hardware attribution via the Windows Raw Input API (`WM_INPUT`) and selective driver-level keystroke isolation (`WH_KEYBOARD_LL`).

---

## Table of Contents

- [Architectural Topology](#architectural-topology)
- [Key Technical Innovations](#key-technical-innovations)
  - [1. Behavioral Keystroke Dynamics Engine](#1-behavioral-keystroke-dynamics-engine)
  - [2. Per-Device Hardware Attribution & Selective Isolation](#2-per-device-hardware-attribution--selective-isolation)
  - [3. Microcontroller Adversarial Evasion](#3-microcontroller-adversarial-evasion)
  - [4. Touch-Optimized Mobile Web Controller](#4-touch-optimized-mobile-web-controller)
- [Hardware Architecture & Pinout](#hardware-architecture--pinout)
- [Empirical Evaluation & Benchmarks](#empirical-evaluation--benchmarks)
- [Educational Demonstration Payloads](#educational-demonstration-payloads)
- [Repository Structure](#repository-structure)
- [Quick Start Guide](#quick-start-guide)
  - [1. Firmware Toolchain & Flashing](#1-firmware-toolchain--flashing)
  - [2. Host Defense Engine Setup](#2-host-defense-engine-setup)
  - [3. Phone Controller Pairing](#3-phone-controller-pairing)
- [REST API Specification](#rest-api-specification)
- [Automated Testing & CI](#automated-testing--ci)
- [Academic Citation & Attribution](#academic-citation--attribution)
- [Ethical & Responsible Disclosure Notice](#ethical--responsible-disclosure-notice)

---

## Architectural Topology

```
+-----------------------------------------------------------------------------------+
|                           SMARTPHONE CONTROLLER (STA / AP)                        |
|   Responsive Dark-Mode SPA served from ESP32 PROGMEM (http://10.85.248.29 / IP)   |
|   [Payload Triggers]   [Live Numpad/Keys]   [Touchpad Mouse]   [Stealth Toggle]   |
+-----------------------------------------------------------------------------------+
                                         |
                               2.4 GHz 802.11b/g/n
                               (HTTP REST API + JSON)
                                         v
+-----------------------------------------------------------------------------------+
|                             ESP32-S3 MICROCONTROLLER                              |
|   - Hardware: Xtensa Dual-Core LX7 @ 240 MHz, 8 MB Flash, 512 KB SRAM            |
|   - Network: Async WebServer (Port 80) with Session Token Authentication          |
|   - Core FSM: Non-blocking Sequential & Direct State Machine                      |
|   - Evasion Engine: Stochastic Jitter Generator + Delimiter Pause Injection       |
|   - Physical Control: GPIO 0 Hardware Debounced Edge-Triggered Button             |
|   - USB Stack: Native USB-OTG TinyUSB Composite HID (Keyboard + Mouse)            |
+-----------------------------------------------------------------------------------+
                                         |
                              Native USB D- (GPIO 19)
                              Native USB D+ (GPIO 20)
                                         v
+-----------------------------------------------------------------------------------+
|                        PROTECTED WINDOWS HOST (WHID-GUARD)                        |
|                                                                                   |
|  +------------------------------+     +----------------------------------------+  |
|  | Windows Raw Input Monitor    |     | Behavioral Keystroke Dynamics Engine   |  |
|  | - RIDEV_INPUTSINK (WM_INPUT) | --> | - Sliding Window W = 10 Events         |  |
|  | - GetRawInputDeviceInfoW     |     | - Mean IKI (u), StdDev (s), CV (s/u)   |  |
|  | - Isolates hDevice & VID/PID |     | - Burst Rate Thresholding (ch/s)       |  |
|  +------------------------------+     +----------------------------------------+  |
|                                                            |                      |
|                                              Decision Boundary (CV, u)            |
|                                                            v                      |
|  +-----------------------------------------------------------------------------+  |
|  | Selective WH_KEYBOARD_LL Filter: Drops malicious hDevice events             |  |
|  | Legitimate keyboards preserved | Watchdog timer (15s disarm failsafe)       |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

![System Architecture](reports/assets/system_architecture.png)

---

## Key Technical Innovations

### 1. Behavioral Keystroke Dynamics Engine

Offensive BadUSB payloads typically inject characters at machine bus speeds (e.g., $10\text{ ms}$ inter-key intervals) with zero mechanical variance. Human operators, by contrast, exhibit neurological latency, finger travel distances, and cognitive pauses.

WHID-Guard evaluates an online sliding window of $W = 10$ consecutive keystroke events:

$$\mu_{\text{IKI}} = \frac{1}{W-1} \sum_{i=1}^{W-1} \Delta t_i \quad \text{where} \quad \Delta t_i = t_{i+1} - t_i$$

$$\sigma_{\text{IKI}} = \sqrt{\frac{1}{W-2} \sum_{i=1}^{W-1} (\Delta t_i - \mu_{\text{IKI}})^2}$$

$$CV = \frac{\sigma_{\text{IKI}}}{\mu_{\text{IKI}}}$$

The real-time classification boundary partitions events into three operational regimes:
- **`LOCKED_DOWN` (Machine Injection)**: Triggered when $\mu_{\text{IKI}} < 25\text{ ms}$ or $CV < 0.15$ over 8 consecutive events. The offending device handle is immediately quarantined.
- **`SAFE` (Human Operator)**: Satisfied when $\mu_{\text{IKI}} > 75\text{ ms}$ and $CV > 0.30$.
- **`SUSPICIOUS` (Adversarial Evasion)**: Intermediate range characterized by synthetic random jitter lacking authentic human digram variance.

![IKI Distribution](reports/assets/fig_iki_distribution.png)

### 2. Per-Device Hardware Attribution & Selective Isolation

Unlike legacy software key-lockers that suppress the entire operating system keyboard pipeline, WHID-Guard isolates the offending peripheral at the hardware level:
1. Registers for background raw keyboard input sink (`RIDEV_INPUTSINK`) via `RegisterRawInputDevices`.
2. Intercepts `WM_INPUT` messages to query `GetRawInputDeviceInfoW` and parse `hDevice` hardware handles, extracting Vendor ID (`VID: 0x303A`) and Product ID (`PID: 0x1001`).
3. Installs a low-level keyboard hook (`WH_KEYBOARD_LL`). When the dynamics engine trips, only events matching the malicious `hDevice` are swallowed (`return 1`). Legitimate user keyboards (`ATK3001` or external peripherals) remain fully operational.

![Defense Architecture](reports/assets/defense_architecture.png)

### 3. Microcontroller Adversarial Evasion

To evaluate defensive robustness against state-of-the-art adversaries, the ESP32-S3 firmware implements a human cadence emulation mode:
- **Stochastic Jitter**: Characters are dispatched with randomized delay:
  $$\Delta t = \text{baseDelayMs} + \text{random}(0, \text{jitterRangeMs})$$
- **Cognitive Delimiter Pauses**: Natural micro-pauses ($150\text{--}300\text{ ms}$) are automatically inserted after spaces, punctuation (`.`, `,`, `!`), and command terminators (`\n`), challenging simplistic static threshold detectors.

### 4. Touch-Optimized Mobile Web Controller

Served directly from microcontroller flash memory using PROGMEM string compression:
- **Zero External Dependencies**: Pure vanilla HTML5, CSS3 flexbox/grid, and ES6 JavaScript.
- **Full HID Remote**: Complete QWERTY keyboard, numeric keypad, modifier toggles (`Ctrl`, `Alt`, `Shift`, `GUI`), one-touch shortcut macros (`Win+R`, `Ctrl+C`, `Ctrl+V`, `Alt+F4`), and a high-resolution virtual mouse touchpad.
- **PIN-Based Authentication**: Protects administrative endpoints with tokenized authorization (`badusb123`).

---

## Hardware Architecture & Pinout

The platform utilizes the **ESP32-S3-WROOM-1** dual-core microcontroller featuring native USB-OTG full-speed transceivers:

| Pin / Interface | Hardware Function | Operational Role |
| :--- | :--- | :--- |
| **GPIO 19** | Native USB D- | Full-speed USB HID data negative line. |
| **GPIO 20** | Native USB D+ | Full-speed USB HID data positive line. |
| **GPIO 0** | Physical BOOT Button | Hardware debounced falling-edge trigger for offline payload cycling. |
| **GPIO 43 (U0TXD)** | Hardware UART TX | CP210x USB-to-UART bridge for programming, serial debugging, and flashing. |
| **GPIO 44 (U0RXD)** | Hardware UART RX | CP210x USB-to-UART bridge for programming. |
| **VBUS / 5V** | Power Rail | Powers microcontroller from target host USB bus. |

> [!NOTE]
> The ESP32-S3 DevKit features two Type-C ports: `COM/UART` (CP210x Bridge for flashing/monitoring) and `USB` (Native USB-OTG for composite keyboard/mouse emulation). Both can be connected simultaneously during testing.

---

## Empirical Evaluation & Benchmarks

Empirical validation was conducted over a controlled 1,500-keystroke benchmark dataset comparing human operators, standard unconstrained BadUSB injection, and adversarial evasion modes:

| Dimension / Metric | Human Operator | Standard BadUSB | Adversarial Evasion |
| :--- | :---: | :---: | :---: |
| **Keystroke Sample Size ($N$)** | 500 keystrokes | 500 keystrokes | 500 keystrokes |
| **Mean IKI ($\mu$)** | **144.18 ms** | **10.01 ms** | **119.28 ms** |
| **Standard Deviation ($\sigma$)** | 91.98 ms | 0.78 ms | 48.88 ms |
| **Coefficient of Variation ($CV$)** | **0.638** | **0.0784** | **0.4098** |
| **Typing Burst Rate** | 6.94 ch/s | 99.95 ch/s | 8.38 ch/s |
| **Quarantine Latency** | **N/A (Authorized)** | **8 characters (<85 ms)** | Suspicious Flagging |
| **False Positive Rate (FPR)** | **0.0%** (0 false blocks) | N/A | N/A |
| **True Positive Detection Rate (TPR)**| N/A | **98.6%** | **25.2%** (Flagged Anomaly)|

![Detection Latency](reports/assets/fig_detection_latency.png)

---

## Educational Demonstration Payloads

All firmware payloads are strictly benign and designed for security education:

| ID | Name | Execution Vector | Demonstration Objective |
| :---: | :--- | :--- | :--- |
| **1** | **Notepad Awareness** | `Win+R` &rarr; `notepad` &rarr; Injects safety notice | Demonstrates basic keystroke injection upon host enumeration. |
| **2** | **Portal Redirection** | `Win+R` &rarr; `cmd` &rarr; Opens academic portal | Demonstrates browser launching and forced navigation threats. |
| **3** | **Ransomware Simulation**| `Win+R` &rarr; `powershell` &rarr; Harmless GUI alert | Demonstrates script automation and simulated extortion awareness. |
| **4** | **Reconnaissance** | `Win+R` &rarr; `cmd` &rarr; `netsh wlan show profiles`| Demonstrates read-only Wi-Fi profile configuration enumeration. |

---

## Repository Structure

```
BadUSB_Using_ESP32/
├── .github/
│   ├── workflows/ci.yml           # Multi-version Windows CI pipeline
│   ├── ISSUE_TEMPLATE/            # Structured bug and enhancement templates
│   └── pull_request_template.md   # Quality assurance PR checklist
├── badusb_firmware/               # Modular ESP32-S3 firmware
│   ├── badusb_firmware.ino        # Primary setup loop & button FSM
│   ├── config.h                   # Pinouts, Wi-Fi credentials, USB descriptors
│   ├── keyboard_controller.cpp/.h # USB HID typing & stealth jitter engine
│   ├── mouse_controller.cpp/.h    # USB HID mouse movement & click handler
│   ├── scenario_controller.cpp/.h # Educational payload sequence coordinator
│   ├── web_assets.h               # Minified dark-mode SPA stored in PROGMEM
│   └── web_server_handler.cpp/.h  # Authenticated REST API router
├── src/                           # WHID-Guard Defensive Framework
│   ├── detection/
│   │   ├── keystroke_dynamics.py  # Sliding-window IKI statistical classifier
│   │   └── raw_input_monitor.py   # Win32 WM_INPUT device attribution monitor
│   └── firewall.py                # Host defense GUI & low-level hook filter
├── tests/                         # Automated Verification Suite
│   ├── test_controller_simulation.py # State machine & payload bounds testing
│   ├── test_firewall.py           # Auto-disarm watchdog & hook isolation
│   ├── test_keystroke_dynamics.py # Detection boundary & FPR verification
│   └── test_live_phone_api.py     # Live phone UI integration (CDP)
├── scripts/                       # Empirical Evaluation & Benchmarks
│   └── run_empirical_evaluation.py# 1,500-event benchmark corpus runner
├── reports/assets/                # Publication-grade figures & vector graphics
├── WHID_GUARD_FINAL_SUBMISSION/   # Standalone IEEE LaTeX Paper Package
├── CITATION.cff                   # Academic citation metadata
├── CONTRIBUTING.md                # Development standards & guidelines
├── LICENSE                        # MIT License
├── pytest.ini                     # Pytest runner configuration
└── requirements.txt               # Host Python dependencies
```

---

## Quick Start Guide

### 1. Firmware Toolchain & Flashing

1. Install [Arduino CLI](https://arduino.github.io/arduino-cli/latest/) and add the ESP32 core index:
   ```bash
   arduino-cli core update-index
   arduino-cli core install esp32:esp32
   ```

2. Compile firmware configured for native USB-OTG hardware CDC mode:
   ```bash
   arduino-cli compile --fqbn esp32:esp32:esp32s3:CDCOnBoot=cdc,USBMode=hwcdc badusb_firmware
   ```

3. Flash to ESP32-S3 (replace `COM5` with your UART port):
   ```bash
   arduino-cli upload -p COM5 --fqbn esp32:esp32:esp32s3:CDCOnBoot=cdc,USBMode=hwcdc badusb_firmware
   ```

### 2. Host Defense Engine Setup

1. Initialize virtual environment and install requirements:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Launch the WHID-Guard Defensive GUI:
   ```powershell
   python firewall.py
   ```
   - Click **TOGGLE** to enable real-time selective suppression.
   - Live telemetry monitors current typing rate, sliding-window $CV$, active hardware `hDevice` handle, and isolation state.

### 3. Phone Controller Pairing

- **Station Mode (Recommended)**: Connect laptop and ESP32-S3 to your phone's personal hotspot. Navigate to `http://<ASSIGNED_IP>` or `http://badusb.local`.
- **SoftAP Mode**: Connect smartphone Wi-Fi to `BadUSB-Controller` (Password: `badusb_control`). Navigate to `http://192.168.4.1`.
- **Default PIN**: Authenticate using `badusb123`.

---

## REST API Specification

| Endpoint | Method | Authentication | Payload / Description |
| :--- | :---: | :---: | :--- |
| `/api/status` | `GET` | None | Returns device health, USB enumeration, and active scenario state. |
| `/api/auth/login` | `POST` | Body (`pin`) | Authenticates session and issues authorization token. |
| `/api/scenario/run` | `POST` | `X-Auth-Token` | `{"scenario": 1-4}` &mdash; Triggers specific demonstration scenario. |
| `/api/scenario/stop` | `POST` | `X-Auth-Token` | Immediately aborts active scenario and releases all keys. |
| `/api/keyboard/type` | `POST` | `X-Auth-Token` | `{"text": "..."}` &mdash; Types text string (max 256 characters). |
| `/api/keyboard/key` | `POST` | `X-Auth-Token` | `{"key": "ENTER", "modifiers": ["CTRL"]}` &mdash; Injects specific key combinations. |
| `/api/mouse/move` | `POST` | `X-Auth-Token` | `{"dx": 10, "dy": -5}` &mdash; Injects relative cursor movement. |
| `/api/settings/stealth`| `POST` | `X-Auth-Token`| `{"enabled": true, "baseMs": 80, "jitterMs": 40}` &mdash; Configures evasion cadence. |

---

## Automated Testing & CI

Execute the test suite locally:
```powershell
.\.venv\Scripts\python -m pytest -v
```

Output:
```text
tests/test_controller_simulation.py::test_startup_executes_payload_1_once PASSED
tests/test_controller_simulation.py::test_sequential_boot_button_advance PASSED
tests/test_controller_simulation.py::test_direct_scenario_selection PASSED
tests/test_controller_simulation.py::test_keyboard_text_bounds PASSED
tests/test_firewall.py::test_firewall_initial_state PASSED
tests/test_firewall.py::test_auto_disarm_timer PASSED
tests/test_keystroke_dynamics.py::test_machine_injection_detection PASSED
tests/test_keystroke_dynamics.py::test_human_typing_cadence PASSED
tests/test_keystroke_dynamics.py::test_multi_device_isolation PASSED
======================= 16 passed, 10 skipped in 0.90s =======================
```

---

## Academic Citation & Attribution

If you utilize this hardware platform, defense framework, or empirical dataset in your academic publications or technical demonstrations, please cite:

```bibtex
@inproceedings{karthik2027whidguard,
  author    = {Ram Karthik G and Harini V},
  title     = {WHID-Guard: Per-Device Behavioral Keystroke Dynamics and Selective Defense Against Hardware-Emulated USB Keystroke Injection},
  booktitle = {Proceedings of the IEEE Conference on Cybersecurity and Hardware Trust},
  year      = {2027},
  institution = {Amrita Vishwa Vidyapeetham, Chennai}
}
```

---

## Ethical & Responsible Disclosure Notice

This repository was created strictly for academic research, defensive tool development, and educational demonstrations in institutional laboratory environments. Keystroke injection demonstrations must only be conducted against hardware you own or have explicit written authorization to test. The authors assume no liability for misuse.
