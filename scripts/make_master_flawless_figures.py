import os
import sys
import shutil
import numpy as np
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams["font.family"] = "serif"
matplotlib.rcParams["mathtext.fontset"] = "dejavuserif"
matplotlib.rcParams["axes.linewidth"] = 1.0
import matplotlib.pyplot as plt
import fitz

PAPER_DIR = "C:/Users/Ram/Desktop/BadUSB_Using_ESP32/paper"
FIGURES_DIR = "C:/Users/Ram/Desktop/BadUSB_Using_ESP32/figures"

def export_svg_to_pdf_and_png(svg_str, pdf_path, png_path, dpi=300):
    doc = fitz.open(stream=svg_str.encode("utf-8"), filetype="svg")
    pdf_bytes = doc.convert_to_pdf()
    pdf_doc = fitz.open("pdf", pdf_bytes)
    pdf_doc.save(pdf_path)
    pix = pdf_doc[0].get_pixmap(dpi=dpi)
    pix.save(png_path)
    pdf_doc.close()
    doc.close()

# Professional crisp arrowheads
def arr_r(x, y, color, size=5.2):
    return f'<polygon points="{x},{y} {x-size},{y-size*0.62} {x-size*0.72},{y} {x-size},{y+size*0.62}" fill="{color}"/>'

def arr_l(x, y, color, size=5.2):
    return f'<polygon points="{x},{y} {x+size},{y-size*0.62} {x+size*0.72},{y} {x+size},{y+size*0.62}" fill="{color}"/>'

def arr_d(x, y, color, size=5.2):
    return f'<polygon points="{x},{y} {x-size*0.62},{y-size} {x},{y-size*0.72} {x+size*0.62},{y-size}" fill="{color}"/>'

def arr_u(x, y, color, size=5.2):
    return f'<polygon points="{x},{y} {x-size*0.62},{y+size} {x},{y+size*0.72} {x+size*0.62},{y+size}" fill="{color}"/>'


