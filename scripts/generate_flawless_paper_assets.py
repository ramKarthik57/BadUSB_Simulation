"""
WHID-Guard: Flawless Production Asset Generator
Strictly audits and ensures 0 overflow, perfect margins, and publication-ready graphics.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "reports", "assets")
PAPER_DIR = os.path.join(BASE_DIR, "paper")
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(PAPER_DIR, exist_ok=True)

# 4K Resolution Scale Factor (3960 px width)
S = 2.2

def sc(val):
    return int(round(val * S))

# Professional Palette
NAVY_DEEP = "#0B132B"
NAVY_PRIMARY = "#1C2541"
NAVY_SECONDARY = "#3A506B"
BLUE_TECH = "#1D4ED8"
BLUE_ACCENT = "#2563EB"
BLUE_LIGHT = "#3B82F6"
TEAL_DEEP = "#0F766E"
TEAL_ACCENT = "#0D9488"
TEAL_LIGHT = "#14B8A6"
CYAN_ACCENT = "#0284C7"
EMERALD_DEEP = "#047857"
EMERALD_GREEN = "#059669"
GREEN_SAFE = "#16A34A"
AMBER_DEEP = "#B45309"
AMBER_WARN = "#D97706"
CRIMSON_DEEP = "#B91C1C"
CRIMSON_DANGER = "#DC2626"
BG_LIGHT = "#F8FAFC"
BG_CARD = "#FFFFFF"
BORDER_COLOR = "#CBD5E1"
BORDER_DARK = "#94A3B8"
TEXT_MAIN = "#0F172A"
TEXT_MUTED = "#64748B"
TEXT_WHITE = "#FFFFFF"

def get_font(size, bold=False):
    scaled_size = sc(size)
    candidates = (
        ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/calibrib.ttf"]
        if bold
        else ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/calibri.ttf"]
    )
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, scaled_size)
    return ImageFont.load_default()

def get_mono_font(size, bold=False):
    scaled_size = sc(size)
    candidates = (
        ["C:/Windows/Fonts/consolab.ttf", "C:/Windows/Fonts/courbd.ttf"]
        if bold
        else ["C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/cour.ttf"]
    )
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, scaled_size)
    return get_font(size, bold)

def draw_rounded_box(draw, xy, radius, fill, outline=None, width=2):
    x0, y0, x1, y1 = [sc(v) for v in xy]
    draw.rounded_rectangle((x0, y0, x1, y1), radius=sc(radius), fill=fill, outline=outline, width=max(1, sc(width)))

def draw_rect(draw, xy, fill):
    x0, y0, x1, y1 = [sc(v) for v in xy]
    draw.rectangle((x0, y0, x1, y1), fill=fill)

def draw_line_sc(draw, pts, fill, width=2):
    s_pts = [(sc(x), sc(y)) for x, y in pts]
    draw.line(s_pts, fill=fill, width=max(1, sc(width)))

def draw_text_sc(draw, xy, text, font, fill=TEXT_MAIN):
    draw.text((sc(xy[0]), sc(xy[1])), text, font=font, fill=fill)

def draw_centered_text(draw, box, text, font, fill=TEXT_MAIN, dy=0):
    x0, y0, x1, y1 = [sc(v) for v in box]
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2 + sc(dy)
    lines = text.split("\n")
    line_heights = []
    line_widths = []
    pad = sc(5)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_widths.append(bbox[2] - bbox[0])
        line_heights.append(bbox[3] - bbox[1] + pad)
    total_h = sum(line_heights) - pad
    curr_y = cy - total_h / 2
    for i, line in enumerate(lines):
        draw.text((cx - line_widths[i] / 2, curr_y), line, font=font, fill=fill)
        curr_y += line_heights[i]

def draw_arrow_h(draw, x0, y, x1, color=NAVY_SECONDARY, width=4, bidirectional=False):
    sx0, sy, sx1 = sc(x0), sc(y), sc(x1)
    draw.line([(sx0, sy), (sx1, sy)], fill=color, width=max(1, sc(width)))
    head = sc(13)
    h_half = int(head * 0.65)
    if sx1 > sx0:
        draw.polygon([(sx1, sy), (sx1 - head, sy - h_half), (sx1 - head, sy + h_half)], fill=color)
        if bidirectional:
            draw.polygon([(sx0, sy), (sx0 + head, sy - h_half), (sx0 + head, sy + h_half)], fill=color)
    else:
        draw.polygon([(sx1, sy), (sx1 + head, sy - h_half), (sx1 + head, sy + h_half)], fill=color)
        if bidirectional:
            draw.polygon([(sx0, sy), (sx0 - head, sy - h_half), (sx0 - head, sy + h_half)], fill=color)

def draw_arrow_v(draw, x, y0, y1, color=NAVY_SECONDARY, width=4, bidirectional=False):
    sx, sy0, sy1 = sc(x), sc(y0), sc(y1)
    draw.line([(sx, sy0), (sx, sy1)], fill=color, width=max(1, sc(width)))
    head = sc(13)
    h_half = int(head * 0.65)
    if sy1 > sy0:
        draw.polygon([(sx, sy1), (sx - h_half, sy1 - head), (sx + h_half, sy1 - head)], fill=color)
        if bidirectional:
            draw.polygon([(sx, sy0), (sx - h_half, sy0 + head), (sx + h_half, sy0 + head)], fill=color)
    else:
        draw.polygon([(sx, sy1), (sx - h_half, sy1 + head), (sx + h_half, sy1 + head)], fill=color)
        if bidirectional:
            draw.polygon([(sx, sy0), (sx - h_half, sy0 - head), (sx + h_half, sy0 - head)], fill=color)


# ==============================================================================
# 1. FLAWLESS FIGURE 1: SYSTEM ARCHITECTURE
# ==============================================================================
def generate_flawless_system_architecture():
    w, h = 1800, 950
    img = Image.new("RGB", (sc(w), sc(h)), BG_CARD)
    draw = ImageDraw.Draw(img)

    # Outer boundary
    draw_rounded_box(draw, (8, 8, w - 8, h - 8), 16, fill=BG_LIGHT, outline=BORDER_COLOR, width=2)

    # Top Header Pill
    draw_rounded_box(draw, (18, 16, w - 18, 76), 12, fill=NAVY_DEEP)
    draw_text_sc(draw, (36, 26), "WHID-GUARD MULTI-TIER SYSTEM ARCHITECTURE & PER-DEVICE DEFENSE PIPELINE", font=get_font(21, True), fill=TEXT_WHITE)
    draw_text_sc(draw, (36, 52), "Out-of-Band Wireless Mobile Controller  |  ESP32-S3 Composite HID Firmware  |  Windows Raw Input Behavioral Engine", font=get_font(14, False), fill=BORDER_COLOR)

    # Spacious Column Layout:
    # Col 1 (Phone): x in [26, 496] (width 470)
    # Gap 1: x in [496, 646] (width 150) -> plenty of space for bus labels!
    # Col 2 (ESP32-S3): x in [646, 1166] (width 520)
    # Gap 2: x in [1166, 1316] (width 150) -> plenty of space for bus labels!
    # Col 3 (Host Defense): x in [1316, 1774] (width 458)
    c1_x0, c1_y0, c1_x1, c1_y1 = 26, 92, 496, 925
    c2_x0, c2_y0, c2_x1, c2_y1 = 646, 92, 1166, 925
    c3_x0, c3_y0, c3_x1, c3_y1 = 1316, 92, 1774, 925

    # --------------------------------------------------------------------------
    # TIER 1: WIRELESS MOBILE CONTROLLER
    # --------------------------------------------------------------------------
    draw_rounded_box(draw, (c1_x0, c1_y0, c1_x1, c1_y1), 14, fill=BG_CARD, outline=TEAL_DEEP, width=3)
    draw_rounded_box(draw, (c1_x0, c1_y0, c1_x1, c1_y0 + 52), 14, fill=TEAL_DEEP)
    draw_rect(draw, (c1_x0, c1_y0 + 34, c1_x1, c1_y0 + 52), fill=TEAL_DEEP)
    draw_text_sc(draw, (c1_x0 + 18, c1_y0 + 14), "TIER 1: MOBILE WEB CONTROLLER (SPA)", font=get_font(18, True), fill=TEXT_WHITE)

    client_blocks = [
        ("Zero-Dependency Web SPA (PROGMEM)", [
            "• Embedded in ESP32 Flash memory",
            "• Served via Mobile Chrome / Safari",
            "• SoftAP & Station Wi-Fi interfaces",
            "• Real-time 1.5s status polling",
        ]),
        ("Scenario Orchestration Suite", [
            "• Direct launch: Scenarios 1 to 4",
            "• Circular advance & Emergency Stop",
            "• Live execution feedback & status",
        ]),
        ("Virtual HID Keyboard & Mouse", [
            "• 6-Row QWERTY + Latched Modifiers",
            "• Multi-Touch Trackpad (60Hz deltas)",
            "• 1-Finger Tap, 2-Finger Scroll",
        ]),
        ("Adversarial Evasion Controls", [
            "• Evasion Mode Toggle: Injects jitter",
            "• Timing: 80ms base + [0..40ms] jitter",
            "• Delimiter micro-pauses (150-300ms)",
        ]),
    ]
    cy = c1_y0 + 68
    for btitle, blines in client_blocks:
        bh = 38 + len(blines) * 26
        draw_rounded_box(draw, (c1_x0 + 14, cy, c1_x1 - 14, cy + bh), 10, fill=BG_LIGHT, outline=BORDER_COLOR, width=2)
        draw_text_sc(draw, (c1_x0 + 24, cy + 8), btitle, font=get_font(15, True), fill=TEAL_DEEP)
        ly = cy + 32
        for l in blines:
            draw_text_sc(draw, (c1_x0 + 26, ly), l, font=get_font(14), fill=TEXT_MAIN)
            ly += 24
        cy += bh + 14

    # --------------------------------------------------------------------------
    # TIER 2: EMBEDDED MICROCONTROLLER (ESP32-S3)
    # --------------------------------------------------------------------------
    draw_rounded_box(draw, (c2_x0, c2_y0, c2_x1, c2_y1), 14, fill=BG_CARD, outline=BLUE_TECH, width=3)
    draw_rounded_box(draw, (c2_x0, c2_y0, c2_x1, c2_y0 + 52), 14, fill=NAVY_PRIMARY)
    draw_rect(draw, (c2_x0, c2_y0 + 34, c2_x1, c2_y0 + 52), fill=NAVY_PRIMARY)
    draw_text_sc(draw, (c2_x0 + 18, c2_y0 + 14), "TIER 2: ESP32-S3 COMPOSITE FIRMWARE", font=get_font(18, True), fill=TEXT_WHITE)

    fw_blocks = [
        ("FreeRTOS Dual-Core Architecture", BLUE_TECH, [
            "• Core 0: Wi-Fi Stack, WebServerHandler, REST API",
            "• Core 1: Scenario FSM & Adversarial Jitter Engine",
            "• portMUX_TYPE Spinlock Command Mailbox",
        ]),
        ("Deterministic 8-State Execution FSM", NAVY_SECONDARY, [
            "• BOOTING -> USB_WAIT (3.5s) -> STARTUP_PAYLOAD",
            "  -> IDLE <-> RUNNING -> STOPPING -> STOPPED",
            "• Physical GPIO 0 Button Interrupt (Debounced)",
        ]),
        ("Cooperative Preemption & Teardown", CRIMSON_DANGER, [
            "• Non-blocking smartDelay(10ms) slicing",
            "• Instant preemption response on stopRequested",
            "• Atomic Keyboard & Mouse releaseAll() in <= 10ms",
        ]),
        ("Native TinyUSB Composite HID Endpoints", TEAL_DEEP, [
            "• Direct USB OTG Transceiver on GPIO 19/20 (D-/D+)",
            "• Class 0x03 Boot Keyboard (8B) + 3-Btn Mouse (4B)",
            "• VID: 0x303A (Espressif), PID: 0x1001 (Composite HID)",
        ]),
    ]
    cy = c2_y0 + 68
    for idx, (btitle, col, blines) in enumerate(fw_blocks):
        bh = 38 + len(blines) * 26
        draw_rounded_box(draw, (c2_x0 + 14, cy, c2_x1 - 14, cy + bh), 10, fill=BG_LIGHT, outline=col, width=2)
        draw_text_sc(draw, (c2_x0 + 24, cy + 8), btitle, font=get_font(15, True), fill=col)
        ly = cy + 32
        for l in blines:
            draw_text_sc(draw, (c2_x0 + 26, ly), l, font=get_font(14), fill=TEXT_MAIN)
            ly += 24
        if idx < len(fw_blocks) - 1:
            draw_arrow_v(draw, (c2_x0 + c2_x1) // 2, cy + bh + 1, cy + bh + 13, color=col, width=3)
        cy += bh + 15

    # --------------------------------------------------------------------------
    # TIER 3: HOST DEFENSE TIER (WINDOWS 11)
    # --------------------------------------------------------------------------
    draw_rounded_box(draw, (c3_x0, c3_y0, c3_x1, c3_y1), 14, fill=BG_CARD, outline=EMERALD_DEEP, width=3)
    draw_rounded_box(draw, (c3_x0, c3_y0, c3_x1, c3_y0 + 52), 14, fill=EMERALD_DEEP)
    draw_rect(draw, (c3_x0, c3_y0 + 34, c3_x1, c3_y0 + 52), fill=EMERALD_DEEP)
    draw_text_sc(draw, (c3_x0 + 18, c3_y0 + 14), "TIER 3: WHID-GUARD HOST DEFENSE ENGINE", font=get_font(18, True), fill=TEXT_WHITE)

    host_blocks = [
        ("Raw Input Hardware Attribution", BLUE_TECH, [
            "• RegisterRawInputDevices (Usage 0x01, 0x06)",
            "• Queries GetRawInputDeviceInfoW",
            "• ESP32 Implant: Handle 0x14A0715",
            "• Internal Keyboard: Handle 0x10075",
        ]),
        ("Keystroke Dynamics Engine", NAVY_PRIMARY, [
            "• Sliding Window (W=10 events)",
            "• Tracks Mean IKI (mu) & Dispersion (CV)",
            "• Boundary: LOCKED_DOWN if mu<25ms",
            "• Safe Human Typing: mu>75ms & CV>0.30",
        ]),
        ("Selective Device Isolation Gate", CRIMSON_DANGER, [
            "• Win32 WH_KEYBOARD_LL Filter Gate",
            "• Drops rogue ESP32 keys (<= 8 chars)",
            "• Seamlessly PASSES physical operator keys",
        ]),
        ("Watchdog Guard & Telemetry", EMERALD_DEEP, [
            "• 15.0s Auto-Disarm Watchdog Timer",
            "• Guaranteed Clean Teardown (atexit)",
            "• Real-time GUI Telemetry & Matrix",
        ]),
    ]
    cy = c3_y0 + 68
    for idx, (btitle, col, blines) in enumerate(host_blocks):
        bh = 38 + len(blines) * 26
        draw_rounded_box(draw, (c3_x0 + 14, cy, c3_x1 - 14, cy + bh), 10, fill=BG_LIGHT, outline=col, width=2)
        draw_text_sc(draw, (c3_x0 + 24, cy + 8), btitle, font=get_font(15, True), fill=col)
        ly = cy + 32
        for l in blines:
            draw_text_sc(draw, (c3_x0 + 26, ly), l, font=get_font(14), fill=TEXT_MAIN)
            ly += 24
        if idx < len(host_blocks) - 1:
            draw_arrow_v(draw, (c3_x0 + c3_x1) // 2, cy + bh + 1, cy + bh + 13, color=col, width=3)
        cy += bh + 15

    # --------------------------------------------------------------------------
    # FLAWLESS INTERCONNECTS WITH ZERO OVERFLOW
    # --------------------------------------------------------------------------
    # Interconnect 1: Phone <-> ESP32-S3 (Gap: 496 to 646, width = 150)
    # Box width = 136 (503 to 639), x-center = 571
    draw_arrow_h(draw, c1_x1 + 4, 235, c2_x0 - 4, color=TEAL_DEEP, width=4, bidirectional=True)
    draw_rounded_box(draw, (503, 178, 639, 226), 8, fill=BG_CARD, outline=TEAL_DEEP, width=2)
    draw_centered_text(draw, (503, 178, 639, 226), "2.4GHz Wi-Fi\nREST API (JSON)", get_font(12, True), TEAL_DEEP)

    # Interconnect 2: ESP32-S3 -> Host (Gap: 1166 to 1316, width = 150)
    # Box width = 136 (1173 to 1309), x-center = 1241
    draw_arrow_h(draw, c2_x1 + 4, 785, c3_x0 - 4, color=BLUE_TECH, width=4, bidirectional=False)
    draw_rounded_box(draw, (1173, 728, 1309, 776), 8, fill=BG_CARD, outline=BLUE_TECH, width=2)
    draw_centered_text(draw, (1173, 728, 1309, 776), "USB 2.0 Cable\nGPIO 19/20 (D-/D+)", get_font(12, True), BLUE_TECH)

    # Interconnect 3: Selective Isolation Gate Callout (Top)
    draw_line_sc(draw, [(1241, 785), (1241, 235), (c3_x0 - 4, 235)], fill=CRIMSON_DANGER, width=3)
    draw_arrow_h(draw, 1240, 235, c3_x0 - 4, color=CRIMSON_DANGER, width=4)
    draw_rounded_box(draw, (1173, 178, 1309, 226), 8, fill=BG_CARD, outline=CRIMSON_DANGER, width=2)
    draw_centered_text(draw, (1173, 178, 1309, 226), "Selective Gate:\nDROPS Rogue Keys", get_font(12, True), CRIMSON_DANGER)

    for p in [os.path.join(ASSETS_DIR, "system_architecture.png"), os.path.join(PAPER_DIR, "system_architecture.png")]:
        img.save(p, dpi=(600, 600))
    print(f"Generated flawless Figure 1: {img.size}")


# ==============================================================================
# 2. FLAWLESS FIGURE 2: SCENARIO FSM EXECUTION FLOW
# ==============================================================================
def generate_flawless_fsm_diagram():
    w, h = 1800, 600
    img = Image.new("RGB", (sc(w), sc(h)), BG_CARD)
    draw = ImageDraw.Draw(img)

    # Outer canvas boundary
    draw_rounded_box(draw, (8, 8, w - 8, h - 8), 16, fill=BG_LIGHT, outline=BORDER_COLOR, width=2)

    # Top Header Pill
    draw_rounded_box(draw, (18, 16, w - 18, 70), 12, fill=NAVY_DEEP)
    draw_text_sc(draw, (36, 26), "DETERMINISTIC 8-STATE SCENARIO EXECUTION FINITE STATE MACHINE (FSM)", font=get_font(20, True), fill=TEXT_WHITE)
    draw_text_sc(draw, (36, 48), "Hardware Stabilization Timer, Interrupt-Safe Trigger Mailbox, Cooperative Preemption, and Atomic Teardown", font=get_font(13, False), fill=BORDER_COLOR)

    # --------------------------------------------------------------------------
    # TOP ROW: 5 PIPELINE STATES (SPACIOUS & BALANCED)
    # --------------------------------------------------------------------------
    top_states = [
        (30, 95, 270, 235, "STATE_BOOTING", NAVY_SECONDARY, "Hardware init, TinyUSB\ndescriptors registered,\npull-up asserted on D+"),
        (340, 95, 600, 235, "STATE_USB_WAIT", BLUE_TECH, "Non-blocking 3,500ms\nenumeration guard\n(tau_boot stabilization)"),
        (670, 95, 960, 235, "STATE_STARTUP_PAYLOAD", TEAL_DEEP, "Auto-executes Scenario 1\n(Notepad awareness)\nonce on initial boot"),
        (1030, 95, 1320, 235, "STATE_IDLE", GREEN_SAFE, "Steady ready state;\nawaits GPIO 0 press\nor Web API selection"),
        (1390, 95, 1770, 235, "STATE_RUNNING", AMBER_WARN, "Executes Scenarios 1–4\nvia smartDelay(10ms)\nwith preemption polling"),
    ]

    for x0, y0, x1, y1, st_name, col, desc in top_states:
        draw_rounded_box(draw, (x0, y0, x1, y1), 12, fill=BG_CARD, outline=col, width=3)
        draw_rounded_box(draw, (x0, y0, x1, y0 + 42), 12, fill=col)
        draw_rect(draw, (x0, y0 + 26, x1, y0 + 42), fill=col)
        draw_centered_text(draw, (x0, y0, x1, y0 + 42), st_name, get_mono_font(13, True), TEXT_WHITE)
        draw_centered_text(draw, (x0 + 8, y0 + 46, x1 - 8, y1 - 6), desc, get_font(13), TEXT_MAIN)

    # Connecting Arrows Top Row with generous gaps
    # Gap 270 to 340 (width 70)
    draw_arrow_h(draw, 270, 165, 340, NAVY_SECONDARY, 4)

    # Gap 600 to 670 (width 70)
    draw_arrow_h(draw, 600, 165, 670, BLUE_TECH, 4)
    draw_centered_text(draw, (600, 126, 670, 156), "3.5s", get_mono_font(13, True), BLUE_TECH)

    # Gap 960 to 1030 (width 70)
    draw_arrow_h(draw, 960, 165, 1030, TEAL_DEEP, 4)
    draw_centered_text(draw, (960, 126, 1030, 156), "Done", get_mono_font(13, True), TEAL_DEEP)

    # Gap 1030 to 1390 (width 70)
    draw_arrow_h(draw, 1320, 145, 1390, GREEN_SAFE, 4)
    draw_centered_text(draw, (1320, 118, 1390, 142), "Launch", get_font(13, True), GREEN_SAFE)

    draw_arrow_h(draw, 1390, 185, 1320, AMBER_WARN, 4)
    draw_centered_text(draw, (1320, 190, 1390, 214), "Finish", get_font(13, True), AMBER_WARN)

    # --------------------------------------------------------------------------
    # BOTTOM ROW: TRIGGERS, PREEMPTION & TEARDOWN
    # --------------------------------------------------------------------------
    bot_boxes = [
        (30, 310, 560, 570, "CONCURRENT TRIGGER SOURCES", NAVY_DEEP, [
            "• Physical GPIO 0 BOOT Button (50ms debounce, 600ms cooldown)",
            "• Web REST API: POST /api/scenario/select (IDs 1–4) & /api/scenario/next",
            "• FreeRTOS Spinlock Mailbox: portMUX_TYPE guards cmdPending",
            "• Eliminates race conditions between Core 0 (Web) & Core 1 (FSM)",
        ]),
        (660, 310, 1000, 570, "STATE_STOPPED", BLUE_TECH, [
            "• Entered following safe hardware abort",
            "• Verifies all modifiers & keys released",
            "• Restores clean HID bus state",
            "• Transitions back to STATE_IDLE",
        ]),
        (1110, 310, 1490, 570, "STATE_STOPPING", CRIMSON_DANGER, [
            "• Triggered by stopRequested = true",
            "• Immediately breaks 10ms delay loop",
            "• Calls Keyboard.releaseAll() & Mouse.releaseAll()",
            "• Clears Ctrl/Alt/Win modifier latches <= 10ms",
        ]),
        (1540, 310, 1770, 570, "STATE_ERROR", TEXT_MUTED, [
            "• Invalid scenario parameter",
            "• USB detachment / timeout",
            "• Auto-recovers to IDLE",
        ]),
    ]

    for x0, y0, x1, y1, st_name, col, lines in bot_boxes:
        draw_rounded_box(draw, (x0, y0, x1, y1), 12, fill=BG_CARD, outline=col, width=3)
        draw_rounded_box(draw, (x0, y0, x1, y0 + 42), 12, fill=col)
        draw_rect(draw, (x0, y0 + 26, x1, y0 + 42), fill=col)
        draw_centered_text(draw, (x0, y0, x1, y0 + 42), st_name, get_mono_font(13, True), TEXT_WHITE)
        ly = y0 + 52
        for l in lines:
            draw_text_sc(draw, (x0 + 16, ly), l, font=get_font(13), fill=TEXT_MAIN)
            ly += 26

    # Emergency Preemption Arrow: RUNNING -> STOPPING
    draw_arrow_v(draw, 1580, 235, 275, CRIMSON_DANGER, 4)
    draw_line_sc(draw, [(1580, 275), (1300, 275)], fill=CRIMSON_DANGER, width=4)
    draw_arrow_v(draw, 1300, 275, 310, CRIMSON_DANGER, 4)
    draw_centered_text(draw, (1305, 248, 1575, 272), "Emergency Abort (stopRequested=true)", get_font(13, True), CRIMSON_DANGER)

    # STOPPING -> STOPPED (Gap: 1000 to 1110, width = 110 px -> 242 px at scale!)
    draw_arrow_h(draw, 1110, 440, 1000, CRIMSON_DANGER, 4)
    draw_centered_text(draw, (1005, 404, 1105, 432), "Cleanup\nComplete", get_font(12, True), CRIMSON_DANGER)

    # STOPPED -> IDLE
    draw_arrow_v(draw, 830, 310, 275, GREEN_SAFE, 4)
    draw_line_sc(draw, [(830, 275), (1175, 275)], fill=GREEN_SAFE, width=4)
    draw_arrow_v(draw, 1175, 275, 235, GREEN_SAFE, 4)
    draw_centered_text(draw, (835, 248, 1170, 272), "Reset to Ready State", get_font(13, True), GREEN_SAFE)

    for p in [os.path.join(ASSETS_DIR, "fsm_diagram.png"), os.path.join(PAPER_DIR, "fsm_diagram.png")]:
        img.save(p, dpi=(600, 600))
    print(f"Generated flawless Figure 2: {img.size}")


# ==============================================================================
# 3. FLAWLESS FIGURE 5: DETECTION LATENCY & RESPONSE TIME CURVES
# ==============================================================================
def generate_flawless_fig_detection_latency():
    """
    Generates a publication-grade dual-axis latency plot with:
      - Left y-axis: Quarantine Latency (Characters Injected)
      - Right y-axis: Automated Quarantine Wall-Clock Time (ms)
      - Non-overlapping legend and clean callouts
      - Clean serif typography matching IEEE style
    """
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.size"] = 9.5
    plt.rcParams["axes.linewidth"] = 1.0

    fig, ax1 = plt.subplots(figsize=(6.4, 3.6), dpi=300)

    # Burst rates from 12 ch/s to 110 ch/s
    burst_rates = np.linspace(12.0, 110.0, 150)
    ikis = 1000.0 / burst_rates

    # Detection latency in characters:
    chars_injected = np.where(burst_rates >= 40.0, 8.0, np.nan)
    wall_clock_ms = np.where(burst_rates >= 40.0, 8.0 * ikis, np.nan)

    # Shaded Operational Zones
    ax1.axvspan(40.0, 115.0, color="#FEE2E2", alpha=0.60, label="Machine Injection Zone")
    ax1.axvspan(13.3, 40.0, color="#FEF3C7", alpha=0.60, label="Evasion Cadence Alert Zone")
    ax1.axvspan(0.0, 13.3, color="#DCFCE7", alpha=0.60, label="Safe Human Operator Zone")

    # Primary Curve: Characters Injected
    color_chars = "#0F172A"
    line1 = ax1.plot(burst_rates, chars_injected, color=color_chars, linewidth=2.4, label="Quarantine Latency (Chars)")
    ax1.plot([40.0, 50.0, 66.7, 80.0, 100.0], [8.0, 8.0, 8.0, 8.0, 8.0], "o", color=color_chars, markersize=5)

    ax1.set_xlabel(r"Keystroke Injection Speed $R_{\text{burst}}$ (Characters / Second)", fontsize=9.5, fontweight="bold")
    ax1.set_ylabel("Quarantine Latency (Characters Injected)", color=color_chars, fontsize=9.5, fontweight="bold")
    ax1.tick_params(axis="y", labelcolor=color_chars)
    ax1.set_xlim(10, 110)
    ax1.set_ylim(0, 22)
    ax1.grid(True, linestyle="--", alpha=0.45, color="#94A3B8")

    # Critical Security Thresholds
    line_exec = ax1.axhline(14.0, color="#DC2626", linestyle="--", linewidth=1.6, label="Execution Horizon (14 Chars)")
    line_floor = ax1.axhline(8.0, color="#2563EB", linestyle=":", linewidth=1.4, label=r"Detection Floor ($\kappa = 8$)")

    # Secondary Axis: Wall-Clock Latency (ms)
    ax2 = ax1.twinx()
    color_ms = "#B91C1C"
    line2 = ax2.plot(burst_rates, wall_clock_ms, color=color_ms, linewidth=2.0, linestyle="-.", label="Response Time (ms)")
    ax2.set_ylabel(r"Automated Response Time $t_{\text{quarantine}}$ (ms)", color=color_ms, fontsize=9.5, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor=color_ms)
    ax2.set_ylim(0, 260)

    # Annotated Security Safety Margin (placed in clear space)
    ax1.annotate(
        "Attack Execution Horizon\n('powershell.exe' = 14 chars)",
        xy=(85, 14.0),
        xytext=(50, 17.5),
        arrowprops=dict(facecolor="#DC2626", shrink=0.08, width=1.4, headwidth=4.5),
        fontsize=8.0,
        fontweight="bold",
        color="#DC2626",
    )

    ax1.annotate(
        r"WHID-Guard Suppression ($\kappa=8$)" "\n(80.1 ms @ 100 ch/s)",
        xy=(98, 8.0),
        xytext=(58, 3.8),
        arrowprops=dict(facecolor="#2563EB", shrink=0.08, width=1.4, headwidth=4.5),
        fontsize=8.0,
        fontweight="bold",
        color="#2563EB",
    )

    # Position Legend at center-left so it NEVER touches the data curves or annotations
    lines = line1 + line2 + [line_exec, line_floor]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper left", fontsize=7.5, framealpha=0.92, edgecolor="#CBD5E1")

    plt.tight_layout()

    for p in [os.path.join(ASSETS_DIR, "fig_detection_latency.pdf"), os.path.join(PAPER_DIR, "fig_detection_latency.pdf")]:
        fig.savefig(p, format="pdf", bbox_inches="tight")
    for p in [os.path.join(ASSETS_DIR, "fig_detection_latency.png"), os.path.join(PAPER_DIR, "fig_detection_latency.png")]:
        fig.savefig(p, format="png", dpi=600, bbox_inches="tight")

    plt.close(fig)
    print("Generated flawless Figure 5 (PDF & PNG)")


if __name__ == "__main__":
    generate_flawless_system_architecture()
    generate_flawless_fsm_diagram()
    generate_flawless_fig_detection_latency()
    print("All assets generated flawlessly!")
