"""
WHID-Guard: Professional Asset Generator for IEEE Research Paper
Generates publication-quality 4K diagrams:
  - Fig 1: system_architecture.png (Multi-tier system architecture)
  - Fig 2: fsm_diagram.png (Deterministic 8-state execution FSM)
  - Fig 5: fig_detection_latency.pdf and fig_detection_latency.png (Dual-axis detection latency curve)
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

# Professional IEEE Color Palette
NAVY_DEEP = "#0F172A"
NAVY_PRIMARY = "#1E293B"
NAVY_SECONDARY = "#334155"
BLUE_TECH = "#2563EB"
BLUE_LIGHT = "#3B82F6"
TEAL_ACCENT = "#0D9488"
TEAL_LIGHT = "#14B8A6"
CYAN_ACCENT = "#0284C7"
EMERALD_GREEN = "#059669"
GREEN_SAFE = "#16A34A"
GREEN_LIGHT = "#22C55E"
AMBER_WARN = "#D97706"
AMBER_LIGHT = "#F59E0B"
CRIMSON_DANGER = "#DC2626"
RED_LIGHT = "#EF4444"
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
    head = sc(12)
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
    head = sc(12)
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
# 1. PERFECT FIGURE 1: SYSTEM ARCHITECTURE
# ==============================================================================
def generate_perfect_system_architecture():
    w, h = 1800, 940
    img = Image.new("RGB", (sc(w), sc(h)), BG_CARD)
    draw = ImageDraw.Draw(img)

    # Outer canvas boundary
    draw_rounded_box(draw, (8, 8, w - 8, h - 8), 16, fill=BG_LIGHT, outline=BORDER_COLOR, width=2)

    # Top Header Pill
    draw_rounded_box(draw, (18, 16, w - 18, 76), 12, fill=NAVY_DEEP)
    draw_text_sc(draw, (36, 26), "WHID-GUARD MULTI-TIER SYSTEM ARCHITECTURE & PER-DEVICE DEFENSE PIPELINE", font=get_font(21, True), fill=TEXT_WHITE)
    draw_text_sc(draw, (36, 52), "Out-of-Band Wireless Mobile Controller  |  ESP32-S3 Composite HID Firmware  |  Windows Raw Input Behavioral Engine", font=get_font(14, False), fill=BORDER_COLOR)

    # --------------------------------------------------------------------------
    # TIER 1: WIRELESS MOBILE CONTROLLER (SPA)
    # --------------------------------------------------------------------------
    c1_x0, c1_y0, c1_x1, c1_y1 = 28, 92, 530, 915
    draw_rounded_box(draw, (c1_x0, c1_y0, c1_x1, c1_y1), 14, fill=BG_CARD, outline=TEAL_ACCENT, width=3)
    draw_rounded_box(draw, (c1_x0, c1_y0, c1_x1, c1_y0 + 52), 14, fill=TEAL_ACCENT)
    draw_rect(draw, (c1_x0, c1_y0 + 34, c1_x1, c1_y0 + 52), fill=TEAL_ACCENT)
    draw_text_sc(draw, (c1_x0 + 20, c1_y0 + 14), "TIER 1: WIRELESS MOBILE CONTROLLER", font=get_font(18, True), fill=TEXT_WHITE)

    client_blocks = [
        ("Zero-Dependency Web SPA (PROGMEM)", [
            "• Embedded in ESP32 Flash program memory",
            "• Rendered in standard mobile browsers",
            "• SoftAP (192.168.4.1) & Station (10.85.248.29)",
            "• Real-time 1.5s status polling (/api/status)",
        ]),
        ("Scenario Orchestrator & Safety", [
            "• Direct launch for Scenarios 1–4",
            "• Circular scenario advance & Emergency Abort",
            "• Live execution status & state feedback",
        ]),
        ("Virtual HID Keyboard & Mouse Suite", [
            "• 6-Row QWERTY + Latched Modifiers (Ctrl/Alt/Win)",
            "• Multi-Touch Trackpad: 60Hz delta throttling",
            "• 1-Finger Tap/Click, 2-Finger Scroll & R-Click",
        ]),
        ("Adversarial Evasion Engine Controller", [
            "• Evasion Mode Toggle: Injects stochastic jitter",
            "• Timing modulation: 80ms base + [0..40ms] jitter",
            "• Contextual delimiter micro-pauses (150-300ms)",
        ]),
    ]
    cy = c1_y0 + 68
    for btitle, blines in client_blocks:
        bh = 38 + len(blines) * 26
        draw_rounded_box(draw, (c1_x0 + 16, cy, c1_x1 - 16, cy + bh), 10, fill=BG_LIGHT, outline=BORDER_COLOR, width=2)
        draw_text_sc(draw, (c1_x0 + 28, cy + 8), btitle, font=get_font(16, True), fill=TEAL_ACCENT)
        ly = cy + 32
        for l in blines:
            draw_text_sc(draw, (c1_x0 + 30, ly), l, font=get_font(14), fill=TEXT_MAIN)
            ly += 24
        cy += bh + 14

    # --------------------------------------------------------------------------
    # TIER 2: EMBEDDED MICROCONTROLLER FIRMWARE (ESP32-S3)
    # --------------------------------------------------------------------------
    c2_x0, c2_y0, c2_x1, c2_y1 = 635, 92, 1180, 915
    draw_rounded_box(draw, (c2_x0, c2_y0, c2_x1, c2_y1), 14, fill=BG_CARD, outline=BLUE_TECH, width=3)
    draw_rounded_box(draw, (c2_x0, c2_y0, c2_x1, c2_y0 + 52), 14, fill=NAVY_PRIMARY)
    draw_rect(draw, (c2_x0, c2_y0 + 34, c2_x1, c2_y0 + 52), fill=NAVY_PRIMARY)
    draw_text_sc(draw, (c2_x0 + 20, c2_y0 + 14), "TIER 2: ESP32-S3 COMPOSITE FIRMWARE", font=get_font(18, True), fill=TEXT_WHITE)

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
        ("Native TinyUSB Composite HID Endpoints", TEAL_ACCENT, [
            "• Direct USB OTG Transceiver on GPIO 19/20 (D-/D+)",
            "• Class 0x03 Boot Keyboard (8B) + 3-Btn Mouse (4B)",
            "• VID: 0x303A (Espressif), PID: 0x1001 (Composite HID)",
        ]),
    ]
    cy = c2_y0 + 68
    for idx, (btitle, col, blines) in enumerate(fw_blocks):
        bh = 38 + len(blines) * 26
        draw_rounded_box(draw, (c2_x0 + 16, cy, c2_x1 - 16, cy + bh), 10, fill=BG_LIGHT, outline=col, width=2)
        draw_text_sc(draw, (c2_x0 + 28, cy + 8), btitle, font=get_font(16, True), fill=col)
        ly = cy + 32
        for l in blines:
            draw_text_sc(draw, (c2_x0 + 30, ly), l, font=get_font(14), fill=TEXT_MAIN)
            ly += 24
        if idx < len(fw_blocks) - 1:
            draw_arrow_v(draw, (c2_x0 + c2_x1) // 2, cy + bh + 1, cy + bh + 13, color=col, width=3)
        cy += bh + 15

    # --------------------------------------------------------------------------
    # TIER 3: HOST DEFENSE TIER (WINDOWS 11 WORKSTATION)
    # --------------------------------------------------------------------------
    c3_x0, c3_y0, c3_x1, c3_y1 = 1285, 92, 1772, 915
    draw_rounded_box(draw, (c3_x0, c3_y0, c3_x1, c3_y1), 14, fill=BG_CARD, outline=EMERALD_GREEN, width=3)
    draw_rounded_box(draw, (c3_x0, c3_y0, c3_x1, c3_y0 + 52), 14, fill=EMERALD_GREEN)
    draw_rect(draw, (c3_x0, c3_y0 + 34, c3_x1, c3_y0 + 52), fill=EMERALD_GREEN)
    draw_text_sc(draw, (c3_x0 + 20, c3_y0 + 14), "TIER 3: WHID-GUARD HOST DEFENSE ENGINE", font=get_font(18, True), fill=TEXT_WHITE)

    host_blocks = [
        ("Windows Raw Input Hardware Attribution", BLUE_TECH, [
            "• RegisterRawInputDevices (Usage 0x01, 0x06, INPUTSINK)",
            "• Intercepts WM_INPUT & queries GetRawInputDeviceInfoW",
            "• Attributed Handles: Implant (0x14A0715) vs",
            "  Physical Built-in Keyboard (Handle: 0x10075)",
        ]),
        ("Online Behavioral Keystroke Dynamics", NAVY_PRIMARY, [
            "• Multi-Device Sliding Window (W=10 events)",
            "• Tracks Mean IKI (mu), Dispersion (sigma), CV = sigma/mu",
            "• Decision Boundary: LOCKED_DOWN if mu<25ms or CV<0.15",
            "• Safe Human Typing: mu>75ms and CV>0.30",
        ]),
        ("Selective Interception & Per-Device Isolation", CRIMSON_DANGER, [
            "• Win32 Low-Level Hook (WH_KEYBOARD_LL) Gate",
            "• Drops rogue ESP32 scancodes within 8 chars (<85ms)",
            "• Concurrently PASSES primary physical keyboard keys",
        ]),
        ("Watchdog Guard & Live Admin Telemetry", EMERALD_GREEN, [
            "• 15.0s Auto-Disarm Watchdog Timer (No lockout)",
            "• Clean teardown on exit (atexit hook release)",
            "• Real-time GUI: Live IKI, CV, burst speed & status",
        ]),
    ]
    cy = c3_y0 + 68
    for idx, (btitle, col, blines) in enumerate(host_blocks):
        bh = 38 + len(blines) * 26
        draw_rounded_box(draw, (c3_x0 + 16, cy, c3_x1 - 16, cy + bh), 10, fill=BG_LIGHT, outline=col, width=2)
        draw_text_sc(draw, (c3_x0 + 28, cy + 8), btitle, font=get_font(16, True), fill=col)
        ly = cy + 32
        for l in blines:
            draw_text_sc(draw, (c3_x0 + 30, ly), l, font=get_font(14), fill=TEXT_MAIN)
            ly += 24
        if idx < len(host_blocks) - 1:
            draw_arrow_v(draw, (c3_x0 + c3_x1) // 2, cy + bh + 1, cy + bh + 13, color=col, width=3)
        cy += bh + 15

    # --------------------------------------------------------------------------
    # INTERCONNECTS AND BUS LABELS
    # --------------------------------------------------------------------------
    # Interconnect 1: Phone <-> ESP32-S3 (2.4GHz Wi-Fi HTTP)
    draw_arrow_h(draw, c1_x1 + 6, 240, c2_x0 - 6, color=TEAL_ACCENT, width=4, bidirectional=True)
    draw_rounded_box(draw, (c1_x1 + 10, 182, c2_x0 - 10, 230), 8, fill=BG_CARD, outline=TEAL_ACCENT, width=2)
    draw_centered_text(draw, (c1_x1 + 10, 182, c2_x0 - 10, 230), "2.4GHz Wi-Fi\nREST API (JSON)", get_font(13, True), TEAL_ACCENT)

    # Interconnect 2: ESP32-S3 -> Windows Host (USB 2.0 Cable)
    draw_arrow_h(draw, c2_x1 + 6, 780, c3_x0 - 6, color=BLUE_TECH, width=4, bidirectional=False)
    draw_rounded_box(draw, (c2_x1 + 10, 722, c3_x0 - 10, 770), 8, fill=BG_CARD, outline=BLUE_TECH, width=2)
    draw_centered_text(draw, (c2_x1 + 10, 722, c3_x0 - 10, 770), "USB 2.0 Full-Speed\nGPIO 19/20 (D-/D+)", get_font(13, True), BLUE_TECH)

    # Top Interconnect: Selective Filtering Action
    draw_line_sc(draw, [(c2_x1 + 52, 780), (c2_x1 + 52, 240), (c3_x0 - 6, 240)], fill=CRIMSON_DANGER, width=3)
    draw_arrow_h(draw, c2_x1 + 50, 240, c3_x0 - 6, color=CRIMSON_DANGER, width=4)
    draw_rounded_box(draw, (c2_x1 + 8, 182, c3_x0 - 8, 230), 8, fill=BG_CARD, outline=CRIMSON_DANGER, width=2)
    draw_centered_text(draw, (c2_x1 + 8, 182, c3_x0 - 8, 230), "Selective Gate:\nDROPS ESP32", get_font(13, True), CRIMSON_DANGER)

    for p in [os.path.join(ASSETS_DIR, "system_architecture.png"), os.path.join(PAPER_DIR, "system_architecture.png")]:
        img.save(p, dpi=(600, 600))
    print(f"Generated perfect Figure 1: {img.size}")


# ==============================================================================
# 2. PERFECT FIGURE 2: SCENARIO FSM EXECUTION FLOW
# ==============================================================================
def generate_perfect_fsm_diagram():
    w, h = 1800, 580
    img = Image.new("RGB", (sc(w), sc(h)), BG_CARD)
    draw = ImageDraw.Draw(img)

    # Outer canvas boundary
    draw_rounded_box(draw, (8, 8, w - 8, h - 8), 16, fill=BG_LIGHT, outline=BORDER_COLOR, width=2)

    # Top Header Pill
    draw_rounded_box(draw, (18, 16, w - 18, 70), 12, fill=NAVY_DEEP)
    draw_text_sc(draw, (36, 26), "DETERMINISTIC 8-STATE SCENARIO EXECUTION FINITE STATE MACHINE (FSM)", font=get_font(20, True), fill=TEXT_WHITE)
    draw_text_sc(draw, (36, 48), "Hardware Stabilization Timer, Interrupt-Safe Trigger Mailbox, Cooperative Preemption, and Atomic Teardown", font=get_font(13, False), fill=BORDER_COLOR)

    # --------------------------------------------------------------------------
    # TOP ROW: 5 PIPELINE STATES
    # --------------------------------------------------------------------------
    top_states = [
        (30, 95, 265, 235, "STATE_BOOTING", NAVY_SECONDARY, "Hardware init, TinyUSB\ndescriptors registered,\npull-up asserted on D+"),
        (325, 95, 595, 235, "STATE_USB_WAIT", BLUE_TECH, "Non-blocking 3,500ms\nenumeration guard\n(tau_boot stabilization)"),
        (655, 95, 955, 235, "STATE_STARTUP_PAYLOAD", TEAL_ACCENT, "Auto-executes Scenario 1\n(Notepad awareness)\nonce on initial boot"),
        (1015, 95, 1315, 235, "STATE_IDLE", GREEN_SAFE, "Steady ready state;\nawaits GPIO 0 press\nor Web API selection"),
        (1375, 95, 1770, 235, "STATE_RUNNING", AMBER_WARN, "Executes Scenarios 1–4\nvia smartDelay(10ms)\nwith preemption polling"),
    ]

    for x0, y0, x1, y1, st_name, col, desc in top_states:
        draw_rounded_box(draw, (x0, y0, x1, y1), 12, fill=BG_CARD, outline=col, width=3)
        draw_rounded_box(draw, (x0, y0, x1, y0 + 42), 12, fill=col)
        draw_rect(draw, (x0, y0 + 26, x1, y0 + 42), fill=col)
        draw_centered_text(draw, (x0, y0, x1, y0 + 42), st_name, get_mono_font(14, True), TEXT_WHITE)
        draw_centered_text(draw, (x0 + 8, y0 + 46, x1 - 8, y1 - 6), desc, get_font(14), TEXT_MAIN)

    # Connecting Arrows Top Row
    draw_arrow_h(draw, 265, 165, 325, NAVY_SECONDARY, 4)
    draw_arrow_h(draw, 595, 165, 655, BLUE_TECH, 4)
    draw_centered_text(draw, (595, 126, 655, 156), "3.5s", get_mono_font(13, True), BLUE_TECH)

    draw_arrow_h(draw, 955, 165, 1015, TEAL_ACCENT, 4)
    draw_centered_text(draw, (955, 126, 1015, 156), "Done", get_mono_font(13, True), TEAL_ACCENT)

    draw_arrow_h(draw, 1315, 145, 1375, GREEN_SAFE, 4)
    draw_centered_text(draw, (1315, 118, 1375, 142), "Launch", get_font(13, True), GREEN_SAFE)

    draw_arrow_h(draw, 1375, 185, 1315, AMBER_WARN, 4)
    draw_centered_text(draw, (1315, 190, 1375, 214), "Finish", get_font(13, True), AMBER_WARN)

    # --------------------------------------------------------------------------
    # BOTTOM ROW: TRIGGERS, PREEMPTION & TEARDOWN
    # --------------------------------------------------------------------------
    bot_boxes = [
        (30, 310, 560, 550, "CONCURRENT TRIGGER SOURCES", NAVY_DEEP, [
            "• Physical GPIO 0 BOOT Button (50ms debounce, 600ms cooldown)",
            "• Web REST API: POST /api/scenario/select (IDs 1–4) & /api/scenario/next",
            "• FreeRTOS Spinlock Mailbox: portMUX_TYPE guards cmdPending",
            "• Eliminates race conditions between Core 0 (Web) & Core 1 (FSM)",
        ]),
        (655, 310, 1015, 550, "STATE_STOPPED", BLUE_TECH, [
            "• Entered following safe hardware abort",
            "• Verifies all modifiers & keys released",
            "• Restores clean HID bus state",
            "• Transitions back to STATE_IDLE",
        ]),
        (1085, 310, 1470, 550, "STATE_STOPPING", CRIMSON_DANGER, [
            "• Triggered by stopRequested = true",
            "• Immediately breaks 10ms delay loop",
            "• Calls Keyboard.releaseAll() & Mouse.releaseAll()",
            "• Clears Ctrl/Alt/Win modifier latches <= 10ms",
        ]),
        (1525, 310, 1770, 550, "STATE_ERROR", TEXT_MUTED, [
            "• Invalid scenario parameter",
            "• USB detachment / timeout",
            "• Auto-recovers to IDLE",
        ]),
    ]

    for x0, y0, x1, y1, st_name, col, lines in bot_boxes:
        draw_rounded_box(draw, (x0, y0, x1, y1), 12, fill=BG_CARD, outline=col, width=3)
        draw_rounded_box(draw, (x0, y0, x1, y0 + 42), 12, fill=col)
        draw_rect(draw, (x0, y0 + 26, x1, y0 + 42), fill=col)
        draw_centered_text(draw, (x0, y0, x1, y0 + 42), st_name, get_mono_font(14, True), TEXT_WHITE)
        ly = y0 + 52
        for l in lines:
            draw_text_sc(draw, (x0 + 16, ly), l, font=get_font(14), fill=TEXT_MAIN)
            ly += 26

    # Emergency Preemption Arrow: RUNNING -> STOPPING
    draw_arrow_v(draw, 1570, 235, 275, CRIMSON_DANGER, 4)
    draw_line_sc(draw, [(1570, 275), (1275, 275)], fill=CRIMSON_DANGER, width=4)
    draw_arrow_v(draw, 1275, 275, 310, CRIMSON_DANGER, 4)
    draw_centered_text(draw, (1280, 248, 1560, 272), "Emergency Abort (stopRequested=true)", get_font(13, True), CRIMSON_DANGER)

    # STOPPING -> STOPPED
    draw_arrow_h(draw, 1085, 430, 1015, CRIMSON_DANGER, 4)
    draw_centered_text(draw, (1015, 396, 1085, 424), "Cleanup\nDone", get_font(12, True), CRIMSON_DANGER)

    # STOPPED -> IDLE
    draw_arrow_v(draw, 835, 310, 275, GREEN_SAFE, 4)
    draw_line_sc(draw, [(835, 275), (1165, 275)], fill=GREEN_SAFE, width=4)
    draw_arrow_v(draw, 1165, 275, 235, GREEN_SAFE, 4)
    draw_centered_text(draw, (840, 248, 1160, 272), "Reset to Ready State", get_font(13, True), GREEN_SAFE)

    for p in [os.path.join(ASSETS_DIR, "fsm_diagram.png"), os.path.join(PAPER_DIR, "fsm_diagram.png")]:
        img.save(p, dpi=(600, 600))
    print(f"Generated perfect Figure 2: {img.size}")


# ==============================================================================
# 3. PERFECT FIGURE 5: DETECTION LATENCY & RESPONSE TIME CURVES
# ==============================================================================
def generate_perfect_fig_detection_latency():
    """
    Generates a publication-grade dual-axis latency plot:
      - Left y-axis: Quarantine Latency (Characters Injected)
      - Right y-axis: Automated Quarantine Wall-Clock Time (ms)
      - Shaded regions for Machine Injection (<=25ms), Evasion (25-75ms), and Human (>75ms)
      - Safety margin callout to Attack Execution Horizon (14 chars)
    """
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.size"] = 10
    plt.rcParams["axes.linewidth"] = 1.0

    fig, ax1 = plt.subplots(figsize=(6.4, 3.7), dpi=300)

    # Burst rates from 10 ch/s to 120 ch/s
    burst_rates = np.linspace(12.0, 110.0, 120)
    # Inter-key interval in ms
    ikis = 1000.0 / burst_rates

    # Detection latency in characters:
    # At machine speed (>= 40 ch/s, IKI <= 25ms): exactly 8 characters
    # Between 13.3 and 40 ch/s: Cadence anomaly zone (alerted, not locked down)
    chars_injected = np.where(burst_rates >= 40.0, 8.0, np.nan)

    # Wall-clock response time in ms: t = 8 * (1000 / R)
    wall_clock_ms = np.where(burst_rates >= 40.0, 8.0 * ikis, np.nan)

    # Shaded Operational Zones
    ax1.axvspan(40.0, 115.0, color="#FEE2E2", alpha=0.65, label="Machine Injection Zone (Quarantined)")
    ax1.axvspan(13.3, 40.0, color="#FEF3C7", alpha=0.65, label="Evasion Cadence Anomaly Zone (Alerted)")
    ax1.axvspan(0.0, 13.3, color="#DCFCE7", alpha=0.65, label="Safe Human Operator Zone (Allowed)")

    # Primary Curve: Characters Injected
    color_chars = "#0F172A"
    line1 = ax1.plot(burst_rates, chars_injected, color=color_chars, linewidth=2.4, label="Quarantine Latency (Chars)")
    ax1.plot([40.0, 50.0, 66.7, 80.0, 100.0], [8.0, 8.0, 8.0, 8.0, 8.0], "o", color=color_chars, markersize=5)

    ax1.set_xlabel(r"Keystroke Injection Speed $R_{\text{burst}}$ (Characters / Second)", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Quarantine Latency (Characters Injected)", color=color_chars, fontsize=10, fontweight="bold")
    ax1.tick_params(axis="y", labelcolor=color_chars)
    ax1.set_xlim(10, 110)
    ax1.set_ylim(0, 22)
    ax1.grid(True, linestyle="--", alpha=0.45, color="#94A3B8")

    # Critical Security Thresholds
    ax1.axhline(14.0, color="#DC2626", linestyle="--", linewidth=1.8, label="Command Execution Horizon (14 Chars)")
    ax1.axhline(8.0, color="#2563EB", linestyle=":", linewidth=1.5, label="Detection Floor (kappa = 8 Chars)")

    # Secondary Axis: Wall-Clock Latency (ms)
    ax2 = ax1.twinx()
    color_ms = "#B91C1C"
    line2 = ax2.plot(burst_rates, wall_clock_ms, color=color_ms, linewidth=2.2, linestyle="-.", label="Quarantine Time (ms)")
    ax2.set_ylabel("Automated Response Time $t_{\text{quarantine}}$ (ms)", color=color_ms, fontsize=10, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor=color_ms)
    ax2.set_ylim(0, 260)

    # Annotated Security Safety Margin
    ax1.annotate(
        "Attack Execution Horizon\n(e.g., 'powershell.exe' = 14 chars)",
        xy=(82, 14.0),
        xytext=(48, 17.5),
        arrowprops=dict(facecolor="#DC2626", shrink=0.08, width=1.5, headwidth=5),
        fontsize=8.5,
        fontweight="bold",
        color="#DC2626",
    )

    ax1.annotate(
        "WHID-Guard Suppression Floor\n(<= 8 chars / 80ms @ 100 ch/s)",
        xy=(95, 8.0),
        xytext=(55, 4.2),
        arrowprops=dict(facecolor="#2563EB", shrink=0.08, width=1.5, headwidth=5),
        fontsize=8.5,
        fontweight="bold",
        color="#2563EB",
    )

    # Combined Legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(loc="upper right", fontsize=8.0, framealpha=0.92, edgecolor="#CBD5E1")

    plt.tight_layout()

    for p in [os.path.join(ASSETS_DIR, "fig_detection_latency.pdf"), os.path.join(PAPER_DIR, "fig_detection_latency.pdf")]:
        fig.savefig(p, format="pdf", bbox_inches="tight")
    for p in [os.path.join(ASSETS_DIR, "fig_detection_latency.png"), os.path.join(PAPER_DIR, "fig_detection_latency.png")]:
        fig.savefig(p, format="png", dpi=600, bbox_inches="tight")

    plt.close(fig)
    print("Generated perfect Figure 5 (PDF & PNG)")


if __name__ == "__main__":
    generate_perfect_system_architecture()
    generate_perfect_fsm_diagram()
    generate_perfect_fig_detection_latency()
    print("All assets generated successfully!")
