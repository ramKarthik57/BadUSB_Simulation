import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join("reports", "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# 4K Resolution Scale Factor (1800 * 2.2 = 3960 px width -> True 4K UHD)
S = 2.2

def sc(val):
    return int(round(val * S))

# Color Palette
NAVY_PRIMARY = "#14263D"
NAVY_SECONDARY = "#243B53"
TEAL_ACCENT = "#0F9D92"
BLUE_TECH = "#3273B9"
BG_LIGHT = "#F1F5F9"
BG_WHITE = "#FFFFFF"
TEXT_MAIN = "#273444"
TEXT_MUTED = "#64748B"
BORDER_COLOR = "#D7E0E8"
AMBER_WARN = "#D97706"
RED_DANGER = "#DC2626"
GREEN_SAFE = "#16A34A"


def get_font(size, bold=False):
    scaled_size = sc(size)
    font_candidates = (
        ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/calibrib.ttf"]
        if bold
        else ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/calibri.ttf"]
    )
    for path in font_candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, scaled_size)
    return ImageFont.load_default()


def get_mono_font(size, bold=False):
    scaled_size = sc(size)
    font_candidates = (
        ["C:/Windows/Fonts/consolab.ttf", "C:/Windows/Fonts/courbd.ttf"]
        if bold
        else ["C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/cour.ttf"]
    )
    for path in font_candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, scaled_size)
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
    pad = sc(6)
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


def generate_cover_banner():
    w, h = 1800, 520
    img = Image.new("RGB", (sc(w), sc(h)), BG_WHITE)
    draw = ImageDraw.Draw(img)

    draw_rounded_box(draw, (10, 10, w - 10, h - 10), 22, fill=BG_LIGHT, outline=BORDER_COLOR, width=3)
    draw_rounded_box(draw, (10, 10, w - 10, 82), 22, fill=NAVY_PRIMARY, outline=None)
    draw_rect(draw, (10, 55, w - 10, 82), fill=NAVY_PRIMARY)
    draw_text_sc(
        draw,
        (45, 28),
        "END-TO-END CYBERSECURITY & EMBEDDED USB HID PLATFORM ARCHITECTURE",
        font=get_font(24, True),
        fill=BG_WHITE,
    )
    draw_text_sc(
        draw,
        (w - 430, 30),
        "ESP32-S3  |  TinyUSB  |  Win32 Hook",
        font=get_mono_font(20, True),
        fill="#5EEAD4",
    )

    boxes = [
        (55, 125, 525, 455, NAVY_SECONDARY, TEAL_ACCENT, "1. MOBILE WEB CONTROLLER", [
            "Responsive Dark-Mode SPA",
            "• Full 6-Row QWERTY + Modifiers",
            "• Multi-Touch Trackpad & Drag Lock",
            "• 4 Educational Scenario Launchers",
            "• Token-Authenticated REST API",
            "• Dual-Mode Wi-Fi (AP + Hotspot STA)",
        ]),
        (665, 125, 1135, 455, NAVY_PRIMARY, BLUE_TECH, "2. ESP32-S3 NATIVE USB CORE", [
            "Xtensa Dual-Core @ 240 MHz",
            "• Native USB OTG (GPIO 19 D- / 20 D+)",
            "• Composite HID (Keyboard + Mouse)",
            "• Deterministic 8-State Scenario FSM",
            "• Physical GPIO 0 BOOT Button Sync",
            "• Immediate Emergency Stop / Release",
        ]),
        (1275, 125, 1745, 455, "#1E293B", GREEN_SAFE, "3. HOST OS & DEFENSE ENGINE", [
            "Windows 10/11 Target & Firewall",
            "• Zero-Driver HID Enumeration",
            "• Automated Keystroke Demo Execution",
            "• Python WH_KEYBOARD_LL Hook",
            "• Real-Time Global Event Suppression",
            "• 15-Second Fail-Safe Watchdog Timer",
        ]),
    ]

    for x0, y0, x1, y1, header_col, accent_col, title, bullets in boxes:
        draw_rounded_box(draw, (x0, y0, x1, y1), 16, fill=BG_WHITE, outline=accent_col, width=3)
        draw_rounded_box(draw, (x0, y0, x1, y0 + 62), 16, fill=header_col)
        draw_rect(draw, (x0, y0 + 42, x1, y0 + 62), fill=header_col)
        draw_text_sc(draw, (x0 + 22, y0 + 18), title, font=get_font(21, True), fill=BG_WHITE)

        by = y0 + 82
        for idx, b in enumerate(bullets):
            f = get_font(20, True) if idx == 0 else get_font(18, False)
            col = accent_col if idx == 0 else TEXT_MAIN
            draw_text_sc(draw, (x0 + 24, by), b, font=f, fill=col)
            by += 39 if idx == 0 else 36

    draw_arrow_h(draw, 535, 275, 655, color=TEAL_ACCENT, width=5, bidirectional=True)
    draw_centered_text(draw, (535, 210, 655, 260), "Wi-Fi HTTP\nREST JSON", get_font(17, True), TEAL_ACCENT)
    draw_centered_text(draw, (535, 290, 655, 340), "Port 80\nAP / STA", get_mono_font(16), TEXT_MUTED)

    draw_arrow_h(draw, 1145, 275, 1265, color=BLUE_TECH, width=5, bidirectional=False)
    draw_centered_text(draw, (1145, 210, 1265, 260), "Native USB\nHID Reports", get_font(17, True), BLUE_TECH)
    draw_centered_text(draw, (1145, 290, 1265, 340), "Keyboard +\nMouse", get_mono_font(16), TEXT_MUTED)

    img.save(os.path.join(ASSETS_DIR, "cover_banner.png"), dpi=(600, 600))


