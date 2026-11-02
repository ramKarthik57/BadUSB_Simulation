import os
import pymupdf

FIG_SOURCE = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\figures\source"
FIG_FINAL = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\figures\final"
PAPER_DIR = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper"

# ========================================================
# FIGURE 1: SYSTEM ARCHITECTURE (Harmonized & Polished)
# ========================================================
svg_fig1 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 180" width="760" height="180" style="background:#ffffff; font-family:Helvetica, Arial, sans-serif;">
  <defs>
    <marker id="arr_purple" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#9333ea" />
    </marker>
    <marker id="arr_green" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#16a34a" />
    </marker>
    <marker id="arr_blue" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#2563eb" />
    </marker>
    <marker id="arr_red" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#ef4444" />
    </marker>
    <marker id="arr_orange" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#ea580c" />
    </marker>
  </defs>

  <!-- TIER 1: MOBILE C2 CONTROLLER (x: 14 to 186, width: 172) -->
  <rect x="14" y="8" width="172" height="164" rx="5" fill="#faf5ff" stroke="#a855f7" stroke-width="1.2"/>
  <text x="100" y="24" font-size="10.0" font-weight="bold" fill="#6b21a8" text-anchor="middle">Tier 1: Mobile C2 Controller</text>
  
  <rect x="24" y="34" width="152" height="34" rx="3.5" fill="#ffffff" stroke="#c084fc" stroke-width="0.9"/>
  <text x="100" y="48" font-size="9.0" font-weight="bold" fill="#1e293b" text-anchor="middle">Touch Web Console</text>
  <text x="100" y="60" font-size="7.5" fill="#64748b" text-anchor="middle">Single-Page App (SPA)</text>
  
  <rect x="24" y="78" width="152" height="34" rx="3.5" fill="#ffffff" stroke="#c084fc" stroke-width="0.9"/>
  <text x="100" y="92" font-size="9.0" font-weight="bold" fill="#1e293b" text-anchor="middle">REST Attack Engine</text>
  <text x="100" y="104" font-size="7.5" fill="#64748b" text-anchor="middle">Scenarios 1–4, Cadence Jitter</text>
  
  <rect x="24" y="122" width="152" height="34" rx="3.5" fill="#ffffff" stroke="#c084fc" stroke-width="0.9"/>
  <text x="100" y="136" font-size="9.0" font-weight="bold" fill="#1e293b" text-anchor="middle">802.11 b/g/n Station</text>
  <text x="100" y="148" font-size="7.5" fill="#64748b" text-anchor="middle">Station Link (192.168.4.1)</text>

  <line x1="100" y1="68" x2="100" y2="76" stroke="#a855f7" stroke-width="1.0" marker-end="url(#arr_purple)"/>
  <line x1="100" y1="112" x2="100" y2="120" stroke="#a855f7" stroke-width="1.0" marker-end="url(#arr_purple)"/>

  <!-- INTER-TIER 1 -> 2: 2.4 GHz SoftAP RF Link (gap: 186 to 246 = 60pt, y = 136) -->
  <line x1="186" y1="136" x2="244" y2="136" stroke="#9333ea" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arr_purple)"/>
  <rect x="191" y="122" width="50" height="28" rx="2.5" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.6"/>
  <text x="216" y="133" font-size="7.0" font-weight="bold" fill="#7e22ce" text-anchor="middle">2.4 GHz</text>
  <text x="216" y="143" font-size="6.5" fill="#475569" text-anchor="middle">SoftAP RF</text>

  <!-- TIER 2: WEAPONIZED ESP32-S3 (x: 246 to 514, width: 268) -->
  <rect x="246" y="8" width="268" height="164" rx="5" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.2"/>
  <text x="380" y="24" font-size="10.0" font-weight="bold" fill="#15803d" text-anchor="middle">Tier 2: Weaponized ESP32-S3 Hardware Implant</text>

  <rect x="256" y="34" width="118" height="38" rx="3.5" fill="#ffffff" stroke="#4ade80" stroke-width="0.9"/>
  <text x="315" y="48" font-size="8.8" font-weight="bold" fill="#1e293b" text-anchor="middle">Core 0: Network</text>
  <text x="315" y="59" font-size="7.2" fill="#64748b" text-anchor="middle">SoftAP &amp; Web Server</text>
  <text x="315" y="68" font-size="7.0" fill="#64748b" text-anchor="middle">TCP/IP Stack Baseband</text>

  <rect x="386" y="34" width="118" height="38" rx="3.5" fill="#ffffff" stroke="#4ade80" stroke-width="0.9"/>
  <text x="445" y="48" font-size="8.8" font-weight="bold" fill="#1e293b" text-anchor="middle">Core 1: HID Engine</text>
  <text x="445" y="59" font-size="7.2" fill="#64748b" text-anchor="middle">8-State Scenario FSM</text>
  <text x="445" y="68" font-size="7.0" fill="#64748b" text-anchor="middle">Native TinyUSB HID</text>

  <!-- Inter-Core Mailbox -->
  <rect x="256" y="80" width="248" height="24" rx="3.5" fill="#dcfce7" stroke="#16a34a" stroke-width="0.9"/>
  <text x="380" y="95" font-size="8.0" font-weight="bold" fill="#14532d" text-anchor="middle">FreeRTOS Spinlock Mailbox (portMUX, Ring Buffer)</text>

  <rect x="256" y="116" width="118" height="38" rx="3.5" fill="#ffffff" stroke="#4ade80" stroke-width="0.9"/>
  <text x="315" y="130" font-size="8.8" font-weight="bold" fill="#1e293b" text-anchor="middle">2.4 GHz Antenna</text>
  <text x="315" y="141" font-size="7.2" fill="#64748b" text-anchor="middle">SoftAP Transceiver</text>
  <text x="315" y="150" font-size="7.0" fill="#64748b" text-anchor="middle">Station Beacon Link</text>

  <rect x="386" y="116" width="118" height="38" rx="3.5" fill="#fff7ed" stroke="#ea580c" stroke-width="0.9"/>
  <text x="445" y="130" font-size="8.8" font-weight="bold" fill="#9a3412" text-anchor="middle">Native USB OTG PHY</text>
  <text x="445" y="141" font-size="7.2" fill="#ea580c" text-anchor="middle">GPIO 19/20 (D+/D-)</text>
  <text x="445" y="150" font-size="7.0" fill="#ea580c" text-anchor="middle">Hardware BOOT Latch</text>

  <line x1="315" y1="72" x2="315" y2="78" stroke="#16a34a" stroke-width="1.0" marker-end="url(#arr_green)"/>
  <line x1="445" y1="72" x2="445" y2="78" stroke="#16a34a" stroke-width="1.0" marker-end="url(#arr_green)"/>
  <line x1="315" y1="104" x2="315" y2="114" stroke="#16a34a" stroke-width="1.0" marker-end="url(#arr_green)"/>
  <line x1="445" y1="104" x2="445" y2="114" stroke="#ea580c" stroke-width="1.0" marker-end="url(#arr_orange)"/>

  <!-- INTER-TIER 2 -> 3: USB 2.0 Bus (gap: 514 to 574 = 60pt, y = 136) -->
  <line x1="514" y1="136" x2="572" y2="136" stroke="#2563eb" stroke-width="1.5" marker-end="url(#arr_blue)"/>
  <rect x="519" y="122" width="50" height="28" rx="2.5" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.6"/>
  <text x="544" y="133" font-size="7.0" font-weight="bold" fill="#1d4ed8" text-anchor="middle">USB 2.0</text>
  <text x="544" y="143" font-size="6.5" fill="#475569" text-anchor="middle">12 Mbps HID</text>

  <!-- TIER 3: WINDOWS HOST (x: 574 to 746, width: 172) -->
  <rect x="574" y="8" width="172" height="164" rx="5" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.2"/>
  <text x="660" y="24" font-size="9.5" font-weight="bold" fill="#1d4ed8" text-anchor="middle">Tier 3: Windows Host (WHID-Guard)</text>

  <rect x="584" y="32" width="152" height="26" rx="3.5" fill="#fef2f2" stroke="#ef4444" stroke-width="0.9"/>
  <text x="660" y="44" font-size="8.2" font-weight="bold" fill="#991b1b" text-anchor="middle">Selective Filter Gate (WH_KEYBOARD_LL)</text>
  <text x="660" y="53" font-size="6.8" fill="#b91c1c" text-anchor="middle">[PASS] Operator Keys / [DROP] Rogue</text>

  <rect x="584" y="66" width="152" height="26" rx="3.5" fill="#ffffff" stroke="#ef4444" stroke-width="0.9"/>
  <text x="660" y="78" font-size="8.2" font-weight="bold" fill="#991b1b" text-anchor="middle">Quarantine Table &amp; Policy Gate</text>
  <text x="660" y="87" font-size="6.8" fill="#64748b" text-anchor="middle">Isolates Rogue h_rogue (15s Auto-Reset)</text>

  <rect x="584" y="100" width="152" height="26" rx="3.5" fill="#ffffff" stroke="#60a5fa" stroke-width="0.9"/>
  <text x="660" y="112" font-size="8.2" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Behavioral Dynamics Engine (W=10)</text>
  <text x="660" y="121" font-size="6.8" fill="#64748b" text-anchor="middle">Evaluates μ &lt; 25ms ∨ CV &lt; 0.15</text>

  <rect x="584" y="134" width="152" height="26" rx="3.5" fill="#ffffff" stroke="#60a5fa" stroke-width="0.9"/>
  <text x="660" y="146" font-size="8.2" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Raw Input Monitor (WM_INPUT)</text>
  <text x="660" y="155" font-size="6.8" fill="#64748b" text-anchor="middle">Hardware Attribution to Origin h_dev</text>

  <!-- Clean vertical flow inside Tier 3 -->
  <line x1="660" y1="134" x2="660" y2="128" stroke="#3b82f6" stroke-width="1.0" marker-end="url(#arr_blue)"/>
  <line x1="660" y1="100" x2="660" y2="94" stroke="#ef4444" stroke-width="1.0" marker-end="url(#arr_red)"/>
  <line x1="660" y1="66" x2="660" y2="60" stroke="#ef4444" stroke-width="1.0" marker-end="url(#arr_red)"/>
