# Security Policy & Responsible Disclosure

## Supported Versions

Only the latest release and the current `main` branch receive active security updates, defense rule refinements, and bug fixes.

| Version / Branch | Supported | Release Date |
| :--- | :---: | :--- |
| `main` (v2.1.0+) | :white_check_mark: | Active Development |
| `< 2.0.0` | :x: | Deprecated |

---

## Purpose & Scope

**WHID-Guard** is an open-source academic cybersecurity research platform designed to evaluate Human Interface Device (HID) keystroke injection attacks and develop defense-in-depth countermeasures using real-time behavioral keystroke dynamics and hardware attribution.

This repository includes:
1. **Defensive Engine (`src/`)**: Detection heuristics, Inter-Key Interval (IKI) statistics, and per-device low-level keyboard hooks.
2. **Controlled Hardware Payloads (`badusb_firmware/`)**: Benign, non-destructive educational demonstration payloads (Notepad awareness, read-only network enumeration, simulated alert dialogs).

---

## Reporting Vulnerabilities

If you discover a security vulnerability within the defensive framework (such as a bypass technique, hook escape, memory corruption in the C++ firmware, or denial-of-service in the host monitor):

1. **Do NOT open a public GitHub Issue.**
2. Send a detailed vulnerability report via email to the project maintainers:
   - **Lead Researcher**: `ramkarthik5757@gmail.com`
3. Include the following details in your advisory:
   - Operating system and kernel version.
   - Exact firmware build configuration and microcontroller revision.
   - Step-by-step reproduction instructions and proof-of-concept (PoC) code.
   - Proposed remediation or defensive patch if available.

### Disclosure Timeline
- **Initial Response**: Within 48 hours of receipt.
- **Triage & Assessment**: Within 5 business days.
- **Patch Development & Verification**: Within 30 days.
- **Public Disclosure**: Coordinated after defensive mitigations have been merged into the `main` branch.

---

## Academic & Educational Use Disclaimer

This software and hardware firmware are provided strictly for research, laboratory verification, and defensive engineering. Deploying hardware implants or keystroke injection scripts against computing systems without explicit, prior written authorization from the system owner is unlawful. The authors and affiliated institutions disclaim all liability for damages resulting from misuse.