def generate_objectives_diagram():
    w, h = 1800, 440
    img = Image.new("RGB", (sc(w), sc(h)), BG_WHITE)
    draw = ImageDraw.Draw(img)

    draw_rounded_box(draw, (10, 10, w - 10, h - 10), 18, fill=BG_LIGHT, outline=BORDER_COLOR, width=2)
    draw_text_sc(
        draw,
        (40, 26),
        "CORE RESEARCH & ENGINEERING OBJECTIVES MATRIX",
        font=get_font(22, True),
        fill=NAVY_PRIMARY,
    )
    draw_line_sc(draw, [(40, 65), (w - 40, 65)], fill=BORDER_COLOR, width=2)

    pillars = [
        ("O1: Native Composite HID", TEAL_ACCENT, [
            "Implement composite USB HID",
            "Keyboard + Mouse on ESP32-S3",
            "using TinyUSB stack over native",
            "GPIO 19 (D-) & GPIO 20 (D+).",
            "Verify zero-driver enumeration.",
        ]),
        ("O2: Dual-Mode Mobile UI", BLUE_TECH, [
            "Serve an embedded PROGMEM SPA",
            "over concurrent SoftAP & Station",
            "Wi-Fi modes with full keyboard,",
            "multi-gesture touchpad, and",
            "PIN-authenticated REST control.",
        ]),
        ("O3: Safe Scenario Engine", NAVY_SECONDARY, [
            "Design a non-blocking 8-state",
            "FSM executing 4 non-destructive",
            "security awareness scenarios via",
            "boot auto-run, GPIO 0 button,",
            "or remote web selection.",
        ]),
        ("O4: Host Keystroke Defense", GREEN_SAFE, [
            "Build a Windows host-side",
            "keystroke firewall utilizing",
            "WH_KEYBOARD_LL hooks with",
            "real-time suppression and a",
            "15-second fail-safe watchdog.",
        ]),
    ]

    pw = 405
    gap = 28
    start_x = 40
    for i, (title, col, lines) in enumerate(pillars):
        x0 = start_x + i * (pw + gap)
        y0 = 88
        x1 = x0 + pw
        y1 = h - 30
        draw_rounded_box(draw, (x0, y0, x1, y1), 14, fill=BG_WHITE, outline=col, width=3)
        draw_rounded_box(draw, (x0, y0, x1, y0 + 54), 14, fill=col)
        draw_rect(draw, (x0, y0 + 38, x1, y0 + 54), fill=col)
        draw_text_sc(draw, (x0 + 20, y0 + 14), title, font=get_font(20, True), fill=BG_WHITE)

        ty = y0 + 76
        for line in lines:
            draw_text_sc(draw, (x0 + 20, ty), line, font=get_font(18), fill=TEXT_MAIN)
            ty += 34

        draw_rounded_box(draw, (x0 + 20, y1 - 52, x1 - 20, y1 - 16), 8, fill=BG_LIGHT, outline=BORDER_COLOR, width=1)
        status_labels = [
            "Verified on ESP32-S3 (COM5)",
            "Verified on Android (CDP/ADB)",
            "Verified FSM & Stop Safety",
            "Verified 22/22 Automated Tests",
        ]
        draw_centered_text(draw, (x0 + 20, y1 - 52, x1 - 20, y1 - 16), status_labels[i], get_font(16, True), col)

    img.save(os.path.join(ASSETS_DIR, "objectives_diagram.png"), dpi=(600, 600))


