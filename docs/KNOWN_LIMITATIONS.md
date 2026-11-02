# Known Technical Limitations & Constraints

This document outlines architectural and environmental limitations inherent to USB Human Interface Device (HID) emulation, local Wi-Fi control, and host operating system security.

---

## 1. USB HID Keyboard & Layout Constraints

1. **US English (QWERTY) Assumption**:
   - USB keyboards transmit physical HID keycodes (Usage IDs per USB HID Usage Tables v1.3), not characters.
   - The ESP32 firmware maps standard ASCII characters to standard US English keycodes. If the host computer is configured with an alternative keyboard layout (e.g. French AZERTY, German QWERTZ, or UK English):
     - Keys such as `Z` and `Y` may be swapped.
     - Punctuation symbols such as `@`, `:`, `_`, and `/` may produce different characters.
2. **Unicode & Non-ASCII Characters**:
   - The USB HID keyboard protocol does not support direct transmission of multi-byte Unicode strings or emojis without specialized OS-specific mechanisms (e.g., Windows `Alt` + Numpad sequences).
   - The firmware gracefully filters out non-ASCII characters outside the standard printable ASCII range (`0x20` to `0x7E`).
3. **Blind Input & Active Window Focus**:
   - USB keyboards have no feedback channel to know which window has focus on the host operating system. Keystrokes are typed directly into whichever window is currently active.
   - If a background process, notification, or user mouse click changes active window focus while a sequence is executing, keystrokes will be received by the new active window.

---

## 2. Wi-Fi & Web Controller Constraints

1. **Unencrypted HTTP on Local Network**:
   - The ESP32 local web server operates over plain HTTP (Port 80) rather than HTTPS due to TLS memory and certificate authority constraints on embedded microcontrollers.
   - Traffic, including the authentication PIN and typed text, is transmitted in cleartext across the local wireless subnet. The network should remain restricted to trusted devices.
2. **mDNS Resolution on Android**:
   - While iOS (Safari) and macOS resolve `.local` domains out of the box via Bonjour, some older Android versions or custom vendor skins do not query mDNS natively without Chrome mDNS flags enabled.
   - In such cases, connect using the ESP32's direct IP address (`http://192.168.4.1` in SoftAP mode or the assigned hotspot IP).
3. **Intermittent Cellular Data Override**:
   - When connecting your phone directly to the ESP32's SoftAP (`BadUSB-Controller`), mobile operating systems (iOS/Android) may detect "No Internet Access" and automatically route browser traffic over cellular data.
   - To prevent this, either connect your phone to the hotspot mode where cellular data remains active, or temporarily disable mobile data while directly connected to the ESP32's SoftAP.

---

## 3. Host-Side Defensive Firewall Limitations

1. **Global Keyboard Interception vs. Device-Level Filtering**:
   - The Python keystroke defense application ([`src/firewall.py`](file:///c:/Users/Ram/Desktop/BadUSB_Using_ESP32/src/firewall.py)) uses a Windows user-mode low-level keyboard hook (`WH_KEYBOARD_LL`).
   - This hook operates globally across all input devices connected to the machine. While **BLOCKING** is active, keystrokes from both the ESP32 and the user's physical laptop keyboard are suppressed.
   - Standard user-mode Windows APIs cannot selectively isolate keystrokes to a specific USB hardware VID/PID without a custom Kernel-Mode Filter Driver (such as a Upper Filter Driver for `KeyboardClassServiceCallback`).
2. **Watchdog Safety Timeout**:
   - To mitigate accidental user lockout caused by global suppression, the firewall enforces a 15-second auto-disarm timer. In a production enterprise setting, permanent kernel-level device whitelisting is required.