</svg>"""

with open(os.path.join(FIG_SOURCE, "fig1_system_architecture.svg"), "w", encoding="utf-8") as f:
    f.write(svg_fig1)


# ========================================================
# FIGURE 2: ADVERSARIAL SCENARIO FSM (Harmonized & Polished)
# ========================================================
svg_fig2 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 180" width="760" height="180" style="background:#ffffff; font-family:Helvetica, Arial, sans-serif;">
  <defs>
    <marker id="arr_black" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#1e293b" />
    </marker>
    <marker id="arr_blue" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#2563eb" />
    </marker>
    <marker id="arr_green" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#16a34a" />
    </marker>
    <marker id="arr_red" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#ef4444" />
    </marker>
    <marker id="arr_orange" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#ea580c" />
    </marker>
  </defs>

  <!-- Start token -->
  <circle cx="18" cy="52" r="6" fill="#1e293b"/>
  <line x1="24" y1="52" x2="42" y2="52" stroke="#1e293b" stroke-width="1.2" marker-end="url(#arr_black)"/>

  <!-- TOP ROW STATES -->
  <!-- 1. BOOTING -->
  <rect x="44" y="32" width="110" height="40" rx="4" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.0"/>
  <text x="99" y="47" font-size="8.8" font-weight="bold" fill="#1e3a8a" text-anchor="middle">STATE_BOOTING</text>
  <text x="99" y="60" font-size="7.2" fill="#64748b" text-anchor="middle">Power-On &amp; USB Init</text>

  <!-- 2. USB_WAIT -->
  <rect x="194" y="32" width="110" height="40" rx="4" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.0"/>
  <text x="249" y="47" font-size="8.8" font-weight="bold" fill="#1e3a8a" text-anchor="middle">STATE_USB_WAIT</text>
  <text x="249" y="60" font-size="7.2" fill="#64748b" text-anchor="middle">Host Enum Δt ≥ 3.5s</text>

  <!-- 3. STARTUP_PAYLOAD -->
  <rect x="344" y="32" width="136" height="40" rx="4" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.0"/>
  <text x="412" y="47" font-size="8.0" font-weight="bold" fill="#1e3a8a" text-anchor="middle">STATE_STARTUP_PAYLOAD</text>
  <text x="412" y="60" font-size="7.2" fill="#64748b" text-anchor="middle">Scenario 1 Injection</text>

  <!-- 4. IDLE -->
  <rect x="518" y="32" width="106" height="40" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1.2"/>
  <text x="571" y="47" font-size="8.8" font-weight="bold" fill="#1e40af" text-anchor="middle">STATE_IDLE</text>
  <text x="571" y="60" font-size="7.2" fill="#475569" text-anchor="middle">Quiescent / Ready</text>

  <!-- 5. RUNNING -->
  <rect x="654" y="32" width="96" height="42" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.2"/>
  <text x="702" y="46" font-size="8.8" font-weight="bold" fill="#14532d" text-anchor="middle">STATE_RUNNING</text>
  <text x="702" y="58" font-size="7.2" fill="#166534" text-anchor="middle">Payload Active</text>
  <text x="702" y="68" font-size="6.8" fill="#15803d" text-anchor="middle">Quantum δt = 10ms</text>

  <!-- BOTTOM ROW STATES -->
  <!-- ERROR -->
  <rect x="194" y="122" width="110" height="40" rx="4" fill="#fff7ed" stroke="#ea580c" stroke-width="1.0"/>
  <text x="249" y="137" font-size="8.8" font-weight="bold" fill="#9a3412" text-anchor="middle">STATE_ERROR</text>
  <text x="249" y="150" font-size="7.2" fill="#64748b" text-anchor="middle">Watchdog / Bus Fault</text>

  <!-- STOPPED -->
  <rect x="518" y="122" width="106" height="40" rx="4" fill="#fef2f2" stroke="#ef4444" stroke-width="1.0"/>
  <text x="571" y="136" font-size="8.8" font-weight="bold" fill="#991b1b" text-anchor="middle">STATE_STOPPED</text>
  <text x="571" y="147" font-size="7.0" fill="#64748b" text-anchor="middle">Atomic Teardown</text>
  <text x="571" y="156" font-size="6.8" fill="#64748b" text-anchor="middle">releaseAll() Latches</text>

  <!-- STOPPING -->
  <rect x="654" y="122" width="96" height="40" rx="4" fill="#fef2f2" stroke="#ef4444" stroke-width="1.0"/>
  <text x="702" y="136" font-size="8.8" font-weight="bold" fill="#991b1b" text-anchor="middle">STATE_STOPPING</text>
  <text x="702" y="147" font-size="7.0" fill="#64748b" text-anchor="middle">Preempt Request</text>
  <text x="702" y="156" font-size="6.8" fill="#64748b" text-anchor="middle">Mailbox φ_stop = 1</text>

  <!-- TRANSITIONS -->
  <!-- Booting -> USB Wait -->
  <line x1="154" y1="52" x2="190" y2="52" stroke="#3b82f6" stroke-width="1.1" marker-end="url(#arr_blue)"/>
  <rect x="158" y="43" width="28" height="14" rx="2" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.5"/>
  <text x="172" y="53" font-size="6.8" fill="#1e3a8a" text-anchor="middle">Init OK</text>

  <!-- USB Wait -> Startup -->
  <line x1="304" y1="52" x2="340" y2="52" stroke="#3b82f6" stroke-width="1.1" marker-end="url(#arr_blue)"/>
  <rect x="307" y="43" width="31" height="14" rx="2" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.5"/>
  <text x="322" y="53" font-size="6.8" fill="#1e3a8a" text-anchor="middle">Enum OK</text>

  <!-- Startup -> Idle -->
  <line x1="480" y1="52" x2="514" y2="52" stroke="#3b82f6" stroke-width="1.1" marker-end="url(#arr_blue)"/>
  <rect x="486" y="43" width="24" height="14" rx="2" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.5"/>
  <text x="498" y="53" font-size="6.8" fill="#1e3a8a" text-anchor="middle">Done</text>

  <!-- Idle -> Running (Trigger) -->
  <line x1="624" y1="44" x2="650" y2="44" stroke="#2563eb" stroke-width="1.3" marker-end="url(#arr_blue)"/>
  <text x="637" y="40" font-size="6.5" font-weight="bold" fill="#1d4ed8" text-anchor="middle">REST/Pin</text>

  <!-- Running -> Idle (Normal complete) -->
  <line x1="654" y1="60" x2="628" y2="60" stroke="#16a34a" stroke-width="1.1" marker-end="url(#arr_green)"/>
  <text x="639" y="69" font-size="6.2" fill="#166534" text-anchor="middle">Complete</text>

  <!-- Running self-loop -->
  <path d="M 684,32 C 684,18 720,18 720,30" fill="none" stroke="#16a34a" stroke-width="1.0" marker-end="url(#arr_green)"/>
  <text x="702" y="16" font-size="6.5" fill="#15803d" text-anchor="middle">δt = 10ms</text>

  <!-- Running -> Stopping (Clean vertical down) -->
  <line x1="702" y1="74" x2="702" y2="118" stroke="#ef4444" stroke-width="1.3" marker-end="url(#arr_red)"/>
  <rect x="706" y="90" width="40" height="14" rx="2" fill="#ffffff" stroke="#fca5a5" stroke-width="0.5"/>
  <text x="726" y="100" font-size="6.5" font-weight="bold" fill="#991b1b" text-anchor="middle">Abort (φ=1)</text>

  <!-- Stopping -> Stopped (Clean horizontal left, centered label, no overlap) -->
  <line x1="654" y1="142" x2="628" y2="142" stroke="#ef4444" stroke-width="1.3" marker-end="url(#arr_red)"/>
  <text x="639" y="137" font-size="6.2" font-weight="bold" fill="#991b1b" text-anchor="middle">≤10ms</text>
  <text x="639" y="152" font-size="6.0" fill="#991b1b" text-anchor="middle">Kill</text>

  <!-- Stopped -> Idle (Clean vertical up) -->
  <line x1="571" y1="122" x2="571" y2="76" stroke="#2563eb" stroke-width="1.3" marker-end="url(#arr_blue)"/>
  <rect x="522" y="91" width="45" height="14" rx="2" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.5"/>
  <text x="544" y="101" font-size="6.8" fill="#1e40af" text-anchor="middle">Latches OK</text>

  <!-- USB Wait -> Error (Timeout down) -->
  <line x1="249" y1="72" x2="249" y2="118" stroke="#ea580c" stroke-width="1.1" stroke-dasharray="3,2" marker-end="url(#arr_orange)"/>
  <rect x="253" y="89" width="44" height="14" rx="2" fill="#ffffff" stroke="#fdba74" stroke-width="0.5"/>
  <text x="275" y="99" font-size="6.8" fill="#9a3412" text-anchor="middle">Enum Timeout</text>

  <!-- Error -> Booting (WDT Reboot) -->
  <path d="M 194,142 L 99,142 L 99,76" fill="none" stroke="#ea580c" stroke-width="1.1" stroke-dasharray="3,2" marker-end="url(#arr_orange)"/>
  <rect x="127" y="135" width="44" height="14" rx="2" fill="#ffffff" stroke="#fdba74" stroke-width="0.5"/>
  <text x="149" y="145" font-size="6.8" fill="#9a3412" text-anchor="middle">WDT Reboot</text>
</svg>"""