def generate_system_architecture():
    w, h = 1800, 960
    img = Image.new("RGB", (sc(w), sc(h)), BG_WHITE)
    draw = ImageDraw.Draw(img)

    draw_rounded_box(draw, (10, 10, w - 10, h - 10), 20, fill=BG_LIGHT, outline=BORDER_COLOR, width=3)
    draw_rounded_box(draw, (10, 10, w - 10, 78), 20, fill=NAVY_PRIMARY)
    draw_rect(draw, (10, 50, w - 10, 78), fill=NAVY_PRIMARY)
    draw_text_sc(
        draw,
        (40, 25),
        "SYSTEM ARCHITECTURE: MOBILE SPA, ESP32-S3 COMPOSITE HID FIRMWARE & HOST DEFENSE",
        font=get_font(23, True),
        fill=BG_WHITE,
    )

    c1_x0, c1_y0, c1_x1, c1_y1 = 40, 105, 520, 920
    draw_rounded_box(draw, (c1_x0, c1_y0, c1_x1, c1_y1), 16, fill=BG_WHITE, outline=TEAL_ACCENT, width=3)
    draw_rounded_box(draw, (c1_x0, c1_y0, c1_x1, c1_y0 + 55), 16, fill=TEAL_ACCENT)
    draw_rect(draw, (c1_x0, c1_y0 + 35, c1_x1, c1_y0 + 55), fill=TEAL_ACCENT)
    draw_text_sc(draw, (c1_x0 + 24, c1_y0 + 14), "TIER 1: ANDROID PHONE CONTROLLER", font=get_font(20, True), fill=BG_WHITE)

    client_blocks = [
        ("Single-Page Web App (PROGMEM)", [
            "• Rendered in Mobile Chrome Browser",
            "• Zero External CDN Dependencies",
            "• 1.5s Live Telemetry Polling (/api/status)",
        ]),
        ("Tab 1: Scenario Orchestrator", [
            "• Direct Launch (Scenarios 1–4)",
            "• Next Scenario & Emergency Stop",
        ]),
        ("Tab 2: Remote Keyboard Suite", [
            "• Full 6-Row QWERTY + Function Row",
            "• Latched Modifiers (Ctrl, Alt, Shift, Win)",
            "• Shortcuts, Bulk Text (256B) & Numpad",
        ]),
        ("Tab 3: Multi-Touch Trackpad", [
            "• 60Hz Delta Throttling (16ms interval)",
            "• 1-Finger Move/Tap, 2-Finger Scroll/R-Click",
            "• Drag Lock, Sensitivity (0.5x–3.0x), Nudge",
        ]),
        ("Tab 4: Security & Network Config", [
            "• X-Auth-Token Session Storage",
            "• Dual IP Telemetry (SoftAP & Hotspot STA)",
        ]),
    ]
    cy = c1_y0 + 75
    for btitle, blines in client_blocks:
        bh = 42 + len(blines) * 28
        draw_rounded_box(draw, (c1_x0 + 20, cy, c1_x1 - 20, cy + bh), 10, fill=BG_LIGHT, outline=BORDER_COLOR, width=2)
        draw_text_sc(draw, (c1_x0 + 34, cy + 8), btitle, font=get_font(18, True), fill=NAVY_PRIMARY)
        ly = cy + 36
        for l in blines:
            draw_text_sc(draw, (c1_x0 + 36, ly), l, font=get_font(16), fill=TEXT_MAIN)
            ly += 26
        cy += bh + 16

    c2_x0, c2_y0, c2_x1, c2_y1 = 640, 105, 1180, 920
    draw_rounded_box(draw, (c2_x0, c2_y0, c2_x1, c2_y1), 16, fill=BG_WHITE, outline=BLUE_TECH, width=3)
    draw_rounded_box(draw, (c2_x0, c2_y0, c2_x1, c2_y0 + 55), 16, fill=NAVY_PRIMARY)
    draw_rect(draw, (c2_x0, c2_y0 + 35, c2_x1, c2_y0 + 55), fill=NAVY_PRIMARY)
    draw_text_sc(draw, (c2_x0 + 24, c2_y0 + 14), "TIER 2: ESP32-S3 FIRMWARE (DUAL-CORE)", font=get_font(20, True), fill=BG_WHITE)

    fw_blocks = [
        ("Dual-Mode Wi-Fi & HTTP Server (Port 80)", BLUE_TECH, [
            "• WIFI_AP_STA: SoftAP (192.168.4.1) + Phone Hotspot STA",
            "• mDNS Responder (http://badusb.local)",
            "• WebServerHandler: Auth Token Verification & CORS",
            "• 13 REST Endpoints (/api/status, /scenario/*, /keyboard/*, /mouse/*)",
        ]),
        ("Thread-Safe Scenario Controller & FSM", NAVY_SECONDARY, [
            "• portMUX_TYPE Spinlock Command Mailbox (cmdPending)",
            "• 8 States: BOOTING -> USB_WAIT (3.5s) -> STARTUP_PAYLOAD",
            "  -> IDLE <-> RUNNING -> STOPPING -> STOPPED",
            "• Cooperative smartDelay(10ms) polling stopRequested flag",
        ]),
        ("Physical Hardware Input (GPIO 0 BOOT)", AMBER_WARN, [
            "• INPUT_PULLUP with 50ms Debounce & 600ms Cooldown",
            "• Advances circularly: Scenario 1 -> 2 -> 3 -> 4 -> 1",
        ]),
        ("Composite TinyUSB HID Engine (GPIO 19/20)", TEAL_ACCENT, [
            "• USBHIDKeyboard: Keypress, Modifiers, Shortcuts, ASCII Type",
            "• USBHIDMouse: Clamped Move (-127..127), Click, Press, Scroll",
            "• Safe Release: releaseAll() on both Keyboard & Mouse on Stop",
        ]),
    ]
    cy = c2_y0 + 75
    for idx, (btitle, col, blines) in enumerate(fw_blocks):
        bh = 46 + len(blines) * 30
        draw_rounded_box(draw, (c2_x0 + 20, cy, c2_x1 - 20, cy + bh), 12, fill=BG_LIGHT, outline=col, width=2)
        draw_text_sc(draw, (c2_x0 + 34, cy + 10), btitle, font=get_font(18, True), fill=col)
        ly = cy + 40
        for l in blines:
            draw_text_sc(draw, (c2_x0 + 36, ly), l, font=get_font(16), fill=TEXT_MAIN)
            ly += 28
        if idx < len(fw_blocks) - 1:
            draw_arrow_v(draw, (c2_x0 + c2_x1) // 2, cy + bh + 2, cy + bh + 24, color=col, width=3)
        cy += bh + 26

    c3_x0, c3_y0, c3_x1, c3_y1 = 1300, 105, 1760, 920
    draw_rounded_box(draw, (c3_x0, c3_y0, c3_x1, c3_y1), 16, fill=BG_WHITE, outline=GREEN_SAFE, width=3)
    draw_rounded_box(draw, (c3_x0, c3_y0, c3_x1, c3_y0 + 55), 16, fill=NAVY_SECONDARY)
    draw_rect(draw, (c3_x0, c3_y0 + 35, c3_x1, c3_y0 + 55), fill=NAVY_SECONDARY)
    draw_text_sc(draw, (c3_x0 + 24, c3_y0 + 14), "TIER 3: WINDOWS HOST & FIREWALL", font=get_font(20, True), fill=BG_WHITE)

    host_blocks = [
        ("Windows OS Kernel USB & HID Stack", BLUE_TECH, [
            "• Enumerates Composite HID Device",
            "• Zero Driver Installation Required",
            "• Translates HID Usage Tables to",
            "  WM_KEYDOWN / Mouse Input Events",
        ]),
        ("Host Keystroke Firewall (src/firewall.py)", RED_DANGER, [
            "• Win32 Low-Level Hook (WH_KEYBOARD_LL)",
            "• Intercepts Keystrokes Before App Focus",
            "• BLOCKING Mode: keyboard.hook(suppress=True)",
            "• Blocks Automated Payloads & Live Keys",
        ]),
        ("Fail-Safe Watchdog & Lifecycle Recovery", GREEN_SAFE, [
            "• 15.0s Auto-Disarm threading.Timer",
            "• Prevents Accidental Host Input Lockout",
            "• Guaranteed Unhook on Exit (atexit +",
            "  WM_DELETE_WINDOW clean teardown)",
        ]),
        ("Target User-Space Applications", NAVY_PRIMARY, [
            "• Notepad / Browser / Command Prompt",
            "• Receives Input ONLY when Firewall is",
            "  in ALLOW (Monitoring) State",
        ]),
    ]
    cy = c3_y0 + 75
    for idx, (btitle, col, blines) in enumerate(host_blocks):
        bh = 46 + len(blines) * 29
        draw_rounded_box(draw, (c3_x0 + 20, cy, c3_x1 - 20, cy + bh), 12, fill=BG_LIGHT, outline=col, width=2)
        draw_text_sc(draw, (c3_x0 + 34, cy + 10), btitle, font=get_font(18, True), fill=col)
        ly = cy + 38
        for l in blines:
            draw_text_sc(draw, (c3_x0 + 36, ly), l, font=get_font(16), fill=TEXT_MAIN)
            ly += 27
        if idx < len(host_blocks) - 1:
            draw_arrow_v(draw, (c3_x0 + c3_x1) // 2, cy + bh + 2, cy + bh + 22, color=col, width=3)
        cy += bh + 24

    draw_arrow_h(draw, c1_x1 + 8, 250, c2_x0 - 8, color=TEAL_ACCENT, width=5, bidirectional=True)
    draw_centered_text(draw, (c1_x1, 185, c2_x0, 240), "HTTP REST\nJSON API", get_font(17, True), TEAL_ACCENT)
    draw_centered_text(draw, (c1_x1, 260, c2_x0, 320), "X-Auth-Token\n2.4GHz Wi-Fi", get_mono_font(15), TEXT_MUTED)

    draw_arrow_h(draw, c2_x1 + 8, 780, c3_x0 - 8, color=BLUE_TECH, width=5, bidirectional=False)
    draw_centered_text(draw, (c2_x1, 710, c3_x0, 768), "USB 2.0 Full\nSpeed HID", get_font(17, True), BLUE_TECH)
    draw_centered_text(draw, (c2_x1, 792, c3_x0, 850), "D- (GPIO19)\nD+ (GPIO20)", get_mono_font(15), TEXT_MUTED)

    draw_line_sc(draw, [(c2_x1 + 60, 780), (c2_x1 + 60, 240), (c3_x0 - 8, 240)], fill=BLUE_TECH, width=4)
    draw.polygon(
        [(sc(c3_x0 - 8), sc(240)), (sc(c3_x0 - 20), sc(232)), (sc(c3_x0 - 20), sc(248))],
        fill=BLUE_TECH,
    )

    img.save(os.path.join(ASSETS_DIR, "system_architecture.png"), dpi=(600, 600))


def generate_fsm_diagram():
    w, h = 1800, 560
    img = Image.new("RGB", (sc(w), sc(h)), BG_WHITE)
    draw = ImageDraw.Draw(img)

    draw_rounded_box(draw, (10, 10, w - 10, h - 10), 18, fill=BG_LIGHT, outline=BORDER_COLOR, width=2)
    draw_text_sc(
        draw,
        (36, 24),
        "SCENARIO CONTROLLER FINITE STATE MACHINE (FSM) & INTERRUPT-SAFE EXECUTION FLOW",
        font=get_font(22, True),
        fill=NAVY_PRIMARY,
    )
    draw_line_sc(draw, [(36, 62), (w - 36, 62)], fill=BORDER_COLOR, width=2)

    top_states = [
        (45, 110, 290, 240, "STATE_BOOTING", NAVY_SECONDARY, "Init Serial, Keyboard,\nMouse & USB.begin()"),
        (355, 110, 620, 240, "STATE_USB_WAIT", BLUE_TECH, "Non-blocking 3500ms\nhost enumeration wait"),
        (685, 110, 990, 240, "STATE_STARTUP_PAYLOAD", TEAL_ACCENT, "Auto-runs Scenario 1\nonce on initial boot"),
        (1055, 110, 1320, 240, "STATE_IDLE", GREEN_SAFE, "Awaits GPIO 0 press\nor Web API selection"),
        (1430, 110, 1745, 240, "STATE_RUNNING", AMBER_WARN, "Executes selected\nScenario 1..4 steps"),
    ]

    for x0, y0, x1, y1, st_name, col, desc in top_states:
        draw_rounded_box(draw, (x0, y0, x1, y1), 14, fill=BG_WHITE, outline=col, width=3)
        draw_rounded_box(draw, (x0, y0, x1, y0 + 46), 14, fill=col)
        draw_rect(draw, (x0, y0 + 30, x1, y0 + 46), fill=col)
        draw_centered_text(draw, (x0, y0, x1, y0 + 46), st_name, get_mono_font(17, True), BG_WHITE)
        draw_centered_text(draw, (x0 + 10, y0 + 50, x1 - 10, y1 - 6), desc, get_font(17), TEXT_MAIN)

    draw_arrow_h(draw, 290, 175, 355, NAVY_SECONDARY, 4)
    draw_arrow_h(draw, 620, 175, 685, BLUE_TECH, 4)
    draw_centered_text(draw, (620, 130, 685, 165), "3.5s", get_mono_font(15, True), BLUE_TECH)
    draw_arrow_h(draw, 990, 175, 1055, TEAL_ACCENT, 4)
    draw_centered_text(draw, (990, 130, 1055, 165), "Done", get_mono_font(15, True), TEAL_ACCENT)
    draw_arrow_h(draw, 1320, 155, 1430, GREEN_SAFE, 4)
    draw_centered_text(draw, (1320, 122, 1430, 150), "Trigger", get_font(15, True), GREEN_SAFE)
    draw_arrow_h(draw, 1430, 200, 1320, AMBER_WARN, 4)
    draw_centered_text(draw, (1320, 206, 1430, 234), "Done", get_font(15, True), AMBER_WARN)

    bot_boxes = [
        (45, 340, 560, 495, "CONCURRENT TRIGGER SOURCES", NAVY_PRIMARY, [
            "• Physical GPIO 0 BOOT Button (50ms debounce, 600ms cooldown)",
            "• Web API: POST /api/scenario/select (id: 1..4) or /api/scenario/next",
            "• Synchronized via portMUX_TYPE Spinlock Mailbox (cmdPending)",
        ]),
        (650, 340, 1000, 495, "STATE_STOPPED", NAVY_SECONDARY, [
            "• Entered after safe abort teardown",
            "• Ready for next GPIO 0 button press",
            "  or Web UI scenario launch command",
        ]),
        (1090, 340, 1460, 495, "STATE_STOPPING", RED_DANGER, [
            "• Triggered by POST /api/scenario/stop",
            "• Interrupts smartDelay(10ms) loop",
            "• Calls Keyboard & Mouse releaseAll()",
        ]),
        (1520, 340, 1745, 495, "STATE_ERROR", "#64748B", [
            "• Invalid Scenario ID",
            "  or USB not ready",
            "• Auto-recovers",
        ]),
    ]

    for x0, y0, x1, y1, st_name, col, lines in bot_boxes:
        draw_rounded_box(draw, (x0, y0, x1, y1), 14, fill=BG_WHITE, outline=col, width=3)
        draw_rounded_box(draw, (x0, y0, x1, y0 + 46), 14, fill=col)
        draw_rect(draw, (x0, y0 + 30, x1, y0 + 46), fill=col)
        draw_centered_text(draw, (x0, y0, x1, y0 + 46), st_name, get_mono_font(17, True), BG_WHITE)
        ly = y0 + 58
        for l in lines:
            draw_text_sc(draw, (x0 + 18, ly), l, font=get_font(16), fill=TEXT_MAIN)
            ly += 29

    draw_arrow_v(draw, 1600, 240, 295, RED_DANGER, 4)
    draw_line_sc(draw, [(1600, 295), (1275, 295)], fill=RED_DANGER, width=4)
    draw_arrow_v(draw, 1275, 295, 340, RED_DANGER, 4)
    draw_centered_text(draw, (1280, 260, 1590, 288), "Stop / Abort (stopRequested=true)", get_font(16, True), RED_DANGER)

    draw_arrow_h(draw, 1090, 418, 1000, RED_DANGER, 4)
    draw_arrow_v(draw, 825, 340, 295, GREEN_SAFE, 4)
    draw_line_sc(draw, [(825, 295), (1185, 295)], fill=GREEN_SAFE, width=4)
    draw_arrow_v(draw, 1185, 295, 240, GREEN_SAFE, 4)
    draw_centered_text(draw, (830, 260, 1180, 288), "New Command / Next Scenario Trigger", get_font(16, True), GREEN_SAFE)

    img.save(os.path.join(ASSETS_DIR, "fsm_diagram.png"), dpi=(600, 600))


def create_phone_composite(img1_path, img2_path, label1, label2, out_name):
    im1 = Image.open(img1_path).convert("RGB")
    im2 = Image.open(img2_path).convert("RGB")

    # Crop out the top phone notification bar & Chrome URL bar
    w1, h1 = im1.size
    crop_top = int(h1 * 0.112)
    crop_bot = int(h1 * 0.965)
    im1_c = im1.crop((0, crop_top, w1, crop_bot))
    im2_c = im2.crop((0, crop_top, w1, crop_bot))

    # Keep ultra-crisp 4K-grade dimensions (1520 px per phone panel -> 3440 px total width)
    target_w = sc(760)
    target_h = int(im1_c.size[1] * (target_w / im1_c.size[0]))
    im1_r = im1_c.resize((target_w, target_h), Image.Resampling.LANCZOS)
    im2_r = im2_c.resize((target_w, target_h), Image.Resampling.LANCZOS)

    canvas_w = 1720
    canvas_h = int(target_h / S) + 130
    canvas = Image.new("RGB", (sc(canvas_w), sc(canvas_h)), BG_LIGHT)
    draw = ImageDraw.Draw(canvas)

    draw_rounded_box(draw, (8, 8, canvas_w - 8, canvas_h - 8), 20, fill=BG_LIGHT, outline=BORDER_COLOR, width=3)

    positions = [(65, 32, im1_r, label1), (895, 32, im2_r, label2)]
    for x, y, sub_im, lbl in positions:
        draw_rounded_box(
            draw,
            (x - 10, y - 10, x + 760 + 10, y + int(target_h / S) + 10),
            24,
            fill=NAVY_PRIMARY,
            outline=TEAL_ACCENT,
            width=3,
        )
        canvas.paste(sub_im, (sc(x), sc(y)))
        draw_centered_text(
            draw,
            (x, y + int(target_h / S) + 22, x + 760, canvas_h - 16),
            lbl,
            get_font(24, True),
            NAVY_PRIMARY,
        )

    canvas.save(os.path.join(ASSETS_DIR, out_name), dpi=(600, 600))


def generate_defense_diagram():
    w, h = 1800, 430
    img = Image.new("RGB", (sc(w), sc(h)), BG_WHITE)
    draw = ImageDraw.Draw(img)

    draw_rounded_box(draw, (10, 10, w - 10, h - 10), 18, fill=BG_LIGHT, outline=BORDER_COLOR, width=2)
    draw_text_sc(
        draw,
        (36, 22),
        "WINDOWS HOST KEYSTROKE FIREWALL: WH_KEYBOARD_LL HOOK & WATCHDOG PIPELINE",
        font=get_font(22, True),
        fill=NAVY_PRIMARY,
    )
    draw_line_sc(draw, [(36, 60), (w - 36, 60)], fill=BORDER_COLOR, width=2)

    stages = [
        (45, 95, 415, 390, "1. HID EVENT INJECTION", BLUE_TECH, [
            "ESP32-S3 Composite HID",
            "or Physical Keyboard sends",
            "USB HID Usage Scancodes",
            "to Windows kbdclass.sys",
            "kernel input queue.",
        ]),
        (485, 95, 895, 390, "2. WIN32 LOW-LEVEL HOOK", NAVY_PRIMARY, [
            "Python keyboard library",
            "registers WH_KEYBOARD_LL",
            "hook in global OS chain",
            "BEFORE events reach",
            "foreground window focus.",
        ]),
        (965, 95, 1365, 390, "3. SUPPRESSION GATE", RED_DANGER, [
            "• ALLOW Mode: Events pass",
            "  normally to applications.",
            "• BLOCKING Mode:",
            "  keyboard.hook(suppress=True)",
            "  drops all injected keys.",
        ]),
        (1435, 95, 1755, 390, "4. 15s FAIL-SAFE TIMER", GREEN_SAFE, [
            "threading.Timer(15.0)",
            "auto-disarms firewall",
            "back to ALLOW mode +",
            "atexit unhook prevents",
            "host lockout.",
        ]),
    ]

    for x0, y0, x1, y1, title, col, lines in stages:
        draw_rounded_box(draw, (x0, y0, x1, y1), 14, fill=BG_WHITE, outline=col, width=3)
        draw_rounded_box(draw, (x0, y0, x1, y0 + 50), 14, fill=col)
        draw_rect(draw, (x0, y0 + 34, x1, y0 + 50), fill=col)
        draw_text_sc(draw, (x0 + 18, y0 + 12), title, font=get_font(19, True), fill=BG_WHITE)
        ly = y0 + 72
        for l in lines:
            draw_text_sc(draw, (x0 + 20, ly), l, font=get_font(18), fill=TEXT_MAIN)
            ly += 34

    draw_arrow_h(draw, 415, 240, 485, BLUE_TECH, 4)
    draw_arrow_h(draw, 895, 240, 965, NAVY_PRIMARY, 4)
    draw_arrow_h(draw, 1365, 240, 1435, GREEN_SAFE, 4, bidirectional=True)

    img.save(os.path.join(ASSETS_DIR, "defense_architecture.png"), dpi=(600, 600))


if __name__ == "__main__":
    generate_cover_banner()
    generate_objectives_diagram()
    generate_system_architecture()
    generate_fsm_diagram()
    create_phone_composite(
        "artifacts/phone-ui/final/01_scenarios.png",
        "artifacts/phone-ui/final/02_keyboard.png",
        "(a) Educational Scenarios & Direct Launch",
        "(b) Full 6-Row Hardware Keyboard & Modifiers",
        "phone_ui_scenarios_keyboard.png",
    )
    create_phone_composite(
        "artifacts/phone-ui/final/03_mouse.png",
        "artifacts/phone-ui/final/04_settings.png",
        "(a) Multi-Touch Trackpad, Clicks & Drag Lock",
        "(b) Masked PIN Auth & Dual-Mode Network State",
        "phone_ui_mouse_settings.png",
    )
    generate_defense_diagram()
    print("All 4K report assets (3960px width, 600 DPI) generated successfully in reports/assets/")
