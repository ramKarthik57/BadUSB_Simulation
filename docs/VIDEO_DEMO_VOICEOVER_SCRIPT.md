# Project Video Demo — Scene-by-Scene Voice-Over Script (3.5 Minutes, Single Narrator)

**Project Title:** ESP32-S3 Phone-Controlled USB HID Keyboard and Mouse with BadUSB Simulation and Defensive Keystroke Firewall  
**Team Members:** Ram Karthik G (`CH.SC.U4CYS23037`) & Harini V (`CH.SC.U4CYS23010`)  
**Department & Institution:** Department of Cybersecurity, Amrita Vishwa Vidyapeetham, Chennai  
**Target Duration:** ~3 minutes 30 seconds (approx. 450–480 spoken words at a natural 135 WPM pace)  
**Recommended Screen Layout:** Laptop screen recording on the left/main area + Phone screen (or camera view of phone & ESP32-S3) on the right.

---

## Pre-Recording Checklist (30 Seconds Before You Hit Record)
1. **Phone Hotspot:** Turn on your phone's **2.4 GHz mobile hotspot** so the ESP32-S3 connects automatically on boot (`STA IP: 10.85.248.29` or `http://badusb.local`).
2. **Phone Browser:** Have Chrome open on your phone, ready to load `http://10.85.248.29` (or `http://192.168.4.1`).
3. **Laptop Screen:** Close sensitive tabs, keep the desktop clean, and have a terminal or folder ready to launch `python src/firewall.py` in Scene 6.
4. **ESP32-S3:** Hold the ESP32-S3 USB cable ready to plug in during Scene 2.

---

## Scene 1 — Introduction & Problem Statement `[0:00 – 0:35]`

* **Visual / On-Screen Action:**
  * Show Page 1 of [ESP32_S3_HID_Project_Report.pdf](../reports/ESP32_S3_HID_Project_Report.pdf) (Title Banner + Figure 1.1 Architecture Diagram), or show the ESP32-S3 board beside your laptop and smartphone.
* **Voice-Over (Spoken Lines):**
  > "Hello everyone. Today I am presenting our Cybersecurity project: the **ESP32-S3 Phone-Controlled USB HID Keyboard and Mouse with BadUSB Simulation and a Defensive Keystroke Firewall**, developed by **Ram Karthik G** and **Harini V** from the Department of Cybersecurity at Amrita Vishwa Vidyapeetham, Chennai.
  >
  > Modern operating systems implicitly trust any USB keyboard or mouse the moment it is plugged in. Attackers exploit this trust in **BadUSB attacks** to inject high-speed commands without needing any device drivers. At the same time, standard wireless keyboard and mouse apps require installing third-party receiver software on the host PC.
  >
  > Our project solves both challenges in a single platform: using the **ESP32-S3’s native TinyUSB hardware**, we built a driverless, phone-controlled composite USB keyboard and multi-touch mouse, an interruptible **4-scenario BadUSB educational simulator**, and a **Windows Host Keystroke Firewall** to defend against it."

---

## Scene 2 — Plug-and-Play Enumeration & Boot Auto-Run (Scenario 1) `[0:35 – 1:10]`

* **Visual / On-Screen Action:**
  * Plug the ESP32-S3 into the laptop's USB port (`COM5`).
  * Wait 3.5 seconds (`USB_READY_WAIT_MS`). Hands off the laptop keyboard!
  * Watch the laptop automatically open `Win + R`, launch **Notepad**, and type the 3-line security awareness message (**Scenario 1: Notepad Awareness**).
* **Voice-Over (Spoken Lines):**
  > "Let's start with the hardware demonstration. When I plug the ESP32-S3 into the laptop, its native USB OTG controller on GPIO 19 and 20 enumerates simultaneously as a standard USB HID Boot Keyboard and a 3-button Scroll Mouse—with zero drivers installed.
  >
  > Inside our firmware, [`ScenarioController`](../badusb_firmware/scenario_controller.cpp) runs a deterministic 8-state Finite State Machine. It first waits 3.5 seconds for Windows USB enumeration to stabilize, and then automatically executes **Scenario 1: Notepad Awareness**. As you can see on screen, without touching the laptop, the ESP32 opens the Run dialog, launches Notepad, and types an educational security warning."

---

## Scene 3 — Physical GPIO 0 BOOT Button & Phone Web UI Authentication `[1:10 – 1:50]`

* **Visual / On-Screen Action:**
  * Show the **Phone Browser** loading `http://10.85.248.29`. Point out the top telemetry badges (`IDLE`, `USB HID: Ready`, `STA IP: 10.85.248.29`, `AP IP: 192.168.4.1`).
  * Tap the **Settings** tab on the phone, enter the security PIN, and tap **Set PIN & Authenticate**.
  * Switch back to the **Scenarios** tab, then press the physical **BOOT button (GPIO 0)** on the ESP32-S3 once or tap **Next (Physical Sync)** to show Scenario 2 launching (`https://intranet.cb.amrita.edu/`).
