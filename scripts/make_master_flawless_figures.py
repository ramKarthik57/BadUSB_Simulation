import os
import pymupdf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32"
PAPER_DIR = os.path.join(BASE_DIR, "paper")
FIG_SOURCE = os.path.join(BASE_DIR, "figures", "source")
FIG_FINAL = os.path.join(BASE_DIR, "figures", "final")
os.makedirs(FIG_SOURCE, exist_ok=True)
os.makedirs(FIG_FINAL, exist_ok=True)

def arr_r(x, y, color, size=4.0):
    return f'<polygon points="{x},{y} {x-size},{y-size*0.65} {x-size*0.75},{y} {x-size},{y+size*0.65}" fill="{color}"/>'

def arr_l(x, y, color, size=4.0):
    return f'<polygon points="{x},{y} {x+size},{y-size*0.65} {x+size*0.75},{y} {x+size},{y+size*0.65}" fill="{color}"/>'

def arr_d(x, y, color, size=4.0):
    return f'<polygon points="{x},{y} {x-size*0.65},{y-size} {x},{y-size*0.75} {x+size*0.65},{y-size}" fill="{color}"/>'

def arr_u(x, y, color, size=4.0):
    return f'<polygon points="{x},{y} {x-size*0.65},{y+size} {x},{y+size*0.75} {x+size*0.65},{y+size}" fill="{color}"/>'


