import os
import json
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1920
HEIGHT = 1080

FONT_PATH_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_PATH_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_PATH_MONO = r"C:\Windows\Fonts\consola.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def render_base_template(scene_idx, total_scenes, scene_title, time_range):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(11, 15, 25)) # #0b0f19
    draw = ImageDraw.Draw(img)

    # Subtle background grid pattern
    for x in range(0, WIDTH, 80):
        draw.line([(x, 0), (x, HEIGHT)], fill=(16, 22, 35), width=1)
    for y in range(0, HEIGHT, 80):
        draw.line([(0, y), (WIDTH, y)], fill=(16, 22, 35), width=1)

    # Top Header Bar
    draw_rounded_rect(draw, (40, 20, 1880, 95), radius=12, fill=(18, 24, 38), outline=(48, 54, 61), width=1)
    
    # Header Branding
    f_univ = get_font(FONT_PATH_BOLD, 16)
    f_proj = get_font(FONT_PATH_BOLD, 22)
    draw.text((65, 32), "AMRITA VISHWA VIDYAPEETHAM  |  DEPARTMENT OF CYBERSECURITY", font=f_univ, fill=(139, 148, 158))
    draw.text((65, 58), "WHID-GUARD  —  DUAL-MODE ESP32-S3 BADUSB & DEFENSIVE PLATFORM", font=f_proj, fill=(88, 166, 255))

    # Scene & Timestamp Pill
    f_badge = get_font(FONT_PATH_BOLD, 15)
    f_time = get_font(FONT_PATH_MONO, 15)
    badge_x = 1530
    draw_rounded_rect(draw, (badge_x, 34, 1680, 78), radius=8, fill=(33, 38, 45), outline=(56, 139, 253), width=1)
    draw.text((badge_x + 18, 46), f"SCENE {scene_idx:02d} / {total_scenes:02d}", font=f_badge, fill=(88, 166, 255))
    
    draw_rounded_rect(draw, (1700, 34, 1855, 78), radius=8, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((1718, 46), time_range, font=f_time, fill=(63, 185, 80)) # Green

    # Bottom Subtitle Box Placeholder
    draw_rounded_rect(draw, (40, 935, 1880, 1055), radius=12, fill=(13, 17, 23), outline=(48, 54, 61), width=1)
    
    # Progress bar line at the very bottom
    draw.line([(0, 1076), (WIDTH, 1076)], fill=(22, 27, 34), width=4)
    progress_w = int(WIDTH * (scene_idx / total_scenes))
    draw.line([(0, 1076), (progress_w, 1076)], fill=(88, 166, 255), width=4)

    return img, draw

def place_image_card(base_img, img_path, bbox, title_label=None):
    if not os.path.exists(img_path):
        return
    x0, y0, x1, y1 = bbox
    target_w = x1 - x0
    target_h = y1 - y0

    # Draw card backing
    draw = ImageDraw.Draw(base_img)
    draw_rounded_rect(draw, (x0 - 4, y0 - 4, x1 + 4, y1 + 4), radius=14, fill=(18, 24, 38), outline=(56, 139, 253), width=1)

    with Image.open(img_path) as im:
        if im.mode != "RGB":
            im = im.convert("RGB")
        im.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
        actual_w, actual_h = im.size
        # Center inside target box
        offset_x = x0 + (target_w - actual_w) // 2
        offset_y = y0 + (target_h - actual_h) // 2
        base_img.paste(im, (offset_x, offset_y))

    if title_label:
        f_lbl = get_font(FONT_PATH_BOLD, 14)
        draw.text((x0 + 10, y0 - 26), title_label.upper(), font=f_lbl, fill=(88, 166, 255))

def render_scene_1(time_range):
    img, draw = render_base_template(1, 9, "Introduction & Problem Statement", time_range)
    
    # Left Content
    f_h1 = get_font(FONT_PATH_BOLD, 38)
    f_sub = get_font(FONT_PATH_REG, 20)
    f_item = get_font(FONT_PATH_REG, 18)
    f_bold = get_font(FONT_PATH_BOLD, 18)

    draw.text((80, 130), "WHID-Guard: USB HID Threat & Defense", font=f_h1, fill=(240, 246, 252))
    draw.text((80, 180), "Dual-Mode Cyber-Physical Hardware Emulation & Behavioral Protection", font=f_sub, fill=(139, 148, 158))

    # Authors card
    draw_rounded_rect(draw, (80, 230, 880, 350), radius=10, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    f_tag = get_font(FONT_PATH_BOLD, 14)
    draw.text((105, 248), "RESEARCH TEAM & ACADEMIC ATTRIBUTION", font=f_tag, fill=(88, 166, 255))
    draw.text((105, 278), "• Ram Karthik G", font=f_bold, fill=(240, 246, 252))
    draw.text((275, 278), "(Roll No: CH.SC.U4CYS23037)  —  Lead Researcher", font=f_item, fill=(139, 148, 158))
    draw.text((105, 310), "• Harini V", font=f_bold, fill=(240, 246, 252))
    draw.text((275, 310), "(Roll No: CH.SC.U4CYS23010)  —  Co-Researcher", font=f_item, fill=(139, 148, 158))

    # Problem Statement Cards
    draw_rounded_rect(draw, (80, 370, 880, 560), radius=10, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((105, 390), "THE SYSTEMIC USB HID TRUST PARADIGM", font=f_tag, fill=(248, 81, 73)) # Red
    bullets = [
        "1. Implicit OS Trust: Host operating systems unconditionally accept HID input.",
        "2. Zero Driver Requirement: Standard boot keyboards require no driver checks.",
        "3. High-Speed Machine Injection: Microcontrollers type >100 characters/second.",
        "4. Conventional Security Blindspot: Antivirus & EDR monitor software, not physical USB bus."
    ]
    y_off = 425
    for b in bullets:
        draw.text((105, y_off), b, font=f_item, fill=(201, 209, 217))
        y_off += 30

    # WHID-Guard Solution Box
    draw_rounded_rect(draw, (80, 580, 880, 770), radius=10, fill=(16, 28, 22), outline=(46, 160, 67), width=1)
    draw.text((105, 600), "THE WHID-GUARD SOLUTION", font=f_tag, fill=(63, 185, 80)) # Green
    sol_bullets = [
        "• Offensive Implant: ESP32-S3 composite keyboard + mouse with Wi-Fi web remote.",
        "• Safety Invariant: Interruptible finite state machine with hardware STOP control.",
        "• Defense Engine: Real-time Keystroke Dynamics analyzing Inter-Key Intervals (IKI).",
        "• Per-Device Attribution: Windows Raw Input isolates offending device handles."
    ]
    y_off = 635
    for b in sol_bullets:
        draw.text((105, y_off), b, font=f_item, fill=(201, 209, 217))
        y_off += 30

    # Right Column: System Architecture Figure
    place_image_card(img, "reports/assets/system_architecture.png", (940, 150, 1850, 770), "Figure 1: End-to-End Cyber-Physical Architecture")

    return img

def render_scene_2(time_range):
    img, draw = render_base_template(2, 9, "Hardware Architecture & Dual-Port Topology", time_range)
    
    f_h1 = get_font(FONT_PATH_BOLD, 36)
    f_sub = get_font(FONT_PATH_REG, 20)
    f_item = get_font(FONT_PATH_REG, 17)
    f_bold = get_font(FONT_PATH_BOLD, 17)
    f_tag = get_font(FONT_PATH_BOLD, 14)

    draw.text((80, 130), "ESP32-S3 Dual-Port Hardware Architecture", font=f_h1, fill=(240, 246, 252))
    draw.text((80, 175), "Xtensa® Dual-Core LX7 @ 240 MHz  •  Native Full-Speed USB-OTG", font=f_sub, fill=(139, 148, 158))

    # Port Comparison Table Card
    draw_rounded_rect(draw, (80, 225, 900, 520), radius=10, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((105, 245), "DUAL-PORT ISOLATION TOPOLOGY", font=f_tag, fill=(88, 166, 255))

    ports = [
        ("Port 1: CP210x UART Bridge", "(COM5)", "Programming, esptool flashing & serial debugging (115200 baud).", (139, 148, 158)),
        ("Port 2: Native USB-OTG", "(GPIO 19/20)", "Direct hardware PHY emulating composite USB HID Keyboard & Mouse.", (63, 185, 80)),
        ("GPIO 0 BOOT Button", "(Debounced)", "Hardware falling-edge trigger cycling offline payload sequences.", (210, 153, 34)),
        ("Power Management", "(5V VBUS)", "Draws ~145 mA active (concurrent 2.4 GHz Wi-Fi AP + USB transmission).", (88, 166, 255)),
    ]
    y_off = 280
    for title, sub, desc, col in ports:
        draw.text((105, y_off), f"• {title} ", font=f_bold, fill=(240, 246, 252))
        draw.text((360, y_off), sub, font=f_bold, fill=col)
        draw.text((125, y_off + 24), desc, font=f_item, fill=(139, 148, 158))
        y_off += 55

    # Hardware Specs Card
    draw_rounded_rect(draw, (80, 540, 900, 770), radius=10, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((105, 560), "HARDWARE CHARACTERISTICS", font=f_tag, fill=(88, 166, 255))
    specs = [
        "• Processor: Espressif ESP32-S3-WROOM-1 (32-bit LX7, 240 MHz dual-core)",
        "• Memory Hierarchy: 512 KB Internal SRAM + 8 MB Quad-SPI Flash",
        "• USB Transceiver: Native USB 2.0 Full-Speed (12 Mbps) composite PHY",
        "• Wireless Radio: 2.4 GHz 802.11b/g/n Wi-Fi + BLE 5.0 (Dual SoftAP + STA)",
        "• Operational Range: -40°C to +85°C industrial envelope (~38°C measured)"
    ]
    y_off = 590
    for s in specs:
        draw.text((105, y_off), s, font=f_item, fill=(201, 209, 217))
        y_off += 32

    # Right Column: System Architecture / Hardware preview
    place_image_card(img, "reports/assets/system_architecture.png", (940, 150, 1850, 770), "Figure 2: Hardware Interconnect & USB PHY Topology")

    return img

def render_scene_3(time_range):
    img, draw = render_base_template(3, 9, "Deterministic Finite State Machine & Payloads", time_range)
    
    f_h1 = get_font(FONT_PATH_BOLD, 36)
    f_sub = get_font(FONT_PATH_REG, 20)
    f_item = get_font(FONT_PATH_REG, 17)
    f_bold = get_font(FONT_PATH_BOLD, 17)
    f_tag = get_font(FONT_PATH_BOLD, 14)

    draw.text((80, 130), "Deterministic Scenario FSM & Educational Payloads", font=f_h1, fill=(240, 246, 252))
    draw.text((80, 175), "8-State Finite State Machine  •  Interruptible Execution  •  Physical Sync", font=f_sub, fill=(139, 148, 158))

    # FSM State Sequence Card
    draw_rounded_rect(draw, (80, 225, 900, 480), radius=10, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((105, 245), "FINITE STATE MACHINE (FSM) ARCHITECTURE", font=f_tag, fill=(88, 166, 255))
    states = [
        ("BOOTING & USB_WAIT", "3.5s bounded wait for host OS enumeration to stabilize."),
        ("STARTUP_PAYLOAD", "Automatically triggers Scenario 1 out-of-the-box once."),
        ("STATE_IDLE", "Awaits physical GPIO 0 button press or authenticated REST API call."),
        ("STATE_RUNNING", "Injects active scenario. Rejects overlapping transmissions."),
        ("STATE_STOPPING", "Emergency abort halts loop in <10ms and calls releaseAll().")
    ]
    y_off = 280
    for st, desc in states:
        draw.text((105, y_off), f"• {st}:", font=f_bold, fill=(63, 185, 80))
        draw.text((125, y_off + 22), desc, font=f_item, fill=(139, 148, 158))
        y_off += 45

    # 4 Scenarios Catalogue Card
    draw_rounded_rect(draw, (80, 500, 900, 770), radius=10, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((105, 520), "FOUR EDUCATIONAL DEMONSTRATION PAYLOADS", font=f_tag, fill=(210, 153, 34))
    scens = [
        ("Scenario 1: Notepad Awareness", "Win+R -> notepad -> types security awareness advisory."),
        ("Scenario 2: Portal Redirection", "Win+R -> cmd -> launches institutional portal in browser."),
        ("Scenario 3: Ransomware Simulation", "Win+R -> powershell -> renders non-destructive GUI alert."),
        ("Scenario 4: Wi-Fi Reconnaissance", "Win+R -> cmd -> netsh wlan show profiles (read-only discovery).")
    ]
    y_off = 550
    for sc, desc in scens:
        draw.text((105, y_off), f"• {sc}", font=f_bold, fill=(240, 246, 252))
        draw.text((125, y_off + 22), desc, font=f_item, fill=(139, 148, 158))
        y_off += 50

    # Right Column: FSM State Machine Diagram
    place_image_card(img, "reports/assets/fsm_diagram.png", (940, 150, 1850, 770), "Figure 3: Deterministic 8-State Scenario Lifecycle FSM")

    return img

def render_scene_4(time_range):
    img, draw = render_base_template(4, 9, "Mobile Web Controller & Remote Peripheral Suite", time_range)
    
    f_h1 = get_font(FONT_PATH_BOLD, 36)
    f_sub = get_font(FONT_PATH_REG, 20)
    f_item = get_font(FONT_PATH_REG, 17)
    f_bold = get_font(FONT_PATH_BOLD, 17)
    f_tag = get_font(FONT_PATH_BOLD, 14)

    draw.text((80, 130), "Mobile Web Controller & Driverless Peripheral Suite", font=f_h1, fill=(240, 246, 252))
    draw.text((80, 175), "PROGMEM Flash SPA  •  RESTful API  •  Zero Host Software Required", font=f_sub, fill=(139, 148, 158))

    # Left Column: Features Card
    draw_rounded_rect(draw, (80, 225, 900, 770), radius=10, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((105, 245), "EMBEDDED CONTROLLER CAPABILITIES", font=f_tag, fill=(88, 166, 255))

    features = [
        ("Zero-Dependency Flash SPA", "Served directly from PROGMEM flash over 2.4 GHz SoftAP/STA (10.85.248.29)."),
        ("Tokenized PIN Security", "Protects all REST endpoints (/api/scenario, /api/keyboard) via X-Auth-Token."),
        ("Full 6-Row QWERTY Keyboard", "Dedicated function keys, navigation cluster, numeric keypad, and live typing."),
        ("Persistent Modifier Latches", "Hardware-accurate latched Ctrl, Alt, Shift, GUI with emergency releaseAll()."),
        ("One-Touch System Shortcuts", "Pre-programmed macros: Win+R, Ctrl+C, Ctrl+V, Alt+Tab, Alt+F4."),
        ("60 Hz Multi-Touch Trackpad Mouse", "Clamped 8-bit cursor deltas, tap-to-click, two-finger scroll, and drag lock.")
    ]
    y_off = 280
    for title, desc in features:
        draw.text((105, y_off), f"• {title}:", font=f_bold, fill=(63, 185, 80))
        draw.text((125, y_off + 24), desc, font=f_item, fill=(139, 148, 158))
        y_off += 75

    # Right Column: Phone UI Composite Capture
    place_image_card(img, "reports/assets/phone_ui_scenarios_keyboard.png", (940, 150, 1850, 770), "Figure 4: Real Phone Controller Interface (Scenarios & Keyboard)")

    return img

def render_scene_5(time_range):
    img, draw = render_base_template(5, 9, "Adversarial Resilience & Cadence Emulation", time_range)
    
    f_h1 = get_font(FONT_PATH_BOLD, 36)
    f_sub = get_font(FONT_PATH_REG, 20)
    f_item = get_font(FONT_PATH_REG, 17)
    f_bold = get_font(FONT_PATH_BOLD, 17)
    f_tag = get_font(FONT_PATH_BOLD, 14)
    f_mono = get_font(FONT_PATH_MONO, 15)

    draw.text((80, 130), "Adversarial Resilience & Human Cadence Emulation", font=f_h1, fill=(240, 246, 252))
    draw.text((80, 175), "Stochastic Timing Jitter  •  Cognitive Delimiter Pauses  •  Defensive Stress-Testing", font=f_sub, fill=(139, 148, 158))

    # Why Evasion Matters Card
    draw_rounded_rect(draw, (80, 225, 900, 470), radius=10, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((105, 245), "LIMITATION OF NAIVE DEFENSIVE THRESHOLDS", font=f_tag, fill=(248, 81, 73))
    points = [
        "• Naive Speed Limiters: Block typing faster than 50 chars/sec (t < 20 ms).",
        "• Adaptive Attackers: Easily bypass static thresholds by adding fixed sleep delays.",
        "• WHID-Guard Goal: Test host defense against human cadence emulation.",
        "• Microcontroller Implementation: Stochastic jitter engine inside keyboard_controller.cpp."
    ]
    y_off = 280
    for p in points:
        draw.text((105, y_off), p, font=f_item, fill=(201, 209, 217))
        y_off += 42

    # Mathematical Jitter Formulation Card
    draw_rounded_rect(draw, (80, 490, 900, 770), radius=10, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((105, 510), "FIRMWARE CADENCE EMULATION ALGORITHM", font=f_tag, fill=(88, 166, 255))
    draw.text((105, 545), "Randomized Inter-Key Interval Formulation:", font=f_bold, fill=(240, 246, 252))
    draw.text((105, 575), "   Δt = baseDelayMs + random(0, jitterRangeMs)", font=f_mono, fill=(63, 185, 80))
    draw.text((105, 615), "Cognitive Delimiter Micro-Pauses:", font=f_bold, fill=(240, 246, 252))
    draw.text((105, 645), "   if char in [' ', '.', ',', '!', '\\n']:", font=f_mono, fill=(210, 153, 34))
    draw.text((105, 675), "       delayMs += random(150, 300)  // Mimics human brain planning", font=f_mono, fill=(139, 148, 158))
    draw.text((105, 715), "• REST Control: POST /api/settings/stealth {'enabled': true}", font=f_item, fill=(88, 166, 255))

    # Right Column: Phone UI Mouse & Settings / Evasion toggle
    place_image_card(img, "reports/assets/phone_ui_mouse_settings.png", (940, 150, 1850, 770), "Figure 5: Mobile Web UI (Virtual Mouse & Adversarial Stealth Mode)")

    return img

def render_scene_6(time_range):
    img, draw = render_base_template(6, 9, "WHID-Guard Behavioral Keystroke Dynamics Engine", time_range)
    
    f_h1 = get_font(FONT_PATH_BOLD, 36)
    f_sub = get_font(FONT_PATH_REG, 20)
    f_item = get_font(FONT_PATH_REG, 17)
    f_bold = get_font(FONT_PATH_BOLD, 17)
    f_tag = get_font(FONT_PATH_BOLD, 14)
    f_mono = get_font(FONT_PATH_MONO, 15)

    draw.text((80, 130), "WHID-Guard: Real-Time Keystroke Dynamics", font=f_h1, fill=(240, 246, 252))
    draw.text((80, 175), "Online Sliding Window (W = 10)  •  Inter-Key Interval (IKI) Statistics", font=f_sub, fill=(139, 148, 158))

    # Mathematical Formulation Card
    draw_rounded_rect(draw, (80, 225, 900, 480), radius=10, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((105, 245), "STATISTICAL FORMULATION OVER SLIDING WINDOW (W = 10)", font=f_tag, fill=(88, 166, 255))

    formulas = [
        ("Mean Inter-Key Interval:", "μ_IKI = (1 / (W-1)) * Σ Δt_i"),
        ("Standard Deviation:", "σ_IKI = sqrt((1 / (W-2)) * Σ (Δt_i - μ)^2)"),
        ("Coefficient of Variation:", "CV = σ_IKI / μ_IKI  (Dimensionless Metric)"),
        ("Typing Burst Rate:", "Burst = 1.0 / μ_IKI  (Characters per second)")
    ]
    y_off = 280
    for lbl, form in formulas:
        draw.text((105, y_off), lbl, font=f_bold, fill=(240, 246, 252))
        draw.text((360, y_off), form, font=f_mono, fill=(63, 185, 80))
        y_off += 45

    # Decision Boundaries Card
    draw_rounded_rect(draw, (80, 500, 900, 770), radius=10, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((105, 520), "REAL-TIME MULTI-STATE CLASSIFICATION RULES", font=f_tag, fill=(210, 153, 34))
    
    rules = [
        ("LOCKED_DOWN (BadUSB)", "μ_IKI < 25 ms  OR  CV < 0.15 (for 8 consecutive events)", (248, 81, 73)),
        ("SAFE (Human Operator)", "μ_IKI > 75 ms  AND  CV > 0.30 (natural variance)", (63, 185, 80)),
        ("SUSPICIOUS (Evasion)", "Intermediate zone: Artificial jitter lacking digram variance", (210, 153, 34)),
    ]
    y_off = 555
    for title, rule, col in rules:
        draw.text((105, y_off), f"• {title}:", font=f_bold, fill=col)
        draw.text((125, y_off + 24), rule, font=f_item, fill=(139, 148, 158))
        y_off += 60

    # Right Column: IKI Distribution Histogram
    place_image_card(img, "reports/assets/fig_iki_distribution.png", (940, 150, 1850, 770), "Figure 6: Empirical Inter-Key Interval (IKI) Distribution Histogram")

    return img

def render_scene_7(time_range):
    img, draw = render_base_template(7, 9, "Per-Device Hardware Attribution & Selective Isolation", time_range)
    
    f_h1 = get_font(FONT_PATH_BOLD, 36)
    f_sub = get_font(FONT_PATH_REG, 20)
    f_item = get_font(FONT_PATH_REG, 17)
    f_bold = get_font(FONT_PATH_BOLD, 17)
    f_tag = get_font(FONT_PATH_BOLD, 14)
    f_mono = get_font(FONT_PATH_MONO, 15)

    draw.text((80, 130), "Hardware Attribution via Windows Raw Input", font=f_h1, fill=(240, 246, 252))
    draw.text((80, 175), "Per-Device Isolation  •  Selective WH_KEYBOARD_LL Filter  •  Zero Legitimate Lockout", font=f_sub, fill=(139, 148, 158))

    # Pipeline Card
    draw_rounded_rect(draw, (80, 225, 900, 520), radius=10, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((105, 245), "SELECTIVE DEFENSE PIPELINE MECHANISM", font=f_tag, fill=(88, 166, 255))

    steps = [
        ("1. Raw Input Sink", "RIDEV_INPUTSINK intercepts all WM_INPUT messages in background."),
        ("2. Device Identification", "GetRawInputDeviceInfoW extracts hDevice, Vendor ID & Product ID."),
        ("3. Device Classification", "Identifies ESP32-S3 (VID:0x303A, PID:0x1001) vs Built-in ATK3001."),
        ("4. Selective Hook Filter", "Low-level WH_KEYBOARD_LL drops only quarantined hDevice events.")
    ]
    y_off = 280
    for st, desc in steps:
        draw.text((105, y_off), f"• {st}:", font=f_bold, fill=(63, 185, 80))
        draw.text((125, y_off + 24), desc, font=f_item, fill=(139, 148, 158))
        y_off += 55

    # Telemetry & Safety Watchdog Card
    draw_rounded_rect(draw, (80, 540, 900, 770), radius=10, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((105, 560), "OPERATIONAL SAFETY & FAILSAFES", font=f_tag, fill=(210, 153, 34))
    
    safeties = [
        ("15-Second Watchdog Timer", "Automatically disarms suppression if an unexpected lock occurs."),
        ("Process Exit Safeguards", "atexit and WM_DELETE_WINDOW unhook drivers immediately upon exit."),
        ("Zero Productivity Disruption", "User's internal laptop keyboard remains 100% responsive during attacks.")
    ]
    y_off = 590
    for title, desc in safeties:
        draw.text((105, y_off), f"• {title}:", font=f_bold, fill=(240, 246, 252))
        draw.text((125, y_off + 22), desc, font=f_item, fill=(139, 148, 158))
        y_off += 55

    # Right Column: Defense Architecture Figure
    place_image_card(img, "reports/assets/defense_architecture.png", (940, 150, 1850, 770), "Figure 7: Selective Hardware Attribution & Isolation Architecture")

    return img

def render_scene_8(time_range):
    img, draw = render_base_template(8, 9, "Quantitative Empirical Evaluation & Benchmark Results", time_range)
    
    f_h1 = get_font(FONT_PATH_BOLD, 36)
    f_sub = get_font(FONT_PATH_REG, 20)
    f_item = get_font(FONT_PATH_REG, 16)
    f_bold = get_font(FONT_PATH_BOLD, 16)
    f_tag = get_font(FONT_PATH_BOLD, 14)

    draw.text((80, 130), "Empirical Benchmark Results & Quantitative Evaluation", font=f_h1, fill=(240, 246, 252))
    draw.text((80, 175), "1,500-Keystroke Corpus  •  0.0% False Positive Rate  •  Sub-85ms Quarantine", font=f_sub, fill=(139, 148, 158))

    # Benchmark Table Card
    draw_rounded_rect(draw, (80, 225, 900, 520), radius=10, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((105, 245), "QUANTITATIVE EMPIRICAL BENCHMARK (1,500 EVENTS)", font=f_tag, fill=(88, 166, 255))

    rows = [
        ("Metric", "Human Baseline", "Standard BadUSB", "Stealth Evasion"),
        ("Mean IKI (μ)", "144.18 ms", "10.01 ms", "119.28 ms"),
        ("Std Dev (σ)", "91.98 ms", "0.78 ms", "48.88 ms"),
        ("Coeff Var (CV)", "0.638 (High)", "0.078 (Zero)", "0.409 (Jitter)"),
        ("Typing Rate", "6.94 ch/s", "99.95 ch/s", "8.38 ch/s"),
        ("Quarantine Latency", "Authorized", "8 chars (<85 ms)", "Flagged Alert"),
        ("False Positive Rate", "0.0%", "N/A", "N/A"),
        ("Detection Rate (TPR)", "N/A", "98.6% Confirmed", "25.2% Flagged"),
    ]
    y_off = 280
    for idx, r in enumerate(rows):
        col_hdr = (88, 166, 255) if idx == 0 else (240, 246, 252)
        f_use = f_bold if idx == 0 else f_item
        draw.text((105, y_off), r[0], font=f_use, fill=col_hdr)
        draw.text((330, y_off), r[1], font=f_use, fill=(63, 185, 80) if idx > 0 else col_hdr)
        draw.text((530, y_off), r[2], font=f_use, fill=(248, 81, 73) if idx > 0 else col_hdr)
        draw.text((720, y_off), r[3], font=f_use, fill=(210, 153, 34) if idx > 0 else col_hdr)
        y_off += 28

    # Key Empirical Insights Card
    draw_rounded_rect(draw, (80, 540, 900, 770), radius=10, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((105, 560), "EMPIRICAL FINDINGS", font=f_tag, fill=(63, 185, 80))
    insights = [
        "• 0.0% False Positive Rate: Zero legitimate human keystrokes were dropped.",
        "• Immediate Attack Neutralization: Malicious BadUSB payloads blocked within 8 chars (<85ms), aborting commands before execution.",
        "• Stealth Resilience: Adversarial jitter flagged in 25.2% of events for inspection.",
        "• 100% Test Pass Rate: 16 passing unit, regression, and simulation tests."
    ]
    y_off = 590
    for ins in insights:
        draw.text((105, y_off), ins, font=f_item, fill=(201, 209, 217))
        y_off += 40

    # Right Column: Detection Latency Curve
    place_image_card(img, "reports/assets/fig_detection_latency.png", (940, 150, 1850, 770), "Figure 8: Quarantine Latency Curve (Neutralization < 85 ms)")

    return img

def render_scene_9(time_range):
    img, draw = render_base_template(9, 9, "Conclusion, IEEE Publication & Open-Source Release", time_range)
    
    f_h1 = get_font(FONT_PATH_BOLD, 36)
    f_sub = get_font(FONT_PATH_REG, 20)
    f_item = get_font(FONT_PATH_REG, 18)
    f_bold = get_font(FONT_PATH_BOLD, 18)
    f_tag = get_font(FONT_PATH_BOLD, 14)
    f_mono = get_font(FONT_PATH_MONO, 16)

    draw.text((80, 130), "Conclusion, Research Impact & Open-Source Release", font=f_h1, fill=(240, 246, 252))
    draw.text((80, 175), "Publication-Ready IEEE Manuscript  •  Reproducible Open-Source GitHub Repository", font=f_sub, fill=(139, 148, 158))

    # Core Deliverables Card
    draw_rounded_rect(draw, (80, 225, 900, 520), radius=10, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((105, 245), "RESEARCH DELIVERABLES SUMMARY", font=f_tag, fill=(88, 166, 255))

    delivs = [
        ("Dual-Mode Hardware Platform", "ESP32-S3 composite keyboard/mouse with web remote."),
        ("Host Keystroke Dynamics Engine", "Real-time sliding-window IKI classifier (CV & burst rate)."),
        ("Per-Device Selective Isolation", "Windows Raw Input attribution protecting legitimate peripherals."),
        ("IEEE Conference Manuscript", "Complete 6-page paper with LaTeX sources & submission bundle."),
        ("Open-Source GitHub Release", "Comprehensive documentation, CI workflow, and test suite.")
    ]
    y_off = 280
    for d, desc in delivs:
        draw.text((105, y_off), f"• {d}:", font=f_bold, fill=(63, 185, 80))
        draw.text((125, y_off + 24), desc, font=f_item, fill=(139, 148, 158))
        y_off += 55

    # Academic Attribution & Links Card
    draw_rounded_rect(draw, (80, 540, 900, 770), radius=10, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((105, 560), "ACADEMIC & REPOSITORY LINKS", font=f_tag, fill=(210, 153, 34))

    draw.text((105, 595), "GitHub Repository:", font=f_bold, fill=(240, 246, 252))
    draw.text((105, 625), "   https://github.com/ramKarthik57/BadUSB_Simulation.git", font=f_mono, fill=(88, 166, 255))
    draw.text((105, 665), "Authors & Affiliation:", font=f_bold, fill=(240, 246, 252))
    draw.text((105, 695), "   Ram Karthik G (CH.SC.U4CYS23037) & Harini V (CH.SC.U4CYS23010)", font=f_item, fill=(201, 209, 217))
    draw.text((105, 725), "   Department of Cybersecurity, Amrita Vishwa Vidyapeetham, Chennai", font=f_item, fill=(139, 148, 158))

    # Right Column: IEEE Paper Preview Card
    place_image_card(img, "WHID_GUARD_FINAL_SUBMISSION/WHID_GUARD_PREVIEW.png", (940, 150, 1850, 770), "Figure 9: Published IEEE Conference Manuscript Preview")

    return img

def render_all_slides():
    os.makedirs("demo_video/slides", exist_ok=True)
    with open("demo_video/scenes_meta.json", "r", encoding="utf-8") as f:
        meta = json.load(f)
    
    scenes_map = {
        1: render_scene_1,
        2: render_scene_2,
        3: render_scene_3,
        4: render_scene_4,
        5: render_scene_5,
        6: render_scene_6,
        7: render_scene_7,
        8: render_scene_8,
        9: render_scene_9
    }

    for sc in meta["scenes"]:
        sc_id = sc["id"]
        t_start = sc["start_time"]
        t_end = sc["end_time"]
        def fmt_m_s(secs):
            m = int(secs // 60)
            s = int(secs % 60)
            return f"{m:02d}:{s:02d}"
        time_str = f"{fmt_m_s(t_start)} - {fmt_m_s(t_end)}"
        
        render_fn = scenes_map[sc_id]
        img = render_fn(time_str)
        out_path = f"demo_video/slides/slide_{sc_id:02d}.png"
        img.save(out_path, quality=95)
        print(f"[INFO] Rendered Slide {sc_id:02d} -> {out_path} ({time_str})")

if __name__ == "__main__":
    render_all_slides()
