# MITRE ATT&CK® Threat Mapping & Defensive Coverage

This document outlines the formal mapping of offensive demonstration vectors and defensive mitigations implemented in **WHID-Guard** against the **MITRE ATT&CK® Enterprise Framework**.

---

## 1. Offensive Attack Vectors (Implant Emulation)

The ESP32-S3 hardware implant emulates composite USB HID peripherals to demonstrate attack techniques across the initial access and execution tactics:

| Tactic | Technique ID | Technique Name | Project Implementation & Mechanism |
| :--- | :--- | :--- | :--- |
| **Initial Access** | [T1200](https://attack.mitre.org/techniques/T1200/) | **Hardware Additions** | Microcontroller connects via native USB-OTG full-speed port (GPIO 19/20), presenting standard boot keyboard and mouse HID descriptors. |
| **Execution** | [T1059.001](https://attack.mitre.org/techniques/T1059/001/) | **PowerShell** | Scenario 3 demonstrates script-based execution via `Win + R` &rarr; `powershell.exe -NoProfile -ExecutionPolicy Bypass`. |
| **Execution** | [T1059.003](https://attack.mitre.org/techniques/T1059/003/) | **Windows Command Shell** | Scenario 2 and Scenario 4 demonstrate automated terminal invocation via `Win + R` &rarr; `cmd.exe /c ...`. |
| **Discovery** | [T1016](https://attack.mitre.org/techniques/T1016/) | **System Network Configuration Discovery** | Scenario 4 issues `netsh wlan show profiles` to enumerate stored Wi-Fi configurations non-destructively. |
| **Defense Evasion** | [T1036](https://attack.mitre.org/techniques/T1036/) | **Masquerading** | Firmware presents legitimate USB Vendor ID (`0x303A`) and Product ID (`0x1001`) with descriptor name `"BadUSB Demo"`, evading standard device blocklists. |
| **Defense Evasion** | [T1027](https://attack.mitre.org/techniques/T1027/) | **Obfuscated Files or Information (Cadence Jitter)** | Adversarial stealth mode inserts randomized Gaussian delays ($\Delta t = \text{base} + \text{jitter}$) and cognitive micro-pauses (150–300 ms) to evade static speed thresholds. |

---

## 2. Defensive Countermeasures (WHID-Guard Host Engine)

WHID-Guard deploys multi-tiered countermeasures across detection, attribution, and mitigation layers:

| Layer | ATT&CK Mitigation / D3FEND Matrix | Countermeasure Description | Defensive Implementation |
| :--- | :--- | :--- | :--- |
| **Behavioral Detection** | **D3-KBA (Keystroke Behavioral Analysis)** | Evaluates Inter-Key Interval (IKI) statistics over a sliding window ($W=10$). Discriminates between human variance ($CV > 0.30$) and machine bursts ($CV < 0.15$). | [`src/detection/keystroke_dynamics.py`](file:///c:/Users/Ram/Desktop/BadUSB_Using_ESP32/src/detection/keystroke_dynamics.py) |
| **Device Attribution** | **D3-HDA (Hardware Device Attribution)** | Monitors `WM_INPUT` messages via Windows Raw Input API (`RIDEV_INPUTSINK`). Queries `GetRawInputDeviceInfoW` to isolate physical `hDevice` handles and VID/PID. | [`src/detection/raw_input_monitor.py`](file:///c:/Users/Ram/Desktop/BadUSB_Using_ESP32/src/detection/raw_input_monitor.py) |
| **Driver Isolation** | **M1013 (Application Execution Control / Input Filter)** | Installs low-level hook (`WH_KEYBOARD_LL`). Selectively drops keystrokes matching quarantined `hDevice`, maintaining responsiveness of legitimate peripherals. | [`src/firewall.py`](file:///c:/Users/Ram/Desktop/BadUSB_Using_ESP32/src/firewall.py) |
| **Failsafe Watchdog** | **Operational Resilience** | Background watchdog timer automatically releases hooks after 15 seconds to prevent accidental permanent user lockout. | [`src/firewall.py`](file:///c:/Users/Ram/Desktop/BadUSB_Using_ESP32/src/firewall.py) |

---

## 3. Quantitative Evasion vs. Detection Matrix

| Metric | Baseline Human Operator | Standard BadUSB (Unconstrained) | Stealth BadUSB (Human Emulation) |
| :--- | :---: | :---: | :---: |
| **Injection Cadence ($\mu_{\text{IKI}}$)** | $144.18\text{ ms}$ | $10.01\text{ ms}$ | $119.28\text{ ms}$ |
| **Coefficient of Variation ($CV$)** | $0.638$ | $0.0784$ | $0.4098$ |
| **Typing Rate** | $6.94\text{ chars/s}$ | $99.95\text{ chars/s}$ | $8.38\text{ chars/s}$ |
| **Quarantine Trigger** | Authorized (`SAFE`) | **8 characters (<85 ms)** | Anomaly Alert (`SUSPICIOUS`) |
| **MITRE Threat Neutralization** | N/A | **Pre-Execution Quarantined** | **Flagged Before Command Dispatch** |