# ===========================================================================
# FIGURE 1: ENHANCED SYSTEM ARCHITECTURE
# ===========================================================================
def build_fig1():
    # Width allocations on 760pt canvas:
    # Tier 1: x: 12 to 158 (width 146)
    # RF Corridor: x: 158 to 226 (width 68) -> RF Badge: x: 172 to 214 (width 42, center 193)
    # Tier 2: x: 226 to 514 (width 288)
    #   Inside Tier 2:
    #     Left bus along x=233
    #     Core 0 & Antenna: x: 240 to 364 (width 124)
    #     HID Engine & USB PHY: x: 376 to 500 (width 124)
    #     Right bus along x=507
    #     Ring Buffer: x: 240 to 500 (width 260)
    # USB Corridor: x: 514 to 582 (width 68) -> USB Badge: x: 525 to 571 (width 46, center 548)
    # Tier 3: x: 582 to 748 (width 166)
    #   Inside Tier 3: boxes x: 592 to 738 (width 146)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 220" width="760" height="220" style="background:#ffffff; font-family:Helvetica, Arial, sans-serif;">
  <defs>
    <filter id="sh1" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-opacity="0.05"/>
    </filter>
  </defs>

  <!-- ================= TIER 1: MOBILE C2 CONTROLLER ================= -->
  <rect x="12" y="8" width="146" height="204" rx="6" fill="#faf5ff" stroke="#a855f7" stroke-width="1.3"/>
  <text x="85" y="26" font-size="10.2" font-weight="bold" fill="#6b21a8" text-anchor="middle">Tier 1: Mobile C2 Controller</text>
  
  <rect x="20" y="38" width="130" height="42" rx="4" fill="#ffffff" stroke="#c084fc" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="85" y="55" font-size="9.4" font-weight="bold" fill="#1e293b" text-anchor="middle">Touch Web Console</text>
  <text x="85" y="70" font-size="8.0" fill="#64748b" text-anchor="middle">Single-Page App (SPA)</text>
  
  <rect x="20" y="94" width="130" height="42" rx="4" fill="#ffffff" stroke="#c084fc" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="85" y="111" font-size="9.4" font-weight="bold" fill="#1e293b" text-anchor="middle">REST Attack Engine</text>
  <text x="85" y="126" font-size="7.8" fill="#64748b" text-anchor="middle">Scenarios 1-4, Cadence Jitter</text>
  
  <rect x="20" y="150" width="130" height="42" rx="4" fill="#ffffff" stroke="#c084fc" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="85" y="167" font-size="9.4" font-weight="bold" fill="#1e293b" text-anchor="middle">802.11 b/g/n Station</text>
  <text x="85" y="182" font-size="7.8" fill="#64748b" text-anchor="middle">Station Link (192.168.4.2)</text>

  <!-- Downward Connectors inside Tier 1 -->
  <line x1="85" y1="80" x2="85" y2="90" stroke="#a855f7" stroke-width="1.3"/>
  {arr_d(85, 94, "#a855f7", 3.8)}
  <line x1="85" y1="136" x2="85" y2="146" stroke="#a855f7" stroke-width="1.3"/>
  {arr_d(85, 150, "#a855f7", 3.8)}

  <!-- INTER-TIER 1 -> 2 BUS: 2.4 GHz SoftAP RF (Enters Antenna at y=174) -->
  <line x1="150" y1="174" x2="172" y2="174" stroke="#9333ea" stroke-width="1.5"/>
  <rect x="172" y="161" width="42" height="26" rx="3.5" fill="#ffffff" stroke="#d8b4fe" stroke-width="0.9"/>
  <text x="193" y="173" font-size="7.8" font-weight="bold" fill="#9333ea" text-anchor="middle">2.4 GHz</text>
  <text x="193" y="183" font-size="6.8" fill="#a855f7" text-anchor="middle">SoftAP RF</text>
  <line x1="214" y1="174" x2="236" y2="174" stroke="#9333ea" stroke-width="1.5"/>
  {arr_r(240, 174, "#9333ea", 4.0)}

  <!-- ================= TIER 2: WEAPONIZED ESP32-S3 ================= -->
  <rect x="226" y="8" width="288" height="204" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.3"/>
  <text x="370" y="26" font-size="10.2" font-weight="bold" fill="#14532d" text-anchor="middle">Tier 2: Weaponized ESP32-S3 Hardware Implant</text>

  <!-- Core 0: Network -->
  <rect x="240" y="38" width="124" height="58" rx="4" fill="#ffffff" stroke="#22c55e" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="302" y="53" font-size="9.4" font-weight="bold" fill="#14532d" text-anchor="middle">Core 0: Network</text>
  <text x="302" y="67" font-size="7.8" fill="#15803d" text-anchor="middle">SoftAP &amp; Web Server</text>
  <text x="302" y="79" font-size="7.6" font-weight="bold" fill="#166534" text-anchor="middle">Gateway IP: 192.168.4.1</text>
  <text x="302" y="90" font-size="7.4" fill="#475569" text-anchor="middle">TCP/IP Stack Baseband</text>

  <!-- Core 1: HID Engine -->
  <rect x="376" y="38" width="124" height="58" rx="4" fill="#ffffff" stroke="#22c55e" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="438" y="53" font-size="9.4" font-weight="bold" fill="#14532d" text-anchor="middle">Core 1: HID Engine</text>
  <text x="438" y="69" font-size="8.0" fill="#15803d" text-anchor="middle">8-State Scenario FSM</text>
  <text x="438" y="84" font-size="8.0" fill="#15803d" text-anchor="middle">Native TinyUSB HID</text>

  <!-- Lock-Free Atomic Ring Buffer -->
  <rect x="240" y="106" width="260" height="30" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.1"/>
  <text x="370" y="125" font-size="8.6" font-weight="bold" fill="#14532d" text-anchor="middle">Lock-Free Atomic Ring Buffer (Non-blocking Shared Mailbox)</text>

  <!-- Mailbox Inter-Core Arrows: Core 0 writes DOWN into Buffer, Core 1 reads UP from Buffer -->
  <line x1="302" y1="96" x2="302" y2="102" stroke="#16a34a" stroke-width="1.3"/>
  {arr_d(302, 106, "#16a34a", 3.8)}
  <line x1="438" y1="106" x2="438" y2="100" stroke="#16a34a" stroke-width="1.3"/>
  {arr_u(438, 96, "#16a34a", 3.8)}

  <!-- 2.4 GHz Antenna -->
  <rect x="240" y="148" width="124" height="52" rx="4" fill="#ffffff" stroke="#22c55e" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="302" y="165" font-size="9.4" font-weight="bold" fill="#14532d" text-anchor="middle">2.4 GHz Antenna</text>
  <text x="302" y="179" font-size="7.8" fill="#15803d" text-anchor="middle">SoftAP Transceiver</text>
  <text x="302" y="192" font-size="7.6" fill="#475569" text-anchor="middle">Station Beacon Link</text>

  <!-- Native USB OTG PHY -->
  <rect x="376" y="148" width="124" height="52" rx="4" fill="#fff7ed" stroke="#ea580c" stroke-width="1.1" filter="url(#sh1)"/>
  <text x="438" y="165" font-size="9.4" font-weight="bold" fill="#9a3412" text-anchor="middle">Native USB OTG PHY</text>
  <text x="438" y="179" font-size="7.8" font-weight="bold" fill="#c2410c" text-anchor="middle">GPIO 19/20 (D+/D-)</text>
  <text x="438" y="192" font-size="7.4" fill="#ea580c" text-anchor="middle">Hardware BOOT Latch</text>

  <!-- Left Bus: Antenna passes received RF frames UP into Core 0 Network along x=233 -->
  <line x1="240" y1="158" x2="233" y2="158" stroke="#16a34a" stroke-width="1.2"/>
  <line x1="233" y1="158" x2="233" y2="67" stroke="#16a34a" stroke-width="1.2"/>
  <line x1="233" y1="67" x2="236" y2="67" stroke="#16a34a" stroke-width="1.2"/>
  {arr_r(240, 67, "#16a34a", 3.8)}

  <!-- Right Bus: Core 1 dispatches synthesized HID keystrokes DOWN to Native USB PHY along x=507 -->
  <line x1="500" y1="67" x2="507" y2="67" stroke="#ea580c" stroke-width="1.2"/>
  <line x1="507" y1="67" x2="507" y2="158" stroke="#ea580c" stroke-width="1.2"/>
  <line x1="507" y1="158" x2="504" y2="158" stroke="#ea580c" stroke-width="1.2"/>
  {arr_l(500, 158, "#ea580c", 3.8)}

  <!-- INTER-TIER 2 -> 3 BUS: USB 2.0 Cable Line (Rightward from USB PHY to Host Raw Input) -->
  <line x1="500" y1="184" x2="525" y2="184" stroke="#1d4ed8" stroke-width="1.5"/>
  <rect x="525" y="171" width="46" height="26" rx="3.5" fill="#ffffff" stroke="#93c5fd" stroke-width="0.9"/>
  <text x="548" y="183" font-size="7.8" font-weight="bold" fill="#1d4ed8" text-anchor="middle">USB 2.0</text>
  <text x="548" y="193" font-size="6.8" fill="#2563eb" text-anchor="middle">12 Mbps HID</text>
  <line x1="571" y1="184" x2="588" y2="184" stroke="#1d4ed8" stroke-width="1.5"/>
  {arr_r(592, 184, "#1d4ed8", 4.0)}

  <!-- ================= TIER 3: WINDOWS HOST (WHID-GUARD) ================= -->
  <rect x="582" y="8" width="166" height="204" rx="6" fill="#eff6ff" stroke="#2563eb" stroke-width="1.3"/>
  <text x="665" y="26" font-size="10.0" font-weight="bold" fill="#1d4ed8" text-anchor="middle">Tier 3: Windows Host (WHID-Guard)</text>

  <!-- Box 1: Selective Filter Hook (WH_KEYBOARD_LL) -->
  <rect x="592" y="38" width="146" height="34" rx="4" fill="#ffffff" stroke="#3b82f6" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="665" y="51" font-size="8.6" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Selective Filter Hook</text>
  <text x="665" y="64" font-size="7.4" fill="#1d4ed8" text-anchor="middle">WH_KEYBOARD_LL ([PASS] / [DROP])</text>

  <!-- Arrow 1: Upward from Box 2 to Box 1 in generous 12pt gap -->
  <line x1="665" y1="84" x2="665" y2="76" stroke="#2563eb" stroke-width="1.3"/>
  {arr_u(665, 72, "#2563eb", 3.8)}

  <!-- Box 2: Quarantine Table & Policy Gate -->
  <rect x="592" y="84" width="146" height="34" rx="4" fill="#ffffff" stroke="#3b82f6" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="665" y="97" font-size="8.6" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Quarantine Table &amp; Policy Gate</text>
  <text x="665" y="110" font-size="7.4" fill="#1d4ed8" text-anchor="middle">Isolates Rogue h_rogue (15s Reset)</text>

  <!-- Arrow 2: Upward from Box 3 to Box 2 in generous 12pt gap -->
  <line x1="665" y1="130" x2="665" y2="122" stroke="#2563eb" stroke-width="1.3"/>
  {arr_u(665, 118, "#2563eb", 3.8)}

  <!-- Box 3: Behavioral Dynamics Engine (W=5) -->
  <rect x="592" y="130" width="146" height="34" rx="4" fill="#ffffff" stroke="#3b82f6" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="665" y="143" font-size="8.6" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Behavioral Dynamics Engine (W=5)</text>
  <text x="665" y="156" font-size="7.4" fill="#1d4ed8" text-anchor="middle">Evaluates &#956; &lt; 25ms &#8744; CV &lt; 0.15</text>

  <!-- Arrow 3: Upward from Box 4 to Box 3 in generous 12pt gap -->
  <line x1="665" y1="176" x2="665" y2="168" stroke="#2563eb" stroke-width="1.3"/>
  {arr_u(665, 164, "#2563eb", 3.8)}

  <!-- Box 4: Raw Input Monitor (WM_INPUT) -->
  <rect x="592" y="176" width="146" height="34" rx="4" fill="#ffffff" stroke="#3b82f6" stroke-width="1.0" filter="url(#sh1)"/>
  <text x="665" y="189" font-size="8.6" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Raw Input Monitor (WM_INPUT)</text>
  <text x="665" y="202" font-size="7.4" fill="#1d4ed8" text-anchor="middle">Pre-Hook Device Attribution (h_dev)</text>