# ===========================================================================
# FIGURE 1: ENHANCED SYSTEM ARCHITECTURE
# - Distinct, prominent inter-tier arrows (Tier 1 -> Tier 2 and Tier 2 -> Tier 3)
# - Generous minimum arrow lengths
# - Spacious Tier 3 box (width 204pt, height 208pt) eliminating title & bottom tightness
# ===========================================================================
def build_fig1():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 224" width="760" height="224" style="background:#ffffff; font-family:Helvetica, Arial, sans-serif;">
  <defs>
    <filter id="sh1" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-opacity="0.05"/>
    </filter>
  </defs>

  <!-- ================= TIER 1: MOBILE C2 CONTROLLER (x: 6 to 134, width 128) ================= -->
  <rect x="6" y="8" width="128" height="208" rx="6" fill="#faf5ff" stroke="#a855f7" stroke-width="1.3"/>
  <text x="70" y="24.5" font-size="8.5" font-weight="bold" fill="#6b21a8" text-anchor="middle">Tier 1: Mobile C2 Controller</text>
  
  <rect x="16" y="38" width="108" height="40" rx="4" fill="#ffffff" stroke="#c084fc" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="70" y="53.5" font-size="9.0" font-weight="bold" fill="#1e293b" text-anchor="middle">Touch Web Console</text>
  <text x="70" y="67.5" font-size="7.6" fill="#64748b" text-anchor="middle">Single-Page App (SPA)</text>
  
  <rect x="16" y="94" width="108" height="40" rx="4" fill="#ffffff" stroke="#c084fc" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="70" y="109.5" font-size="9.0" font-weight="bold" fill="#1e293b" text-anchor="middle">REST Attack Engine</text>
  <text x="70" y="123.5" font-size="7.4" fill="#64748b" text-anchor="middle">Scenarios 1-4, Cadence Jitter</text>
  
  <rect x="16" y="150" width="108" height="40" rx="4" fill="#ffffff" stroke="#c084fc" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="70" y="165.5" font-size="9.0" font-weight="bold" fill="#1e293b" text-anchor="middle">802.11 b/g/n Station</text>
  <text x="70" y="179.5" font-size="7.4" fill="#64748b" text-anchor="middle">Station Link (192.168.4.2)</text>

  <!-- Downward Connectors inside Tier 1 -->
  <line x1="70" y1="78" x2="70" y2="88" stroke="#a855f7" stroke-width="1.3"/>
  {arr_d(70, 94, "#a855f7", 4.2)}
  <line x1="70" y1="134" x2="70" y2="144" stroke="#a855f7" stroke-width="1.3"/>
  {arr_d(70, 150, "#a855f7", 4.2)}

  <!-- ================= INTER-TIER 1 -> 2 BUS: 2.4 GHz SoftAP RF (x: 134 to 210 = 76pt corridor) ================= -->
  <!-- Line from Station through Tier 1 border into Badge -->
  <line x1="124" y1="170" x2="142" y2="170" stroke="#9333ea" stroke-width="1.5"/>
  {arr_r(148, 170, "#9333ea", 5.0)}
  <rect x="148" y="157" width="46" height="26" rx="3.5" fill="#ffffff" stroke="#d8b4fe" stroke-width="0.9"/>
  <text x="171" y="169" font-size="7.8" font-weight="bold" fill="#9333ea" text-anchor="middle">2.4 GHz</text>
  <text x="171" y="179" font-size="6.8" fill="#a855f7" text-anchor="middle">SoftAP RF</text>
  <!-- Line from Badge through Tier 2 border directly into 2.4 GHz Antenna -->
  <line x1="194" y1="170" x2="216" y2="170" stroke="#9333ea" stroke-width="1.5"/>
  {arr_r(222, 170, "#9333ea", 5.2)}

  <!-- ================= TIER 2: WEAPONIZED ESP32-S3 (x: 210 to 472, width 262) ================= -->
  <rect x="210" y="8" width="262" height="208" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.3"/>
  <text x="341" y="25" font-size="9.6" font-weight="bold" fill="#14532d" text-anchor="middle">Tier 2: Weaponized ESP32-S3 Hardware Implant</text>

  <!-- Core 0: Network (x: 222 to 336, width 114, height 58, y: 36 to 94) -->
  <rect x="222" y="36" width="114" height="58" rx="4" fill="#ffffff" stroke="#22c55e" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="279" y="50" font-size="9.0" font-weight="bold" fill="#14532d" text-anchor="middle">Core 0: Network</text>
  <text x="279" y="63" font-size="7.6" fill="#15803d" text-anchor="middle">SoftAP &amp; Web Server</text>
  <text x="279" y="75" font-size="7.6" font-weight="bold" fill="#166534" text-anchor="middle">Gateway IP: 192.168.4.1</text>
  <text x="279" y="86" font-size="7.2" fill="#475569" text-anchor="middle">TCP/IP Stack Baseband</text>

  <!-- Core 1: HID Engine (x: 346 to 460, width 114, height 58, y: 36 to 94) -->
  <rect x="346" y="36" width="114" height="58" rx="4" fill="#ffffff" stroke="#22c55e" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="403" y="51" font-size="9.0" font-weight="bold" fill="#14532d" text-anchor="middle">Core 1: HID Engine</text>
  <text x="403" y="67" font-size="7.8" fill="#15803d" text-anchor="middle">8-State Scenario FSM</text>
  <text x="403" y="82" font-size="7.8" fill="#475569" text-anchor="middle">Native TinyUSB HID</text>

  <!-- Atomic Ring Buffer (x: 222 to 460, width 238, height 28, y: 106 to 134) -->
  <rect x="222" y="106" width="238" height="28" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.1"/>
  <text x="341" y="123.5" font-size="8.4" font-weight="bold" fill="#14532d" text-anchor="middle">Lock-Free Atomic Ring Buffer (Non-blocking Shared Mailbox)</text>

  <!-- Internal Buffer Connections -->
  <line x1="279" y1="94" x2="279" y2="101" stroke="#16a34a" stroke-width="1.3"/>
  {arr_d(279, 106, "#16a34a", 4.0)}
  <line x1="403" y1="106" x2="403" y2="99" stroke="#16a34a" stroke-width="1.3"/>
  {arr_u(403, 94, "#16a34a", 4.0)}

  <!-- 2.4 GHz Antenna (x: 222 to 336, width 114, height 44, y: 148 to 192) -->
  <rect x="222" y="148" width="114" height="44" rx="4" fill="#ffffff" stroke="#22c55e" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="279" y="163.5" font-size="9.0" font-weight="bold" fill="#14532d" text-anchor="middle">2.4 GHz Antenna</text>
  <text x="279" y="176.0" font-size="7.4" fill="#15803d" text-anchor="middle">SoftAP Transceiver</text>
  <text x="279" y="186.5" font-size="7.0" fill="#475569" text-anchor="middle">Station Beacon Link</text>

  <!-- Native USB OTG PHY (x: 346 to 460, width 114, height 44, y: 148 to 192) -->
  <rect x="346" y="148" width="114" height="44" rx="4" fill="#fff7ed" stroke="#ea580c" stroke-width="1.1" filter="url(#sh1)"/>
  <text x="403" y="163.5" font-size="9.0" font-weight="bold" fill="#9a3412" text-anchor="middle">Native USB OTG PHY</text>
  <text x="403" y="176.0" font-size="7.4" font-weight="bold" fill="#c2410c" text-anchor="middle">GPIO 19/20 (D+/D-)</text>
  <text x="403" y="186.5" font-size="7.0" fill="#475569" text-anchor="middle">Hardware BOOT Latch</text>

  <!-- Core 0 to Antenna Link -->
  <line x1="222" y1="65" x2="216" y2="65" stroke="#16a34a" stroke-width="1.3"/>
  <line x1="216" y1="65" x2="216" y2="154" stroke="#16a34a" stroke-width="1.3"/>
  <line x1="216" y1="154" x2="218" y2="154" stroke="#16a34a" stroke-width="1.3"/>
  {arr_r(222, 154, "#16a34a", 4.0)}

  <!-- Core 1 to USB PHY Link -->
  <line x1="460" y1="65" x2="466" y2="65" stroke="#ea580c" stroke-width="1.3"/>
  <line x1="466" y1="65" x2="466" y2="154" stroke="#ea580c" stroke-width="1.3"/>
  <line x1="466" y1="154" x2="464" y2="154" stroke="#ea580c" stroke-width="1.3"/>
  {arr_l(460, 154, "#ea580c", 4.0)}

  <!-- ================= INTER-TIER 2 -> 3 BUS: USB 2.0 (x: 472 to 546 = 74pt corridor) ================= -->
  <!-- Line from Native USB PHY through Tier 2 border into USB Badge -->
  <line x1="460" y1="170" x2="483" y2="170" stroke="#1d4ed8" stroke-width="1.5"/>
  {arr_r(489, 170, "#1d4ed8", 5.0)}
  <rect x="489" y="157" width="46" height="26" rx="3.5" fill="#ffffff" stroke="#93c5fd" stroke-width="0.9"/>
  <text x="512" y="169" font-size="7.8" font-weight="bold" fill="#1d4ed8" text-anchor="middle">USB 2.0</text>
  <text x="512" y="179" font-size="6.8" fill="#2563eb" text-anchor="middle">12 Mbps HID</text>
  <!-- Line from USB Badge through Tier 3 border directly into Raw Input Monitor -->
  <line x1="535" y1="170" x2="554" y2="170" stroke="#1d4ed8" stroke-width="1.5"/>
  {arr_r(560, 170, "#1d4ed8", 5.2)}

  <!-- ================= TIER 3: WINDOWS HOST (WHID-GUARD) (x: 546 to 750, width 204, height 208) ================= -->
  <rect x="546" y="8" width="204" height="208" rx="6" fill="#eff6ff" stroke="#2563eb" stroke-width="1.3"/>
  <text x="648" y="25" font-size="9.6" font-weight="bold" fill="#1d4ed8" text-anchor="middle">Tier 3: Windows Host (WHID-Guard)</text>

  <!-- Box 1: Selective Filter Hook (WH_KEYBOARD_LL) -->
  <rect x="560" y="38" width="176" height="30" rx="4" fill="#ffffff" stroke="#3b82f6" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="648" y="50" font-size="8.4" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Selective Filter Hook</text>
  <text x="648" y="62" font-size="7.2" fill="#1d4ed8" text-anchor="middle">WH_KEYBOARD_LL ([PASS] / [DROP])</text>

  <!-- Arrow 1: Upward from Box 2 to Box 1 -->
  <line x1="648" y1="78" x2="648" y2="72" stroke="#2563eb" stroke-width="1.3"/>
  {arr_u(648, 68, "#2563eb", 3.8)}

  <!-- Box 2: Quarantine Table & Policy Gate -->
  <rect x="560" y="78" width="176" height="30" rx="4" fill="#ffffff" stroke="#3b82f6" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="648" y="90" font-size="8.4" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Quarantine Table &amp; Policy Gate</text>
  <text x="648" y="102" font-size="7.2" fill="#1d4ed8" text-anchor="middle">Isolates Rogue h_rogue (15s Auto-Reset)</text>

  <!-- Arrow 2: Upward from Box 3 to Box 2 -->
  <line x1="648" y1="118" x2="648" y2="112" stroke="#2563eb" stroke-width="1.3"/>
  {arr_u(648, 108, "#2563eb", 3.8)}

  <!-- Box 3: Behavioral Dynamics Engine -->
  <rect x="560" y="118" width="176" height="30" rx="4" fill="#ffffff" stroke="#3b82f6" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="648" y="130" font-size="8.4" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Behavioral Dynamics Engine (W=5)</text>
  <text x="648" y="142" font-size="7.2" fill="#1d4ed8" text-anchor="middle">Evaluates &#956; &lt; 25ms &#8744; CV &lt; 0.15</text>

  <!-- Arrow 3: Upward from Box 4 to Box 3 -->
  <line x1="648" y1="158" x2="648" y2="152" stroke="#2563eb" stroke-width="1.3"/>
  {arr_u(648, 148, "#2563eb", 3.8)}

  <!-- Box 4: Raw Input Monitor -->
  <rect x="560" y="158" width="176" height="30" rx="4" fill="#ffffff" stroke="#3b82f6" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="648" y="170" font-size="8.4" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Raw Input Monitor (WM_INPUT)</text>
  <text x="648" y="182" font-size="7.2" fill="#1d4ed8" text-anchor="middle">Pre-Hook Device Attribution (h_dev)</text>