* **Voice-Over (Spoken Lines):**
  > "Concurrently, the ESP32-S3 operates in dual **SoftAP plus Station Wi-Fi mode**, connecting directly to my phone’s 2.4 gigahertz hotspot while hosting a responsive dark-mode Single-Page Application from flash memory.
  >
  > To prevent unauthorized wireless access, every command endpoint is protected. In the **Settings** tab, I enter our security PIN, which authenticates against `/api/auth/login` and attaches an `X-Auth-Token` header to all requests.
  >
  > We can advance scenarios either from the phone UI or by pressing the physical **GPIO 0 BOOT button** on the ESP32-S3, which uses a 50-millisecond debounce filter and spinlock-protected command mailbox to cycle circularly from Scenario 1 through 4."

---

## Scene 4 — Direct Scenario Launch & Emergency Stop Safety `[1:50 – 2:20]`

* **Visual / On-Screen Action:**
  * On the phone's **Scenarios** tab, tap **Launch** on **Scenario 4 (Wi-Fi Reconnaissance)** (`netsh wlan show profiles` in Command Prompt).
  * Next, tap **Launch** on **Scenario 3 (Ransomware Awareness)**, and **while it is typing in Notepad**, tap the red **Stop / Abort** button on the phone! Show that typing stops immediately.
* **Voice-Over (Spoken Lines):**
  > "From the **Scenarios** tab, we can also trigger any demonstration directly—such as **Scenario 4**, which opens Command Prompt and runs a non-destructive `netsh wlan show profiles` check to list saved Wi-Fi networks.
  >
  > Unlike traditional static BadUSB tools that blindly finish their payload even if focus is lost, our firmware uses a non-blocking `smartDelay()` loop that polls every 10 milliseconds. If I launch **Scenario 3** and tap the red **Stop / Abort** button mid-execution, the ESP32 halts within 10 milliseconds and calls `releaseAll()` on both keyboard and mouse buses so no modifier keys are ever left stuck."

---

## Scene 5 — Live Remote Keyboard & Multi-Touch Trackpad `[2:20 – 3:00]`

* **Visual / On-Screen Action:**
  * Focus the Notepad window on the laptop.
  * On the phone, switch to the **Keyboard** tab:
    * Tap a few keys on the **Full 6-Row Layout**, or use **Shortcuts** (`Ctrl+A`, `Ctrl+C`, `Ctrl+V`), or send a sentence from the **Text & Live** sub-tab.
  * Switch to the **Mouse** tab on the phone:
    * Drag one finger across the **Touchpad** to smoothly move the laptop cursor.
    * Tap once for Left Click, two-finger tap for Right Click, use two-finger vertical drag to scroll, and show the **Drag Lock** and **Precision Nudge** buttons.
* **Voice-Over (Spoken Lines):**
  > "Beyond security scenarios, the platform transforms the smartphone into a complete driverless wireless peripheral.
  >
  > In the **Keyboard** tab, we have a persistent hardware modifier bar—supporting latched Control, Alt, Shift, and Windows keys—along with four views: a **Full 6-Row Desktop Layout**, one-tap **System Shortcuts**, a **256-character Bulk & Live Text** transmitter, and a **Numeric Keypad**.
  >
  > Switching to the **Mouse** tab gives us a 60-hertz multi-touch trackpad. Single-finger motion sends clamped 8-bit relative cursor deltas to the laptop; a one-finger tap left-clicks; a two-finger tap opens the right-click context menu; and a two-finger drag scrolls the page. It also includes **Drag Lock** and pixel-accurate **Precision Nudge** controls."

---

## Scene 6 — Host-Side Keystroke Firewall Defense & Conclusion `[3:00 – 3:35]`

* **Visual / On-Screen Action:**
  * On the laptop, run `python src/firewall.py` to open the **Keystroke Firewall** GUI window.
  * Point out that its initial state is **ALLOW (Monitoring)**.
  * Click the button to switch the Firewall to **BLOCKING (Armed)** mode.
  * Immediately tap **Launch** on Scenario 1 (or type from the phone keyboard). Show that **zero characters reach Notepad** because the firewall suppresses them!
  * Point out the **15-second fail-safe auto-disarm timer** returning the firewall to ALLOW mode so the user is never locked out.
* **Voice-Over (Spoken Lines):**
  > "Finally, to demonstrate endpoint defense against unauthorized HID injection, we built a **Windows Host Keystroke Firewall** in Python.
  >
  > When I arm the firewall into **BLOCKING** mode, it registers a Win32 low-level keyboard hook—`WH_KEYBOARD_LL`—with global event suppression enabled. Now, when I trigger a BadUSB scenario or type from the phone, the firewall intercepts and drops the injected scancodes at the operating-system hook layer before they ever reach the foreground application.
  >
  > To prevent accidental host lockout, the firewall includes a **15-second fail-safe watchdog timer** and clean exit handlers that automatically disarm the hook and restore normal keyboard input.
  >
  > Together, our ESP32-S3 firmware, mobile web controller, and host firewall passed **all 22 automated unit, simulation, and live browser tests**, delivering a complete offensive-and-defensive USB HID platform. Thank you for watching!"
