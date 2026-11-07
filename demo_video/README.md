# WHID-Guard: 5-Minute Technical Project Demonstration Video

**Project Title:** WHID-Guard: Dual-Mode ESP32-S3 BadUSB Emulation Platform & Behavioral Keystroke Dynamics Defense  
**Student Authors:** Ram Karthik G (`CH.SC.U4CYS23037`) & Harini V (`CH.SC.U4CYS23010`)  
**Department & Institution:** Department of Cybersecurity, Amrita Vishwa Vidyapeetham, Chennai  
**Evaluation Target:** Faculty Project Evaluation, Academic Viva Voce, and IEEE Conference Demonstration  

---

## Video Specifications

| Parameter | Specification | Details |
| :--- | :--- | :--- |
| **Output File** | [`WHID_Guard_5Min_Demo_1080p.mp4`](WHID_Guard_5Min_Demo_1080p.mp4) | High-definition master demo video |
| **Video Resolution** | **1920 x 1080 (1080p Full HD)** | Enhanced 1080p 30 fps progressive scan |
| **Video Codec** | H.264 / MPEG-4 AVC (`libx264`, High Profile, CRF 18) | Visually lossless, universal playback |
| **Audio Track** | AAC Stereo @ 48 kHz (192 kbps) | Studio-grade natural neural narration |
| **Narration Voice** | `en-US-ChristopherNeural` | Authoritative, articulate technical delivery |
| **Subtitles** | **Burned-in High-Contrast 1080p Subtitles** | Stylized subtitle overlay inside dedicated container |
| **Subtitle File** | [`subtitles.srt`](subtitles.srt) & [`subtitles.ass`](subtitles.ass) | Standalone subtitle tracks for external players |
| **Total Duration** | **5 minutes 14 seconds (314.15 seconds)** | Paced for 5-minute academic evaluation |
| **File Size** | **13.86 MB** | Lightweight, emailable, and fast streaming |

---

## Timestamped Scene Breakdown & Table of Contents

| Time | Scene | Topic & Demonstrated Features | Primary Figures & Visuals |
| :---: | :--- | :--- | :--- |
| **`00:00 - 00:39`** | **Scene 1** | **Introduction & Problem Statement**<br/>• Student authors & institution<br/>• Inherent USB HID trust paradigm<br/>• High-speed automated hardware injection | Project Title Banner, Team Roll Numbers, End-to-End Cyber-Physical Architecture (Figure 1). |
| **`00:39 - 01:20`** | **Scene 2** | **Hardware Architecture & Dual-Port Topology**<br/>• ESP32-S3 dual-core LX7 @ 240 MHz<br/>• Native USB-OTG on GPIO 19/20 (Port 2)<br/>• CP210x UART bridge on Port 1 (`COM5`) | Hardware interconnect schematics, dual Type-C port isolation, and power specs (Figure 2). |
| **`01:20 - 02:00`** | **Scene 3** | **Deterministic Finite State Machine & Payloads**<br/>• 8-state deterministic FSM<br/>• Scenarios 1–4 educational catalogue<br/>• GPIO 0 BOOT button edge debouncing | 8-State Scenario FSM Diagram (Figure 3), safe `releaseAll()` key release invariants. |
| **`02:00 - 02:36`** | **Scene 4** | **Mobile Web Controller & Remote Peripheral Suite**<br/>• PROGMEM flash dark-mode SPA<br/>• Tokenized PIN authentication (`badusb123`)<br/>• 6-Row QWERTY, numpad, shortcuts, trackpad | Real mobile UI captures (Figure 4) showing Scenarios, Keyboard, and Touchpad Mouse. |
| **`02:36 - 03:10`** | **Scene 5** | **Adversarial Resilience & Cadence Emulation**<br/>• Limitations of static speed thresholds<br/>• Stochastic timing jitter ($\Delta t = \text{base} + \text{jitter}$)<br/>• Cognitive micro-pauses (150–300 ms) | Firmware cadence emulation formulation, mobile UI stealth toggle, and timing waveform (Figure 5). |
| **`03:10 - 03:49`** | **Scene 6** | **Behavioral Keystroke Dynamics Engine**<br/>• Online sliding window ($W = 10$ events)<br/>• Mean IKI ($\mu$), std ($\sigma$), coefficient of variation ($CV$)<br/>• Decision boundary: $CV < 0.15 \Rightarrow$ Machine Lock | Empirical IKI Distribution Histogram (Figure 6) comparing Human vs. BadUSB vs. Evasion. |
| **`03:49 - 04:22`** | **Scene 7** | **Hardware Attribution & Selective Quarantine**<br/>• Windows Raw Input `WM_INPUT` sink<br/>• Hardware handle (`hDevice`) & VID/PID extraction<br/>• Selective `WH_KEYBOARD_LL` driver hook filter | Selective Defense Pipeline Diagram (Figure 7), 15s watchdog failsafe, zero legitimate lockout. |
| **`04:22 - 04:58`** | **Scene 8** | **Quantitative Empirical Benchmark Results**<br/>• 1,500-keystroke empirical corpus<br/>• 0.0% False Positive Rate on human typing<br/>• 98.6% True Positive Rate, $<85\text{ ms}$ ($\le 8$ chars) quarantine | Quarantine Latency Curve (Figure 8) and quantitative empirical evaluation data matrix. |
| **`04:58 - 05:14`** | **Scene 9** | **Conclusion, IEEE Publication & Open Source**<br/>• 6-Page IEEE Conference Paper package<br/>• Open-source GitHub repository release<br/>• Faculty and departmental acknowledgments | Published IEEE Paper Preview (Figure 9) and GitHub repository link. |