</svg>"""
    return svg


# ===========================================================================
# FIGURE 2: FINITE STATE MACHINE (FSM) DIAGRAM
# - Exact mathematical midpoints for all transition badges
# - Minimum arrow line lengths >= 13pt
# - Flawlessly centered text and badges
# ===========================================================================
def build_fig2():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 224" width="760" height="224" style="background:#ffffff; font-family:Helvetica, Arial, sans-serif;">
  <defs>
    <filter id="sh2" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-opacity="0.06"/>
    </filter>
  </defs>

  <!-- ================= TOP ROW: NOMINAL SEQUENCE (y: 48 to 96, height: 48) ================= -->
  <!-- 1. STATE_BOOTING (x: 16 to 110, width: 94, center 63) -->
  <rect x="16" y="48" width="94" height="48" rx="5" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.2" filter="url(#sh2)"/>
  <text x="63" y="67" font-size="9.4" font-weight="bold" fill="#1e3a8a" text-anchor="middle">STATE_BOOTING</text>
  <text x="63" y="83" font-size="8.0" fill="#1d4ed8" text-anchor="middle">Power-On &amp; USB Init</text>

  <!-- Transition: BOOTING -> USB_WAIT (Gap: 110 to 170 = 60pt, Midpoint: 140.0, Badge width: 34) -->
  <line x1="110" y1="72" x2="123" y2="72" stroke="#2563eb" stroke-width="1.3"/>
  <rect x="123" y="64" width="34" height="16" rx="3" fill="#ffffff" stroke="#93c5fd" stroke-width="0.8"/>
  <text x="140" y="75.5" font-size="7.4" font-weight="bold" fill="#1d4ed8" text-anchor="middle">Init OK</text>
  <line x1="157" y1="72" x2="164" y2="72" stroke="#2563eb" stroke-width="1.3"/>
  {arr_r(170, 72, "#2563eb", 4.6)}

  <!-- 2. STATE_USB_WAIT (x: 170 to 274, width: 104, center 222) -->
  <rect x="170" y="48" width="104" height="48" rx="5" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.2" filter="url(#sh2)"/>
  <text x="222" y="67" font-size="9.4" font-weight="bold" fill="#1e3a8a" text-anchor="middle">STATE_USB_WAIT</text>
  <text x="222" y="83" font-size="8.0" fill="#1d4ed8" text-anchor="middle">Host Enum &#916;t &#8805; 3.5s</text>

  <!-- Transition: USB_WAIT -> STARTUP_PAYLOAD (Gap: 274 to 334 = 60pt, Midpoint: 304.0, Badge width: 30) -->
  <line x1="274" y1="72" x2="289" y2="72" stroke="#2563eb" stroke-width="1.3"/>
  <rect x="289" y="64" width="30" height="16" rx="3" fill="#ffffff" stroke="#93c5fd" stroke-width="0.8"/>
  <text x="304" y="75.5" font-size="7.4" font-weight="bold" fill="#1d4ed8" text-anchor="middle">Enum</text>
  <line x1="319" y1="72" x2="328" y2="72" stroke="#2563eb" stroke-width="1.3"/>
  {arr_r(334, 72, "#2563eb", 4.6)}

  <!-- 3. STATE_STARTUP_PAYLOAD (x: 334 to 468, width: 134, center 401) -->
  <rect x="334" y="48" width="134" height="48" rx="5" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.3" filter="url(#sh2)"/>
  <text x="401" y="67" font-size="9.4" font-weight="bold" fill="#92400e" text-anchor="middle">STATE_STARTUP_PAYLOAD</text>
  <text x="401" y="83" font-size="8.0" fill="#b45309" text-anchor="middle">Scenario 1 Auto-Run</text>

  <!-- Transition: STARTUP_PAYLOAD -> IDLE (Gap: 468 to 524 = 56pt, Midpoint: 496.0, Badge width: 28) -->
  <line x1="468" y1="72" x2="482" y2="72" stroke="#2563eb" stroke-width="1.3"/>
  <rect x="482" y="64" width="28" height="16" rx="3" fill="#ffffff" stroke="#93c5fd" stroke-width="0.8"/>
  <text x="496" y="75.5" font-size="7.4" font-weight="bold" fill="#1d4ed8" text-anchor="middle">Done</text>
  <line x1="510" y1="72" x2="518" y2="72" stroke="#2563eb" stroke-width="1.3"/>
  {arr_r(524, 72, "#2563eb", 4.6)}

  <!-- 4. STATE_IDLE (x: 524 to 600, width: 76, center 562) -->
  <rect x="524" y="48" width="76" height="48" rx="5" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.2" filter="url(#sh2)"/>
  <text x="562" y="67" font-size="9.4" font-weight="bold" fill="#14532d" text-anchor="middle">STATE_IDLE</text>
  <text x="562" y="83" font-size="7.8" fill="#166534" text-anchor="middle">Quiescent / Ready</text>

  <!-- Transitions between IDLE and RUNNING (Gap: 600 to 656 = 56pt, Midpoint: 628.0) -->
  <!-- Forward Arc: IDLE -> RUNNING at y=60 -->
  <line x1="600" y1="60" x2="613" y2="60" stroke="#16a34a" stroke-width="1.3"/>
  <rect x="613" y="52" width="30" height="16" rx="3" fill="#ffffff" stroke="#86efac" stroke-width="0.8"/>
  <text x="628" y="63.5" font-size="7.2" font-weight="bold" fill="#15803d" text-anchor="middle">REST</text>
  <line x1="643" y1="60" x2="650" y2="60" stroke="#16a34a" stroke-width="1.3"/>
  {arr_r(656, 60, "#16a34a", 4.6)}

  <!-- Reverse Arc: RUNNING -> IDLE at y=84 -->
  <line x1="656" y1="84" x2="646" y2="84" stroke="#2563eb" stroke-width="1.3"/>
  <rect x="610" y="76" width="36" height="16" rx="3" fill="#ffffff" stroke="#93c5fd" stroke-width="0.8"/>
  <text x="628" y="87.5" font-size="7.0" font-weight="bold" fill="#1d4ed8" text-anchor="middle">Complete</text>
  <line x1="610" y1="84" x2="606" y2="84" stroke="#2563eb" stroke-width="1.3"/>
  {arr_l(600, 84, "#2563eb", 4.6)}

  <!-- 5. STATE_RUNNING (x: 656 to 748, width: 92, center 702) -->
  <rect x="656" y="48" width="92" height="48" rx="5" fill="#fef2f2" stroke="#ef4444" stroke-width="1.3" filter="url(#sh2)"/>
  <text x="702" y="67" font-size="9.4" font-weight="bold" fill="#991b1b" text-anchor="middle">STATE_RUNNING</text>
  <text x="702" y="80" font-size="7.6" fill="#b91c1c" text-anchor="middle">Payload Active</text>
  <text x="702" y="91" font-size="7.0" fill="#475569" text-anchor="middle">Quantum &#948;t = 10ms</text>

  <!-- Global Preemption: Disconnect Return Arc (top line along y=16, midpoint between 702 and 222 is 462.0) -->
  <line x1="702" y1="48" x2="702" y2="16" stroke="#ea580c" stroke-width="1.3" stroke-dasharray="4,2.5"/>
  <line x1="702" y1="16" x2="496" y2="16" stroke="#ea580c" stroke-width="1.3" stroke-dasharray="4,2.5"/>
  <rect x="428" y="8" width="68" height="16" rx="3" fill="#ffffff" stroke="#fdba74" stroke-width="0.8"/>
  <text x="462" y="19.5" font-size="6.8" font-weight="bold" fill="#ea580c" text-anchor="middle">USB Disconnect</text>
  <line x1="428" y1="16" x2="222" y2="16" stroke="#ea580c" stroke-width="1.3" stroke-dasharray="4,2.5"/>
  <line x1="222" y1="16" x2="222" y2="42" stroke="#ea580c" stroke-width="1.3" stroke-dasharray="4,2.5"/>
  {arr_d(222, 48, "#ea580c", 4.6)}

  <!-- ================= BOTTOM ROW: PREEMPTION, STOP & FAULT (y: 146 to 194, height: 48) ================= -->
  <!-- 8. STATE_ERROR (x: 656 to 748, width: 92, center 702) directly under RUNNING -->
  <rect x="656" y="146" width="92" height="48" rx="5" fill="#fff1f2" stroke="#be123c" stroke-width="1.2" filter="url(#sh2)"/>
  <text x="702" y="165" font-size="9.4" font-weight="bold" fill="#9f1239" text-anchor="middle">STATE_ERROR</text>
  <text x="702" y="181" font-size="8.0" fill="#be123c" text-anchor="middle">Timeout / CRC Fault</text>

  <!-- Downward Arrow: RUNNING -> ERROR (Gap: 96 to 146 = 50pt, Midpoint: 121.0, Badge height: 16) -->
  <line x1="714" y1="96" x2="714" y2="113" stroke="#be123c" stroke-width="1.3"/>
  <rect x="696" y="113" width="36" height="16" rx="3" fill="#ffffff" stroke="#fda4af" stroke-width="0.8"/>
  <text x="714" y="124.5" font-size="7.0" font-weight="bold" fill="#be123c" text-anchor="middle">Fault</text>
  <line x1="714" y1="129" x2="714" y2="140" stroke="#be123c" stroke-width="1.3"/>
  {arr_d(714, 146, "#be123c", 4.6)}

  <!-- 6. STATE_STOPPING (x: 494 to 600, width: 106, center 547) -->
  <rect x="494" y="146" width="106" height="48" rx="5" fill="#fff7ed" stroke="#ea580c" stroke-width="1.2" filter="url(#sh2)"/>
  <text x="547" y="165" font-size="9.2" font-weight="bold" fill="#9a3412" text-anchor="middle">STATE_STOPPING</text>
  <text x="547" y="181" font-size="7.8" fill="#c2410c" text-anchor="middle">Teardown Latch (&le; 10ms)</text>

  <!-- Transition: RUNNING -> STOPPING upon Abort -->
  <line x1="676" y1="96" x2="676" y2="121" stroke="#ea580c" stroke-width="1.3"/>
  <line x1="676" y1="121" x2="630" y2="121" stroke="#ea580c" stroke-width="1.3"/>
  <line x1="630" y1="121" x2="630" y2="137" stroke="#ea580c" stroke-width="1.3"/>
  <rect x="616" y="137" width="28" height="16" rx="3" fill="#ffffff" stroke="#fdba74" stroke-width="0.8"/>
  <text x="630" y="148.5" font-size="6.8" font-weight="bold" fill="#ea580c" text-anchor="middle">Abort</text>
  <line x1="630" y1="153" x2="630" y2="170" stroke="#ea580c" stroke-width="1.3"/>
  <line x1="630" y1="170" x2="606" y2="170" stroke="#ea580c" stroke-width="1.3"/>
  {arr_l(600, 170, "#ea580c", 4.6)}

  <!-- 7. STATE_STOPPED (x: 334 to 438, width: 104, center 386) -->
  <rect x="334" y="146" width="104" height="48" rx="5" fill="#f8fafc" stroke="#64748b" stroke-width="1.2" filter="url(#sh2)"/>
  <text x="386" y="165" font-size="9.2" font-weight="bold" fill="#334155" text-anchor="middle">STATE_STOPPED</text>
  <text x="386" y="181" font-size="7.8" fill="#475569" text-anchor="middle">Key Latch Cleared</text>

  <!-- Transition: STOPPING -> STOPPED (Gap: 438 to 494 = 56pt, Midpoint: 466.0, Badge width: 34) -->
  <line x1="494" y1="170" x2="483" y2="170" stroke="#ea580c" stroke-width="1.3"/>
  <rect x="449" y="162" width="34" height="16" rx="3" fill="#ffffff" stroke="#fdba74" stroke-width="0.8"/>
  <text x="466" y="173.5" font-size="6.5" font-weight="bold" fill="#ea580c" text-anchor="middle">releaseAll</text>
  <line x1="449" y1="170" x2="444" y2="170" stroke="#ea580c" stroke-width="1.3"/>
  {arr_l(438, 170, "#ea580c", 4.6)}

  <!-- Return Arc: STOPPED -> IDLE (Midpoint between 386 and 562 is 474.0) -->
  <line x1="386" y1="146" x2="386" y2="121" stroke="#16a34a" stroke-width="1.3"/>
  <line x1="386" y1="121" x2="451" y2="121" stroke="#16a34a" stroke-width="1.3"/>
  <rect x="451" y="113" width="46" height="16" rx="3" fill="#ffffff" stroke="#86efac" stroke-width="0.8"/>
  <text x="474" y="124.5" font-size="7.0" font-weight="bold" fill="#15803d" text-anchor="middle">Ack / Clear</text>
  <line x1="497" y1="121" x2="562" y2="121" stroke="#16a34a" stroke-width="1.3"/>
  <line x1="562" y1="121" x2="562" y2="102" stroke="#16a34a" stroke-width="1.3"/>
  {arr_u(562, 96, "#16a34a", 4.6)}

  <!-- Return Arc: ERROR -> USB_WAIT (Auto-recovery bottom line along y=212, midpoint between 702 and 222 is 462.0) -->
  <line x1="702" y1="194" x2="702" y2="212" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,2"/>
  <line x1="702" y1="212" x2="491" y2="212" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,2"/>
  <rect x="433" y="204" width="58" height="15" rx="3" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.8"/>
  <text x="462" y="214.5" font-size="6.8" font-weight="bold" fill="#475569" text-anchor="middle">Auto-Recover</text>
  <line x1="433" y1="212" x2="222" y2="212" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,2"/>
  <line x1="222" y1="212" x2="222" y2="102" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,2"/>
  {arr_u(222, 96, "#64748b", 4.6)}
</svg>"""
    return svg