with open(os.path.join(FIG_SOURCE, "fig2_scenario_fsm.svg"), "w", encoding="utf-8") as f:
    f.write(svg_fig2)


# ========================================================
# FIGURE 3: SELECTIVE DEFENSE (Spacious Vertical Stack)
# ========================================================
svg_fig3 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 180" width="760" height="180" style="background:#ffffff; font-family:Helvetica, Arial, sans-serif;">
  <defs>
    <marker id="arr_blue" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#2563eb" />
    </marker>
    <marker id="arr_red" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#ef4444" />
    </marker>
    <marker id="arr_purple" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#9333ea" />
    </marker>
    <marker id="arr_green" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#16a34a" />
    </marker>
    <marker id="arr_orange" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#ea580c" />
    </marker>
  </defs>

  <!-- COLUMN 1: Physical Peripherals (x: 12 to 120) -->
  <rect x="12" y="32" width="108" height="38" rx="4" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.0"/>
  <text x="66" y="46" font-size="8.8" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Physical Keyboard</text>
  <text x="66" y="58" font-size="7.2" fill="#64748b" text-anchor="middle">Genuine HID (h_legit)</text>

  <rect x="12" y="112" width="108" height="38" rx="4" fill="#fef2f2" stroke="#ef4444" stroke-width="1.0"/>
  <text x="66" y="126" font-size="8.8" font-weight="bold" fill="#991b1b" text-anchor="middle">Rogue ESP32-S3</text>
  <text x="66" y="138" font-size="7.2" fill="#64748b" text-anchor="middle">BadUSB (h_rogue)</text>

  <!-- COLUMN 2: USB Root Hub (x: 138 to 162) -->
  <rect x="138" y="24" width="24" height="134" rx="3" fill="#f1f5f9" stroke="#64748b" stroke-width="1.0"/>
  <text x="150" y="94" font-size="8.5" font-weight="bold" fill="#334155" text-anchor="middle" transform="rotate(-90 150 94)">USB Root Hub</text>

  <line x1="120" y1="51" x2="136" y2="51" stroke="#2563eb" stroke-width="1.1" marker-end="url(#arr_blue)"/>
  <line x1="120" y1="131" x2="136" y2="131" stroke="#ef4444" stroke-width="1.1" marker-end="url(#arr_red)"/>

  <!-- HOST OS CONTAINER (x: 180 to 748, width: 568) -->
  <rect x="180" y="8" width="568" height="164" rx="5" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.0" stroke-dasharray="4,3"/>
  <text x="194" y="22" font-size="8.5" font-weight="bold" fill="#475569">Host OS Defense Daemon (WHID-Guard Framework)</text>

  <!-- COLUMN 3: Ingestion Channels (x: 194 to 312) -->
  <rect x="194" y="32" width="118" height="38" rx="4" fill="#ffffff" stroke="#3b82f6" stroke-width="1.0"/>
  <text x="253" y="46" font-size="8.8" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Low-Level Hook</text>
  <text x="253" y="58" font-size="7.2" fill="#64748b" text-anchor="middle">WH_KEYBOARD_LL</text>

  <rect x="194" y="112" width="118" height="38" rx="4" fill="#ffffff" stroke="#3b82f6" stroke-width="1.0"/>
  <text x="253" y="126" font-size="8.8" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Raw Input Monitor</text>
  <text x="253" y="138" font-size="7.2" fill="#64748b" text-anchor="middle">WM_INPUT (Origin h_dev)</text>

  <line x1="162" y1="51" x2="190" y2="51" stroke="#2563eb" stroke-width="1.1" marker-end="url(#arr_blue)"/>
  <line x1="162" y1="131" x2="190" y2="131" stroke="#2563eb" stroke-width="1.1" marker-end="url(#arr_blue)"/>

  <!-- COLUMN 4: Behavioral Dynamics Engine (x: 338 to 456) -->
  <rect x="338" y="108" width="118" height="44" rx="4" fill="#ffffff" stroke="#3b82f6" stroke-width="1.0"/>
  <text x="397" y="122" font-size="8.8" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Dynamics Engine</text>
  <text x="397" y="133" font-size="7.0" fill="#64748b" text-anchor="middle">Sliding Window (W = 10)</text>
  <text x="397" y="144" font-size="7.0" fill="#64748b" text-anchor="middle">Evaluates μ_IKI &amp; CV_IKI</text>

  <line x1="312" y1="131" x2="334" y2="131" stroke="#2563eb" stroke-width="1.1" marker-end="url(#arr_blue)"/>

  <!-- Scancode Stream (Low-Level Hook -> Filter Gate) -->
  <line x1="312" y1="51" x2="476" y2="51" stroke="#2563eb" stroke-width="1.1" marker-end="url(#arr_blue)"/>
  <rect x="366" y="42" width="66" height="15" rx="2" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.5"/>
  <text x="399" y="52" font-size="6.8" fill="#1e3a8a" text-anchor="middle">Scancode Stream</text>

  <!-- COLUMN 5: Defense & Enforcement Stack (x: 480 to 618) -->
  <!-- Top: Selective Filter Gate (y: 28 to 60, height: 32) -->
  <rect x="480" y="28" width="138" height="32" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1.2"/>
  <text x="549" y="42" font-size="8.8" font-weight="bold" fill="#1e40af" text-anchor="middle">Selective Filter Gate</text>
  <text x="549" y="53" font-size="7.0" fill="#1e3a8a" text-anchor="middle">Inspects h_origin ∈ Q_quar</text>

  <!-- Middle: Quarantine Table (y: 72 to 98, height: 26) -->
  <rect x="480" y="72" width="138" height="26" rx="4" fill="#fef2f2" stroke="#ef4444" stroke-width="1.0"/>
  <text x="549" y="84" font-size="8.2" font-weight="bold" fill="#991b1b" text-anchor="middle">Quarantine Table (Blacklist)</text>
  <text x="549" y="93" font-size="6.8" fill="#b91c1c" text-anchor="middle">Isolates Handle h_rogue</text>

  <!-- Bottom: Decision Boundary (y: 110 to 142, height: 32) -->
  <rect x="480" y="110" width="138" height="32" rx="4" fill="#faf5ff" stroke="#a855f7" stroke-width="1.0"/>
  <text x="549" y="123" font-size="8.5" font-weight="bold" fill="#6b21a8" text-anchor="middle">Decision Boundary</text>
  <text x="549" y="134" font-size="7.0" fill="#7e22ce" text-anchor="middle">μ &lt; 25ms ∨ CV &lt; 0.15</text>

  <!-- Watchdog Timer (y: 150 to 170, height: 20) -->
  <rect x="480" y="150" width="138" height="18" rx="3" fill="#fff7ed" stroke="#ea580c" stroke-width="0.9" stroke-dasharray="3,2"/>
  <text x="549" y="162" font-size="7.2" font-weight="bold" fill="#9a3412" text-anchor="middle">15s Watchdog (Auto-Reset)</text>

  <!-- Connectors in Stack: Generous 10-12 pt gaps -->
  <!-- Dynamics -> Decision -->
  <line x1="456" y1="126" x2="476" y2="126" stroke="#9333ea" stroke-width="1.1" marker-end="url(#arr_purple)"/>

  <!-- Decision -> Q-Tab (gap: 110 - 98 = 12 pt, arrow y: 110 -> 100) -->
  <line x1="549" y1="110" x2="549" y2="100" stroke="#ef4444" stroke-width="1.1" marker-end="url(#arr_red)"/>
  <rect x="418" y="86" width="56" height="14" rx="2" fill="#ffffff" stroke="#fca5a5" stroke-width="0.5"/>
  <text x="446" y="96" font-size="6.5" font-weight="bold" fill="#991b1b" text-anchor="middle">Lockdown (κ≥8)</text>

  <!-- Q-Tab -> Gate (gap: 72 - 60 = 12 pt, arrow y: 72 -> 62) -->
  <line x1="549" y1="72" x2="549" y2="62" stroke="#ef4444" stroke-width="1.1" marker-end="url(#arr_red)"/>

  <!-- WDT -> Decision (gap: 150 - 142 = 8 pt, arrow y: 150 -> 144) -->
  <line x1="549" y1="150" x2="549" y2="144" stroke="#ea580c" stroke-width="0.9" stroke-dasharray="2,2" marker-end="url(#arr_orange)"/>

  <!-- COLUMN 6: Enforcement Outputs (x: 648 to 740) -->
  <!-- Drop -->
  <rect x="648" y="24" width="92" height="28" rx="3.5" fill="#fee2e2" stroke="#ef4444" stroke-width="1.0"/>
  <text x="694" y="36" font-size="8.0" font-weight="bold" fill="#991b1b" text-anchor="middle">[DROP EVENT]</text>
  <text x="694" y="46" font-size="6.8" fill="#b91c1c" text-anchor="middle">Suppress Scancode</text>

  <!-- Pass -->
  <rect x="648" y="58" width="92" height="28" rx="3.5" fill="#dcfce7" stroke="#16a34a" stroke-width="1.0"/>
  <text x="694" y="70" font-size="8.0" font-weight="bold" fill="#166534" text-anchor="middle">[PASS EVENT]</text>
  <text x="694" y="80" font-size="6.8" fill="#15803d" text-anchor="middle">Allow Keystroke</text>

  <!-- Active Window -->
  <rect x="648" y="102" width="92" height="34" rx="3.5" fill="#f8fafc" stroke="#cbd5e1" stroke-width="0.9"/>
  <text x="694" y="116" font-size="8.0" font-weight="bold" fill="#334155" text-anchor="middle">Active Window</text>
  <text x="694" y="127" font-size="6.8" fill="#64748b" text-anchor="middle">Foreground Target</text>

  <!-- Routing from Gate to Outputs -->
  <path d="M 618,38 L 634,38 L 634,38 L 646,38" fill="none" stroke="#ef4444" stroke-width="1.1" marker-end="url(#arr_red)"/>
  <path d="M 618,52 L 634,52 L 634,72 L 646,72" fill="none" stroke="#16a34a" stroke-width="1.1" marker-end="url(#arr_green)"/>
  <line x1="694" y1="86" x2="694" y2="100" stroke="#16a34a" stroke-width="0.9" marker-end="url(#arr_green)"/>