---

## Full Voice-Over Narration Script

### Scene 1: Introduction & Problem Statement [00:00 – 00:39]
> *"Hello everyone, and welcome to our demonstration of WHID-Guard: an ESP32-S3 Phone-Controlled USB HID Keyboard and Mouse platform with BadUSB Simulation and a Defensive Keystroke Firewall. Developed by Ram Karthik G and Harini V from the Department of Cybersecurity at Amrita Vishwa Vidyapeetham, Chennai. Modern operating systems implicitly trust Human Interface Devices, allowing unauthorized hardware implants to inject destructive payloads at microsecond bus speeds without host consent. WHID-Guard provides an interruptible hardware emulation suite paired with an intelligent, per-device behavioral defense."*

### Scene 2: Hardware Architecture & Dual-Port Topology [00:39 – 01:20]
> *"The system is powered by the ESP32-S3 dual-core microcontroller running at 240 megahertz with native USB-OTG full-speed hardware directly on GPIO 19 and 20. Our custom dual-port topology cleanly isolates attack vectors from developer controls. The primary USB-OTG port connects to the target laptop, enumerating immediately as a standard driverless composite HID keyboard and multi-button mouse. Concurrently, the CP210x UART bridge on Port 1 provides isolated serial telemetry and firmware flashing on COM5, ensuring continuous laboratory monitoring without disrupting the target host's USB bus."*

### Scene 3: Deterministic Finite State Machine & Payloads [01:20 – 02:00]
> *"Inside the firmware, an 8-state deterministic Finite State Machine governs scenario lifecycles. Upon initial connection, it enforces a bounded 3.5-second wait for host USB enumeration to stabilize, and then automatically executes Scenario 1: an educational Notepad security awareness notification. The platform includes four demonstration scenarios: Notepad awareness, institutional portal redirection, simulated PowerShell ransomware alerts, and Wi-Fi profile reconnaissance. Scenarios can also be advanced offline using the physical GPIO 0 BOOT button, which employs a 50-millisecond hardware debounce filter."*