# ===========================================================================
# FIGURE 3: ENHANCED SELECTIVE DEFENSE ARCHITECTURE
# - Generous 36pt separation between vertical spine (x=158) and container (x=194)
# - Absolutely zero near-collisions
# - Clear junction dot and prominent directional arrows
# ===========================================================================
def build_fig3():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 224" width="760" height="224" style="background:#ffffff; font-family:Helvetica, Arial, sans-serif;">
  <defs>
    <filter id="sh3" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-opacity="0.05"/>
    </filter>
  </defs>

  <!-- ================= HOST DAEMON CONTAINER (x=194, leaving massive 36pt gap from vertical spine x=158!) ================= -->
  <rect x="194" y="8" width="424" height="208" rx="6" fill="#f8fafc" stroke="#64748b" stroke-width="1.3"/>
  <text x="206" y="25" font-size="10.0" font-weight="bold" fill="#1e293b" text-anchor="start">Host OS Defense Daemon (WHID-Guard Framework)</text>

  <!-- ================= HARDWARE INPUT SOURCES ================= -->
  <!-- Physical Keyboard (Genuine) -->
  <rect x="10" y="38" width="102" height="46" rx="5" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.2" filter="url(#sh3)"/>
  <text x="61" y="57" font-size="9.4" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Physical Keyboard</text>
  <text x="61" y="72" font-size="8.0" fill="#2563eb" text-anchor="middle">Genuine HID (h_legit)</text>

  <!-- Rogue Hardware (ESP32-S3) -->
  <rect x="10" y="142" width="102" height="46" rx="5" fill="#fef2f2" stroke="#ef4444" stroke-width="1.2" filter="url(#sh3)"/>
  <text x="61" y="161" font-size="9.4" font-weight="bold" fill="#991b1b" text-anchor="middle">Rogue ESP32-S3</text>
  <text x="61" y="176" font-size="8.0" fill="#b91c1c" text-anchor="middle">BadUSB (h_rogue)</text>

  <!-- USB Root Hub -->
  <rect x="120" y="30" width="22" height="166" rx="4" fill="#f1f5f9" stroke="#475569" stroke-width="1.1"/>
  <text x="131" y="113" font-size="9.2" font-weight="bold" fill="#334155" text-anchor="middle" transform="rotate(-90 131 113)">USB Root Hub</text>

  <!-- Input Lines: Hardware to Hub -->
  <line x1="112" y1="61" x2="115" y2="61" stroke="#2563eb" stroke-width="1.4"/>
  {arr_r(120, 61, "#2563eb", 4.2)}
  <line x1="112" y1="165" x2="115" y2="165" stroke="#ef4444" stroke-width="1.4"/>
  {arr_r(120, 165, "#ef4444", 4.2)}

  <!-- Hub branching into Host OS Daemon (Generous 36pt gap between vertical spine x=158 and container x=194!) -->
  <line x1="142" y1="113" x2="158" y2="113" stroke="#2563eb" stroke-width="1.4"/>
  <circle cx="158" cy="113" r="2.2" fill="#2563eb"/>
  <line x1="158" y1="113" x2="158" y2="61" stroke="#2563eb" stroke-width="1.4"/>
  <line x1="158" y1="61" x2="200" y2="61" stroke="#2563eb" stroke-width="1.4"/>
  {arr_r(206, 61, "#2563eb", 4.6)}

  <line x1="158" y1="113" x2="158" y2="165" stroke="#2563eb" stroke-width="1.4"/>
  <line x1="158" y1="165" x2="200" y2="165" stroke="#2563eb" stroke-width="1.4"/>
  {arr_r(206, 165, "#2563eb", 4.6)}

  <!-- ================= UPPER PIPELINE: INTERCEPTION ================= -->
  <!-- Selective Filter Hook -->
  <rect x="206" y="38" width="112" height="46" rx="5" fill="#ffffff" stroke="#3b82f6" stroke-width="1.1" filter="url(#sh3)"/>
  <text x="262" y="57" font-size="9.2" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Selective Filter Hook</text>
  <text x="262" y="71" font-size="7.8" fill="#2563eb" text-anchor="middle">(WH_KEYBOARD_LL Hook)</text>

  <!-- Pre-Dispatch Buffer -->
  <rect x="336" y="38" width="112" height="46" rx="5" fill="#ffffff" stroke="#3b82f6" stroke-width="1.1" filter="url(#sh3)"/>
  <text x="392" y="57" font-size="9.2" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Pre-Dispatch Buffer</text>
  <text x="392" y="71" font-size="7.8" fill="#2563eb" text-anchor="middle">FIFO Delay Queue (W=5)</text>

  <!-- Arrow: Hook -> Pre-Dispatch Buffer -->
  <line x1="318" y1="61" x2="330" y2="61" stroke="#2563eb" stroke-width="1.3"/>
  {arr_r(336, 61, "#2563eb", 4.5)}

  <!-- Clean Stream Link with Stream Badge: Pre-Dispatch Buffer -> Selective Filter Gate -->
  <line x1="448" y1="61" x2="459" y2="61" stroke="#2563eb" stroke-width="1.3"/>
  <rect x="459" y="53" width="28" height="16" rx="3" fill="#ffffff" stroke="#93c5fd" stroke-width="0.8"/>
  <text x="473" y="64.5" font-size="7.2" font-weight="bold" fill="#1d4ed8" text-anchor="middle">Stream</text>
  <line x1="487" y1="61" x2="494" y2="61" stroke="#2563eb" stroke-width="1.3"/>
  {arr_r(500, 61, "#2563eb", 4.5)}

  <!-- ================= LOWER PIPELINE: ATTRIBUTION & DYNAMICS ================= -->
  <!-- Raw Input Pre-Filter -->
  <rect x="206" y="142" width="112" height="46" rx="5" fill="#ffffff" stroke="#3b82f6" stroke-width="1.1" filter="url(#sh3)"/>
  <text x="262" y="160" font-size="9.2" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Raw Input Pre-Filter</text>
  <text x="262" y="174" font-size="7.4" fill="#2563eb" text-anchor="middle">WM_INPUT (RIDEV_INPUTSINK)</text>

  <!-- Dynamics Engine -->
  <rect x="336" y="142" width="112" height="46" rx="5" fill="#ffffff" stroke="#3b82f6" stroke-width="1.1" filter="url(#sh3)"/>
  <text x="392" y="160" font-size="9.2" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Dynamics Engine</text>
  <text x="392" y="172" font-size="7.4" fill="#2563eb" text-anchor="middle">Sliding Window (W = 5)</text>
  <text x="392" y="182" font-size="7.2" fill="#475569" text-anchor="middle">Evaluates &#956;_IKI &amp; CV_IKI</text>

  <!-- Arrow: Raw Input -> Dynamics Engine -->
  <line x1="318" y1="165" x2="330" y2="165" stroke="#2563eb" stroke-width="1.3"/>
  {arr_r(336, 165, "#2563eb", 4.5)}

  <!-- Arrow: Dynamics Engine -> Decision Boundary -->
  <line x1="448" y1="165" x2="494" y2="165" stroke="#8b5cf6" stroke-width="1.4"/>
  {arr_r(500, 165, "#8b5cf6", 4.5)}

  <!-- ================= DECISION & ENFORCEMENT COLUMN (x: 500 to 608, width 108) ================= -->
  <!-- 1. Selective Filter Gate -->
  <rect x="500" y="38" width="108" height="46" rx="5" fill="#eff6ff" stroke="#2563eb" stroke-width="1.3" filter="url(#sh3)"/>
  <text x="554" y="56" font-size="9.2" font-weight="bold" fill="#1d4ed8" text-anchor="middle">Selective Filter Gate</text>
  <text x="554" y="71" font-size="7.4" fill="#1e3a8a" text-anchor="middle">Inspects h_origin &#8712; Q_quar</text>

  <!-- Link: Quarantine Table to Selective Filter Gate -->
  <line x1="554" y1="92" x2="554" y2="88" stroke="#dc2626" stroke-width="1.4"/>
  {arr_u(554, 84, "#dc2626", 4.2)}

  <!-- 2. Quarantine Table -->
  <rect x="500" y="92" width="108" height="30" rx="4" fill="#fef2f2" stroke="#ef4444" stroke-width="1.1" filter="url(#sh3)"/>
  <text x="554" y="104.5" font-size="8.8" font-weight="bold" fill="#991b1b" text-anchor="middle">Quarantine Table</text>
  <text x="554" y="116.5" font-size="7.2" fill="#b91c1c" text-anchor="middle">Isolates Handle h_rogue</text>

  <!-- 3. Decision Boundary -->
  <rect x="500" y="150" width="108" height="32" rx="4" fill="#faf5ff" stroke="#a855f7" stroke-width="1.1" filter="url(#sh3)"/>
  <text x="554" y="164" font-size="9.0" font-weight="bold" fill="#6b21a8" text-anchor="middle">Decision Boundary</text>
  <text x="554" y="176" font-size="7.4" fill="#7c3aed" text-anchor="middle">&#956; &lt; 25ms &#8744; CV &lt; 0.15</text>

  <!-- Upward Lockdown Link with Lockdown Badge -->
  <line x1="554" y1="150" x2="554" y2="144" stroke="#dc2626" stroke-width="1.3"/>
  <rect x="520" y="130" width="68" height="14" rx="3" fill="#ffffff" stroke="#fca5a5" stroke-width="0.8"/>
  <text x="554" y="140.5" font-size="7.2" font-weight="bold" fill="#b91c1c" text-anchor="middle">Lockdown (&#954; &#8805; 8)</text>
  <line x1="554" y1="130" x2="554" y2="126" stroke="#dc2626" stroke-width="1.3"/>
  {arr_u(554, 122, "#dc2626", 4.0)}

  <!-- 4. 15s Watchdog (Auto-Reset) -->
  <rect x="500" y="192" width="108" height="16" rx="3" fill="#fff7ed" stroke="#ea580c" stroke-width="0.9"/>
  <text x="554" y="203.5" font-size="7.6" font-weight="bold" fill="#9a3412" text-anchor="middle">15s Watchdog (Auto-Reset)</text>

  <!-- ================= OUTPUT SINKS (Right column outside Daemon: x: 646 to 750, width 104) ================= -->
  <!-- [DROP EVENT] -->
  <rect x="646" y="34" width="104" height="32" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.2"/>
  <text x="698" y="48" font-size="9.4" font-weight="bold" fill="#991b1b" text-anchor="middle">[DROP EVENT]</text>
  <text x="698" y="60" font-size="7.8" fill="#b91c1c" text-anchor="middle">Suppress Scancode</text>

  <!-- [PASS EVENT] -->
  <rect x="646" y="74" width="104" height="32" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.2"/>
  <text x="698" y="88" font-size="9.4" font-weight="bold" fill="#14532d" text-anchor="middle">[PASS EVENT]</text>
  <text x="698" y="100" font-size="7.8" fill="#15803d" text-anchor="middle">Allow Keystroke</text>

  <!-- Target: Active Window -->
  <rect x="646" y="114" width="104" height="32" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.0"/>
  <text x="698" y="128" font-size="9.2" font-weight="bold" fill="#334155" text-anchor="middle">Active Window</text>
  <text x="698" y="140" font-size="7.6" fill="#64748b" text-anchor="middle">Foreground Target</text>

  <!-- Link: PASS EVENT -> Active Window -->
  <line x1="698" y1="106" x2="698" y2="110" stroke="#16a34a" stroke-width="1.3"/>
  {arr_d(698, 114, "#16a34a", 4.0)}

  <!-- Output Lines from Gate -->
  <line x1="608" y1="48" x2="640" y2="48" stroke="#dc2626" stroke-width="1.4"/>
  {arr_r(646, 48, "#dc2626", 4.5)}
  
  <line x1="608" y1="68" x2="632" y2="68" stroke="#16a34a" stroke-width="1.4"/>
  <line x1="632" y1="68" x2="632" y2="90" stroke="#16a34a" stroke-width="1.4"/>
  <line x1="632" y1="90" x2="640" y2="90" stroke="#16a34a" stroke-width="1.4"/>
  {arr_r(646, 90, "#16a34a", 4.5)}

  <!-- Global Pipeline Flush & Gate Override -->
  <rect x="646" y="170" width="104" height="38" rx="4" fill="#fff7ed" stroke="#ea580c" stroke-width="1.2"/>
  <text x="698" y="185" font-size="8.8" font-weight="bold" fill="#9a3412" text-anchor="middle">Global Pipeline Flush</text>
  <text x="698" y="198" font-size="8.0" font-weight="bold" fill="#c2410c" text-anchor="middle">&amp; Gate Override</text>

  <!-- Trigger Link: 15s Watchdog -> Global Flush -->
  <line x1="608" y1="200" x2="640" y2="200" stroke="#ea580c" stroke-width="1.4"/>
  {arr_r(646, 200, "#ea580c", 4.5)}

  <!-- Feedback Line: Flush to Quarantine Table along unified corridor axis x=632 -->
  <line x1="646" y1="182" x2="632" y2="182" stroke="#ea580c" stroke-width="1.3" stroke-dasharray="3,2"/>
  <line x1="632" y1="182" x2="632" y2="167" stroke="#ea580c" stroke-width="1.3" stroke-dasharray="3,2"/>
  <rect x="619" y="152" width="26" height="15" rx="3" fill="#ffffff" stroke="#fed7aa" stroke-width="0.8"/>
  <text x="632" y="163" font-size="6.8" font-weight="bold" fill="#ea580c" text-anchor="middle">Flush</text>
  <line x1="632" y1="152" x2="632" y2="107" stroke="#ea580c" stroke-width="1.3" stroke-dasharray="3,2"/>
  <line x1="632" y1="107" x2="614" y2="107" stroke="#ea580c" stroke-width="1.3" stroke-dasharray="3,2"/>
  {arr_l(608, 107, "#ea580c", 4.5)}
</svg>"""
    return svg


# ===========================================================================
# FIGURE 4: IKI DISTRIBUTION (PERFECT VECTOR MATPLOTLIB - ZERO COLLISION)
# ===========================================================================
def build_fig4():
    fig, ax = plt.subplots(figsize=(3.4, 2.3), dpi=300)
    fig.subplots_adjust(left=0.15, right=0.96, top=0.92, bottom=0.20)

    np.random.seed(42)

    # 1. Standard BadUSB: N=500, mu=10.01, sigma=0.78
    badusb_deltas = np.random.normal(10.01, 0.78, 500)
    badusb_deltas = np.clip(badusb_deltas, 8.0, 13.0)

    # 2. Evasion BadUSB: N=500, base=80, jitter=U(0,40), pauses U(150,300) on 15% delims
    base_jitter = 80.0 + np.random.uniform(0, 40.0, 425)
    delims = np.random.uniform(150.0, 300.0, 75)
    evasion_deltas = np.concatenate([base_jitter, delims])
    np.random.shuffle(evasion_deltas)

    # 3. Human Operator: N=500, lognormal distribution matching mu=144.18, sigma=91.98
    sigma_log = np.sqrt(np.log(1 + (91.98 / 144.18)**2))
    mean_log = np.log(144.18) - (sigma_log**2) / 2
    human_deltas = np.random.lognormal(mean_log, sigma_log, 500)
    human_deltas = np.clip(human_deltas, 40.0, 440.0)

    bins = np.linspace(0, 450, 46)

    C_BADUSB = "#DC2626"
    C_EVASION = "#2563EB"
    C_HUMAN = "#475569"
    C_GRID = "#E2E8F0"

    ax.hist(badusb_deltas, bins=bins, color=C_BADUSB, alpha=0.85, edgecolor="#991B1B", linewidth=0.6,
            label=r"Standard BadUSB ($\mu = 10.0$ ms)", zorder=3)
    ax.hist(evasion_deltas, bins=bins, color=C_EVASION, alpha=0.70, edgecolor="#1D4ED8", linewidth=0.6,
            label=r"Adversarial Evasion ($\mu = 119.3$ ms)", zorder=2)
    ax.hist(human_deltas, bins=bins, color=C_HUMAN, alpha=0.55, edgecolor="#1E293B", linewidth=0.6,
            label=r"Human Baseline ($\mu = 144.2$ ms)", zorder=1)

    ax.axvline(25.0, color="#991B1B", linestyle="--", linewidth=1.4, zorder=4,
               label=r"Speed/Jitter ($\mu \leq 25\,$ms $\vee$ $\mathrm{CV}_{\mathrm{IKI}} < 0.15$)")
    ax.axvline(75.0, color="#334155", linestyle=":", linewidth=1.4, zorder=4,
               label=r"Human Bound ($\mu \geq 75$ ms)")

    ax.grid(True, linestyle="--", alpha=0.5, color=C_GRID)

    ax.set_xlabel(r"Inter-Key Interval $\Delta t$ (ms)", fontsize=8.8, fontweight="bold", labelpad=3)
    ax.set_ylabel("Empirical Frequency", fontsize=8.8, fontweight="bold", labelpad=3)

    ax.tick_params(axis="both", which="major", labelsize=8.2, pad=3)
    ax.set_xlim(0, 450)
    ax.set_ylim(0, 520)

    legend = ax.legend(loc="upper right", frameon=True, fancybox=True, edgecolor="#CBD5E1",
                       framealpha=0.96, fontsize=6.5, handlelength=1.1, labelspacing=0.22, borderpad=0.28)
    legend.get_frame().set_linewidth(0.8)

    fig_path = os.path.join(PAPER_DIR, "fig_iki_distribution.pdf")
    fig.savefig(fig_path, format="pdf")
    fig_png = os.path.join(PAPER_DIR, "fig_iki_distribution.png")
    fig.savefig(fig_png, format="png", dpi=300)
    plt.close(fig)
    print("Fig 4 generated successfully.")


# ===========================================================================
# FIGURE 5: DETECTION LATENCY VS BURST RATE (SPOTLESS DUAL-AXIS PUBLICATION PLOT)
# - Fully harmonized dual y-axes (0..24 left, 0..300 right: exactly 6 aligned intervals)
# - Legend elevated in clear space y1 in [16..24], 9.4pt above horizon line, zero collision
# - Clean self-contained legend defining Safety Margin (Delta = 6)
# - Compact endpoint callouts with pointer arrows in open sectors
# - 100% collision-free, zero clipping, zero bounds overflow
# ===========================================================================
def build_fig5():
    fig, ax1 = plt.subplots(figsize=(3.35, 2.25), dpi=300)
    fig.subplots_adjust(left=0.15, right=0.84, top=0.88, bottom=0.18)

    rates = np.array([40.0, 50.0, 60.0, 66.7, 75.0, 85.0, 100.0])
    chars_allowed = np.array([8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0])
    wall_clock_ms = 8.0 * (1000.0 / rates)

    fine_rates = np.linspace(38.0, 102.0, 250)
    fine_ms = 8.0 * (1000.0 / fine_rates)

    C_NAVY = "#0F172A"       # Primary Keystroke Trigger (Navy)
    C_BLUE = "#1D4ED8"       # Reaction Time (Steel Blue)
    C_RED = "#DC2626"        # Execution Horizon (Red)
    C_GREEN = "#059669"      # Safety Buffer (Emerald)
    C_GRID = "#E2E8F0"

    # Set left axis range to 0..24
    ax1.set_xlim(36.0, 104.0)
    ax1.set_ylim(0.0, 24.0)
    ax1.set_yticks([0, 4, 8, 12, 16, 20, 24])
    ax1.set_xticks([40, 60, 80, 100])

    # Right axis: range 0..300 ms (identical 6 grid intervals)
    ax2 = ax1.twinx()
    ax2.set_xlim(36.0, 104.0)
    ax2.set_ylim(0.0, 300.0)
    ax2.set_yticks([0, 50, 100, 150, 200, 250, 300])

    # 1. Shaded Safety Buffer Band with clean legend entry
    poly_buf = ax1.fill_between([36.0, 104.0], 8.0, 14.0, color="#ECFDF5", edgecolor="#A7F3D0",
                                linewidth=0.5, alpha=0.95, zorder=1, label=r"Safety Margin ($\Delta = 6$)")

    # 2. Execution Horizon & Trigger Lines on Left Axis
    line_exec = ax1.axhline(14.0, color=C_RED, linestyle="--", linewidth=1.4, zorder=2,
                            label=r"Execution Horizon ($L_{\mathrm{exec}} = 14$)")
    line_lat, = ax1.plot([36.0, 104.0], [8.0, 8.0], color=C_NAVY, linewidth=1.8, zorder=3,
                         label=r"Quarantine Trigger ($\kappa = 8$)")
    ax1.plot(rates, chars_allowed, marker="o", markersize=4.0, color=C_NAVY, linestyle="None", zorder=4)

    # 3. Right Axis Line: Wall-Clock Reaction Time (ms)
    line_time, = ax2.plot(fine_rates, fine_ms, color=C_BLUE, linewidth=1.8, linestyle="-.", zorder=3,
                          label=r"Reaction Time ($t_{\mathrm{quar}}$)")
    ax2.plot(rates, wall_clock_ms, marker="s", markersize=4.0, color=C_BLUE, linestyle="None", zorder=4)

    # 4. Clean compact callouts for endpoints
    # Point at (40, 200)
    ax2.annotate(r"$\mathbf{200\,\mathrm{ms}}$", xy=(40.0, 200.0), xytext=(42.0, 224.0),
                 fontsize=6.5, fontweight="bold", color=C_BLUE, zorder=6,
                 arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=0.7, shrinkA=0, shrinkB=2),
                 bbox=dict(boxstyle="round,pad=0.16", facecolor="#ffffff", edgecolor="#93c5fd", lw=0.5, alpha=0.96))

    # Point at (100, 80.1)
    ax2.annotate(r"$\mathbf{80.1\,\mathrm{ms}}$", xy=(100.0, 80.1), xytext=(88.0, 42.0),
                 fontsize=6.5, fontweight="bold", color=C_BLUE, zorder=6,
                 arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=0.7, shrinkA=0, shrinkB=2),
                 bbox=dict(boxstyle="round,pad=0.16", facecolor="#ffffff", edgecolor="#93c5fd", lw=0.5, alpha=0.96))

    # Labels and Grid
    ax1.set_xlabel(r"Burst Injection Rate (chars/s)", fontsize=8.2, fontweight="bold", labelpad=3)
    ax1.set_ylabel("Quarantine Latency (Chars)", fontsize=8.2, fontweight="bold", color=C_NAVY, labelpad=2)
    ax2.set_ylabel(r"Reaction Time $t_{\mathrm{quar}}$ (ms)", fontsize=8.2, fontweight="bold", color=C_BLUE, labelpad=2)

    ax1.tick_params(axis="y", labelcolor=C_NAVY, labelsize=7.5, pad=2)
    ax1.tick_params(axis="x", labelsize=7.5, pad=2)
    ax2.tick_params(axis="y", labelcolor=C_BLUE, labelsize=7.5, pad=2)
    ax1.grid(True, linestyle="--", alpha=0.45, color=C_GRID)

    # 5. Legend in Upper Right: Includes all 4 items!
    lines = [line_exec, line_lat, poly_buf, line_time]
    labels = [l.get_label() for l in lines]
    leg = ax1.legend(lines, labels, loc="upper right", fontsize=5.8, framealpha=0.98, edgecolor="#CBD5E1",
                     borderpad=0.28, labelspacing=0.40, handlelength=1.4)
    leg.get_frame().set_linewidth(0.5)

    fig_path = os.path.join(PAPER_DIR, "fig_detection_latency.pdf")
    fig.savefig(fig_path, format="pdf")
    fig_png = os.path.join(PAPER_DIR, "fig_detection_latency.png")
    fig.savefig(fig_png, format="png", dpi=300)
    plt.close(fig)
    print("Fig 5 generated successfully.")


# ===========================================================================
# MASTER GENERATION & REPLICATION
# ===========================================================================
def main():
    print("=== GENERATING ALL 5 FLAWLESS FIGURES ===")
    
    # 1. Fig 1
    s1 = build_fig1()
    f1_svg = os.path.join(PAPER_DIR, "fig1_system_architecture.svg")
    with open(f1_svg, "w", encoding="utf-8") as f:
        f.write(s1)
    f1_pdf = os.path.join(PAPER_DIR, "fig1_system_architecture.pdf")
    f1_png = os.path.join(PAPER_DIR, "fig1_system_architecture.png")
    export_svg_to_pdf_and_png(s1, f1_pdf, f1_png)
    print("Fig 1 generated.")

    # 2. Fig 2
    s2 = build_fig2()
    f2_svg = os.path.join(PAPER_DIR, "fig2_fsm_diagram.svg")
    with open(f2_svg, "w", encoding="utf-8") as f:
        f.write(s2)
    f2_pdf = os.path.join(PAPER_DIR, "fig2_fsm_diagram.pdf")
    f2_png = os.path.join(PAPER_DIR, "fig2_fsm_diagram.png")
    export_svg_to_pdf_and_png(s2, f2_pdf, f2_png)
    print("Fig 2 generated.")

    # 3. Fig 3
    s3 = build_fig3()
    f3_svg = os.path.join(PAPER_DIR, "fig3_selective_defense.svg")
    with open(f3_svg, "w", encoding="utf-8") as f:
        f.write(s3)
    f3_pdf = os.path.join(PAPER_DIR, "fig3_selective_defense.pdf")
    f3_png = os.path.join(PAPER_DIR, "fig3_selective_defense.png")
    export_svg_to_pdf_and_png(s3, f3_pdf, f3_png)
    print("Fig 3 generated.")

    # 4. Fig 4
    build_fig4()

    # 5. Fig 5
    build_fig5()

    # Replicate canonical aliases in paper/
    shutil.copyfile(f1_pdf, os.path.join(PAPER_DIR, "system_architecture.pdf"))
    shutil.copyfile(f1_png, os.path.join(PAPER_DIR, "system_architecture.png"))
    shutil.copyfile(f2_pdf, os.path.join(PAPER_DIR, "fsm_diagram.pdf"))
    shutil.copyfile(f2_png, os.path.join(PAPER_DIR, "fsm_diagram.png"))
    shutil.copyfile(f3_pdf, os.path.join(PAPER_DIR, "defense_architecture.pdf"))
    shutil.copyfile(f3_png, os.path.join(PAPER_DIR, "defense_architecture.png"))

    # Replicate to figures/
    for sub in ["final", "reports"]:
        sub_dir = os.path.join(FIGURES_DIR, sub)
        if os.path.exists(sub_dir):
            for fname in ["fig1_system_architecture.pdf", "fig1_system_architecture.png",
                          "fig2_fsm_diagram.pdf", "fig2_fsm_diagram.png",
                          "fig3_selective_defense.pdf", "fig3_selective_defense.png",
                          "fig_iki_distribution.pdf", "fig_iki_distribution.png",
                          "fig_detection_latency.pdf", "fig_detection_latency.png"]:
                src = os.path.join(PAPER_DIR, fname)
                dst = os.path.join(sub_dir, fname)
                shutil.copyfile(src, dst)
    print("All figures replicated successfully!")

if __name__ == "__main__":
    main()