</svg>"""

with open(os.path.join(FIG_SOURCE, "fig3_selective_defense.svg"), "w", encoding="utf-8") as f:
    f.write(svg_fig3)

print("Saved SVG sources for Figs 1, 2, 3.")

# Convert to PDF and PNG
for fname, p_out in [
    ("fig1_system_architecture", "system_architecture"),
    ("fig2_scenario_fsm", "fsm_diagram"),
    ("fig3_selective_defense", "defense_architecture")
]:
    svg_p = os.path.join(FIG_SOURCE, f"{fname}.svg")
    pdf_dest1 = os.path.join(FIG_FINAL, f"{fname}.pdf")
    png_dest1 = os.path.join(FIG_FINAL, f"{fname}.png")
    pdf_dest2 = os.path.join(PAPER_DIR, f"{p_out}.pdf")
    png_dest2 = os.path.join(PAPER_DIR, f"{p_out}.png")
    
    with open(svg_p, "rb") as f:
        svg_bytes = f.read()
    
    doc = pymupdf.open(stream=svg_bytes, filetype="svg")
    pdf_bytes = doc.convert_to_pdf()
    
    with open(pdf_dest1, "wb") as f:
        f.write(pdf_bytes)
    with open(pdf_dest2, "wb") as f:
        f.write(pdf_bytes)
        
    doc_pdf = pymupdf.open(pdf_dest1)
    page = doc_pdf[0]
    pix = page.get_pixmap(dpi=300)
    pix.save(png_dest1)
    pix.save(png_dest2)
    print(f"Generated {fname} -> {pdf_dest1} and PNG.")