### Scene 4: Mobile Web Controller & Remote Peripheral Suite [02:00 – 02:36]
> *"Concurrently, the ESP32-S3 broadcasts a 2.4 gigahertz Wi-Fi network, hosting a responsive dark-mode Single-Page Application served entirely from PROGMEM flash memory. Users authenticate against our REST API using a secure PIN, which issues tokenized credentials. The interface features one-touch scenario execution with live status polling, a complete 6-row QWERTY keyboard with latched modifiers and system shortcuts, a 256-character bulk text transmitter, and a 60-hertz virtual trackpad mouse with relative motion clamping and precision drag-lock controls."*

### Scene 5: Adversarial Resilience & Human Cadence Emulation [02:36 – 03:10]
> *"Standard BadUSB tools inject keystrokes at rigid 10-millisecond intervals, making them trivial to block with rudimentary speed limiters. To rigorously test defensive resilience, we implemented an adversarial stealth mode in the ESP32-S3 firmware. When toggled from the mobile interface, the controller replaces deterministic timing with stochastic jitter and automatically injects cognitive micro-pauses of 150 to 300 milliseconds following whitespace and punctuation marks, mimicking the natural neuromuscular delays of human operators."*

### Scene 6: WHID-Guard Behavioral Keystroke Dynamics Engine [03:10 – 03:49]
> *"To counter these sophisticated threats, we developed the WHID-Guard host defense engine. Rather than relying on simplistic rate limits, WHID-Guard computes behavioral keystroke dynamics over an online sliding window of ten events. It continuously calculates the mean Inter-Key Interval, standard deviation, coefficient of variation, and burst typing rate. While human typing exhibits natural cognitive variance with a coefficient of variation exceeding 0.30, unconstrained BadUSB injection demonstrates rigid consistency below 0.15, enabling precise algorithmic classification without false alarms."*

### Scene 7: Per-Device Hardware Attribution & Selective Isolation [03:49 – 04:22]
> *"Traditional security tools install global keyboard hooks that lock out all typing indiscriminately. WHID-Guard solves this problem through per-device hardware attribution via the Windows Raw Input API. By registering for raw input message sinks and querying device names, our engine extracts the physical hardware device handle and USB Vendor and Product IDs. When an injection attack is detected, our low-level keyboard hook drops only the malicious hardware packets, keeping the user's legitimate laptop keyboard completely active and responsive."*

### Scene 8: Quantitative Empirical Evaluation & Benchmark Results [04:22 – 04:58]
> *"We conducted an extensive empirical evaluation across a 1,500-keystroke benchmark corpus. On human baseline typing, WHID-Guard achieved a 0.0 percent False Positive Rate across 500 consecutive keystrokes. Against unconstrained BadUSB attacks, the system achieved a 98.6 percent True Positive Detection Rate, quarantining the offending implant within exactly 8 characters—less than 85 milliseconds of total execution time. Against stealth cadence emulation, it successfully flagged 25.2 percent of suspicious events."*

### Scene 9: Conclusion, IEEE Publication & Open-Source Release [04:58 – 05:14]
> *"In conclusion, WHID-Guard bridges offensive hardware exploration and host-level defensive resilience. Our complete research manuscript and reproducible codebase are open-sourced on GitHub. Thank you for your evaluation of our project."*

---

## How to Play and Submit

- **Direct Local Playback**: Open [`demo_video/WHID_Guard_5Min_Demo_1080p.mp4`](WHID_Guard_5Min_Demo_1080p.mp4) in any media player (Windows Media Player, VLC, QuickTime, Chrome, Edge).
- **Subtitles**: Subtitles are already burned into the video in high-contrast 1080p format. The standalone [`subtitles.srt`](subtitles.srt) is also provided for platforms like YouTube or Microsoft Teams.
- **Faculty Evaluation**: Share the MP4 file directly via pen drive, Google Drive, OneDrive, or upload to the course submission portal.
