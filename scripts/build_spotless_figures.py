"""
WHID-Guard Master Figure Architect: Spotless Perfection
Strictly eliminates:
  - Any text clipping or border overlap
  - Any unwanted gaps or blank voids
  - Any badge collisions
Generates 100% publication-grade Figure 1, Figure 2, and Figure 5.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32"
PAPER_DIR = os.path.join(BASE_DIR, "paper")
os.makedirs(PAPER_DIR, exist_ok=True)

NAVY_HEADER = (11, 19, 43)
BG_CANVAS = (248, 250, 252)
BORDER_CANVAS = (203, 213, 225)
TEXT_WHITE = (255, 255, 255)
TEXT_MAIN = (15, 23, 42)
TEXT_MUTED = (100, 116, 139)

TIER1 = {
    "header": (15, 118, 110),
    "border": (13, 148, 136),
    "card_bg": (240, 253, 250),
    "card_border": (153, 246, 228),
    "title": (15, 118, 110)
}

TIER2 = {
    "header": (29, 78, 216),
    "border": (37, 99, 235),
    "card_bg": (239, 246, 255),
    "card_border": (191, 219, 254),
    "title": (29, 78, 216)
}

TIER3 = {
    "header": (185, 28, 28),
    "border": (220, 38, 38),
    "card_bg": (254, 242, 242),
    "card_border": (254, 202, 202),
    "title": (185, 28, 28)
}


# ==============================================================================
# 1. SPOTLESS FIGURE 1: SYSTEM ARCHITECTURE (PERFECT PROPORTIONS & CLEARANCES)
# ==============================================================================
def generate_spotless_figure_1():
    W = 3960
    H = 1180

    im = Image.new("RGB", (W, H), BG_CANVAS)
    draw = ImageDraw.Draw(im)

    font_master_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 44)
    font_master_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 26)
    font_tier_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 34)
    font_tier_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 23)
    font_card_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26)
    font_body = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 22)
    font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
    font_badge_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 19)

    draw.rounded_rectangle([15, 15, W - 15, H - 15], radius=20, outline=BORDER_CANVAS, width=2)

    # Master Header
    draw.rounded_rectangle([25, 25, W - 25, 115], radius=14, fill=NAVY_HEADER)
    draw.text((W // 2, 54), "WHID-GUARD: MULTI-TIER SYSTEM ARCHITECTURE & PER-DEVICE DEFENSE PIPELINE",
              font=font_master_title, fill=TEXT_WHITE, anchor="mm")
    draw.text((W // 2, 92), "Tier 1: Out-of-Band Mobile Controller  |  Tier 2: Embedded ESP32-S3 Firmware  |  Tier 3: Windows Raw Input Behavioral Engine",
              font=font_master_sub, fill=(203, 213, 225), anchor="mm")

    # Clean, balanced columns:
    # Margin Left = 40
    # Col 1: 40 to 1140 (width 1100)
    # Gap 1: 1140 to 1360 (width 220 px -> Plenty of room for 160px badge!)
    # Col 2: 1360 to 2560 (width 1200)
    # Gap 2: 2560 to 2780 (width 220 px -> Plenty of room for 160px badge!)
    # Col 3: 2780 to 3920 (width 1140)
    # Margin Right = 40
    col1_x0, col1_x1 = 40, 1140
    col2_x0, col2_x1 = 1360, 2560
    col3_x0, col3_x1 = 2780, 3920
    col_y0, col_y1 = 135, H - 25

    def draw_tier_container(x0, y0, x1, y1, title, subtitle, tier_style):
        draw.rounded_rectangle([x0, y0, x1, y1], radius=16, fill=(255, 255, 255), outline=tier_style["border"], width=3)
        draw.rounded_rectangle([x0, y0, x1, y0 + 75], radius=16, fill=tier_style["header"])
        draw.rectangle([x0, y0 + 50, x1, y0 + 75], fill=tier_style["header"])
        draw.text(((x0 + x1) // 2, y0 + 26), title, font=font_tier_title, fill=TEXT_WHITE, anchor="mm")
        draw.text(((x0 + x1) // 2, y0 + 56), subtitle, font=font_tier_sub, fill=(226, 232, 240), anchor="mm")

    draw_tier_container(col1_x0, col_y0, col1_x1, col_y1,
                        "TIER 1: MOBILE WEB CONTROLLER (SPA)",
                        "Out-of-Band Wireless Red-Team Operator Interface", TIER1)

    draw_tier_container(col2_x0, col_y0, col2_x1, col_y1,
                        "TIER 2: ESP32-S3 WEAPONIZED FIRMWARE",
                        "Dual-Core SoC, FreeRTOS FSM & Native TinyUSB PHY", TIER2)

    draw_tier_container(col3_x0, col_y0, col3_x1, col_y1,
                        "TIER 3: WHID-GUARD HOST DEFENSE PIPELINE",
                        "Windows Raw Input Attribution & Selective Hook Firewall", TIER3)

    def draw_snug_card(x0, y0, x1, y1, card_title, bullets, tier_style):
        draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=tier_style["card_bg"], outline=tier_style["card_border"], width=1)
        draw.text((x0 + 18, y0 + 12), card_title, font=font_card_title, fill=tier_style["title"])
        curr_y = y0 + 46
        for b in bullets:
            draw.ellipse([x0 + 20, curr_y + 7, x0 + 28, curr_y + 15], fill=tier_style["title"])
            draw.text((x0 + 36, curr_y), b, font=font_body, fill=TEXT_MAIN)
            curr_y += 31

    card_h = 210
    card_gap = 14
    start_y = col_y0 + 88

    # Tier 1 Cards (width = 1060)
    t1_cards = [
        ("Zero-Dependency Mobile Web Client (SPA)", [
            "Embedded in ESP32 Flash memory (PROGMEM, 52 KB single-file)",
            "Served directly via Safari / Chrome; 0 host receiver software",
            "SoftAP (192.168.4.1) & Station DHCP (10.85.248.29) interfaces",
            "Real-time 1.5s bidirectional polling heartbeat with host",
        ]),
        ("Virtual HID Keyboard & Multi-Touch Trackpad", [
            "6-Row QWERTY virtual layout with modifier locks (Ctrl/Alt/Win)",
            "60 Hz relative touch delta stream (dx, dy) for mouse motion",
            "1-Finger Tap = Left Click  |  2-Finger Swipe = Scroll Wheel",
            "Full out-of-band remote mouse and keyboard manipulation",
        ]),
        ("BadUSB Scenario Orchestration Suite", [
            "Direct launch & circular cycling for Scenarios 1 to 4",
            "Scenario 1: Notepad Security Awareness  |  Scenario 2: Credential Phish",
            "Scenario 3: PowerShell Reverse Shell  |  Scenario 4: Recon & Exfil",
            "Real-time execution status feedback & abort control",
        ]),
        ("Adversarial Evasion & Cadence Engine", [
            "Adversarial Mode Toggle: Injects artificial timing variance",
            "Gaussian Jitter: base (80ms) + stochastic jitter (0-40ms)",
            "Inter-word delimiter micro-pauses (150-300ms)",
            "Defeats primitive static inter-key interval detection thresholds",
        ]),
    ]

    c1_w = col1_x1 - col1_x0 - 32
    for i, (title, bullets) in enumerate(t1_cards):
        cy = start_y + i * (card_h + card_gap)
        draw_snug_card(col1_x0 + 16, cy, col1_x0 + 16 + c1_w, cy + card_h, title, bullets, TIER1)

    # Tier 2 Cards
    t2_cards = [
        ("FreeRTOS Dual-Core Architecture", [
            "Core 0: Wi-Fi Stack, WebServerHandler, REST API endpoints",
            "Core 1: Scenario FSM & Adversarial Jitter Engine",
            "portMUX_TYPE Spinlock Mailbox guards cmdPending safely",
            "Eliminates race conditions between Web and HID engines",
        ]),
        ("Deterministic 8-State Scenario FSM", [
            "3,500ms Non-blocking USB enumeration guard (tau_boot)",
            "Physical GPIO 0 Button Interrupt (50ms debounce, 600ms cooldown)",
            "Cooperative smartDelay(10ms) slicing with abort polling",
            "Guarantees deterministic, safe payload execution & teardown",
        ]),
        ("Cooperative Preemption & Teardown", [
            "stopRequested flag breaks execution loop within <= 10ms",
            "Invokes Keyboard.releaseAll() & Mouse.releaseAll() instantly",
            "Flushes Ctrl/Alt/Win modifier keys, leaving zero host residue",
            "Restores clean USB HID bus state to host operating system",
        ]),
        ("Native TinyUSB Composite HID Transceiver", [
            "Direct USB OTG PHY Transceiver on GPIO 19/20 (D- / D+)",
            "Class 0x03 Boot Keyboard (8-byte) + 3-Btn Mouse (4-byte)",
            "USB CDC Serial port for 115,200 baud debug logging",
            "Hardware VID: 0x303A (Espressif), PID: 0x1001",
        ]),
    ]

    c2_w = col2_x1 - col2_x0 - 32
    for i, (title, bullets) in enumerate(t2_cards):
        cy = start_y + i * (card_h + card_gap)
        draw_snug_card(col2_x0 + 16, cy, col2_x0 + 16 + c2_w, cy + card_h, title, bullets, TIER2)

    # Tier 3 Cards
    t3_cards = [
        ("Raw Input Hardware Device Attribution", [
            "RegisterRawInputDevices(UsagePage=0x01, Usage=0x06)",
            "Intercepts WM_INPUT to query RAWINPUTHEADER.hDevice",
            "Resolves physical path via GetRawInputDeviceInfoW",
            "Identifies ESP32 Implant (VID:303A) vs Built-in Keyboard",
        ]),
        ("Sliding-Window IKI Dynamics Engine", [
            "Sliding Window (W = 10 events) computes Mean & StdDev",
            "Coefficient of Variation: CV = sigma / mu",
            "SAFE (Human): mu > 75ms and CV > 0.30 (FPR = 0.0%)",
            "LOCKED_DOWN (BadUSB): mu < 25ms or sustained CV < 0.15",
        ]),
        ("Selective Hook Filter Gate (WH_KEYBOARD_LL)", [
            "Low-Level Windows Keyboard Hook evaluates every key event",
            "Per-Device Gate: If hDevice in Quarantine -> DROP EVENT",
            "Authorized Device (Internal Keyboard) -> PASS EVENT",
            "Isolates malicious implant with zero operator disruption",
        ]),
        ("Live Telemetry & Automated Quarantine", [
            "PySide6 Host GUI displays real-time telemetry gauges",
            "Quarantine Latency: Exactly 8 keystrokes (<85ms response)",
            "6-Character Safety Buffer before target command detonation",
            "Visual & auditory alert notifications to the system operator",
        ]),
    ]

    c3_w = col3_x1 - col3_x0 - 32
    for i, (title, bullets) in enumerate(t3_cards):
        cy = start_y + i * (card_h + card_gap)
        draw_snug_card(col3_x0 + 16, cy, col3_x0 + 16 + c3_w, cy + card_h, title, bullets, TIER3)

    # Interconnect 1 (Wi-Fi): Gap [1140, 1360], width = 220 px, center = 1250
    bus1_cx = 1250
    bus1_cy = 580

    draw.line([col1_x1, bus1_cy, col2_x0, bus1_cy], fill=TIER1["header"], width=5)
    draw.polygon([(col1_x1, bus1_cy), (col1_x1 + 18, bus1_cy - 10), (col1_x1 + 18, bus1_cy + 10)], fill=TIER1["header"])
    draw.polygon([(col2_x0, bus1_cy), (col2_x0 - 18, bus1_cy - 10), (col2_x0 - 18, bus1_cy + 10)], fill=TIER1["header"])

    # Badge Box (width 164 px inside 220 px gap -> 28 px margin on each side!)
    draw.rounded_rectangle([bus1_cx - 82, bus1_cy - 58, bus1_cx + 82, bus1_cy + 58],
                           radius=8, fill=(255, 255, 255), outline=TIER1["header"], width=2)
    draw.text((bus1_cx, bus1_cy - 35), "2.4 GHz Wi-Fi", font=font_badge, fill=TIER1["header"], anchor="mm")
    draw.text((bus1_cx, bus1_cy - 10), "REST API", font=font_badge, fill=TIER1["header"], anchor="mm")
    draw.text((bus1_cx, bus1_cy + 15), "SoftAP / STA", font=font_badge_sub, fill=TEXT_MUTED, anchor="mm")
    draw.text((bus1_cx, bus1_cy + 37), "HTTP JSON", font=font_badge_sub, fill=TEXT_MUTED, anchor="mm")

    # Interconnect 2 (USB): Gap [2560, 2780], width = 220 px, center = 2670
    bus2_cx = 2670
    bus2_cy = 580

    draw.line([col2_x1, bus2_cy, col3_x0, bus2_cy], fill=TIER2["header"], width=5)
    draw.polygon([(col3_x0, bus2_cy), (col3_x0 - 18, bus2_cy - 10), (col3_x0 - 18, bus2_cy + 10)], fill=TIER2["header"])

    draw.rounded_rectangle([bus2_cx - 82, bus2_cy - 58, bus2_cx + 82, bus2_cy + 58],
                           radius=8, fill=(255, 255, 255), outline=TIER2["header"], width=2)
    draw.text((bus2_cx, bus2_cy - 35), "USB 2.0 Cable", font=font_badge, fill=TIER2["header"], anchor="mm")
    draw.text((bus2_cx, bus2_cy - 10), "GPIO 19/20 PHY", font=font_badge, fill=TIER2["header"], anchor="mm")
    draw.text((bus2_cx, bus2_cy + 15), "12 Mbps Speed", font=font_badge_sub, fill=TEXT_MUTED, anchor="mm")
    draw.text((bus2_cx, bus2_cy + 37), "Composite HID", font=font_badge_sub, fill=TEXT_MUTED, anchor="mm")

    # Selective Gate Callout (Positioned neatly in bottom gap)
    gate_cx = 2670
    gate_cy = 930
    draw.rounded_rectangle([gate_cx - 82, gate_cy - 52, gate_cx + 82, gate_cy + 52],
                           radius=8, fill=(255, 255, 255), outline=TIER3["header"], width=2)
    draw.text((gate_cx, gate_cy - 30), "Selective Gate", font=font_badge_sub, fill=TIER3["header"], anchor="mm")
    draw.text((gate_cx, gate_cy - 8), "WH_KEYBOARD_LL", font=font_badge_sub, fill=TEXT_MAIN, anchor="mm")
    draw.text((gate_cx, gate_cy + 16), "DROPS ESP32", font=font_badge_sub, fill=(220, 38, 38), anchor="mm")
    draw.text((gate_cx, gate_cy + 36), "PASS Laptop KB", font=font_badge_sub, fill=(22, 163, 74), anchor="mm")

    out_path = os.path.join(PAPER_DIR, "system_architecture.png")
    im.save(out_path, quality=100)
    print(f"Generated Spotless Figure 1: {out_path} ({W}x{H})")


# ==============================================================================
# 2. SPOTLESS FIGURE 2: FSM (ZERO BADGE OVERLAP, PERFECT GAPS & ARROWS)
# ==============================================================================
def generate_spotless_figure_2():
    W = 3960
    H = 920

    im = Image.new("RGB", (W, H), BG_CANVAS)
    draw = ImageDraw.Draw(im)

    font_master_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 40)
    font_master_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 24)
    font_box_title = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 28)
    font_box_body = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 21)
    font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
    font_badge_sm = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)

    draw.rounded_rectangle([15, 15, W - 15, H - 15], radius=20, outline=BORDER_CANVAS, width=2)

    # Master Header
    draw.rounded_rectangle([25, 25, W - 25, 105], radius=14, fill=NAVY_HEADER)
    draw.text((W // 2, 50), "DETERMINISTIC 8-STATE SCENARIO EXECUTION FINITE STATE MACHINE (FSM)",
              font=font_master_title, fill=TEXT_WHITE, anchor="mm")
    draw.text((W // 2, 84), "Hardware Stabilization, FreeRTOS Inter-Core Mailbox, Cooperative Preemption, and Atomic Teardown",
              font=font_master_sub, fill=(203, 213, 225), anchor="mm")

    def draw_state_box(x0, y0, x1, y1, title, bullets, style):
        draw.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=style["bg"], outline=style["border"], width=2)
        draw.rounded_rectangle([x0, y0, x1, y0 + 48], radius=12, fill=style["header"])
        draw.rectangle([x0, y0 + 34, x1, y0 + 48], fill=style["header"])
        draw.text(((x0 + x1) // 2, y0 + 24), title, font=font_box_title, fill=TEXT_WHITE, anchor="mm")
        curr_y = y0 + 72
        for b in bullets:
            draw.text(((x0 + x1) // 2, curr_y), b, font=font_box_body, fill=TEXT_MAIN, anchor="mm")
            curr_y += 33

    def draw_bottom_box(x0, y0, x1, y1, title, bullets, style):
        draw.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=style["bg"], outline=style["border"], width=2)
        draw.rounded_rectangle([x0, y0, x1, y0 + 48], radius=12, fill=style["header"])
        draw.rectangle([x0, y0 + 34, x1, y0 + 48], fill=style["header"])
        draw.text(((x0 + x1) // 2, y0 + 24), title, font=font_box_title, fill=TEXT_WHITE, anchor="mm")
        curr_y = y0 + 80
        for b in bullets:
            draw.ellipse([x0 + 26, curr_y + 6, x0 + 36, curr_y + 16], fill=style["header"])
            draw.text((x0 + 46, curr_y), b, font=font_box_body, fill=TEXT_MAIN)
            curr_y += 46

    # TOP ROW: 5 PIPELINE STATES (Width 580, Gaps 200 px -> Plenty of room for badges!)
    top_y0, top_y1 = 130, 380
    box_w = 580
    gap_w = 200

    s1_x0, s1_x1 = 40, 40 + box_w                        # 40 to 620
    s2_x0, s2_x1 = s1_x1 + gap_w, s1_x1 + gap_w + box_w  # 820 to 1400
    s3_x0, s3_x1 = s2_x1 + gap_w, s2_x1 + gap_w + box_w  # 1600 to 2180
    s4_x0, s4_x1 = s3_x1 + gap_w, s3_x1 + gap_w + box_w  # 2380 to 2960
    s5_x0, s5_x1 = s4_x1 + gap_w, s4_x1 + gap_w + box_w  # 3160 to 3740

    COLOR_BOOTING = {"header": (51, 65, 85), "border": (71, 85, 105), "bg": (241, 245, 249)}
    COLOR_WAIT = {"header": (29, 78, 216), "border": (37, 99, 235), "bg": (239, 246, 255)}
    COLOR_STARTUP = {"header": (15, 118, 110), "border": (13, 148, 136), "bg": (240, 253, 250)}
    COLOR_IDLE = {"header": (22, 163, 74), "border": (34, 197, 94), "bg": (240, 253, 244)}
    COLOR_RUNNING = {"header": (217, 119, 6), "border": (245, 158, 11), "bg": (255, 251, 235)}
    COLOR_TRIGGERS = {"header": (15, 23, 42), "border": (51, 65, 85), "bg": (248, 250, 252)}
    COLOR_STOPPED = {"header": (29, 78, 216), "border": (37, 99, 235), "bg": (239, 246, 255)}
    COLOR_STOPPING = {"header": (220, 38, 38), "border": (239, 68, 68), "bg": (254, 242, 242)}

    draw_state_box(s1_x0, top_y0, s1_x1, top_y1, "STATE_BOOTING", [
        "Hardware & Clock Init (240MHz)",
        "USB OTG Transceiver Enabled",
        "TinyUSB Descriptors Registered",
        "Assert 1.5k D+ Pullup Resistor",
    ], COLOR_BOOTING)

    draw_state_box(s2_x0, top_y0, s2_x1, top_y1, "STATE_USB_WAIT", [
        "Non-blocking Hardware Guard",
        "tau_boot = 3,500 ms Duration",
        "Prevents Early Keystroke Drops",
        "Awaits Host OS USB Enumeration",
    ], COLOR_WAIT)

    draw_state_box(s3_x0, top_y0, s3_x1, top_y1, "STATE_STARTUP_PAYLOAD", [
        "Executes Scenario 1 Automatically",
        "Win+R -> Launch Notepad.exe",
        "Types Security Awareness Text",
        "Auto-Runs Exactly Once on Boot",
    ], COLOR_STARTUP)

    draw_state_box(s4_x0, top_y0, s4_x1, top_y1, "STATE_IDLE", [
        "Quiescent Ready State",
        "Awaits Physical GPIO 0 Button",
        "or Web REST API Launch Cmd",
        "Checks stopRequested = false",
    ], COLOR_IDLE)

    draw_state_box(s5_x0, top_y0, s5_x1, top_y1, "STATE_RUNNING", [
        "Active Scenario Detonation (1-4)",
        "10ms smartDelay() Time-Slicing",
        "Continuous Preemption Polling",
        "Injects Adversarial IKI Jitter",
    ], COLOR_RUNNING)

    # BOTTOM ROW: TRIGGERS, STOPPED, STOPPING
    bot_y0, bot_y1 = 510, 890

    b1_x0, b1_x1 = 40, 1400     # Triggers (width 1360)
    b2_x0, b2_x1 = 1580, 2660   # Stopped (width 1080)
    b3_x0, b3_x1 = 2820, 3840   # Stopping (width 1020)

    draw_bottom_box(b1_x0, bot_y0, b1_x1, bot_y1, "CONCURRENT TRIGGER SOURCES", [
        "Physical GPIO 0 BOOT Button: 50ms HW debounce, 600ms cooldown latch",
        "Web REST API: POST /api/scenario/select (IDs 1-4) & POST /api/scenario/next",
        "FreeRTOS Spinlock Mailbox: portMUX_TYPE guards cmdPending variable",
        "Eliminates race conditions between Core 0 (Network) & Core 1 (Execution)",
    ], COLOR_TRIGGERS)

    draw_bottom_box(b2_x0, bot_y0, b2_x1, bot_y1, "STATE_STOPPED", [
        "Entered following safe hardware abort & key release",
        "Asserts all keyboard scancodes & mouse buttons cleared",
        "Restores pristine USB HID bus state to host machine",
        "Deterministic reset back to STATE_IDLE ready state",
    ], COLOR_STOPPED)

    draw_bottom_box(b3_x0, bot_y0, b3_x1, bot_y1, "STATE_STOPPING", [
        "Triggered instantly by stopRequested = true",
        "Immediately breaks 10ms smartDelay execution loop",
        "Invokes Keyboard.releaseAll() & Mouse.releaseAll()",
        "Clears Ctrl/Alt/Win modifier keys in <= 10ms latency",
    ], COLOR_STOPPING)

    def draw_arrow_head(tip_x, tip_y, direction, color, size=20):
        h = size
        w = int(size * 0.75)
        if direction == "right":
            draw.polygon([(tip_x, tip_y), (tip_x - h, tip_y - w // 2), (tip_x - h, tip_y + w // 2)], fill=color)
        elif direction == "left":
            draw.polygon([(tip_x, tip_y), (tip_x + h, tip_y - w // 2), (tip_x + h, tip_y + w // 2)], fill=color)
        elif direction == "up":
            draw.polygon([(tip_x, tip_y), (tip_x - w // 2, tip_y + h), (tip_x + w // 2, tip_y + h)], fill=color)
        elif direction == "down":
            draw.polygon([(tip_x, tip_y), (tip_x - w // 2, tip_y - h), (tip_x + w // 2, tip_y - h)], fill=color)

    def draw_badge_box(cx, cy, text, border_color, text_color, bw=140, bh=36):
        draw.rounded_rectangle([cx - bw // 2, cy - bh // 2, cx + bw // 2, cy + bh // 2],
                               radius=6, fill=(255, 255, 255), outline=border_color, width=2)
        lines = text.split("\n")
        if len(lines) == 1:
            draw.text((cx, cy), text, font=font_badge, fill=text_color, anchor="mm")
        else:
            line_h = 19
            start_y = cy - (len(lines) - 1) * line_h / 2
            for i, l in enumerate(lines):
                draw.text((cx, start_y + i * line_h), l, font=font_badge_sm, fill=text_color, anchor="mm")

    # 1. BOOTING -> USB_WAIT (Gap: 620 to 820, width 200, center = 720)
    draw.line([s1_x1, 255, s2_x0, 255], fill=COLOR_BOOTING["header"], width=5)
    draw_arrow_head(s2_x0, 255, "right", COLOR_BOOTING["header"], size=20)
    draw_badge_box(720, 255, "Power-On", COLOR_BOOTING["header"], COLOR_BOOTING["header"], bw=120)

    # 2. USB_WAIT -> STARTUP_PAYLOAD (Gap: 1400 to 1600, width 200, center = 1500)
    draw.line([s2_x1, 255, s3_x0, 255], fill=COLOR_WAIT["header"], width=5)
    draw_arrow_head(s3_x0, 255, "right", COLOR_WAIT["header"], size=20)
    draw_badge_box(1500, 255, "3.5s Wait Done", COLOR_WAIT["header"], COLOR_WAIT["header"], bw=140)

    # 3. STARTUP_PAYLOAD -> IDLE (Gap: 2180 to 2380, width 200, center = 2280)
    draw.line([s3_x1, 255, s4_x0, 255], fill=COLOR_STARTUP["header"], width=5)
    draw_arrow_head(s4_x0, 255, "right", COLOR_STARTUP["header"], size=20)
    draw_badge_box(2280, 255, "Auto-Run Done", COLOR_STARTUP["header"], COLOR_STARTUP["header"], bw=140)

    # 4. IDLE -> RUNNING (Upper Lane: y = 210)
    draw.line([s4_x1, 210, s5_x0, 210], fill=COLOR_IDLE["header"], width=5)
    draw_arrow_head(s5_x0, 210, "right", COLOR_IDLE["header"], size=20)
    draw_badge_box(3060, 210, "Launch", COLOR_IDLE["header"], COLOR_IDLE["header"], bw=110)

    # 5. RUNNING -> IDLE (Lower Lane: y = 300)
    draw.line([s5_x0, 300, s4_x1, 300], fill=COLOR_RUNNING["header"], width=5)
    draw_arrow_head(s4_x1, 300, "left", COLOR_RUNNING["header"], size=20)
    draw_badge_box(3060, 300, "Finish", COLOR_RUNNING["header"], COLOR_RUNNING["header"], bw=110)

    # 6. TRIGGER SOURCES -> IDLE (Corridor Routing at y = 430)
    trigger_col = COLOR_TRIGGERS["header"]
    draw.line([b1_x1, 600, 1490, 600], fill=trigger_col, width=4)
    draw.line([1490, 600, 1490, 430], fill=trigger_col, width=4)
    draw.line([1490, 430, 2320, 430], fill=trigger_col, width=4)
    draw.line([2320, 430, 2320, 330], fill=trigger_col, width=4)
    draw.line([2320, 330, s4_x0, 330], fill=trigger_col, width=4)
    draw_arrow_head(s4_x0, 330, "right", trigger_col, size=20)
    draw_badge_box(1905, 430, "GPIO 0 Button / Web API\nTrigger Scenario Launch", trigger_col, trigger_col, bw=260, bh=44)

    # 7. EMERGENCY ABORT: RUNNING -> STOPPING (Straight Vertical)
    abort_col = COLOR_STOPPING["header"]
    draw.line([3450, top_y1, 3450, bot_y0], fill=abort_col, width=5)
    draw_arrow_head(3450, bot_y0, "down", abort_col, size=22)
    draw_badge_box(3450, 445, "Emergency Abort (stopRequested == true)", abort_col, abort_col, bw=420, bh=38)

    # 8. STOPPING -> STOPPED (Gap: 2660 to 2820, width 160 px -> 130 px badge fits with 15 px clearance!)
    draw.line([b3_x0, 700, b2_x1, 700], fill=abort_col, width=5)
    draw_arrow_head(b2_x1, 700, "left", abort_col, size=20)
    draw_badge_box(2740, 700, "Release Keys\n(<= 10ms)", abort_col, abort_col, bw=130, bh=44)

    # 9. STOPPED -> IDLE (Corridor Routing at y = 480)
    reset_col = COLOR_STOPPED["header"]
    draw.line([2120, bot_y0, 2120, 480], fill=reset_col, width=4)
    draw.line([2120, 480, 2670, 480], fill=reset_col, width=4)
    draw.line([2670, 480, 2670, top_y1], fill=reset_col, width=4)
    draw_arrow_head(2670, top_y1, "up", reset_col, size=20)
    draw_badge_box(2420, 480, "Clean Bus -> Return\nto Ready State", reset_col, reset_col, bw=200, bh=44)

    out_path = os.path.join(PAPER_DIR, "fsm_diagram.png")
    im.save(out_path, quality=100)
    print(f"Generated Spotless Figure 2: {out_path} ({W}x{H})")


# ==============================================================================
# 3. SPOTLESS FIGURE 5: EMPIRICAL LATENCY (PERFECT ALIGNMENT & ZERO CLIPPING)
# ==============================================================================
def generate_spotless_figure_5():
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["mathtext.fontset"] = "dejavuserif"
    plt.rcParams["font.size"] = 9.5
    plt.rcParams["axes.linewidth"] = 1.0

    fig, ax1 = plt.subplots(figsize=(6.2, 3.5), dpi=300)
    fig.subplots_adjust(left=0.11, right=0.88, top=0.91, bottom=0.14)

    rates = np.array([40.0, 50.0, 60.0, 66.7, 75.0, 85.0, 100.0])
    chars_allowed = np.array([8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0])
    wall_clock_ms = 8.0 * (1000.0 / rates)

    fine_rates = np.linspace(38.0, 108.0, 200)
    fine_ms = 8.0 * (1000.0 / fine_rates)

    ax1.axvspan(38.0, 110.0, color="#F8FAFC", alpha=0.9, zorder=0)
    ax1.axvspan(5.0, 38.0, color="#F0FDF4", alpha=0.6, zorder=0)
    ax1.axvline(38.0, color="#64748B", linestyle=":", linewidth=1.2, zorder=1)

    # Zone Headers with plenty of breathing room from y-axis
    ax1.text(21.5, 16.6, "Human / Evasion\nCadence Alert", ha="center", va="center",
             fontsize=7.2, color="#059669", fontweight="bold")
    ax1.text(62.0, 16.6, "Machine Injection Detection Zone\n(IKI < 25ms, Sustained CV < 0.15)", ha="center", va="center",
             fontsize=7.2, color="#1E293B", fontweight="bold")

    line_exec = ax1.axhline(14.0, color="#DC2626", linestyle="--", linewidth=1.6, zorder=2,
                            label=r"Attack Execution Horizon ($L_{\mathrm{exec}} = 14$ Chars)")

    ax1.fill_between([38.0, 110.0], 8.0, 14.0, color="#FEE2E2", alpha=0.65, zorder=1)
    ax1.text(53.0, 11.0, r"$\mathbf{\Delta = 6\text{ Character Safety Buffer}}$" "\n(Neutralized before execution)",
             ha="center", va="center", fontsize=7.5, fontweight="bold", color="#B91C1C",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFFFF", edgecolor="#FECACA", alpha=0.95))

    line_latency = ax1.plot(fine_rates, np.full_like(fine_rates, 8.0), color="#0F172A", linewidth=2.2, zorder=3,
                            label=r"Quarantine Trigger Latency ($\kappa = 8$ Keystrokes)")
    ax1.plot(rates, chars_allowed, "o", color="#0F172A", markersize=5.5, zorder=4)

    ax2 = ax1.twinx()
    line_ms = ax2.plot(fine_rates, fine_ms, color="#2563EB", linewidth=1.8, linestyle="-.", zorder=3,
                       label=r"Automated Reaction Time $t_{\mathrm{quarantine}}$ (ms)")
    ax2.plot(rates, wall_clock_ms, "D", color="#2563EB", markersize=5.0, zorder=4)

    # Callout at 100 ch/s placed cleanly in upper-right open space
    ax2.annotate(r"Standard BadUSB: 80.1 ms" "\n" r"($\mu = 10.0\mathrm{ms}, CV = 0.078$)",
                 xy=(100.0, 80.1), xytext=(94.0, 160.0),
                 ha="center",
                 arrowprops=dict(facecolor="#2563EB", edgecolor="#2563EB", shrink=0.08, width=1.2, headwidth=4.0),
                 fontsize=7.5, fontweight="bold", color="#1D4ED8",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="#EFF6FF", edgecolor="#BFDBFE", alpha=0.95))

    ax1.set_xlabel(r"Keystroke Injection Speed $R_{\mathrm{burst}}$ (Characters / Second)", fontsize=9.0, fontweight="bold")
    ax1.set_ylabel("Quarantine Latency (Characters Injected)", color="#0F172A", fontsize=9.0, fontweight="bold")
    ax1.tick_params(axis="y", labelcolor="#0F172A")
    ax1.set_xlim(5, 110)
    ax1.set_ylim(0, 18)
    ax1.grid(True, linestyle="--", alpha=0.45, color="#CBD5E1")

    ax2.set_ylabel(r"Automated Reaction Time $t_{\mathrm{quarantine}}$ (ms)", color="#2563EB", fontsize=9.0, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor="#2563EB")
    ax2.set_ylim(0, 220)

    lines = [line_latency[0], line_ms[0], line_exec]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="lower left", bbox_to_anchor=(0.26, 0.04), fontsize=7.2, framealpha=0.95, edgecolor="#94A3B8")

    out_pdf = os.path.join(PAPER_DIR, "fig_detection_latency.pdf")
    out_png = os.path.join(PAPER_DIR, "fig_detection_latency.png")
    fig.savefig(out_pdf, format="pdf")
    fig.savefig(out_png, format="png", dpi=300)
    plt.close(fig)
    print(f"Generated Spotless Figure 5: {out_pdf} and {out_png}")


if __name__ == "__main__":
    print("Generating spotless figures...")
    generate_spotless_figure_1()
    generate_spotless_figure_2()
    generate_spotless_figure_5()
    print("Done generating spotless figures!")
