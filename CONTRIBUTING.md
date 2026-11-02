# Contributing to WHID-Guard & BadUSB Research Platform

Thank you for your interest in contributing to **WHID-Guard**! We welcome contributions ranging from firmware optimizations and defensive modeling to empirical benchmarks and documentation.

---

## Code of Conduct & Ethical Guidelines

This repository contains dual-purpose security research materials:
1. **Defensive Research**: Keystroke dynamics modeling, hardware attribution, and selective driver suppression.
2. **Offensive Emulation**: Controlled hardware payloads for educational and defensive evaluation.

**Strict Ethical Constraint**: Contributions introducing destructive payloads, weaponized evasion techniques without defensive counterparts, or malicious exploits targeting external systems will be rejected immediately.

---

## Development Workflow

1. **Fork the Repository**:
   Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Set Up Python Virtual Environment**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate   # Windows
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Run Automated Tests**:
   All contributions must pass the local test suite prior to submitting a PR:
   ```bash
   pytest -v
   ```

4. **Firmware Guidelines (`badusb_firmware/`)**:
   - Firmware is written for the **ESP32-S3** using the Arduino ESP32 core (`v3.0+`) with native USB-OTG CDC/HID support.
   - Maintain non-blocking state loops in `badusb_firmware.ino`. Avoid unbounded `delay()` calls in web handlers or event loops.
   - Keep PROGMEM assets in `web_assets.h` lightweight and compressed where possible.
   - Compile firmware locally to verify syntax before opening a PR:
     ```bash
     arduino-cli compile --fqbn esp32:esp32:esp32s3:CDCOnBoot=cdc,USBMode=hwcdc badusb_firmware
     ```

5. **Python & Defense Engine Guidelines (`src/`)**:
   - Follow PEP 8 guidelines.
   - Windows API interactions via `ctypes` must use explicit 64-bit struct definitions (e.g. `POINT`, `RAWINPUTHEADER`, `wintypes`) with declared `argtypes` and `restype`.
   - Never suppress keystrokes indiscriminately without verifying device attribution handles (`hDevice`).

6. **Submitting Pull Requests**:
   - Commit messages must follow conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`.
   - Ensure the pull request template is completely filled out.
