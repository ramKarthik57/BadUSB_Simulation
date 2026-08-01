# BadUSB Simulation

**Educational BadUSB Attack Simulation & Keystroke-Injection Defense on ESP32-S3**

This project demonstrates, in a controlled and educational context, how a
programmable USB HID device (an ESP32-S3 running TinyUSB) can impersonate a
keyboard and inject keystrokes into a host machine — the mechanism behind
real-world "BadUSB" attacks — alongside a companion Windows defense tool that
detects and blocks unauthorized automated keystroke injection.

> ⚠️ **For authorized, educational, and research use only.** Only run the
> firmware against hardware/systems you own or have explicit permission to
> test. See [Disclaimer](#disclaimer).

---

## Overview

The project has two parts:

1. **Attack simulation (firmware)** — `tusb_hid_example_main.c` runs on an
   ESP32-S3 Devkit and uses [TinyUSB](https://github.com/hathach/tinyusb) to
   present the board to a host computer as a standard USB HID keyboard. On a
   button press, it "types" one of several pre-programmed demo payloads to
   illustrate how an attacker-controlled USB device can execute commands
   without any user typing.
2. **Defense tool (`firewall.py`)** — A Windows desktop utility ("Keystroke
   Firewall") built with `tkinter` and the `keyboard` library that hooks the
   keyboard input stream and can suppress/block keystrokes system-wide,
   simulating a countermeasure against unattended/injected keyboard input.

A full write-up of the methodology, threat model, and results is included in
`BadUSB_Report_Final.pdf` / `.docx`.

## How the Attack Simulation Works

- The ESP32-S3 enumerates over USB as a standard HID keyboard (no drivers
  required on the host — this is what makes BadUSB attacks effective).
- Pressing the onboard button (`GPIO0`) triggers `run_payload()`, which
  cycles through four demo payloads on successive presses:

  | # | Payload             | What it demonstrates                                          |
  |---|----------------------|----------------------------------------------------------------|
  | 1 | `payload_notepad`     | Opens Notepad and types an on-screen awareness message        |
  | 2 | `payload_website`      | Opens a command prompt and launches a browser to a URL       |
  | 3 | `payload_awareness`     | Opens PowerShell and invokes a local awareness/demo script  |
  | 4 | `payload_wifi_demo`      | Opens a command prompt and lists saved Wi-Fi profile names |

- All payloads are intentionally benign/demonstrative — they open visible
  applications and print awareness text rather than exfiltrating data or
  causing damage — to illustrate the *injection technique* without
  performing a real attack.

## How the Defense Tool Works

`firewall.py` provides a minimal always-on-top desktop widget with a single
toggle:

- **ALLOW** — keystrokes pass through normally.
- **BLOCKING** — a low-level keyboard hook (`keyboard.hook(..., suppress=True)`)
  intercepts and suppresses all keystroke events, which would also block
  injected HID keystrokes from a malicious USB device.

This is a proof-of-concept mitigation, not a production security control —
see [Limitations](#limitations).

## Hardware & Software Requirements

### Firmware (attack simulation)

- ESP32-S3 development board (Devkit) with native USB OTG support
- [ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/get-started/) toolchain
- TinyUSB component (bundled with ESP-IDF)

### Defense tool

- Windows 10/11
- Python 3.9+
- Dependencies: `keyboard`, `tkinter` (bundled with most Python installs)

## Getting Started

### 1. Flash the firmware

```bash
# From an ESP-IDF project containing this file as main/main.c
idf.py set-target esp32s3
idf.py build
idf.py -p <PORT> flash monitor
```

Connect the ESP32-S3 to a **test machine** via USB. Press the onboard button
(`GPIO0`) to cycle through and trigger the demo payloads.

### 2. Run the defense tool

```bash
pip install keyboard
python firewall.py
```

> `keyboard` requires elevated/administrator privileges on Windows to
> install a global hook.

Toggle the on-screen button to switch between **ALLOW** and **BLOCKING**.

## Project Structure

```
BadUSB_Simulation/
├── tusb_hid_example_main.c      # ESP32-S3 TinyUSB HID keyboard emulation & demo payloads
├── firewall.py                   # Windows keystroke-injection defense utility
├── BadUSB_Report_Final.pdf        # Full research write-up (report)
└── BadUSB_Report_Final.docx       # Full research write-up (editable)
```

## Limitations

- The defense tool suppresses **all** keyboard input while active, including
  legitimate input — it does not yet distinguish HID-injected keystrokes
  from genuine ones (e.g. by timing/cadence analysis or USB device
  enumeration checks).
- The firmware payloads are illustrative demos, not a general-purpose
  attack framework.
- This is a research/learning project, not a hardened security product.

## Disclaimer

This project is intended strictly for **educational purposes and authorized
security research**. Using this firmware or technique against systems you do
not own or lack explicit permission to test is illegal in most
jurisdictions. The authors and contributors assume no liability for misuse
or damage caused by this project.

## License

Released under the [MIT License](LICENSE).
