"""
Crafts a 100% pixel-perfect, publication-grade Figure 1 (System Architecture).
Uses PIL with direct pixel coordinates, smooth anti-aliased geometry,
gorgeous rounded cards, clean bullet dots, and pristine bus connections.
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32"
PAPER_DIR = os.path.join(BASE_DIR, "paper")
os.makedirs(PAPER_DIR, exist_ok=True)

# 4K Canvas Dimensions
W = 3960
H = 2050

# Professional IEEE Palette
NAVY_HEADER = (11, 19, 43)
BG_CANVAS = (248, 250, 252)
BORDER_CANVAS = (203, 213, 225)

# Tier Colors: (HeaderFill, Border, CardFill, CardBorder, TitleText)
TIER1 = {
    "header": (15, 118, 110),       # Deep Teal
    "border": (13, 148, 136),
    "card_bg": (240, 253, 250),
    "card_border": (153, 246, 228),
    "title": (15, 118, 110)
}

TIER2 = {
    "header": (29, 78, 216),        # Tech Blue
    "border": (37, 99, 235),
    "card_bg": (239, 246, 255),
    "card_border": (191, 219, 254),
    "title": (29, 78, 216)
}

TIER3 = {
    "header": (185, 28, 28),        # Deep Crimson
    "border": (220, 38, 38),
    "card_bg": (254, 242, 242),
    "card_border": (254, 202, 202),
    "title": (185, 28, 28)
}

TEXT_MAIN = (15, 23, 42)      # Slate 900
TEXT_MUTED = (100, 116, 139)  # Slate 500
TEXT_WHITE = (255, 255, 255)

# Load High-Resolution Windows Fonts
font_master_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 52)
font_master_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 32)
font_tier_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 38)
font_tier_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 26)
font_card_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 32)
font_body = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 27)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26)
font_badge_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 23)

im = Image.new("RGB", (W, H), BG_CANVAS)
draw = ImageDraw.Draw(im)

# Outer Border
draw.rounded_rectangle([20, 20, W - 20, H - 20], radius=24, outline=BORDER_CANVAS, width=3)

# ------------------------------------------------------------------------------
# MASTER HEADER
# ------------------------------------------------------------------------------
draw.rounded_rectangle([36, 36, W - 36, 170], radius=18, fill=NAVY_HEADER)
draw.text((W // 2, 72), "WHID-GUARD: MULTI-TIER SYSTEM ARCHITECTURE & DEFENSE PIPELINE",
          font=font_master_title, fill=TEXT_WHITE, anchor="mm")
draw.text((W // 2, 130), "Tier 1: Out-of-Band Wireless Controller  |  Tier 2: Embedded ESP32-S3 Hardware  |  Tier 3: Windows Host Keystroke Firewall",
          font=font_master_sub, fill=(203, 213, 225), anchor="mm")

# ------------------------------------------------------------------------------
# 3-TIER COLUMN GEOMETRY
# ------------------------------------------------------------------------------
# Canvas Width = 3960
# Col 1: 50 to 1180 (width 1130)
# Gap 1: 1180 to 1420 (width 240) -> Interconnect 1 (Wi-Fi)
# Col 2: 1420 to 2550 (width 1130)
# Gap 2: 2550 to 2790 (width 240) -> Interconnect 2 (USB 2.0 PHY)
# Col 3: 2790 to 3910 (width 1120)

col1_x0, col1_x1 = 50, 1180
col2_x0, col2_x1 = 1420, 2550
col3_x0, col3_x1 = 2790, 3910
col_y0, col_y1 = 200, H - 45

# Helper function to draw Tier Container
def draw_tier_container(x0, y0, x1, y1, title, subtitle, tier_style):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=(255, 255, 255), outline=tier_style["border"], width=4)
    # Header box
    draw.rounded_rectangle([x0, y0, x1, y0 + 105], radius=20, fill=tier_style["header"])
    draw.rectangle([x0, y0 + 70, x1, y0 + 105], fill=tier_style["header"]) # flatten bottom corners
    draw.text(((x0 + x1) // 2, y0 + 38), title, font=font_tier_title, fill=TEXT_WHITE, anchor="mm")
    draw.text(((x0 + x1) // 2, y0 + 78), subtitle, font=font_tier_sub, fill=(226, 232, 240), anchor="mm")

# Draw the 3 Primary Containers
draw_tier_container(col1_x0, col_y0, col1_x1, col_y1,
                    "TIER 1: MOBILE WEB CONTROLLER (SPA)",
                    "Out-of-Band Wireless Red-Team Operator Interface", TIER1)

draw_tier_container(col2_x0, col_y0, col2_x1, col_y1,
                    "TIER 2: ESP32-S3 WEAPONIZED FIRMWARE",
                    "Dual-Core SoC, FreeRTOS FSM & Native TinyUSB PHY", TIER2)

draw_tier_container(col3_x0, col_y0, col3_x1, col_y1,
                    "TIER 3: WHID-GUARD HOST DEFENSE PIPELINE",
                    "Windows Raw Input Attribution & Selective Hook Firewall", TIER3)

# Helper function to draw sub-cards with bullet points
def draw_sub_card(x0, y0, x1, y1, card_title, bullets, tier_style):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=tier_style["card_bg"], outline=tier_style["card_border"], width=2)
    # Card Title
    draw.text((x0 + 26, y0 + 20), card_title, font=font_card_title, fill=tier_style["title"])
    # Bullets
    curr_y = y0 + 64
    for b in bullets:
        # Draw neat filled circular bullet
        draw.ellipse([x0 + 28, curr_y + 10, x0 + 38, curr_y + 20], fill=tier_style["title"])
        draw.text((x0 + 48, curr_y), b, font=font_body, fill=TEXT_MAIN)
        curr_y += 42

# ------------------------------------------------------------------------------
# TIER 1 CARDS
# ------------------------------------------------------------------------------
t1_cards = [
    ("Zero-Dependency Mobile Web Client (SPA)", [
        "Embedded in ESP32 Flash memory (PROGMEM, 52 KB)",
        "Zero host receiver software; served via Safari / Chrome",
        "Dual Wi-Fi: SoftAP (192.168.4.1) & Station (10.85.248.29)",
        "Real-time 1.5s bidirectional polling heartbeat",
    ]),
    ("Virtual HID Input & Touch Trackpad", [
        "6-Row QWERTY virtual keyboard with modifier latches",
        "Touch trackpad streaming relative deltas (dx, dy) at 60 Hz",
        "1-Finger Tap = Left Click  |  2-Finger Swipe = Scroll Wheel",
        "Instant responsive pointer control with zero host latency",
    ]),
    ("BadUSB Scenario Orchestration Suite", [
        "Direct launch & circular advance for Scenarios 1 to 4",
        "Scenario 1: Notepad Security Awareness Warning",
        "Scenario 2: Fake Windows Credential Prompt Phish",
        "Scenario 3: PowerShell Reverse Shell Detonation",
        "Scenario 4: Automated Recon & Data Exfiltration",
    ]),
    ("Adversarial Evasion & Cadence Controls", [
        "Stealth Mode Toggle: Injects artificial inter-key timing",
        "Gaussian Jitter: base delay (80ms) + stochastic jitter (0-40ms)",
        "Inter-word delimiter micro-pauses (150-300ms)",
        "Bypasses primitive static threshold keystroke filters",
    ]),
]

card_w = 1070
c1_left = col1_x0 + 30
card_h = 245
card_gap = 25
start_y = col_y0 + 130

for i, (ctitle, cbullets) in enumerate(t1_cards):
    cy = start_y + i * (card_h + card_gap)
    draw_sub_card(c1_left, cy, c1_left + card_w, cy + card_h, ctitle, cbullets, TIER1)

# ------------------------------------------------------------------------------
# TIER 2 CARDS
# ------------------------------------------------------------------------------
t2_cards = [
    ("FreeRTOS Dual-Core Architecture", [
        "Core 0: Wi-Fi Stack, Web Server & REST API endpoints",
        "Core 1: Scenario FSM & Adversarial Timing Generator",
        "portMUX_TYPE Spinlock Mailbox guards cmdPending",
        "Zero race conditions between asynchronous network & HID",
    ]),
    ("Deterministic 8-State Scenario FSM", [
        "3,500ms Non-blocking USB enumeration guard (tau_boot)",
        "Physical GPIO 0 BOOT Button (50ms debounce, 600ms cooldown)",
        "Cooperative smartDelay(10ms) slicing with abort polling",
        "Guarantees safe deterministic state transitions",
    ]),
    ("Cooperative Preemption & Teardown", [
        "stopRequested flag breaks execution loop within <= 10ms",
        "Calls Keyboard.releaseAll() and Mouse.releaseAll()",
        "Flushes Ctrl/Alt/Win modifier keys, leaving zero residue",
        "Restores clean USB HID bus state back to host",
    ]),
    ("Native TinyUSB Composite Transceiver", [
        "Direct USB OTG PHY Transceiver on GPIO 19/20 (D- / D+)",
        "Class 0x03 Boot Keyboard (8-byte) + 3-Btn Mouse (4-byte)",
        "USB CDC Serial port for 115,200 baud debug logging",
        "Hardware IDs: VID: 0x303A (Espressif), PID: 0x1001",
    ]),
]

c2_left = col2_x0 + 30
for i, (ctitle, cbullets) in enumerate(t2_cards):
    cy = start_y + i * (card_h + card_gap)
    draw_sub_card(c2_left, cy, c2_left + card_w, cy + card_h, ctitle, cbullets, TIER2)

# ------------------------------------------------------------------------------
# TIER 3 CARDS
# ------------------------------------------------------------------------------
t3_cards = [
    ("Raw Input Hardware Device Attribution", [
        "RegisterRawInputDevices(UsagePage=0x01, Usage=0x06)",
        "Intercepts WM_INPUT to read RAWINPUTHEADER.hDevice",
        "Queries GetRawInputDeviceInfoW(RIDI_DEVICENAME)",
        "Distinguishes ESP32 Implant (VID:303A) from Built-in Keyboard",
    ]),
    ("Sliding-Window IKI Dynamics Engine", [
        "Sliding Window (W = 10 events) computes Mean & StdDev",
        "Coefficient of Variation: CV = sigma / mu",
        "SAFE (Human): mu > 75ms and CV > 0.30 (FPR = 0.0%)",
        "LOCKED_DOWN (BadUSB): mu < 25ms or sustained CV < 0.15",
    ]),
    ("Selective Hook Filter Gate (WH_KEYBOARD_LL)", [
        "Low-Level Windows Keyboard Hook intercepts all keypresses",
        "Per-Device Gate: If hDevice in Quarantine -> DROP EVENT",
        "Authorized Device (Laptop Keyboard) -> PASS EVENT",
        "Surgically isolates malicious implant with 0 operator impact",
    ]),
    ("Live Telemetry & Automated Quarantine", [
        "PySide6 Host GUI displays real-time telemetry gauges",
        "Quarantine Latency: Exactly 8 keystrokes (<85ms response)",
        "6-Character Safety Buffer before command detonation",
        "Triggers visual and auditory lockdown alert to operator",
    ]),
]

c3_left = col3_x0 + 30
for i, (ctitle, cbullets) in enumerate(t3_cards):
    cy = start_y + i * (card_h + card_gap)
    draw_sub_card(c3_left, cy, c3_left + card_w, cy + card_h, ctitle, cbullets, TIER3)

# ------------------------------------------------------------------------------
# PROTOCOL INTERCONNECT BUSSES & ARROWS (PERFECTLY ALIGNED IN GAPS)
# ------------------------------------------------------------------------------
# Helper for clean horizontal arrow with sharp head
def draw_arrow_horizontal(x0, x1, y, color, width=5, head_len=24, head_h=18, bidirectional=False):
    draw.line([x0, y, x1, y], fill=color, width=width)
    # Right arrow head at x1
    draw.polygon([(x1, y), (x1 - head_len, y - head_h // 2), (x1 - head_len, y + head_h // 2)], fill=color)
    if bidirectional:
        # Left arrow head at x0
        draw.polygon([(x0, y), (x0 + head_len, y - head_h // 2), (x0 + head_len, y + head_h // 2)], fill=color)

# Interconnect 1: Between Tier 1 and Tier 2 (x in [1180, 1420], width 240)
# Centered at x = 1300, y = 730
bus1_cx = 1300
bus1_cy = 730

draw_arrow_horizontal(col1_x1, col2_x0, bus1_cy, color=TIER1["header"], width=6, bidirectional=True)
# Badge Box
draw.rounded_rectangle([bus1_cx - 105, bus1_cy - 70, bus1_cx + 105, bus1_cy + 70],
                       radius=12, fill=(255, 255, 255), outline=TIER1["header"], width=3)
draw.text((bus1_cx, bus1_cy - 42), "2.4 GHz Wi-Fi", font=font_badge, fill=TIER1["header"], anchor="mm")
draw.text((bus1_cx, bus1_cy - 10), "REST API (JSON)", font=font_badge, fill=TIER1["header"], anchor="mm")
draw.text((bus1_cx, bus1_cy + 22), "SoftAP / Station", font=font_badge_sub, fill=TEXT_MUTED, anchor="mm")
draw.text((bus1_cx, bus1_cy + 48), "HTTP POST /api/*", font=font_badge_sub, fill=TEXT_MUTED, anchor="mm")

# Interconnect 2: Between Tier 2 and Tier 3 (x in [2550, 2790], width 240)
# Centered at x = 2670, y = 730
bus2_cx = 2670
bus2_cy = 730

draw_arrow_horizontal(col2_x1, col3_x0, bus2_cy, color=TIER2["header"], width=6, bidirectional=False)
draw.rounded_rectangle([bus2_cx - 105, bus2_cy - 70, bus2_cx + 105, bus2_cy + 70],
                       radius=12, fill=(255, 255, 255), outline=TIER2["header"], width=3)
draw.text((bus2_cx, bus2_cy - 42), "USB 2.0 Cable", font=font_badge, fill=TIER2["header"], anchor="mm")
draw.text((bus2_cx, bus2_cy - 10), "GPIO 19/20 PHY", font=font_badge, fill=TIER2["header"], anchor="mm")
draw.text((bus2_cx, bus2_cy + 22), "12 Mbps Full-Speed", font=font_badge_sub, fill=TEXT_MUTED, anchor="mm")
draw.text((bus2_cx, bus2_cy + 48), "Composite CDC/HID", font=font_badge_sub, fill=TEXT_MUTED, anchor="mm")

# Selective Gate Callout Badge (Positioned cleanly at bottom gap x = 2670, y = 1450)
gate_cx = 2670
gate_cy = 1450
draw.line([col3_x0 - 5, gate_cy, col3_x0 + 15, gate_cy], fill=TIER3["header"], width=4)
draw.rounded_rectangle([gate_cx - 105, gate_cy - 65, gate_cx + 105, gate_cy + 65],
                       radius=12, fill=(255, 255, 255), outline=TIER3["header"], width=3)
draw.text((gate_cx, gate_cy - 38), "Selective Gate", font=font_badge, fill=TIER3["header"], anchor="mm")
draw.text((gate_cx, gate_cy - 10), "WH_KEYBOARD_LL", font=font_badge_sub, fill=TEXT_MAIN, anchor="mm")
draw.text((gate_cx, gate_cy + 18), "DROPS: ESP32", font=font_badge, fill=(220, 38, 38), anchor="mm")
draw.text((gate_cx, gate_cy + 44), "PASS: Laptop KB", font=font_badge, fill=(22, 163, 74), anchor="mm")

out_path = os.path.join(PAPER_DIR, "system_architecture.png")
im.save(out_path, quality=100)
print(f"Generated Flawless Figure 1: {out_path} ({W}x{H})")