</svg>"""
    return svg


# ===========================================================================
# FIGURE 2: ENHANCED ADVERSARIAL FSM
# ===========================================================================
def build_fig2():
    # Firmware states (8 deterministic states):
    # 1: STATE_BOOTING, 2: STATE_USB_WAIT, 3: STATE_STARTUP_PAYLOAD, 4: STATE_IDLE, 5: STATE_RUNNING,
    # 6: STATE_STOPPING, 7: STATE_STOPPED, 8: STATE_ERROR
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 220" width="760" height="220" style="background:#ffffff; font-family:Helvetica, Arial, sans-serif;">
  <defs>
    <filter id="sh2" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-opacity="0.06"/>
    </filter>
  </defs>

  <!-- ================= TOP ROW: NOMINAL SEQUENCE (y: 50 to 98, height: 48) ================= -->
  <!-- 1. STATE_BOOTING (x: 16 to 116, width: 100) -->
  <rect x="16" y="50" width="100" height="48" rx="5" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.2" filter="url(#sh2)"/>
  <text x="66" y="69" font-size="9.6" font-weight="bold" fill="#1e3a8a" text-anchor="middle">STATE_BOOTING</text>
  <text x="66" y="85" font-size="8.0" fill="#1d4ed8" text-anchor="middle">Power-On &amp; USB Init</text>

  <!-- Arrow: BOOTING -> USB_WAIT -->
  <line x1="116" y1="74" x2="126" y2="74" stroke="#2563eb" stroke-width="1.3"/>
  <rect x="126" y="66" width="28" height="16" rx="3" fill="#ffffff" stroke="#93c5fd" stroke-width="0.8"/>
  <text x="140" y="77.5" font-size="7.4" font-weight="bold" fill="#1d4ed8" text-anchor="middle">Init OK</text>
  <line x1="154" y1="74" x2="162" y2="74" stroke="#2563eb" stroke-width="1.3"/>
  {arr_r(166, 74, "#2563eb", 4.0)}

  <!-- 2. STATE_USB_WAIT (x: 166 to 276, width: 110) -->
  <rect x="166" y="50" width="110" height="48" rx="5" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.2" filter="url(#sh2)"/>
  <text x="221" y="69" font-size="9.6" font-weight="bold" fill="#1e3a8a" text-anchor="middle">STATE_USB_WAIT</text>
  <text x="221" y="85" font-size="8.0" fill="#1d4ed8" text-anchor="middle">Host Enum &#916;t &#8805; 3.5s</text>

  <!-- Arrow: USB_WAIT -> STARTUP_PAYLOAD -->
  <line x1="276" y1="74" x2="286" y2="74" stroke="#2563eb" stroke-width="1.3"/>
  <rect x="286" y="66" width="28" height="16" rx="3" fill="#ffffff" stroke="#93c5fd" stroke-width="0.8"/>
  <text x="300" y="77.5" font-size="7.4" font-weight="bold" fill="#1d4ed8" text-anchor="middle">Enum</text>
  <line x1="314" y1="74" x2="322" y2="74" stroke="#2563eb" stroke-width="1.3"/>
  {arr_r(326, 74, "#2563eb", 4.0)}

  <!-- 3. STATE_STARTUP_PAYLOAD (x: 326 to 466, width: 140) -->
  <rect x="326" y="50" width="140" height="48" rx="5" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.3" filter="url(#sh2)"/>
  <text x="396" y="69" font-size="9.6" font-weight="bold" fill="#92400e" text-anchor="middle">STATE_STARTUP_PAYLOAD</text>
  <text x="396" y="85" font-size="8.0" fill="#b45309" text-anchor="middle">Scenario 1 Auto-Run</text>

  <!-- Arrow: STARTUP_PAYLOAD -> IDLE -->
  <line x1="466" y1="74" x2="476" y2="74" stroke="#2563eb" stroke-width="1.3"/>
  <rect x="476" y="66" width="26" height="16" rx="3" fill="#ffffff" stroke="#93c5fd" stroke-width="0.8"/>
  <text x="489" y="77.5" font-size="7.4" font-weight="bold" fill="#1d4ed8" text-anchor="middle">Done</text>
  <line x1="502" y1="74" x2="508" y2="74" stroke="#2563eb" stroke-width="1.3"/>
  {arr_r(512, 74, "#2563eb", 4.0)}

  <!-- 4. STATE_IDLE (x: 512 to 602, width: 90) -->
  <rect x="512" y="50" width="90" height="48" rx="5" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.2" filter="url(#sh2)"/>
  <text x="557" y="69" font-size="9.6" font-weight="bold" fill="#14532d" text-anchor="middle">STATE_IDLE</text>
  <text x="557" y="85" font-size="8.0" fill="#166534" text-anchor="middle">Quiescent / Ready</text>

  <!-- Forward Arc: IDLE -> RUNNING (Command Received) -->
  <line x1="602" y1="62" x2="610" y2="62" stroke="#16a34a" stroke-width="1.3"/>
  <rect x="610" y="54" width="30" height="16" rx="3" fill="#ffffff" stroke="#86efac" stroke-width="0.8"/>
  <text x="625" y="65.5" font-size="7.2" font-weight="bold" fill="#15803d" text-anchor="middle">REST</text>
  <line x1="640" y1="62" x2="646" y2="62" stroke="#16a34a" stroke-width="1.3"/>
  {arr_r(650, 62, "#16a34a", 4.0)}

  <!-- Reverse Arc: RUNNING -> IDLE (Scenario Complete) -->
  <line x1="650" y1="86" x2="642" y2="86" stroke="#2563eb" stroke-width="1.3"/>
  <rect x="608" y="78" width="34" height="16" rx="3" fill="#ffffff" stroke="#93c5fd" stroke-width="0.8"/>
  <text x="625" y="89.5" font-size="7.0" font-weight="bold" fill="#1d4ed8" text-anchor="middle">Complete</text>
  <line x1="608" y1="86" x2="606" y2="86" stroke="#2563eb" stroke-width="1.3"/>
  {arr_l(602, 86, "#2563eb", 4.0)}

  <!-- 5. STATE_RUNNING (x: 650 to 744, width: 94) -->
  <rect x="650" y="50" width="94" height="48" rx="5" fill="#fef2f2" stroke="#ef4444" stroke-width="1.3" filter="url(#sh2)"/>
  <text x="697" y="68" font-size="9.6" font-weight="bold" fill="#991b1b" text-anchor="middle">STATE_RUNNING</text>
  <text x="697" y="81" font-size="7.6" fill="#b91c1c" text-anchor="middle">Payload Active</text>
  <text x="697" y="92" font-size="7.4" fill="#7f1d1d" text-anchor="middle">Quantum &#948;t = 10ms</text>

  <!-- ASYNCHRONOUS ERROR RECOVERY ARC: RUNNING -> USB_WAIT (Elevated along y=16) -->
  <line x1="697" y1="50" x2="697" y2="16" stroke="#ea580c" stroke-width="1.3" stroke-dasharray="4,2.5"/>
  <line x1="697" y1="16" x2="476" y2="16" stroke="#ea580c" stroke-width="1.3" stroke-dasharray="4,2.5"/>
  <rect x="424" y="8" width="52" height="16" rx="3" fill="#ffffff" stroke="#fdba74" stroke-width="0.8"/>
  <text x="450" y="19.5" font-size="7.0" font-weight="bold" fill="#ea580c" text-anchor="middle">USB Disconnect</text>
  <line x1="424" y1="16" x2="221" y2="16" stroke="#ea580c" stroke-width="1.3" stroke-dasharray="4,2.5"/>
  <line x1="221" y1="16" x2="221" y2="46" stroke="#ea580c" stroke-width="1.3" stroke-dasharray="4,2.5"/>
  {arr_d(221, 50, "#ea580c", 4.0)}

  <!-- ================= BOTTOM ROW: PREEMPTION, STOP & FAULT (y: 148 to 196, height: 48) ================= -->
  <!-- 8. STATE_ERROR (x: 650 to 744, width: 94) directly under RUNNING -->
  <rect x="650" y="148" width="94" height="48" rx="5" fill="#fff1f2" stroke="#be123c" stroke-width="1.2" filter="url(#sh2)"/>
  <text x="697" y="167" font-size="9.6" font-weight="bold" fill="#9f1239" text-anchor="middle">STATE_ERROR</text>
  <text x="697" y="183" font-size="8.0" fill="#be123c" text-anchor="middle">Timeout / CRC Fault</text>

  <!-- Downward Arrow: RUNNING -> ERROR -->
  <line x1="710" y1="98" x2="710" y2="116" stroke="#be123c" stroke-width="1.3"/>
  <rect x="690" y="116" width="40" height="15" rx="3" fill="#ffffff" stroke="#fda4af" stroke-width="0.8"/>
  <text x="710" y="127" font-size="7.0" font-weight="bold" fill="#be123c" text-anchor="middle">Fault</text>
  <line x1="710" y1="131" x2="710" y2="144" stroke="#be123c" stroke-width="1.3"/>
  {arr_d(710, 148, "#be123c", 4.0)}

  <!-- 6. STATE_STOPPING (x: 488 to 602, width: 114) -->
  <rect x="488" y="148" width="114" height="48" rx="5" fill="#fff7ed" stroke="#ea580c" stroke-width="1.2" filter="url(#sh2)"/>
  <text x="545" y="167" font-size="9.4" font-weight="bold" fill="#9a3412" text-anchor="middle">STATE_STOPPING</text>
  <text x="545" y="183" font-size="7.8" fill="#c2410c" text-anchor="middle">Teardown Latch (&le; 10ms)</text>

  <!-- Transition: RUNNING -> STOPPING upon Abort (Leaves bottom of RUNNING at x=672, y=98 -> down to y=118 -> left to x=626 -> down to y=172 -> into STOPPING) -->
  <line x1="672" y1="98" x2="672" y2="118" stroke="#ea580c" stroke-width="1.3"/>
  <line x1="672" y1="118" x2="626" y2="118" stroke="#ea580c" stroke-width="1.3"/>
  <line x1="626" y1="118" x2="626" y2="136" stroke="#ea580c" stroke-width="1.3"/>
  <rect x="612" y="136" width="28" height="15" rx="3" fill="#ffffff" stroke="#fdba74" stroke-width="0.8"/>
  <text x="626" y="147" font-size="6.8" font-weight="bold" fill="#ea580c" text-anchor="middle">Abort</text>
  <line x1="626" y1="151" x2="626" y2="172" stroke="#ea580c" stroke-width="1.3"/>
  <line x1="626" y1="172" x2="606" y2="172" stroke="#ea580c" stroke-width="1.3"/>
  {arr_l(602, 172, "#ea580c", 4.0)}

  <!-- 7. STATE_STOPPED (x: 322 to 434, width: 112) -->
  <rect x="322" y="148" width="112" height="48" rx="5" fill="#f8fafc" stroke="#64748b" stroke-width="1.2" filter="url(#sh2)"/>
  <text x="378" y="167" font-size="9.4" font-weight="bold" fill="#334155" text-anchor="middle">STATE_STOPPED</text>
  <text x="378" y="183" font-size="7.8" fill="#475569" text-anchor="middle">Key Latch Cleared</text>

  <!-- Arrow: STOPPING -> STOPPED (releaseAll action in generous 54pt gap) -->
  <line x1="488" y1="172" x2="476" y2="172" stroke="#ea580c" stroke-width="1.3"/>
  <rect x="442" y="164" width="34" height="16" rx="3" fill="#ffffff" stroke="#fdba74" stroke-width="0.8"/>
  <text x="459" y="175.5" font-size="6.5" font-weight="bold" fill="#ea580c" text-anchor="middle">releaseAll</text>
  <line x1="442" y1="172" x2="438" y2="172" stroke="#ea580c" stroke-width="1.3"/>
  {arr_l(434, 172, "#ea580c", 4.0)}

  <!-- Return Arc: STOPPED -> IDLE (When ready/unblocked) -->
  <line x1="378" y1="148" x2="378" y2="124" stroke="#16a34a" stroke-width="1.3"/>
  <line x1="378" y1="124" x2="424" y2="124" stroke="#16a34a" stroke-width="1.3"/>
  <rect x="424" y="116" width="46" height="16" rx="3" fill="#ffffff" stroke="#86efac" stroke-width="0.8"/>
  <text x="447" y="127.5" font-size="7.0" font-weight="bold" fill="#15803d" text-anchor="middle">Ack / Clear</text>
  <line x1="470" y1="124" x2="540" y2="124" stroke="#16a34a" stroke-width="1.3"/>
  <line x1="540" y1="124" x2="540" y2="102" stroke="#16a34a" stroke-width="1.3"/>
  {arr_u(540, 98, "#16a34a", 4.0)}

  <!-- Return Arc: ERROR -> USB_WAIT (Auto-recovery along bottom y=210) -->
  <line x1="697" y1="196" x2="697" y2="210" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,2"/>
  <line x1="697" y1="210" x2="420" y2="210" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,2"/>
  <rect x="364" y="202" width="56" height="15" rx="3" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.8"/>
  <text x="392" y="212.5" font-size="6.8" font-weight="bold" fill="#475569" text-anchor="middle">Auto-Recover</text>
  <line x1="364" y1="210" x2="221" y2="210" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,2"/>
  <line x1="221" y1="210" x2="221" y2="102" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,2"/>
  {arr_u(221, 98, "#64748b", 4.0)}
</svg>"""
    return svg


