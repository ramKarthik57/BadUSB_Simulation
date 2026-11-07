import os
import sys
import json
import time
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

WIDTH = 1920
HEIGHT = 1080
FPS = 20

FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def draw_top_bar(draw, scene_idx, total_scenes, scene_title, elapsed_scene, dur_scene, elapsed_global, dur_global):
    # Top container
    draw_rounded_rect(draw, (40, 20, 1880, 95), radius=12, fill=(18, 24, 38), outline=(48, 54, 61), width=1)
    
    # Institution & Project Titles
    f_univ = get_font(FONT_BOLD, 15)
    f_proj = get_font(FONT_BOLD, 21)
    f_auth = get_font(FONT_REG, 13)
    
    draw.text((65, 30), "AMRITA VISHWA VIDYAPEETHAM  |  DEPARTMENT OF CYBERSECURITY", font=f_univ, fill=(139, 148, 158))
    draw.text((65, 54), "WHID-GUARD  —  DUAL-MODE ESP32-S3 BADUSB & DEFENSE", font=f_proj, fill=(88, 166, 255))
    draw.text((65, 78), "Authors: Ram Karthik G (CH.SC.U4CYS23037) & Harini V (CH.SC.U4CYS23010)", font=f_auth, fill=(110, 118, 129))

    # Live indicator badge (pulsing red dot)
    pulse = (math.sin(elapsed_global * 4.0) + 1.0) / 2.0
    dot_r = int(200 + 55 * pulse)
    f_live = get_font(FONT_BOLD, 14)
    live_x = 1290
    draw_rounded_rect(draw, (live_x, 34, live_x + 195, 78), radius=8, fill=(26, 18, 20), outline=(248, 81, 73), width=1)
    draw.ellipse([live_x + 14, 50, live_x + 24, 60], fill=(dot_r, 40, 40))
    draw.text((live_x + 32, 47), "LIVE DEMO WORKING", font=f_live, fill=(248, 81, 73))

    # Scene pill
    f_badge = get_font(FONT_BOLD, 14)
    f_time = get_font(FONT_MONO, 14)
    scene_x = 1500
    draw_rounded_rect(draw, (scene_x, 34, scene_x + 165, 78), radius=8, fill=(33, 38, 45), outline=(56, 139, 253), width=1)
    draw.text((scene_x + 16, 47), f"SCENE {scene_idx:02d} / {total_scenes:02d}", font=f_badge, fill=(88, 166, 255))
    
    # Time pill
    mins = int(elapsed_global // 60)
    secs = int(elapsed_global % 60)
    tot_mins = int(dur_global // 60)
    tot_secs = int(dur_global % 60)
    draw_rounded_rect(draw, (1680, 34, 1855, 78), radius=8, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((1696, 47), f"{mins:02d}:{secs:02d} / {tot_mins:02d}:{tot_secs:02d}", font=f_time, fill=(63, 185, 80))

    # Subtitle placeholder bar
    draw_rounded_rect(draw, (40, 935, 1880, 1055), radius=12, fill=(13, 17, 23), outline=(48, 54, 61), width=1)

    # Global progress bar line
    draw.line([(0, 1076), (WIDTH, 1076)], fill=(22, 27, 34), width=4)
    progress_w = int(WIDTH * (elapsed_global / max(1.0, dur_global)))
    draw.line([(0, 1076), (progress_w, 1076)], fill=(88, 166, 255), width=4)

def draw_window_header(draw, bbox, title, is_active=True, icon_symbol="💻"):
    x0, y0, x1, y1 = bbox
    header_h = 34
    header_fill = (33, 38, 45) if is_active else (22, 27, 34)
    draw.rectangle([x0, y0, x1, y0 + header_h], fill=header_fill)
    
    f_title = get_font(FONT_BOLD, 13)
    draw.text((x0 + 12, y0 + 7), f"{icon_symbol}  {title}", font=f_title, fill=(240, 246, 252) if is_active else (139, 148, 158))
    
    draw.text((x1 - 80, y0 + 5), "—", font=f_title, fill=(139, 148, 158))
    draw.text((x1 - 50, y0 + 5), "□", font=f_title, fill=(139, 148, 158))
    draw.text((x1 - 22, y0 + 5), "✕", font=f_title, fill=(248, 81, 73) if is_active else (139, 148, 158))
    draw.line([(x0, y0 + header_h), (x1, y0 + header_h)], fill=(48, 54, 61), width=1)

def draw_desktop_taskbar(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(20, 25, 34))
    draw.line([(x0, y0), (x1, y0)], fill=(48, 54, 61), width=1)
    
    cx = (x0 + x1) // 2
    icons = ["🪟", "🔍", "📁", "💻", "📝", "🛡️"]
    for i, ic in enumerate(icons):
        ix = cx - 120 + i * 40
        f_ic = get_font(FONT_BOLD, 16)
        draw.text((ix, y0 + 6), ic, font=f_ic, fill=(200, 210, 225))
    
    f_tray = get_font(FONT_REG, 11)
    draw.text((x1 - 180, y0 + 10), "ENG  📶  🔊  12:00 PM", font=f_tray, fill=(139, 148, 158))

def draw_phone_frame(draw, x0, y0, x1, y1, active_tab="scenarios", touch_ripple=None):
    draw_rounded_rect(draw, (x0, y0, x1, y1), radius=30, fill=(20, 24, 32), outline=(56, 139, 253), width=2)
    sx0, sy0, sx1, sy1 = x0 + 12, y0 + 12, x1 - 12, y1 - 12
    draw_rounded_rect(draw, (sx0, sy0, sx1, sy1), radius=20, fill=(13, 17, 23), outline=(48, 54, 61), width=1)

    notch_w = 70
    cx = (sx0 + sx1) // 2
    draw_rounded_rect(draw, (cx - notch_w//2, sy0 + 6, cx + notch_w//2, sy0 + 18), radius=6, fill=(6, 9, 15))
    draw.ellipse([cx + 18, sy0 + 9, cx + 24, sy0 + 15], fill=(20, 35, 60))

    f_stat = get_font(FONT_REG, 11)
    f_mono = get_font(FONT_MONO, 11)
    draw.text((sx0 + 18, sy0 + 6), "12:00", font=f_stat, fill=(139, 148, 158))
    draw.text((sx1 - 90, sy0 + 6), "5G  📶  100%", font=f_mono, fill=(139, 148, 158))

    url_y0 = sy0 + 26
    url_y1 = url_y0 + 26
    draw_rounded_rect(draw, (sx0 + 12, url_y0, sx1 - 12, url_y1), radius=6, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    f_url = get_font(FONT_MONO, 11)
    draw.text((sx0 + 22, url_y0 + 5), "🔒 http://10.85.248.29", font=f_url, fill=(63, 185, 80))

    hdr_y0 = url_y1 + 8
    draw_rounded_rect(draw, (sx0 + 12, hdr_y0, sx1 - 12, hdr_y0 + 40), radius=8, fill=(18, 24, 38), outline=(56, 139, 253), width=1)
    f_whid = get_font(FONT_BOLD, 14)
    draw.text((sx0 + 22, hdr_y0 + 10), "WHID-Guard ESP32-S3", font=f_whid, fill=(240, 246, 252))
    
    draw_rounded_rect(draw, (sx1 - 105, hdr_y0 + 8, sx1 - 20, hdr_y0 + 32), radius=6, fill=(22, 38, 26), outline=(63, 185, 80), width=1)
    f_badge = get_font(FONT_BOLD, 10)
    draw.text((sx1 - 95, hdr_y0 + 12), "● ONLINE", font=f_badge, fill=(63, 185, 80))

    tab_y0 = hdr_y0 + 46
    tab_w = (sx1 - sx0 - 24) // 4
    tabs = [("scenarios", "Scenarios"), ("keyboard", "Keyboard"), ("mouse", "Mouse"), ("settings", "Settings")]
    for i, (tab_id, tab_label) in enumerate(tabs):
        tx0 = sx0 + 12 + i * tab_w
        tx1 = tx0 + tab_w - 3
        is_sel = (active_tab.lower() == tab_id.lower())
        t_fill = (33, 38, 45) if is_sel else (18, 22, 30)
        t_out = (56, 139, 253) if is_sel else (48, 54, 61)
        draw_rounded_rect(draw, (tx0, tab_y0, tx1, tab_y0 + 30), radius=6, fill=t_fill, outline=t_out, width=1)
        f_tab = get_font(FONT_BOLD if is_sel else FONT_REG, 11)
        txt_w = draw.textlength(tab_label, font=f_tab)
        draw.text((tx0 + (tab_w - txt_w)//2 - 1, tab_y0 + 7), tab_label, font=f_tab, fill=(88, 166, 255) if is_sel else (139, 148, 158))

    if touch_ripple:
        rx, ry, radius, intensity = touch_ripple
        draw.ellipse([rx - radius, ry - radius, rx + radius, ry + radius], outline=(56, 139, 253), width=3)
        draw.ellipse([rx - 6, ry - 6, rx + 6, ry + 6], fill=(88, 166, 255))

    return sx0 + 12, tab_y0 + 38, sx1 - 12, sy1 - 16

def paste_scaled_image(base_img, img_path, bbox):
    if not os.path.exists(img_path):
        return
    x0, y0, x1, y1 = bbox
    tw = x1 - x0
    th = y1 - y0
    try:
        with Image.open(img_path) as im:
            if im.mode != "RGB":
                im = im.convert("RGB")
            im.thumbnail((tw, th), Image.Resampling.LANCZOS)
            aw, ah = im.size
            ox = x0 + (tw - aw) // 2
            oy = y0 + (th - ah) // 2
            base_img.paste(im, (ox, oy))
    except Exception as e:
        print(f"Error pasting image {img_path}: {e}")

# ==========================================
# SCENE 1 RENDERER
# ==========================================
def render_frame_scene_1(t, dur, t_glob, dur_glob):
    img = Image.new("RGB", (WIDTH, HEIGHT), (11, 15, 25))
    draw = ImageDraw.Draw(img)
    draw_top_bar(draw, 1, 9, "Introduction & Architecture Overview", t, dur, t_glob, dur_glob)

    lx0, ly0, lx1, ly1 = 40, 110, 1280, 915
    draw_rounded_rect(draw, (lx0, ly0, lx1, ly1), radius=12, fill=(15, 20, 32), outline=(48, 54, 61), width=1)
    draw_desktop_taskbar(draw, lx0, ly1 - 38, lx1, ly1)

    wx0, wy0, wx1, wy1 = lx0 + 20, ly0 + 20, lx1 - 20, ly1 - 55
    draw_rounded_rect(draw, (wx0, wy0, wx1, wy1), radius=8, fill=(18, 24, 38), outline=(56, 139, 253), width=1)
    draw_window_header(draw, (wx0, wy0, wx1, wy1), "WHID-Guard System Architecture & Dual-Port Setup", True, "🛡️")

    diag_box = (wx0 + 15, wy0 + 45, wx0 + 720, wy1 - 15)
    draw_rounded_rect(draw, diag_box, radius=8, fill=(13, 17, 23), outline=(48, 54, 61), width=1)
    paste_scaled_image(img, "paper/fig1_system_architecture.png", (diag_box[0]+10, diag_box[1]+10, diag_box[2]-10, diag_box[3]-10))

    rx0, ry0, rx1, ry1 = wx0 + 740, wy0 + 45, wx1 - 15, wy1 - 15
    draw_rounded_rect(draw, (rx0, ry0, rx1, ry1), radius=8, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    f_h2 = get_font(FONT_BOLD, 16)
    f_body = get_font(FONT_REG, 13)
    f_mono = get_font(FONT_MONO, 12)
    
    draw.text((rx0 + 18, ry0 + 18), "PHYSICAL HARDWARE SPECS", font=f_h2, fill=(88, 166, 255))
    specs = [
        ("SoC Processor", "ESP32-S3 Dual-Core @ 240 MHz"),
        ("Native USB-OTG", "GPIO 19 (D-), GPIO 20 (D+)"),
        ("Host Enumeration", "Composite HID (Keyboard + Mouse)"),
        ("Flashing / Telemetry", "CP2102 UART Bridge on COM5"),
        ("Wireless Control", "Wi-Fi 802.11 b/g/n (SoftAP / STA)"),
        ("Security PIN", "badusb123 (Argon2 / SHA Token)"),
        ("Physical Advance", "GPIO 0 BOOT Button (50ms Debounce)"),
        ("Host Defense OS", "Microsoft Windows 11 Enterprise"),
        ("Detection API", "Windows Raw Input (WM_INPUT)"),
        ("Mitigation Hook", "WH_KEYBOARD_LL Selective Drop"),
    ]
    for idx, (k, v) in enumerate(specs):
        sy = ry0 + 55 + idx * 30
        draw.text((rx0 + 18, sy), k + ":", font=f_body, fill=(139, 148, 158))
        draw.text((rx0 + 195, sy), v, font=f_mono, fill=(240, 246, 252))

    px0, py0, px1, py1 = 1320, 110, 1880, 915
    cx0, cy0, cx1, cy1 = draw_phone_frame(draw, px0, py0, px1, py1, active_tab="scenarios")
    
    f_sc = get_font(FONT_BOLD, 13)
    f_desc = get_font(FONT_REG, 11)
    scenarios_list = [
        ("1. System Info Advisory", "Auto-run Notepad security notification"),
        ("2. Campus Portal Redirect", "Opens Amrita Intranet Login"),
        ("3. Simulated Ransomware", "PowerShell pop-up alert & note"),
        ("4. Wi-Fi Profile Recon", "CMD netsh wlan show profiles"),
    ]
    for idx, (title, desc) in enumerate(scenarios_list):
        sy = cy0 + 15 + idx * 75
        draw_rounded_rect(draw, (cx0 + 10, sy, cx1 - 10, sy + 65), radius=8, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
        draw.text((cx0 + 22, sy + 10), title, font=f_sc, fill=(240, 246, 252))
        draw.text((cx0 + 22, sy + 34), desc, font=f_desc, fill=(139, 148, 158))
        draw_rounded_rect(draw, (cx1 - 70, sy + 18, cx1 - 20, sy + 48), radius=6, fill=(33, 38, 45), outline=(56, 139, 253), width=1)
        draw.text((cx1 - 58, sy + 25), "RUN", font=f_sc, fill=(88, 166, 255))

    draw_rounded_rect(draw, (cx0 + 10, cy1 - 75, cx1 - 10, cy1 - 15), radius=8, fill=(50, 18, 20), outline=(248, 81, 73), width=2)
    f_em = get_font(FONT_BOLD, 14)
    draw.text((cx0 + 40, cy1 - 52), "🚨 EMERGENCY STOP (Release)", font=f_em, fill=(248, 81, 73))

    return img

# ==========================================
# SCENE 2 RENDERER
# ==========================================
def render_frame_scene_2(t, dur, t_glob, dur_glob):
    img = Image.new("RGB", (WIDTH, HEIGHT), (11, 15, 25))
    draw = ImageDraw.Draw(img)
    draw_top_bar(draw, 2, 9, "Live Demo 1: Auto-Run Notepad Injection", t, dur, t_glob, dur_glob)

    lx0, ly0, lx1, ly1 = 40, 110, 1280, 915
    draw_rounded_rect(draw, (lx0, ly0, lx1, ly1), radius=12, fill=(15, 20, 32), outline=(48, 54, 61), width=1)
    draw_desktop_taskbar(draw, lx0, ly1 - 38, lx1, ly1)

    if t < 8.0:
        tx0, ty0, tx1, ty1 = lx0 + 350, ly0 + 250, lx0 + 890, ly0 + 430
        draw_rounded_rect(draw, (tx0, ty0, tx1, ty1), radius=10, fill=(22, 27, 34), outline=(56, 139, 253), width=2)
        f_toast_h = get_font(FONT_BOLD, 18)
        f_toast_b = get_font(FONT_REG, 14)
        f_mono = get_font(FONT_MONO, 13)
        draw.text((tx0 + 25, ty0 + 20), "🔌 USB HID DEVICE DETECTED", font=f_toast_h, fill=(88, 166, 255))
        draw.text((tx0 + 25, ty0 + 55), "Device: ESP32-S3 Composite HID (Keyboard + Mouse)", font=f_toast_b, fill=(240, 246, 252))
        draw.text((tx0 + 25, ty0 + 85), "Hardware VID: 0x303A | PID: 0x1001 (Espressif)", font=f_mono, fill=(139, 148, 158))
        
        prog = min(1.0, t / 4.0)
        draw.text((tx0 + 25, ty0 + 120), f"Stabilization Delay: {min(3.5, t):.1f}s / 3.5s", font=f_mono, fill=(63, 185, 80))
        draw_rounded_rect(draw, (tx0 + 25, ty0 + 145, tx1 - 25, ty0 + 155), radius=4, fill=(13, 17, 23))
        draw_rounded_rect(draw, (tx0 + 25, ty0 + 145, tx0 + 25 + int((tx1 - tx0 - 50) * prog), ty0 + 155), radius=4, fill=(63, 185, 80))

    if 8.0 <= t < 15.0:
        rx0, ry0, rx1, ry1 = lx0 + 100, ly1 - 320, lx0 + 540, ly1 - 60
        draw_rounded_rect(draw, (rx0, ry0, rx1, ry1), radius=8, fill=(28, 33, 44), outline=(56, 139, 253), width=2)
        draw_window_header(draw, (rx0, ry0, rx1, ry1), "Run", True, "⚙️")
        f_lbl = get_font(FONT_REG, 13)
        f_inp = get_font(FONT_MONO, 14)
        draw.text((rx0 + 20, ry0 + 50), "Type the name of a program, folder, or document:", font=f_lbl, fill=(240, 246, 252))
        
        draw_rounded_rect(draw, (rx0 + 70, ry0 + 95, rx1 - 20, ry0 + 130), radius=4, fill=(13, 17, 23), outline=(56, 139, 253), width=1)
        draw.text((rx0 + 20, ry0 + 102), "Open:", font=f_lbl, fill=(139, 148, 158))
        
        typed_chars = min(7, int((t - 9.0) * 4)) if t > 9.0 else 0
        cmd_str = "notepad"[:typed_chars]
        cursor = "|" if int(t * 3) % 2 == 0 else ""
        draw.text((rx0 + 82, ry0 + 102), cmd_str + cursor, font=f_inp, fill=(240, 246, 252))
        
        draw_rounded_rect(draw, (rx1 - 180, ry1 - 45, rx1 - 105, ry1 - 15), radius=4, fill=(56, 139, 253) if t > 12.0 else (33, 38, 45))
        draw.text((rx1 - 155, ry1 - 38), "OK", font=f_lbl, fill=(255, 255, 255))
        draw_rounded_rect(draw, (rx1 - 95, ry1 - 45, rx1 - 20, ry1 - 15), radius=4, fill=(33, 38, 45))
        draw.text((rx1 - 80, ry1 - 38), "Cancel", font=f_lbl, fill=(139, 148, 158))

    if t >= 15.0:
        nx0, ny0, nx1, ny1 = lx0 + 50, ly0 + 35, lx1 - 50, ly1 - 65
        draw_rounded_rect(draw, (nx0, ny0, nx1, ny1), radius=8, fill=(18, 22, 30), outline=(56, 139, 253), width=2)
        draw_window_header(draw, (nx0, ny0, nx1, ny1), "*Untitled - Notepad", True, "📝")
        
        f_menu = get_font(FONT_REG, 12)
        draw.rectangle([nx0, ny0 + 35, nx1, ny0 + 60], fill=(22, 27, 34))
        draw.text((nx0 + 15, ny0 + 40), "File    Edit    View", font=f_menu, fill=(139, 148, 158))
        draw.line([(nx0, ny0 + 60), (nx1, ny0 + 60)], fill=(48, 54, 61), width=1)
        
        full_text = (
            "========================================================================\n"
            "       [SECURITY AWARENESS: BADUSB CYBER-PHYSICAL ATTACK DEMO]          \n"
            "========================================================================\n"
            "Platform: ESP32-S3 Dual-Core SoC @ 240 MHz (Native USB-OTG Full-Speed)  \n"
            "USB Vendor ID: 0x303A | Product ID: 0x1001 (Espressif Systems)         \n"
            "Injection Vector: Implicit Operating System Trust of USB HID Peripherals\n"
            "Scenario: Auto-Run Scenario 1 (Triggered without User Interaction)      \n"
            "Status: System Susceptible to Arbitrary Keystroke Injection!            \n"
            "Typing Rate: 100 keystrokes/sec (10ms Inter-Key Interval)               \n"
            "Host Mitigation: WHID-Guard Keystroke Dynamics Firewall Active          \n"
            "========================================================================"
        )
        elapsed_typing = t - 15.0
        num_chars = min(len(full_text), int(elapsed_typing * 28))
        displayed_text = full_text[:num_chars]
        cursor = " █" if int(t * 3) % 2 == 0 else ""
        
        f_note = get_font(FONT_MONO, 14)
        draw.text((nx0 + 20, ny0 + 75), displayed_text + cursor, font=f_note, fill=(240, 246, 252))

        ax0, ay0, ax1, ay1 = nx1 - 380, ny0 + 75, nx1 - 20, ny0 + 185
        draw_rounded_rect(draw, (ax0, ay0, ax1, ay1), radius=8, fill=(35, 18, 20), outline=(248, 81, 73), width=2)
        f_att_h = get_font(FONT_BOLD, 14)
        f_att_b = get_font(FONT_MONO, 12)
        draw.text((ax0 + 14, ay0 + 10), "⚠️ UNCONSTRAINED BADUSB INJECTION", font=f_att_h, fill=(248, 81, 73))
        draw.text((ax0 + 14, ay0 + 35), "Cadence: Deterministic (10ms IKI)", font=f_att_b, fill=(240, 246, 252))
        draw.text((ax0 + 14, ay0 + 58), "Typing Burst: 100.0 chars/sec", font=f_att_b, fill=(240, 246, 252))
        draw.text((ax0 + 14, ay0 + 81), "Variance CV: 0.038 (Rigid Machine)", font=f_att_b, fill=(248, 81, 73))

    px0, py0, px1, py1 = 1320, 110, 1880, 915
    cx0, cy0, cx1, cy1 = draw_phone_frame(draw, px0, py0, px1, py1, active_tab="scenarios")
    
    f_sc = get_font(FONT_BOLD, 13)
    f_desc = get_font(FONT_REG, 11)
    sy = cy0 + 15
    draw_rounded_rect(draw, (cx0 + 10, sy, cx1 - 10, sy + 75), radius=8, fill=(20, 35, 55), outline=(56, 139, 253), width=2)
    draw.text((cx0 + 22, sy + 12), "1. System Info Advisory", font=f_sc, fill=(88, 166, 255))
    draw.text((cx0 + 22, sy + 36), "Auto-run payload executing...", font=f_desc, fill=(240, 246, 252))
    draw_rounded_rect(draw, (cx1 - 95, sy + 18, cx1 - 20, sy + 48), radius=6, fill=(22, 38, 26), outline=(63, 185, 80), width=1)
    draw.text((cx1 - 85, sy + 25), "ACTIVE", font=f_sc, fill=(63, 185, 80))

    for idx, (title, desc) in enumerate([("2. Campus Portal Redirect", "Opens Amrita Intranet Login"), ("3. Simulated Ransomware", "PowerShell pop-up alert & note"), ("4. Wi-Fi Profile Recon", "CMD netsh wlan show profiles")], 1):
        oy = sy + idx * 85
        draw_rounded_rect(draw, (cx0 + 10, oy, cx1 - 10, oy + 70), radius=8, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
        draw.text((cx0 + 22, oy + 12), title, font=f_sc, fill=(139, 148, 158))
        draw.text((cx0 + 22, oy + 36), desc, font=f_desc, fill=(110, 118, 129))

    draw_rounded_rect(draw, (cx0 + 10, cy1 - 75, cx1 - 10, cy1 - 15), radius=8, fill=(50, 18, 20), outline=(248, 81, 73), width=2)
    f_em = get_font(FONT_BOLD, 14)
    draw.text((cx0 + 40, cy1 - 52), "🚨 EMERGENCY STOP (Release)", font=f_em, fill=(248, 81, 73))

    return img

# ==========================================
# SCENE 3 RENDERER
# ==========================================
def render_frame_scene_3(t, dur, t_glob, dur_glob):
    img = Image.new("RGB", (WIDTH, HEIGHT), (11, 15, 25))
    draw = ImageDraw.Draw(img)
    draw_top_bar(draw, 3, 9, "Live Demo 2: Phone UI & Physical Button Advancement", t, dur, t_glob, dur_glob)

    lx0, ly0, lx1, ly1 = 40, 110, 1280, 915
    draw_rounded_rect(draw, (lx0, ly0, lx1, ly1), radius=12, fill=(15, 20, 32), outline=(48, 54, 61), width=1)
    draw_desktop_taskbar(draw, lx0, ly1 - 38, lx1, ly1)

    wx0, wy0, wx1, wy1 = lx0 + 30, ly0 + 25, lx1 - 30, ly1 - 55
    draw_rounded_rect(draw, (wx0, wy0, wx1, wy1), radius=8, fill=(13, 17, 23), outline=(56, 139, 253), width=1)
    draw_window_header(draw, (wx0, wy0, wx1, wy1), "Windows Terminal — COM5 Serial Telemetry (115200 Baud)", True, "💻")

    f_mono = get_font(FONT_MONO, 13)
    logs = [
        "[12:00:01.042] [INIT] ESP32-S3 Dual-Core SoC 240MHz Booted (ESP-IDF v5.1)",
        "[12:00:01.215] [USB] Native USB-OTG Initialized on GPIO 19/20 (Full-Speed)",
        "[12:00:01.350] [USB] USB HID Keyboard & Mouse Descriptors Registered",
        "[12:00:02.100] [WIFI] SoftAP Active: SSID 'ESP32-BadUSB-AP' | IP: 192.168.4.1",
        "[12:00:02.105] [WIFI] Station Connected: IP '10.85.248.29'",
        "[12:00:04.410] [HTTP] Client connected from 10.85.248.15: GET /",
    ]
    if t >= 8.0:
        logs.append("[12:00:08.520] [AUTH] POST /api/auth (PIN: ****** ) -> VALID PIN")
        logs.append("[12:00:08.525] [AUTH] Session Token Issued: 0x8F9B2A1C (Role: Admin)")
    if t >= 18.0:
        logs.append("[12:00:18.102] [GPIO0] Physical BOOT Button Pressed (Debounce 50ms)")
        logs.append("[12:00:18.105] [FSM] Circular Sequence Advanced -> Scenario 2: Campus Portal Redirect")
    if t >= 24.0:
        logs.append("[12:00:24.085] [GPIO0] Physical BOOT Button Pressed (Debounce 50ms)")
        logs.append("[12:00:24.088] [FSM] Circular Sequence Advanced -> Scenario 3: Simulated Ransomware")
    if t >= 30.0:
        logs.append("[12:00:30.120] [GPIO0] Physical BOOT Button Pressed (Debounce 50ms)")
        logs.append("[12:00:30.124] [FSM] Circular Sequence Advanced -> Scenario 4: Wi-Fi Reconnaissance")
    if t >= 36.0:
        logs.append("[12:00:36.050] [GPIO0] Physical BOOT Button Pressed (Debounce 50ms)")
        logs.append("[12:00:36.054] [FSM] Circular Sequence Advanced -> Scenario 1: System Info Advisory")

    for i, line in enumerate(logs[-16:]):
        color = (63, 185, 80) if "[AUTH]" in line else ((88, 166, 255) if "[GPIO0]" in line else ((248, 81, 73) if "Scenario 3" in line else (200, 215, 230)))
        draw.text((wx0 + 20, wy0 + 50 + i * 26), line, font=f_mono, fill=color)

    px0, py0, px1, py1 = 1320, 110, 1880, 915
    active_tab = "settings" if t < 16.0 else "scenarios"
    
    ripple = None
    if 7.0 <= t < 9.0:
        prog = (t - 7.0) / 2.0
        ripple = (1600, 360, int(prog * 35), 1.0 - prog)

    cx0, cy0, cx1, cy1 = draw_phone_frame(draw, px0, py0, px1, py1, active_tab=active_tab, touch_ripple=ripple)

    if t < 16.0:
        f_h = get_font(FONT_BOLD, 15)
        f_lbl = get_font(FONT_REG, 12)
        f_val = get_font(FONT_MONO, 12)
        
        draw.text((cx0 + 15, cy0 + 15), "SECURITY & CREDENTIALS", font=f_h, fill=(88, 166, 255))
        
        draw_rounded_rect(draw, (cx0 + 15, cy0 + 45, cx1 - 15, cy0 + 85), radius=6, fill=(22, 27, 34), outline=(56, 139, 253), width=1)
        draw.text((cx0 + 25, cy0 + 56), "PIN:", font=f_lbl, fill=(139, 148, 158))
        draw.text((cx0 + 70, cy0 + 56), "● ● ● ● ● ● ● ●  (badusb123)", font=f_val, fill=(240, 246, 252))

        btn_fill = (22, 38, 26) if t >= 8.0 else (33, 38, 45)
        btn_out = (63, 185, 80) if t >= 8.0 else (56, 139, 253)
        draw_rounded_rect(draw, (cx0 + 15, cy0 + 100, cx1 - 15, cy0 + 140), radius=6, fill=btn_fill, outline=btn_out, width=1)
        btn_txt = "✓ AUTHENTICATED (ADMIN)" if t >= 8.0 else "AUTHENTICATE"
        draw.text((cx0 + 120, cy0 + 112), btn_txt, font=f_h, fill=(63, 185, 80) if t >= 8.0 else (88, 166, 255))

        draw_rounded_rect(draw, (cx0 + 15, cy0 + 160, cx1 - 15, cy0 + 380), radius=8, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
        draw.text((cx0 + 25, cy0 + 175), "SYSTEM TELEMETRY", font=f_h, fill=(240, 246, 252))
        info = [
            ("SoC Firmware", "WHID-Guard v2.4 (2027)"),
            ("Active Port", "USB-OTG Native HID"),
            ("Session Token", "0x8F9B2A1C" if t >= 8.0 else "None"),
            ("BOOT Switch", "GPIO 0 (Active LOW)"),
            ("Debounce Time", "50 milliseconds"),
            ("Current State", "AUTHENTICATED" if t >= 8.0 else "UNAUTHENTICATED"),
        ]
        for idx, (k, v) in enumerate(info):
            iy = cy0 + 210 + idx * 26
            draw.text((cx0 + 25, iy), k + ":", font=f_lbl, fill=(139, 148, 158))
            draw.text((cx0 + 140, iy), v, font=f_val, fill=(63, 185, 80) if "AUTH" in v or "8F9" in v else (240, 246, 252))
    else:
        active_scenario_num = 2 if t < 24.0 else (3 if t < 30.0 else (4 if t < 36.0 else 1))
        f_sc = get_font(FONT_BOLD, 13)
        f_desc = get_font(FONT_REG, 11)
        
        draw_rounded_rect(draw, (cx0 + 10, cy0 + 10, cx1 - 10, cy0 + 120), radius=8, fill=(20, 25, 35), outline=(56, 139, 253), width=1)
        draw.text((cx0 + 20, cy0 + 20), "ESP32-S3 PHYSICAL CONTROLS", font=f_sc, fill=(88, 166, 255))
        
        pulse_btn = (math.sin(t * 8.0) > 0.3)
        btn_col = (255, 200, 50) if pulse_btn else (88, 166, 255)
        draw_rounded_rect(draw, (cx0 + 25, cy0 + 50, cx0 + 150, cy0 + 100), radius=6, fill=(33, 38, 45), outline=btn_col, width=2)
        draw.text((cx0 + 38, cy0 + 68), "BOOT (GPIO 0)", font=get_font(FONT_BOLD, 12), fill=btn_col)
        draw.text((cx0 + 165, cy0 + 60), f"Cycle -> Scenario {active_scenario_num}", font=f_sc, fill=(63, 185, 80))
        draw.text((cx0 + 165, cy0 + 82), "Hardware Debounce: 50ms", font=f_desc, fill=(139, 148, 158))

        scenarios_meta = [
            (1, "1. System Info Advisory", "Notepad security alert"),
            (2, "2. Campus Portal Redirect", "Opens Amrita Intranet Login"),
            (3, "3. Simulated Ransomware", "PowerShell pop-up alert & note"),
            (4, "4. Wi-Fi Profile Recon", "CMD netsh wlan show profiles"),
        ]
        for sc_id, title, desc in scenarios_meta:
            sy = cy0 + 135 + (sc_id - 1) * 75
            is_active = (sc_id == active_scenario_num)
            fill_c = (20, 35, 55) if is_active else (22, 27, 34)
            out_c = (56, 139, 253) if is_active else (48, 54, 61)
            draw_rounded_rect(draw, (cx0 + 10, sy, cx1 - 10, sy + 68), radius=8, fill=fill_c, outline=out_c, width=2 if is_active else 1)
            draw.text((cx0 + 22, sy + 12), title, font=f_sc, fill=(240, 246, 252) if is_active else (139, 148, 158))
            draw.text((cx0 + 22, sy + 36), desc, font=f_desc, fill=(88, 166, 255) if is_active else (110, 118, 129))
            if is_active:
                draw_rounded_rect(draw, (cx1 - 95, sy + 18, cx1 - 20, sy + 48), radius=6, fill=(22, 38, 26), outline=(63, 185, 80), width=1)
                draw.text((cx1 - 85, sy + 25), "ACTIVE", font=f_sc, fill=(63, 185, 80))

    return img

# ==========================================
# SCENE 4 RENDERER
# ==========================================
def render_frame_scene_4(t, dur, t_glob, dur_glob):
    img = Image.new("RGB", (WIDTH, HEIGHT), (11, 15, 25))
    draw = ImageDraw.Draw(img)
    draw_top_bar(draw, 4, 9, "Live Demo 3: Remote Scenario Execution & Emergency Stop", t, dur, t_glob, dur_glob)

    lx0, ly0, lx1, ly1 = 40, 110, 1280, 915
    draw_rounded_rect(draw, (lx0, ly0, lx1, ly1), radius=12, fill=(15, 20, 32), outline=(48, 54, 61), width=1)
    draw_desktop_taskbar(draw, lx0, ly1 - 38, lx1, ly1)

    if t < 22.0:
        wx0, wy0, wx1, wy1 = lx0 + 40, ly0 + 30, lx1 - 40, ly1 - 60
        draw_rounded_rect(draw, (wx0, wy0, wx1, wy1), radius=8, fill=(12, 12, 16), outline=(56, 139, 253), width=2)
        draw_window_header(draw, (wx0, wy0, wx1, wy1), "Command Prompt — Administrator: C:\\Windows\\System32\\cmd.exe", True, "💻")
        
        f_mono = get_font(FONT_MONO, 14)
        cmd_lines = [
            "Microsoft Windows [Version 10.0.22631.4317]",
            "(c) Microsoft Corporation. All rights reserved.",
            "",
            "C:\\Windows\\System32> netsh wlan show profiles",
            "",
            "Profiles on interface Wi-Fi:",
            "Group policy profiles (read only)",
            "    ---------------------------------",
            "    <None>",
            "",
            "User profiles",
            "    -------------",
            "    All User Profile     : Campus-Secure-5G",
            "    All User Profile     : Lab-Research-WLAN",
            "    All User Profile     : WHID-Guard-TestNet",
            "    All User Profile     : Faculty-Guest-Access",
            "",
            "C:\\Windows\\System32> "
        ]
        num_lines = min(len(cmd_lines), int((t - 4.0) * 4)) if t > 4.0 else 3
        for i in range(num_lines):
            draw.text((wx0 + 20, wy0 + 48 + i * 24), cmd_lines[i], font=f_mono, fill=(240, 246, 252))

        draw_rounded_rect(draw, (wx1 - 420, wy0 + 48, wx1 - 20, wy0 + 130), radius=8, fill=(22, 27, 34), outline=(63, 185, 80), width=1)
        draw.text((wx1 - 400, wy0 + 62), "SCENARIO 4: RECONNAISSANCE", font=get_font(FONT_BOLD, 13), fill=(63, 185, 80))
        draw.text((wx1 - 400, wy0 + 88), "Enumerating saved wireless profiles", font=get_font(FONT_REG, 12), fill=(240, 246, 252))
    else:
        nx0, ny0, nx1, ny1 = lx0 + 50, ly0 + 40, lx1 - 50, ly1 - 70
        draw_rounded_rect(draw, (nx0, ny0, nx1, ny1), radius=8, fill=(20, 15, 20), outline=(248, 81, 73), width=2)
        draw_window_header(draw, (nx0, ny0, nx1, ny1), "CRITICAL ALERT - Ransomware Simulation", True, "⚠️")

        f_note = get_font(FONT_MONO, 14)
        if t < 28.0:
            text_r = (
                "[!] WARNING: SIMULATED RANSOMWARE PAYLOAD EXECUTING\n\n"
                "All personal workstation files have been encrypted using AES-256...\n"
                "Private decryption key held at remote server.\n"
                "Typing payload character-by-character...\n"
            )
            draw.text((nx0 + 25, ny0 + 60), text_r, font=f_note, fill=(248, 81, 73))
        else:
            text_h = (
                "[!] WARNING: SIMULATED RANSOMWARE PAYLOAD EXECUTING\n\n"
                "All personal workstation files have been encrypted using AES-256...\n"
                "Private decryption key held at remote server.\n"
                "Typing payload charac-- [HALTED BY EMERGENCY STOP]"
            )
            draw.text((nx0 + 25, ny0 + 60), text_h, font=f_note, fill=(139, 148, 158))

            bx0, by0, bx1, by1 = nx0 + 60, ny0 + 220, nx1 - 60, ny0 + 420
            draw_rounded_rect(draw, (bx0, by0, bx1, by1), radius=12, fill=(35, 18, 20), outline=(248, 81, 73), width=3)
            f_em_h = get_font(FONT_BOLD, 22)
            f_em_b = get_font(FONT_MONO, 15)
            draw.text((bx0 + 40, by0 + 30), "🛑 EMERGENCY STOP EXECUTED IN < 10 MS", font=f_em_h, fill=(248, 81, 73))
            draw.text((bx0 + 40, by0 + 80), "Firmware Command: Keyboard.releaseAll() & Mouse.releaseAll()", font=f_em_b, fill=(240, 246, 252))
            draw.text((bx0 + 40, by0 + 115), "HID Report: 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 (Zero Stuck Keys)", font=f_em_b, fill=(63, 185, 80))
            draw.text((bx0 + 40, by0 + 150), "Status: Keyboard Bus Reset | Payload Injection Aborted", font=f_em_b, fill=(88, 166, 255))

    px0, py0, px1, py1 = 1320, 110, 1880, 915
    ripple = None
    if 2.0 <= t < 4.0:
        ripple = (1600, 520, int((t - 2.0) * 35), 1.0)
    elif 22.0 <= t < 24.0:
        ripple = (1600, 440, int((t - 22.0) * 35), 1.0)
    elif 27.0 <= t < 29.0:
        ripple = (1600, 750, int((t - 27.0) * 45), 1.0)

    cx0, cy0, cx1, cy1 = draw_phone_frame(draw, px0, py0, px1, py1, active_tab="scenarios", touch_ripple=ripple)
    f_sc = get_font(FONT_BOLD, 13)
    f_desc = get_font(FONT_REG, 11)

    sc_items = [
        ("1. System Info Advisory", "Notepad security alert", False),
        ("2. Campus Portal Redirect", "Opens Amrita Intranet Login", False),
        ("3. Simulated Ransomware", "PowerShell pop-up alert & note", (22.0 <= t < 28.0)),
        ("4. Wi-Fi Profile Recon", "CMD netsh wlan show profiles", (t < 22.0)),
    ]
    for idx, (title, desc, is_act) in enumerate(sc_items):
        sy = cy0 + 15 + idx * 75
        fill_c = (20, 35, 55) if is_act else (22, 27, 34)
        out_c = (56, 139, 253) if is_act else (48, 54, 61)
        draw_rounded_rect(draw, (cx0 + 10, sy, cx1 - 10, sy + 65), radius=8, fill=fill_c, outline=out_c, width=2 if is_act else 1)
        draw.text((cx0 + 22, sy + 12), title, font=f_sc, fill=(240, 246, 252) if is_act else (139, 148, 158))
        draw.text((cx0 + 22, sy + 36), desc, font=f_desc, fill=(88, 166, 255) if is_act else (110, 118, 129))
        if is_act:
            draw_rounded_rect(draw, (cx1 - 95, sy + 18, cx1 - 20, sy + 48), radius=6, fill=(22, 38, 26), outline=(63, 185, 80), width=1)
            draw.text((cx1 - 85, sy + 25), "ACTIVE", font=f_sc, fill=(63, 185, 80))

    em_pulse = (t >= 28.0)
    draw_rounded_rect(draw, (cx0 + 10, cy1 - 75, cx1 - 10, cy1 - 15), radius=8, fill=(70, 20, 25) if em_pulse else (50, 18, 20), outline=(248, 81, 73), width=3 if em_pulse else 2)
    f_em = get_font(FONT_BOLD, 14)
    draw.text((cx0 + 40, cy1 - 52), "🚨 EMERGENCY STOP (Triggered!)" if em_pulse else "🚨 EMERGENCY STOP (Release)", font=f_em, fill=(248, 81, 73))

    return img

# ==========================================
# SCENE 5 RENDERER
# ==========================================
def render_frame_scene_5(t, dur, t_glob, dur_glob):
    img = Image.new("RGB", (WIDTH, HEIGHT), (11, 15, 25))
    draw = ImageDraw.Draw(img)
    draw_top_bar(draw, 5, 9, "Live Demo 4: Wireless Keyboard & Multi-Touch Trackpad Mouse", t, dur, t_glob, dur_glob)

    lx0, ly0, lx1, ly1 = 40, 110, 1280, 915
    draw_rounded_rect(draw, (lx0, ly0, lx1, ly1), radius=12, fill=(15, 20, 32), outline=(48, 54, 61), width=1)
    draw_desktop_taskbar(draw, lx0, ly1 - 38, lx1, ly1)

    nx0, ny0, nx1, ny1 = lx0 + 40, ly0 + 30, lx1 - 40, ly1 - 60
    draw_rounded_rect(draw, (nx0, ny0, nx1, ny1), radius=8, fill=(18, 24, 38), outline=(56, 139, 253), width=2)
    draw_window_header(draw, (nx0, ny0, nx1, ny1), "*Remote Input Capture - Notepad", True, "📝")

    f_note = get_font(FONT_MONO, 14)
    text_phone = (
        "------------------------------------------------------------------------\n"
        "WHID-GUARD REMOTE SMARTPHONE PERIPHERAL DEMONSTRATION                   \n"
        "------------------------------------------------------------------------\n\n"
        "> Testing wireless keyboard input from phone browser...\n"
        "> Typing: 'Hello from Amrita Cybersecurity Research Lab!'\n"
        "> Hardware Modifier Latches: CTRL [ON], WIN [ON]\n"
        "> Text Transmitter Buffer: 256 bytes PROGMEM queue\n\n"
        "> Testing 60Hz virtual trackpad relative mouse nudging...\n"
        "> Packet stream active: 8-bit signed delta coordinates (dX, dY)\n"
    )
    chars = min(len(text_phone), int(t * 30))
    cursor = " █" if int(t * 3) % 2 == 0 else ""
    draw.text((nx0 + 25, ny0 + 55), text_phone[:chars] + cursor, font=f_note, fill=(240, 246, 252))

    if t >= 16.0:
        mt = t - 16.0
        cur_x = int(lx0 + 400 + 250 * math.cos(mt * 1.5))
        cur_y = int(ly0 + 450 + 140 * math.sin(mt * 3.0))
        
        draw.polygon([(cur_x, cur_y), (cur_x + 18, cur_y + 12), (cur_x + 11, cur_y + 13), (cur_x + 16, cur_y + 24), (cur_x + 12, cur_y + 26), (cur_x + 7, cur_y + 15), (cur_x, cur_y + 20)], fill=(255, 255, 255), outline=(0, 0, 0))
        
        draw_rounded_rect(draw, (cur_x + 24, cur_y - 20, cur_x + 260, cur_y + 18), radius=6, fill=(22, 27, 34), outline=(56, 139, 253), width=1)
        f_coord = get_font(FONT_MONO, 11)
        dx = int(12 * math.cos(mt * 1.5))
        dy = int(10 * math.sin(mt * 3.0))
        draw.text((cur_x + 32, cur_y - 12), f"Cursor: ({cur_x}, {cur_y}) | Δ: ({dx:+d}, {dy:+d})", font=f_coord, fill=(63, 185, 80))

    px0, py0, px1, py1 = 1320, 110, 1880, 915
    active_tab = "keyboard" if t < 16.0 else "mouse"
    cx0, cy0, cx1, cy1 = draw_phone_frame(draw, px0, py0, px1, py1, active_tab=active_tab)

    if t < 16.0:
        f_k_h = get_font(FONT_BOLD, 13)
        draw.text((cx0 + 15, cy0 + 12), "VIRTUAL 6-ROW QWERTY KEYBOARD", font=f_k_h, fill=(88, 166, 255))
        
        draw_rounded_rect(draw, (cx0 + 15, cy0 + 35, cx1 - 15, cy0 + 75), radius=6, fill=(22, 27, 34), outline=(56, 139, 253), width=1)
        draw.text((cx0 + 25, cy0 + 46), "Hello from Amrita Cybersecurity!", font=get_font(FONT_MONO, 12), fill=(240, 246, 252))

        mods = [("CTRL", True), ("ALT", False), ("WIN", True), ("SHIFT", False)]
        mw = (cx1 - cx0 - 30) // 4
        for i, (m_txt, m_on) in enumerate(mods):
            mx = cx0 + 15 + i * mw
            draw_rounded_rect(draw, (mx, cy0 + 90, mx + mw - 6, cy0 + 125), radius=6, fill=(20, 35, 55) if m_on else (22, 27, 34), outline=(56, 139, 253) if m_on else (48, 54, 61), width=1)
            draw.text((mx + 12, cy0 + 98), m_txt, font=get_font(FONT_BOLD, 11), fill=(88, 166, 255) if m_on else (139, 148, 158))

        rows = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "ENTER"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "BKSP"],
        ]
        for r_idx, row in enumerate(rows):
            kw = (cx1 - cx0 - 20) // len(row)
            for c_idx, key in enumerate(row):
                kx = cx0 + 10 + c_idx * kw
                ky = cy0 + 140 + r_idx * 40
                draw_rounded_rect(draw, (kx, ky, kx + kw - 3, ky + 34), radius=4, fill=(28, 33, 44), outline=(48, 54, 61), width=1)
                draw.text((kx + 6, ky + 8), key, font=get_font(FONT_BOLD, 10), fill=(240, 246, 252))

        draw_rounded_rect(draw, (cx0 + 15, cy0 + 280, cx1 - 15, cy0 + 320), radius=6, fill=(22, 38, 26), outline=(63, 185, 80), width=1)
        draw.text((cx0 + 120, cy0 + 292), "SEND TEXT STREAM", font=f_k_h, fill=(63, 185, 80))
    else:
        f_m_h = get_font(FONT_BOLD, 13)
        draw.text((cx0 + 15, cy0 + 12), "60Hz VIRTUAL MULTI-TOUCH TRACKPAD", font=f_m_h, fill=(88, 166, 255))
        
        tx0, ty0, tx1, ty1 = cx0 + 15, cy0 + 38, cx1 - 15, cy1 - 90
        draw_rounded_rect(draw, (tx0, ty0, tx1, ty1), radius=10, fill=(18, 24, 38), outline=(56, 139, 253), width=2)
        
        draw.line([((tx0 + tx1)//2, ty0 + 20), ((tx0 + tx1)//2, ty1 - 20)], fill=(28, 35, 50), width=1)
        draw.line([(tx0 + 20, (ty0 + ty1)//2), (tx1 - 20, (ty0 + ty1)//2)], fill=(28, 35, 50), width=1)
        
        mt = t - 16.0
        fx = int((tx0 + tx1)//2 + 90 * math.cos(mt * 1.5))
        fy = int((ty0 + ty1)//2 + 70 * math.sin(mt * 3.0))
        draw.ellipse([fx - 18, fy - 18, fx + 18, fy + 18], fill=(35, 60, 95), outline=(88, 166, 255), width=2)
        draw.ellipse([fx - 6, fy - 6, fx + 6, fy + 6], fill=(88, 166, 255))
        draw.text((fx + 22, fy - 10), "Touch Point", font=get_font(FONT_REG, 10), fill=(88, 166, 255))

        bw = (cx1 - cx0 - 36) // 2
        draw_rounded_rect(draw, (cx0 + 15, cy1 - 75, cx0 + 15 + bw, cy1 - 25), radius=6, fill=(28, 33, 44), outline=(48, 54, 61), width=1)
        draw.text((cx0 + 45, cy1 - 58), "LEFT CLICK", font=f_m_h, fill=(240, 246, 252))
        
        draw_rounded_rect(draw, (cx0 + 21 + bw, cy1 - 75, cx1 - 15, cy1 - 25), radius=6, fill=(28, 33, 44), outline=(48, 54, 61), width=1)
        draw.text((cx0 + 50 + bw, cy1 - 58), "RIGHT CLICK", font=f_m_h, fill=(240, 246, 252))

    return img

# ==========================================
# SCENE 6 RENDERER
# ==========================================
def render_frame_scene_6(t, dur, t_glob, dur_glob):
    img = Image.new("RGB", (WIDTH, HEIGHT), (11, 15, 25))
    draw = ImageDraw.Draw(img)
    draw_top_bar(draw, 6, 9, "Live Demo 5: Adversarial Evasion & Cadence Jitter", t, dur, t_glob, dur_glob)

    lx0, ly0, lx1, ly1 = 40, 110, 1280, 915
    draw_rounded_rect(draw, (lx0, ly0, lx1, ly1), radius=12, fill=(15, 20, 32), outline=(48, 54, 61), width=1)
    draw_desktop_taskbar(draw, lx0, ly1 - 38, lx1, ly1)

    wx0, wy0, wx1, wy1 = lx0 + 30, ly0 + 25, lx1 - 30, ly1 - 55
    draw_rounded_rect(draw, (wx0, wy0, wx1, wy1), radius=8, fill=(18, 24, 38), outline=(56, 139, 253), width=2)
    draw_window_header(draw, (wx0, wy0, wx1, wy1), "Keystroke Timing Analysis & Cadence Comparison", True, "📊")

    f_h2 = get_font(FONT_BOLD, 15)
    f_sub = get_font(FONT_REG, 12)
    f_mono = get_font(FONT_MONO, 12)

    g1_y0 = wy0 + 45
    draw_rounded_rect(draw, (wx0 + 20, g1_y0, wx1 - 20, g1_y0 + 175), radius=8, fill=(13, 17, 23), outline=(248, 81, 73), width=1)
    draw.text((wx0 + 35, g1_y0 + 12), "1. STANDARD MACHINE BADUSB INJECTION (RIGID 10ms CADENCE)", font=f_h2, fill=(248, 81, 73))
    draw.text((wx0 + 35, g1_y0 + 34), "Parameters: Δt = 10ms constant | σ = 0.4ms | CV = 0.040 (Predictable Robotic)", font=f_sub, fill=(139, 148, 158))
    
    for i in range(28):
        px = wx0 + 45 + i * 40
        draw.line([(px, g1_y0 + 150), (px, g1_y0 + 75)], fill=(248, 81, 73), width=3)
        draw.line([(px, g1_y0 + 75), (px + 10, g1_y0 + 75)], fill=(248, 81, 73), width=3)
        draw.line([(px + 10, g1_y0 + 75), (px + 10, g1_y0 + 150)], fill=(248, 81, 73), width=3)
        draw.line([(px + 10, g1_y0 + 150), (px + 40, g1_y0 + 150)], fill=(139, 148, 158), width=1)

    draw_rounded_rect(draw, (wx1 - 240, g1_y0 + 15, wx1 - 35, g1_y0 + 55), radius=6, fill=(35, 18, 20), outline=(248, 81, 73), width=1)
    draw.text((wx1 - 225, g1_y0 + 25), "TRIPS DEFENSE: FAST", font=f_h2, fill=(248, 81, 73))

    g2_y0 = g1_y0 + 195
    draw_rounded_rect(draw, (wx0 + 20, g2_y0, wx1 - 20, g2_y0 + 210), radius=8, fill=(13, 17, 23), outline=(63, 185, 80), width=1)
    draw.text((wx0 + 35, g2_y0 + 12), "2. ADVERSARIAL STEALTH MODE (STOCHASTIC JITTER & COGNITIVE PAUSES)", font=f_h2, fill=(63, 185, 80))
    draw.text((wx0 + 35, g2_y0 + 34), "Parameters: Δt = 80 ± 40ms normal | Micro-pauses: 150-300ms | CV = 0.420 (Human-Like)", font=f_sub, fill=(139, 148, 158))

    delays = [30, 45, 25, 75, 35, 110, 40, 25, 85, 30, 140, 35, 50, 25, 90, 40]
    cur_x = wx0 + 45
    for idx, d in enumerate(delays):
        if cur_x + d + 15 > wx1 - 50:
            break
        draw.line([(cur_x, g2_y0 + 180), (cur_x, g2_y0 + 85)], fill=(63, 185, 80), width=3)
        draw.line([(cur_x, g2_y0 + 85), (cur_x + 12, g2_y0 + 85)], fill=(63, 185, 80), width=3)
        draw.line([(cur_x + 12, g2_y0 + 85), (cur_x + 12, g2_y0 + 180)], fill=(63, 185, 80), width=3)
        draw.line([(cur_x + 12, g2_y0 + 180), (cur_x + d, g2_y0 + 180)], fill=(139, 148, 158), width=1)
        if d > 100:
            draw.text((cur_x + 20, g2_y0 + 155), "Cognitive Pause (250ms)", font=get_font(FONT_REG, 10), fill=(88, 166, 255))
        cur_x += d

    draw_rounded_rect(draw, (wx1 - 260, g2_y0 + 15, wx1 - 35, g2_y0 + 55), radius=6, fill=(22, 38, 26), outline=(63, 185, 80), width=1)
    draw.text((wx1 - 245, g2_y0 + 25), "EMULATES HUMAN CV", font=f_h2, fill=(63, 185, 80))

    px0, py0, px1, py1 = 1320, 110, 1880, 915
    ripple = None
    if 5.0 <= t < 7.0:
        ripple = (1750, 480, int((t - 5.0) * 35), 1.0)

    cx0, cy0, cx1, cy1 = draw_phone_frame(draw, px0, py0, px1, py1, active_tab="scenarios", touch_ripple=ripple)

    f_sc = get_font(FONT_BOLD, 13)
    f_desc = get_font(FONT_REG, 11)
    
    ey0 = cy0 + 20
    is_on = (t >= 6.0)
    draw_rounded_rect(draw, (cx0 + 10, ey0, cx1 - 10, ey0 + 150), radius=10, fill=(20, 35, 55) if is_on else (22, 27, 34), outline=(63, 185, 80) if is_on else (48, 54, 61), width=2)
    draw.text((cx0 + 22, ey0 + 16), "ADVERSARIAL EVASION MODE", font=f_sc, fill=(63, 185, 80) if is_on else (240, 246, 252))
    draw.text((cx0 + 22, ey0 + 40), "Emulate human cognitive cadences", font=f_desc, fill=(139, 148, 158))
    
    sw_x0 = cx1 - 90
    sw_y0 = ey0 + 20
    draw_rounded_rect(draw, (sw_x0, sw_y0, sw_x0 + 60, sw_y0 + 28), radius=14, fill=(63, 185, 80) if is_on else (48, 54, 61))
    circle_x = sw_x0 + 46 if is_on else sw_x0 + 14
    draw.ellipse([circle_x - 10, sw_y0 + 4, circle_x + 10, sw_y0 + 24], fill=(255, 255, 255))
    
    draw.text((cx0 + 22, ey0 + 72), "• Base Delay: 80 ms (Randomized Normal)", font=f_mono, fill=(240, 246, 252))
    draw.text((cx0 + 22, ey0 + 96), "• Stochastic Jitter: ±40 ms Range", font=f_mono, fill=(240, 246, 252))
    draw.text((cx0 + 22, ey0 + 120), "• Cognitive Micro-Pauses: 150-300 ms", font=f_mono, fill=(88, 166, 255))

    for idx, (title, desc) in enumerate([("1. System Info Advisory", "Notepad security alert"), ("2. Campus Portal Redirect", "Opens Amrita Intranet Login"), ("3. Simulated Ransomware", "PowerShell pop-up alert & note")], 1):
        sy = ey0 + 165 + (idx - 1) * 75
        draw_rounded_rect(draw, (cx0 + 10, sy, cx1 - 10, sy + 65), radius=8, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
        draw.text((cx0 + 22, sy + 12), title, font=f_sc, fill=(139, 148, 158))
        draw.text((cx0 + 22, sy + 36), desc, font=f_desc, fill=(110, 118, 129))

    return img

# ==========================================
# SCENE 7 RENDERER
# ==========================================
def render_frame_scene_7(t, dur, t_glob, dur_glob):
    img = Image.new("RGB", (WIDTH, HEIGHT), (11, 15, 25))
    draw = ImageDraw.Draw(img)
    draw_top_bar(draw, 7, 9, "Live Demo 6: WHID-Guard Host Defense in Action", t, dur, t_glob, dur_glob)

    lx0, ly0, lx1, ly1 = 40, 110, 1280, 915
    draw_rounded_rect(draw, (lx0, ly0, lx1, ly1), radius=12, fill=(15, 20, 32), outline=(48, 54, 61), width=1)
    draw_desktop_taskbar(draw, lx0, ly1 - 38, lx1, ly1)

    is_attack = (t >= 16.0)
    is_locked = (t >= 22.0)
    has_laptop_typing = (t >= 36.0)

    fx0, fy0, fx1, fy1 = lx0 + 20, ly0 + 20, lx0 + 680, ly1 - 50
    draw_rounded_rect(draw, (fx0, fy0, fx1, fy1), radius=8, fill=(18, 24, 38), outline=(248, 81, 73) if is_locked else (56, 139, 253), width=2)
    draw_window_header(draw, (fx0, fy0, fx1, fy1), "WHID-Guard: USB Keystroke Firewall", True, "🛡️")

    f_fh = get_font(FONT_BOLD, 14)
    f_fb = get_font(FONT_REG, 12)
    f_fm = get_font(FONT_MONO, 12)
    f_stat = get_font(FONT_BOLD, 18)

    stat_col = (248, 81, 73) if is_locked else ((210, 153, 34) if is_attack else (63, 185, 80))
    stat_txt = "STATUS: LOCKED DOWN (QUARANTINED)" if is_locked else ("STATUS: ANALYZING INJECTION BURST" if is_attack else "STATUS: ARMED (BLOCKING MODE)")
    draw_rounded_rect(draw, (fx0 + 15, fy0 + 45, fx1 - 15, fy0 + 105), radius=8, fill=(35, 18, 20) if is_locked else ((35, 30, 18) if is_attack else (22, 38, 26)), outline=stat_col, width=2)
    draw.text((fx0 + 30, fy0 + 62), stat_txt, font=f_stat, fill=stat_col)

    draw_rounded_rect(draw, (fx0 + 15, fy0 + 118, fx1 - 15, fy0 + 340), radius=8, fill=(13, 17, 23), outline=(48, 54, 61), width=1)
    draw.text((fx0 + 25, fy0 + 130), "PER-DEVICE BEHAVIORAL TELEMETRY", font=f_fh, fill=(88, 166, 255))
    
    mean_iki = "15.8 ms" if is_attack else "142.5 ms"
    cv_val = "0.068 (Robotic)" if is_attack else "0.382 (Human)"
    speed = "63.3 chars/s" if is_attack else "5.2 chars/s"
    t_rows = [
        ("Monitored Device", "ESP32-S3 USB Composite HID"),
        ("Hardware Handle", "hDevice: 0x000E2B80 (RawInput)"),
        ("USB VID / PID", "VID: 0x303A | PID: 0x1001 (Espressif)"),
        ("Inter-Key Interval (μ)", mean_iki),
        ("Cadence Variance (CV)", cv_val),
        ("Instantaneous Speed", speed),
        ("Detection Latency", "8 keystrokes / 84 ms" if is_locked else "Monitoring (W = 10)"),
        ("Selective Suppression", "WH_KEYBOARD_LL Packet Drop" if is_locked else "Pass-Through Active"),
    ]
    for idx, (k, v) in enumerate(t_rows):
        ty = fy0 + 160 + idx * 21
        draw.text((fx0 + 25, ty), k + ":", font=f_fb, fill=(139, 148, 158))
        draw.text((fx0 + 210, ty), v, font=f_fm, fill=(248, 81, 73) if ("Robotic" in v or "84 ms" in v) else (240, 246, 252))

    draw_rounded_rect(draw, (fx0 + 15, fy0 + 355, fx1 - 15, fy1 - 15), radius=8, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
    draw.text((fx0 + 25, fy0 + 368), "SELECTIVE DEVICE ATTRIBUTION AUDIT", font=f_fh, fill=(240, 246, 252))
    
    draw_rounded_rect(draw, (fx0 + 25, fy0 + 398, fx1 - 25, fy0 + 450), radius=6, fill=(35, 18, 20) if is_locked else (22, 27, 34), outline=(248, 81, 73) if is_locked else (48, 54, 61), width=1)
    draw.text((fx0 + 35, fy0 + 412), "ESP32-S3 (0x000E2B80):", font=f_fh, fill=(248, 81, 73) if is_locked else (139, 148, 158))
    draw.text((fx0 + 240, fy0 + 414), "BLOCKED (128 / 128 Dropped)" if is_locked else "MONITORING...", font=f_fm, fill=(248, 81, 73) if is_locked else (139, 148, 158))

    draw_rounded_rect(draw, (fx0 + 25, fy0 + 460, fx1 - 25, fy0 + 512), radius=6, fill=(22, 38, 26) if has_laptop_typing else (22, 27, 34), outline=(63, 185, 80) if has_laptop_typing else (48, 54, 61), width=1)
    draw.text((fx0 + 35, fy0 + 474), "Internal KB (0x00021A40):", font=f_fh, fill=(63, 185, 80) if has_laptop_typing else (139, 148, 158))
    draw.text((fx0 + 240, fy0 + 476), "AUTHORIZED (100% Passthrough)" if has_laptop_typing else "READY (Pass-Through)", font=f_fm, fill=(63, 185, 80) if has_laptop_typing else (139, 148, 158))

    nox0, noy0, nox1, noy1 = lx0 + 695, ly0 + 20, lx1 - 20, ly1 - 50
    draw_rounded_rect(draw, (nox0, noy0, nox1, noy1), radius=8, fill=(18, 24, 38), outline=(56, 139, 253), width=2)
    draw_window_header(draw, (nox0, noy0, nox1, noy1), "Untitled - Notepad (Target App)", True, "📝")

    f_np = get_font(FONT_MONO, 14)
    if is_locked and not has_laptop_typing:
        draw.text((nox0 + 25, noy0 + 60), "[Notepad is completely blank]\n\nZero BadUSB keystrokes reached this window!\nAll 128 malicious keystrokes were dropped\nby WHID-Guard's low-level keyboard hook.", font=f_np, fill=(139, 148, 158))
        draw_rounded_rect(draw, (nox0 + 25, noy0 + 220, nox1 - 25, noy0 + 320), radius=8, fill=(22, 38, 26), outline=(63, 185, 80), width=2)
        draw.text((nox0 + 45, noy0 + 245), "✓ ATTACK NEUTRALIZED", font=f_stat, fill=(63, 185, 80))
        draw.text((nox0 + 45, noy0 + 280), "Execution halted before payload completed.", font=f_fb, fill=(240, 246, 252))
    elif has_laptop_typing:
        lt_text = (
            "Testing user laptop keyboard:\n\n"
            "Typing normally from laptop internal keyboard...\n"
            "Notice how legitimate human typing is completely\n"
            "unrestricted and responsive!\n\n"
            "WHID-Guard selective per-device defense successfully\n"
            "quarantines only the malicious ESP32 hardware handle\n"
            "while preserving full access for the user."
        )
        cur_chars = min(len(lt_text), int((t - 36.0) * 25))
        cursor = " █" if int(t * 3) % 2 == 0 else ""
        draw.text((nox0 + 25, noy0 + 60), lt_text[:cur_chars] + cursor, font=f_np, fill=(240, 246, 252))
    else:
        draw.text((nox0 + 25, noy0 + 60), "Notepad waiting for input...", font=f_np, fill=(110, 118, 129))

    px0, py0, px1, py1 = 1320, 110, 1880, 915
    ripple = None
    if 14.0 <= t < 16.0:
        ripple = (1600, 280, int((t - 14.0) * 35), 1.0)

    cx0, cy0, cx1, cy1 = draw_phone_frame(draw, px0, py0, px1, py1, active_tab="scenarios", touch_ripple=ripple)
    
    f_sc = get_font(FONT_BOLD, 13)
    f_desc = get_font(FONT_REG, 11)
    
    sy = cy0 + 15
    draw_rounded_rect(draw, (cx0 + 10, sy, cx1 - 10, sy + 75), radius=8, fill=(20, 35, 55) if is_attack else (22, 27, 34), outline=(56, 139, 253) if is_attack else (48, 54, 61), width=2 if is_attack else 1)
    draw.text((cx0 + 22, sy + 12), "1. System Info Advisory", font=f_sc, fill=(240, 246, 252))
    draw.text((cx0 + 22, sy + 36), "Triggered injection attack...", font=f_desc, fill=(88, 166, 255) if is_attack else (139, 148, 158))
    
    if is_locked:
        draw_rounded_rect(draw, (cx0 + 10, cy0 + 110, cx1 - 10, cy0 + 220), radius=8, fill=(35, 18, 20), outline=(248, 81, 73), width=2)
        draw.text((cx0 + 20, cy0 + 125), "⚠️ HOST DEFENSE INTERVENTION", font=f_sc, fill=(248, 81, 73))
        draw.text((cx0 + 20, cy0 + 155), "Host Firewall: WHID-Guard", font=f_desc, fill=(240, 246, 252))
        draw.text((cx0 + 20, cy0 + 180), "Action: Selective Port Suppression Active", font=f_desc, fill=(248, 81, 73))

    return img

# ==========================================
# SCENE 8 RENDERER
# ==========================================
def render_frame_scene_8(t, dur, t_glob, dur_glob):
    img = Image.new("RGB", (WIDTH, HEIGHT), (11, 15, 25))
    draw = ImageDraw.Draw(img)
    draw_top_bar(draw, 8, 9, "Quantitative Empirical Benchmark Evaluation", t, dur, t_glob, dur_glob)

    bx0, by0, bx1, by1 = 40, 110, 1880, 915
    draw_rounded_rect(draw, (bx0, by0, bx1, by1), radius=12, fill=(15, 20, 32), outline=(48, 54, 61), width=1)

    tx0, ty0, tx1, ty1 = bx0 + 25, by0 + 25, bx0 + 880, by1 - 25
    draw_rounded_rect(draw, (tx0, ty0, tx1, ty1), radius=10, fill=(18, 24, 38), outline=(56, 139, 253), width=2)
    f_th = get_font(FONT_BOLD, 18)
    f_tb_h = get_font(FONT_BOLD, 13)
    f_tb = get_font(FONT_REG, 13)
    f_mono = get_font(FONT_MONO, 12)

    draw.text((tx0 + 25, ty0 + 20), "EMPIRICAL BENCHMARK EVALUATION (N = 1,500 STROKES)", font=f_th, fill=(88, 166, 255))

    headers = [("Metric", 220), ("Human Baseline", 180), ("Standard BadUSB", 190), ("Adversarial Evasion", 190)]
    hx = tx0 + 25
    for title, width in headers:
        draw.text((hx, ty0 + 65), title, font=f_tb_h, fill=(139, 148, 158))
        hx += width
    draw.line([(tx0 + 20, ty0 + 95), (tx1 - 20, ty0 + 95)], fill=(48, 54, 61), width=1)

    data = [
        ("Total Keystrokes", "500 keys", "500 keys", "500 keys"),
        ("Mean IKI (μ)", "148.6 ms", "15.9 ms", "82.4 ms"),
        ("Std Deviation (σ)", "61.2 ms", "1.1 ms", "32.1 ms"),
        ("Coefficient of Var (CV)", "0.412 (High)", "0.068 (Near-Zero)", "0.389 (Emulated)"),
        ("Burst Typing Rate", "6.7 chars/sec", "63.0 chars/sec", "12.1 chars/sec"),
        ("Detection Latency", "N/A (0% FPR)", "8 keys (84 ms)", "12 keys (145 ms)"),
        ("False Positive Rate", "0.0% (Zero alarms)", "—", "—"),
        ("True Positive Rate", "—", "98.6% Quarantined", "25.2% Flagged Suspicious"),
        ("Host Protection", "100% Passthrough", "100% Suppressed", "Quarantined on Anomaly"),
    ]
    for row_idx, row in enumerate(data):
        ry = ty0 + 115 + row_idx * 48
        if row_idx % 2 == 1:
            draw.rectangle([tx0 + 20, ry - 6, tx1 - 20, ry + 36], fill=(22, 27, 34))
        rx = tx0 + 25
        for col_idx, cell in enumerate(row):
            w = headers[col_idx][1]
            col = (240, 246, 252)
            if col_idx == 1 and "0.0%" in cell:
                col = (63, 185, 80)
            elif col_idx == 2 and ("98.6%" in cell or "8 keys" in cell or "100%" in cell):
                col = (63, 185, 80)
            elif col_idx == 3 and "Flagged" in cell:
                col = (210, 153, 34)
            draw.text((rx, ry), cell, font=f_mono if col_idx > 0 else f_tb, fill=col)
            rx += w

    fx0, fy0, fx1, fy1 = bx0 + 915, by0 + 25, bx1 - 25, by0 + 365
    draw_rounded_rect(draw, (fx0, fy0, fx1, fy1), radius=10, fill=(18, 24, 38), outline=(56, 139, 253), width=1)
    draw.text((fx0 + 20, fy0 + 15), "FIGURE 4: INTER-KEY INTERVAL (IKI) DISTRIBUTIONS", font=f_tb_h, fill=(88, 166, 255))
    paste_scaled_image(img, "paper/fig_iki_distribution.png", (fx0 + 15, fy0 + 40, fx1 - 15, fy1 - 15))

    gx0, gy0, gx1, gy1 = bx0 + 915, by0 + 385, bx1 - 25, by1 - 25
    draw_rounded_rect(draw, (gx0, gy0, gx1, gy1), radius=10, fill=(18, 24, 38), outline=(56, 139, 253), width=1)
    draw.text((gx0 + 20, gy0 + 15), "FIGURE 5: DETECTION LATENCY VS. BURST INJECTION RATE", font=f_tb_h, fill=(88, 166, 255))
    paste_scaled_image(img, "paper/fig_detection_latency.png", (gx0 + 15, gy0 + 40, gx1 - 15, gy1 - 15))

    return img

# ==========================================
# SCENE 9 RENDERER
# ==========================================
def render_frame_scene_9(t, dur, t_glob, dur_glob):
    img = Image.new("RGB", (WIDTH, HEIGHT), (11, 15, 25))
    draw = ImageDraw.Draw(img)
    draw_top_bar(draw, 9, 9, "Conclusion, IEEE Publication & Open-Source Release", t, dur, t_glob, dur_glob)

    bx0, by0, bx1, by1 = 40, 110, 1880, 915
    draw_rounded_rect(draw, (bx0, by0, bx1, by1), radius=12, fill=(15, 20, 32), outline=(48, 54, 61), width=1)

    px0, py0, px1, py1 = bx0 + 25, by0 + 25, bx0 + 880, by1 - 25
    draw_rounded_rect(draw, (px0, py0, px1, py1), radius=10, fill=(18, 24, 38), outline=(56, 139, 253), width=2)
    f_h2 = get_font(FONT_BOLD, 18)
    draw.text((px0 + 25, py0 + 20), "IEEE RESEARCH MANUSCRIPT (WHID_GUARD_2027.pdf)", font=f_h2, fill=(88, 166, 255))
    paste_scaled_image(img, "paper/WHID_GUARD_PREVIEW.png", (px0 + 20, py0 + 55, px1 - 20, py1 - 20))

    gx0, gy0, gx1, gy1 = bx0 + 915, by0 + 25, bx1 - 25, by1 - 25
    draw_rounded_rect(draw, (gx0, gy0, gx1, gy1), radius=10, fill=(18, 24, 38), outline=(56, 139, 253), width=2)
    
    draw.text((gx0 + 30, gy0 + 25), "OPEN-SOURCE REPOSITORY & VERIFICATION", font=f_h2, fill=(88, 166, 255))
    
    f_sub = get_font(FONT_REG, 15)
    f_mono = get_font(FONT_MONO, 14)
    f_b = get_font(FONT_BOLD, 15)

    draw.text((gx0 + 30, gy0 + 75), "Repository:", font=f_sub, fill=(139, 148, 158))
    draw.text((gx0 + 130, gy0 + 75), "https://github.com/ramKarthik57/BadUSB_Simulation", font=f_mono, fill=(88, 166, 255))

    badges = [
        ("CI / Automated Tests", "100% Passing (Python 3.11 & 3.12)", (63, 185, 80)),
        ("License", "MIT Open-Source License", (88, 166, 255)),
        ("Firmware Target", "ESP32-S3 Dual-Core (USB-OTG CDC+HID)", (240, 246, 252)),
        ("Host Platform", "Windows 11 RawInput & WH_KEYBOARD_LL", (240, 246, 252)),
        ("Research Paper", "IEEE Conference Format (6 Pages)", (210, 153, 34)),
    ]
    for idx, (lbl, val, col) in enumerate(badges):
        by = gy0 + 125 + idx * 45
        draw_rounded_rect(draw, (gx0 + 30, by, gx1 - 30, by + 36), radius=6, fill=(22, 27, 34), outline=(48, 54, 61), width=1)
        draw.text((gx0 + 45, by + 8), lbl + ":", font=f_b, fill=(139, 148, 158))
        draw.text((gx0 + 260, by + 8), val, font=f_mono, fill=col)

    cy0 = gy0 + 380
    draw_rounded_rect(draw, (gx0 + 30, cy0, gx1 - 30, gy1 - 30), radius=10, fill=(13, 17, 23), outline=(56, 139, 253), width=1)
    draw.text((gx0 + 50, cy0 + 25), "AMRITA VISHWA VIDYAPEETHAM", font=get_font(FONT_BOLD, 20), fill=(240, 246, 252))
    draw.text((gx0 + 50, cy0 + 60), "Department of Cybersecurity — Chennai Campus", font=f_sub, fill=(139, 148, 158))
    draw.text((gx0 + 50, cy0 + 95), "Student Authors & Researchers:", font=f_b, fill=(88, 166, 255))
    draw.text((gx0 + 70, cy0 + 130), "• Ram Karthik G  (Roll No: CH.SC.U4CYS23037)", font=f_mono, fill=(240, 246, 252))
    draw.text((gx0 + 70, cy0 + 165), "• Harini V        (Roll No: CH.SC.U4CYS23010)", font=f_mono, fill=(240, 246, 252))
    draw.text((gx0 + 50, cy0 + 215), "Thank you for evaluating our project!", font=get_font(FONT_BOLD, 18), fill=(63, 185, 80))

    return img

SCENE_RENDERERS = {
    1: render_frame_scene_1,
    2: render_frame_scene_2,
    3: render_frame_scene_3,
    4: render_frame_scene_4,
    5: render_frame_scene_5,
    6: render_frame_scene_6,
    7: render_frame_scene_7,
    8: render_frame_scene_8,
    9: render_frame_scene_9,
}

def main():
    print("=" * 70)
    print("      WHID-GUARD: 1080p ENHANCED LIVE DEMO VIDEO BUILDER")
    print("=" * 70)
    
    meta_path = "demo_video/scenes_live_meta.json"
    if not os.path.exists(meta_path):
        print(f"Error: {meta_path} not found!")
        sys.exit(1)
        
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
        
    total_dur = meta["total_duration"]
    scenes = meta["scenes"]
    print(f"[INFO] Loaded {len(scenes)} scenes | Total duration: {total_dur:.2f}s ({total_dur/60:.2f} min)")

    os.makedirs("demo_video/live_clips", exist_ok=True)
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    clip_paths = []

    for sc in scenes:
        sc_id = sc["id"]
        sc_title = sc["title"]
        sc_dur = sc["final_duration"]
        sc_start = sc["start_time"]
        audio_file = f"demo_video/audio_live/scene_{sc_id}.mp3"
        out_clip = f"demo_video/live_clips/clip_{sc_id}.mp4"
        clip_paths.append(os.path.abspath(out_clip))

        num_frames = int(round(sc_dur * FPS))
        print(f"\n[ENCODE] Scene {sc_id} ({sc_title}): {sc_dur:.2f}s -> {num_frames} frames @ {FPS} fps...")

        renderer = SCENE_RENDERERS[sc_id]

        cmd = [
            ffmpeg_exe, "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{WIDTH}x{HEIGHT}",
            "-pix_fmt", "rgb24",
            "-r", str(FPS),
            "-i", "-",
            "-i", audio_file,
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            out_clip
        ]

        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        t0 = time.time()

        for f_idx in range(num_frames):
            t_scene = f_idx / FPS
            t_glob = sc_start + t_scene
            frame = renderer(t_scene, sc_dur, t_glob, total_dur)
            proc.stdin.write(frame.tobytes())

        proc.stdin.close()
        proc.wait()
        elapsed = time.time() - t0
        print(f"         Done in {elapsed:.1f}s ({num_frames/elapsed:.1f} fps). Output: {out_clip}")

    # Step 2: Concatenate all clips
    print("\n[INFO] Concatenating all 9 scene clips...")
    list_file = "demo_video/live_clips/clips_concat.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for p in clip_paths:
            escaped = p.replace("\\", "/")
            f.write(f"file '{escaped}'\n")

    raw_master = "demo_video/WHID_Guard_5Min_Live_Demo_Raw.mp4"
    cmd_concat = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        raw_master
    ]
    subprocess.run(cmd_concat, check=True)
    print(f"[SUCCESS] Raw concatenated video: {raw_master}")

    # Step 3: Burn in styled subtitles from subtitles_live.ass
    final_video = "demo_video/WHID_Guard_5Min_Live_Demo_1080p.mp4"
    ass_path = os.path.abspath("demo_video/subtitles_live.ass").replace("\\", "/").replace(":", "\\:")
    print(f"\n[INFO] Burning in styled subtitles ({ass_path})...")
    
    cmd_sub = [
        ffmpeg_exe, "-y",
        "-i", raw_master,
        "-vf", f"ass={ass_path}",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        final_video
    ]
    subprocess.run(cmd_sub, check=True)
    print(f"\n[SUCCESS] Final 1080p Enhanced Live Demo Video created: {final_video}")

    if os.path.exists(final_video):
        size_mb = os.path.getsize(final_video) / (1024 * 1024)
        print(f"[STATUS] Final File Size: {size_mb:.2f} MB")

if __name__ == "__main__":
    main()