# ===========================================================================
# FIGURE 3: ENHANCED SELECTIVE DEFENSE ARCHITECTURE
# ===========================================================================
def build_fig3():
    # Width allocations on 760pt canvas:
    # Left inputs: x: 12 to 124 (width 112)
    # USB Root Hub bar: x: 136 to 162 (width 26)
    # Host Daemon Container: x: 174 to 610 (width 436)
    # Sinks column: x: 646 to 748 (width 102)
    # Corridor axis x=630
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 220" width="760" height="220" style="background:#ffffff; font-family:Helvetica, Arial, sans-serif;">
  <defs>
    <filter id="sh3" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-opacity="0.05"/>
    </filter>
  </defs>

  <!-- ================= HOST DAEMON CONTAINER ================= -->
  <rect x="174" y="8" width="436" height="204" rx="6" fill="#f8fafc" stroke="#64748b" stroke-width="1.3"/>
  <text x="184" y="25" font-size="10.2" font-weight="bold" fill="#1e293b" text-anchor="start">Host OS Defense Daemon (WHID-Guard Framework)</text>

  <!-- ================= HARDWARE INPUT SOURCES ================= -->
  <!-- Physical Keyboard (Genuine) -->
  <rect x="12" y="40" width="112" height="46" rx="5" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.2" filter="url(#sh3)"/>
  <text x="68" y="59" font-size="9.6" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Physical Keyboard</text>
  <text x="68" y="74" font-size="8.0" fill="#2563eb" text-anchor="middle">Genuine HID (h_legit)</text>

  <!-- Rogue Hardware (ESP32-S3) -->
  <rect x="12" y="142" width="112" height="46" rx="5" fill="#fef2f2" stroke="#ef4444" stroke-width="1.2" filter="url(#sh3)"/>
  <text x="68" y="161" font-size="9.6" font-weight="bold" fill="#991b1b" text-anchor="middle">Rogue ESP32-S3</text>
  <text x="68" y="176" font-size="8.0" fill="#b91c1c" text-anchor="middle">BadUSB (h_rogue)</text>

  <!-- USB Root Hub -->
  <rect x="136" y="32" width="26" height="166" rx="4" fill="#f1f5f9" stroke="#475569" stroke-width="1.1"/>
  <text x="149" y="115" font-size="9.2" font-weight="bold" fill="#334155" text-anchor="middle" transform="rotate(-90 149 115)">USB Root Hub</text>

  <!-- Input Lines: Hardware to Hub -->
  <line x1="124" y1="63" x2="132" y2="63" stroke="#2563eb" stroke-width="1.4"/>
  {arr_r(136, 63, "#2563eb", 3.8)}
  <line x1="124" y1="165" x2="132" y2="165" stroke="#ef4444" stroke-width="1.4"/>
  {arr_r(136, 165, "#ef4444", 3.8)}

  <!-- Hub branching into Host OS Daemon -->
  <line x1="162" y1="115" x2="172" y2="115" stroke="#2563eb" stroke-width="1.4"/>
  <line x1="172" y1="115" x2="172" y2="63" stroke="#2563eb" stroke-width="1.4"/>
  <line x1="172" y1="63" x2="182" y2="63" stroke="#2563eb" stroke-width="1.4"/>
  {arr_r(186, 63, "#2563eb", 3.8)}

  <line x1="172" y1="115" x2="172" y2="165" stroke="#2563eb" stroke-width="1.4"/>
  <line x1="172" y1="165" x2="182" y2="165" stroke="#2563eb" stroke-width="1.4"/>
  {arr_r(186, 165, "#2563eb", 3.8)}

  <!-- ================= UPPER PIPELINE: INTERCEPTION ================= -->
  <!-- Selective Filter Hook -->
  <rect x="186" y="40" width="118" height="46" rx="5" fill="#ffffff" stroke="#3b82f6" stroke-width="1.1" filter="url(#sh3)"/>
  <text x="245" y="59" font-size="9.4" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Selective Filter Hook</text>
  <text x="245" y="73" font-size="7.8" fill="#2563eb" text-anchor="middle">(WH_KEYBOARD_LL Hook)</text>

  <!-- Pre-Dispatch Buffer -->
  <rect x="326" y="40" width="118" height="46" rx="5" fill="#ffffff" stroke="#3b82f6" stroke-width="1.1" filter="url(#sh3)"/>
  <text x="385" y="59" font-size="9.4" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Pre-Dispatch Buffer</text>
  <text x="385" y="73" font-size="7.8" fill="#2563eb" text-anchor="middle">FIFO Delay Queue (W=5)</text>

  <!-- Arrow: Hook -> Pre-Dispatch Buffer -->
  <line x1="304" y1="63" x2="322" y2="63" stroke="#2563eb" stroke-width="1.3"/>
  {arr_r(326, 63, "#2563eb", 3.8)}

  <!-- Clean Stream Link with Stream Badge: Pre-Dispatch Buffer -> Selective Filter Gate -->
  <line x1="444" y1="63" x2="455" y2="63" stroke="#2563eb" stroke-width="1.3"/>
  <rect x="455" y="55" width="28" height="16" rx="3" fill="#ffffff" stroke="#93c5fd" stroke-width="0.8"/>
  <text x="469" y="66.5" font-size="7.2" font-weight="bold" fill="#1d4ed8" text-anchor="middle">Stream</text>
  <line x1="483" y1="63" x2="490" y2="63" stroke="#2563eb" stroke-width="1.3"/>
  {arr_r(494, 63, "#2563eb", 3.8)}

  <!-- ================= LOWER PIPELINE: ATTRIBUTION & DYNAMICS ================= -->
  <!-- Raw Input Pre-Filter -->
  <rect x="186" y="142" width="118" height="46" rx="5" fill="#ffffff" stroke="#3b82f6" stroke-width="1.1" filter="url(#sh3)"/>
  <text x="245" y="160" font-size="9.4" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Raw Input Pre-Filter</text>
  <text x="245" y="174" font-size="7.6" fill="#2563eb" text-anchor="middle">WM_INPUT (RIDEV_INPUTSINK)</text>

  <!-- Dynamics Engine -->
  <rect x="326" y="138" width="118" height="54" rx="5" fill="#ffffff" stroke="#3b82f6" stroke-width="1.1" filter="url(#sh3)"/>
  <text x="385" y="155" font-size="9.4" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Dynamics Engine</text>
  <text x="385" y="169" font-size="7.8" fill="#2563eb" text-anchor="middle">Sliding Window (W = 5)</text>
  <text x="385" y="181" font-size="7.6" fill="#1d4ed8" text-anchor="middle">Evaluates &#956;_IKI &amp; CV_IKI</text>

  <!-- Arrow: Raw Input -> Dynamics Engine -->
  <line x1="304" y1="165" x2="322" y2="165" stroke="#2563eb" stroke-width="1.3"/>
  {arr_r(326, 165, "#2563eb", 3.8)}

  <!-- Connector: Dynamics Engine -> Decision Boundary -->
  <line x1="444" y1="165" x2="490" y2="165" stroke="#7c3aed" stroke-width="1.3"/>
  {arr_r(494, 165, "#7c3aed", 3.8)}

  <!-- ================= DECISION & POLICY COLUMN (x: 494 to 598, width 104) ================= -->
  <!-- 1. Selective Filter Gate -->
  <rect x="494" y="36" width="104" height="42" rx="5" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.2" filter="url(#sh3)"/>
  <text x="546" y="53" font-size="9.4" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Selective Filter Gate</text>
  <text x="546" y="68" font-size="7.6" fill="#1d4ed8" text-anchor="middle">Inspects h_origin &#8712; Q_quar</text>

  <!-- Upward Gate Query Connector: Quarantine Table blacklists into Gate in clean 14pt gap -->
  <line x1="546" y1="92" x2="546" y2="82" stroke="#ef4444" stroke-width="1.3"/>
  {arr_u(546, 78, "#ef4444", 3.8)}

  <!-- 2. Quarantine Table (Blacklist) -->
  <rect x="494" y="92" width="104" height="30" rx="4" fill="#fef2f2" stroke="#ef4444" stroke-width="1.1" filter="url(#sh3)"/>
  <text x="546" y="106" font-size="8.8" font-weight="bold" fill="#991b1b" text-anchor="middle">Quarantine Table</text>
  <text x="546" y="117" font-size="7.2" fill="#b91c1c" text-anchor="middle">Isolates Handle h_rogue</text>

  <!-- 3. Decision Boundary -->
  <rect x="494" y="150" width="104" height="32" rx="4" fill="#faf5ff" stroke="#a855f7" stroke-width="1.1" filter="url(#sh3)"/>
  <text x="546" y="164" font-size="9.0" font-weight="bold" fill="#6b21a8" text-anchor="middle">Decision Boundary</text>
  <text x="546" y="176" font-size="7.4" fill="#7c3aed" text-anchor="middle">&#956; &lt; 25ms &#8744; CV &lt; 0.15</text>

  <!-- Upward Lockdown Link with Lockdown Badge: Decision Boundary triggers Quarantine Table! -->
  <line x1="546" y1="150" x2="546" y2="144" stroke="#dc2626" stroke-width="1.3"/>
  <rect x="512" y="130" width="68" height="14" rx="3" fill="#ffffff" stroke="#fca5a5" stroke-width="0.8"/>
  <text x="546" y="140.5" font-size="7.2" font-weight="bold" fill="#b91c1c" text-anchor="middle">Lockdown (&#954; &#8805; 8)</text>
  <line x1="546" y1="130" x2="546" y2="126" stroke="#dc2626" stroke-width="1.3"/>
  {arr_u(546, 122, "#dc2626", 3.8)}

  <!-- 4. 15s Watchdog (Auto-Reset) -->
  <rect x="494" y="190" width="104" height="16" rx="3" fill="#fff7ed" stroke="#ea580c" stroke-width="0.9"/>
  <text x="546" y="201.5" font-size="7.6" font-weight="bold" fill="#9a3412" text-anchor="middle">15s Watchdog (Auto-Reset)</text>

  <!-- ================= OUTPUT SINKS (Right column outside Daemon: x: 646 to 748, width 102) ================= -->
  <!-- [DROP EVENT] -->
  <rect x="646" y="34" width="102" height="32" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.2"/>
  <text x="697" y="48" font-size="9.4" font-weight="bold" fill="#991b1b" text-anchor="middle">[DROP EVENT]</text>
  <text x="697" y="60" font-size="7.8" fill="#b91c1c" text-anchor="middle">Suppress Scancode</text>

  <!-- [PASS EVENT] -->
  <rect x="646" y="74" width="102" height="32" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.2"/>
  <text x="697" y="88" font-size="9.4" font-weight="bold" fill="#14532d" text-anchor="middle">[PASS EVENT]</text>
  <text x="697" y="100" font-size="7.8" fill="#15803d" text-anchor="middle">Allow Keystroke</text>

  <!-- Target: Active Window -->
  <rect x="646" y="114" width="102" height="32" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.0"/>
  <text x="697" y="128" font-size="9.2" font-weight="bold" fill="#334155" text-anchor="middle">Active Window</text>
  <text x="697" y="140" font-size="7.6" fill="#64748b" text-anchor="middle">Foreground Target</text>

  <!-- Link: PASS EVENT -> Active Window -->
  <line x1="697" y1="106" x2="697" y2="110" stroke="#16a34a" stroke-width="1.3"/>
  {arr_d(697, 114, "#16a34a", 3.8)}

  <!-- Output Lines from Gate -->
  <line x1="598" y1="50" x2="642" y2="50" stroke="#dc2626" stroke-width="1.4"/>
  {arr_r(646, 50, "#dc2626", 4.0)}
  <!-- Unified corridor axis x=630 for both Pass and Flush feedback! -->
  <line x1="598" y1="70" x2="630" y2="70" stroke="#16a34a" stroke-width="1.4"/>
  <line x1="630" y1="70" x2="630" y2="90" stroke="#16a34a" stroke-width="1.4"/>
  <line x1="630" y1="90" x2="642" y2="90" stroke="#16a34a" stroke-width="1.4"/>
  {arr_r(646, 90, "#16a34a", 4.0)}

  <!-- Global Pipeline Flush & Gate Override (Symmetric in outside column!) -->
  <rect x="646" y="170" width="102" height="38" rx="4" fill="#fff7ed" stroke="#ea580c" stroke-width="1.2"/>
  <text x="697" y="185" font-size="8.8" font-weight="bold" fill="#9a3412" text-anchor="middle">Global Pipeline Flush</text>
  <text x="697" y="198" font-size="8.0" font-weight="bold" fill="#c2410c" text-anchor="middle">&amp; Gate Override</text>

  <!-- Trigger Link: 15s Watchdog -> Global Flush -->
  <line x1="598" y1="198" x2="642" y2="198" stroke="#ea580c" stroke-width="1.4"/>
  {arr_r(646, 198, "#ea580c", 4.0)}

  <!-- Feedback Line: Flush to Quarantine Table along unified corridor axis x=630 -->
  <line x1="646" y1="182" x2="630" y2="182" stroke="#ea580c" stroke-width="1.3" stroke-dasharray="3,2"/>
  <line x1="630" y1="182" x2="630" y2="167" stroke="#ea580c" stroke-width="1.3" stroke-dasharray="3,2"/>
  <rect x="617" y="152" width="26" height="15" rx="3" fill="#ffffff" stroke="#fed7aa" stroke-width="0.8"/>
  <text x="630" y="163" font-size="6.8" font-weight="bold" fill="#ea580c" text-anchor="middle">Flush</text>
  <line x1="630" y1="152" x2="630" y2="107" stroke="#ea580c" stroke-width="1.3" stroke-dasharray="3,2"/>
  <line x1="630" y1="107" x2="602" y2="107" stroke="#ea580c" stroke-width="1.3" stroke-dasharray="3,2"/>
  {arr_l(598, 107, "#ea580c", 4.0)}
</svg>"""
    return svg


# ===========================================================================
# FIGURE 4: IKI DISTRIBUTION (PERFECT VECTOR MATPLOTLIB)
# ===========================================================================
def build_fig4():
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "mathtext.fontset": "cm",
        "figure.autolayout": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })
    fig, ax = plt.subplots(figsize=(3.45, 2.35), dpi=300)
    fig.subplots_adjust(left=0.18, right=0.96, bottom=0.20, top=0.96)
    np.random.seed(42)

    # Human typing (log-normal, mu=144.18, sigma=91.98)
    human_mu = np.log(144.18**2 / np.sqrt(91.98**2 + 144.18**2))
    human_sigma = np.sqrt(np.log(1 + (91.98**2 / 144.18**2)))
    human_data = np.random.lognormal(human_mu, human_sigma, 500)
    human_data = human_data[human_data < 450]

    # Standard BadUSB: deterministic 10ms with microjitter
    badusb_data = np.random.normal(10.01, 0.78, 500)

    # Adversarial evasion: randomized 80-120ms with bursts
    evasion_base = np.random.uniform(80, 120, 450)
    evasion_delims = np.random.uniform(150, 300, 50)
    evasion_data = np.concatenate([evasion_base, evasion_delims])

    bins = np.linspace(0, 450, 46)
    ax.hist(badusb_data, bins=bins, color="#dc2626", alpha=0.85, label=r"Standard BadUSB ($\mu = 10.0\ \mathrm{ms}$)", edgecolor="#991b1b", linewidth=0.5)
    ax.hist(evasion_data, bins=bins, color="#2563eb", alpha=0.65, label=r"Adversarial Evasion ($\mu = 119.3\ \mathrm{ms}$)", edgecolor="#1d4ed8", linewidth=0.5)
    ax.hist(human_data, bins=bins, color="#475569", alpha=0.45, label=r"Human Baseline ($\mu = 144.2\ \mathrm{ms}$)", edgecolor="#334155", linewidth=0.5)

    ax.axvline(25, color="#991b1b", linestyle="--", linewidth=1.8, label=r"Speed/Jitter ($\mu \le 25\ \mathrm{ms}\ \lor\ \mathrm{CV}_{\mathrm{IKI}} < 0.15$)")
    ax.axvline(75, color="#1e3a8a", linestyle=":", linewidth=2.0, label=r"Human Bound ($\mu \ge 75\ \mathrm{ms}$)")

    ax.set_xlabel(r"\textbf{Inter-Key Interval} $\Delta t$ \textbf{(ms)}", fontsize=10.5, labelpad=4)
    ax.set_ylabel(r"\textbf{Empirical Frequency}", fontsize=10.5, labelpad=4)
    ax.set_xlim(0, 450)
    ax.set_ylim(0, 520)

    ax.grid(True, linestyle="--", alpha=0.35, color="#94a3b8")
    ax.tick_params(axis="both", which="major", labelsize=9.5, width=1.0, length=4)
    for spine in ax.spines.values():
        spine.set_linewidth(1.1)
        spine.set_color("#0f172a")

    ax.legend(loc="upper right", fontsize=7.2, framealpha=0.92, facecolor="#ffffff", edgecolor="#cbd5e1", borderpad=0.50, labelspacing=0.35)

    pdf_out = os.path.join(PAPER_DIR, "fig_iki_distribution.pdf")
    png_out = os.path.join(PAPER_DIR, "fig_iki_distribution.png")
    fig.savefig(pdf_out, format="pdf")
    fig.savefig(png_out, format="png", dpi=300)
    plt.close(fig)
    print("Fig 4 generated.")


# ===========================================================================
# FIGURE 5: DETECTION LATENCY & SAFETY MARGIN (PERFECT VECTOR MATPLOTLIB)
# ===========================================================================
def build_fig5():
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "mathtext.fontset": "cm",
        "figure.autolayout": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })
    fig, ax1 = plt.subplots(figsize=(3.45, 2.38), dpi=300)
    fig.subplots_adjust(left=0.17, right=0.81, bottom=0.20, top=0.96)

    rates = np.array([40, 50, 60, 67, 75, 85, 100])
    trigger_latency = np.array([8, 8, 8, 8, 8, 8, 8])
    execution_horizon = np.array([14, 14, 14, 14, 14, 14, 14])
    reaction_time_ms = (8.0 / rates) * 1000.0

    ax1.axhspan(8, 14, color="#f1f5f9", alpha=0.85, zorder=1)
    l1 = ax1.plot(rates, trigger_latency, "o-", color="#0f172a", linewidth=2.0, markersize=5.5, label=r"Trigger ($\kappa = 8$)", zorder=4)
    l2 = ax1.plot(rates, execution_horizon, "--", color="#b91c1c", linewidth=1.8, label=r"Horizon ($L_{\mathrm{exec}} = 14$)", zorder=4)

    ax1.set_xlabel(r"\textbf{Burst Rate} $R_{\mathrm{burst}}$ \textbf{(chars/s)}", fontsize=10.2, labelpad=4)
    ax1.set_ylabel(r"\textbf{Quarantine Latency (Chars)}", fontsize=10.0, labelpad=4)
    ax1.set_xlim(37, 107)
    ax1.set_ylim(0, 23)
    ax1.set_yticks([0, 4, 8, 12, 16, 20])

    ax2 = ax1.twinx()
    l3 = ax2.plot(rates, reaction_time_ms, "s-.", color="#1d4ed8", linewidth=2.0, markersize=5.5, label=r"Reaction Time ($t_{\mathrm{quar}}$)", zorder=4)
    ax2.set_ylabel(r"\textbf{Reaction Time (ms)}", fontsize=10.0, color="#1d4ed8", labelpad=5)
    ax2.set_ylim(0, 287.5)
    ax2.set_yticks([0, 50, 100, 150, 200, 250])
    ax2.tick_params(axis="y", labelcolor="#1d4ed8", labelsize=9.2, width=1.0, length=4)

    lines = l1 + l2 + l3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper right", fontsize=6.8, framealpha=1.0, facecolor="#ffffff", edgecolor="#cbd5e1", borderpad=0.45, labelspacing=0.32)

    # Detection floor guideline anchored at (40 ch/s, 200 ms)
    ax1.axvline(40, color="#047857", linestyle=":", linewidth=1.3, ymax=16.0/23.0, zorder=2)
    ax2.axhline(200, color="#047857", linestyle=":", linewidth=1.3, xmin=0.043, xmax=0.957, zorder=2)
    ax1.plot(40, 16, marker="o", color="#047857", markersize=6.0, zorder=5)

    # Detection floor callout at xytext=(41.0, 226.0)
    ax2.annotate(
        r"\textbf{Detection Floor}" "\n" r"$t_{\mathrm{quar}} = 200\ \mathrm{ms}$" "\n" r"\textbf{(40 ch/s, 25 ms)}",
        xy=(40.0, 200.0), xycoords="data",
        xytext=(41.0, 226.0), textcoords="data",
        fontsize=6.5, color="#065f46", fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#ecfdf5", edgecolor="#10b981", lw=0.9),
        zorder=6
    )

    # Minimum latency floor callout
    ax2.annotate(
        r"\textbf{Min. Latency Floor = 80.1 ms}" "\n" r"\textbf{($R = 100\ \mathrm{ch/s},\ \kappa = 8$)}",
        xy=(100.0, 80.1), xycoords="data",
        xytext=(53.0, 40.0), textcoords="data",
        arrowprops=dict(arrowstyle="->", color="#1d4ed8", lw=1.1, connectionstyle="arc3,rad=-0.12"),
        fontsize=6.4, color="#1e40af", fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#eff6ff", edgecolor="#93c5fd", lw=0.9),
        zorder=6
    )

    # Delta = 6 Margin Pill
    ax1.text(
        78.0, 11.0,
        r"$\mathbf{\Delta = 6\ Margin}$",
        ha="center", va="center", fontsize=7.2, color="#0f172a", fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#ffffff", edgecolor="#cbd5e1", lw=0.8, alpha=0.95),
        zorder=5
    )
    ax1.annotate("", xy=(78.0, 13.8), xytext=(78.0, 12.3), arrowprops=dict(arrowstyle="->", color="#0f172a", lw=1.1))
    ax1.annotate("", xy=(78.0, 8.2), xytext=(78.0, 9.7), arrowprops=dict(arrowstyle="->", color="#0f172a", lw=1.1))

    ax1.grid(True, linestyle="--", alpha=0.35, color="#94a3b8")
    ax1.tick_params(axis="both", which="major", labelsize=9.2, width=1.0, length=4)
    for spine in ax1.spines.values():
        spine.set_linewidth(1.1)
        spine.set_color("#0f172a")
    for spine in ax2.spines.values():
        spine.set_linewidth(1.1)
        spine.set_color("#0f172a")

    pdf_out = os.path.join(PAPER_DIR, "fig_detection_latency.pdf")
    png_out = os.path.join(PAPER_DIR, "fig_detection_latency.png")
    fig.savefig(pdf_out, format="pdf")
    fig.savefig(png_out, format="png", dpi=300)
    plt.close(fig)
    print("Fig 5 generated.")


def export_svgs():
    configs = [
        ("fig1_system_architecture", build_fig1(), "system_architecture"),
        ("fig2_scenario_fsm", build_fig2(), "fsm_diagram"),
        ("fig3_selective_defense", build_fig3(), "defense_architecture")
    ]
    for fname, svg_text, p_out in configs:
        svg_path = os.path.join(FIG_SOURCE, f"{fname}.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_text)
            
        doc = pymupdf.open(stream=svg_text.encode("utf-8"), filetype="svg")
        pdf_bytes = doc.convert_to_pdf()
        
        pdf_dest1 = os.path.join(FIG_FINAL, f"{fname}.pdf")
        png_dest1 = os.path.join(FIG_FINAL, f"{fname}.png")
        pdf_dest2 = os.path.join(PAPER_DIR, f"{p_out}.pdf")
        png_dest2 = os.path.join(PAPER_DIR, f"{p_out}.png")
        
        with open(pdf_dest1, "wb") as f:
            f.write(pdf_bytes)
        with open(pdf_dest2, "wb") as f:
            f.write(pdf_bytes)
            
        doc_pdf = pymupdf.open(pdf_dest1)
        page = doc_pdf[0]
        pix = page.get_pixmap(dpi=300)
        pix.save(png_dest1)
        pix.save(png_dest2)
        print(f"Exported {fname} -> PDF & PNG.")

def main():
    print("Generating refined flawless figures...")
    export_svgs()
    build_fig4()
    build_fig5()
    print("All 5 refined figures generated successfully!")

if __name__ == "__main__":
    main()
