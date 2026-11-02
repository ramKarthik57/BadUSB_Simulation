"""
Mermaid, Draw.io & Inkscape SVG Generator for Figure 2: Adversarial Scenario FSM
Creates:
  1. figures/source/fig2_scenario_fsm.mmd (Mermaid stateDiagram-v2)
  2. figures/source/fig2_scenario_fsm.drawio (Native draw.io XML)
  3. figures/source/fig2_scenario_fsm.svg (Inkscape-compliant SVG)
  4. paper/fsm_diagram.pdf & figures/final/fig2_scenario_fsm.pdf (Vector PDF)
"""

import os
import fitz

BASE_DIR = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32"
FIG_SOURCE = os.path.join(BASE_DIR, "figures", "source")
FIG_FINAL = os.path.join(BASE_DIR, "figures", "final")
PAPER_DIR = os.path.join(BASE_DIR, "paper")

# ---------------------------------------------------------------------------
# 1. Mermaid stateDiagram-v2 Definition
# ---------------------------------------------------------------------------
mermaid_code = '''stateDiagram-v2
    [*] --> STATE_BOOTING: Power On
    
    STATE_BOOTING: Power-On & USB Init
    STATE_USB_WAIT: Host Enum (Δt ≥ 3.5s)
    STATE_STARTUP_PAYLOAD: Scenario 1 Auto-Exec
    STATE_IDLE: Quiescent / C2 Listening
    STATE_RUNNING: Payload Exec (Quantum δt=10ms)
    STATE_STOPPING: Preempt Request (φ_stop=1)
    STATE_STOPPED: Atomic Teardown (releaseAll)
    STATE_ERROR: Watchdog / Bus Fault

    STATE_BOOTING --> STATE_USB_WAIT: Init OK
    STATE_USB_WAIT --> STATE_STARTUP_PAYLOAD: Enum Done
    STATE_STARTUP_PAYLOAD --> STATE_IDLE: Payload Done
    
    STATE_IDLE --> STATE_RUNNING: C2 REST / BOOT Pin
    STATE_RUNNING --> STATE_IDLE: Completed
    STATE_RUNNING --> STATE_RUNNING: Quantum δt=10ms
    
    STATE_RUNNING --> STATE_STOPPING: Abort Signal
    STATE_STOPPING --> STATE_STOPPED: ≤10ms Teardown
    STATE_STOPPED --> STATE_IDLE: Latches Cleared
    
    STATE_USB_WAIT --> STATE_ERROR: Enum Timeout
    STATE_ERROR --> STATE_BOOTING: WDT Reboot
'''

mmd_path = os.path.join(FIG_SOURCE, "fig2_scenario_fsm.mmd")
with open(mmd_path, "w", encoding="utf-8") as f:
    f.write(mermaid_code)
print(f"Saved Mermaid model: {mmd_path}")

# ---------------------------------------------------------------------------
# 2. Native draw.io XML Definition
# ---------------------------------------------------------------------------
drawio_xml = '''<mxfile host="app.diagrams.net" modified="2026-11-02T08:50:00.000Z" agent="PipeJack/WHID-Guard FSM Designer" version="24.0.0" type="device">
  <diagram id="fig2_fsm" name="Scenario Execution FSM">
    <mxGraphModel dx="1200" dy="500" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="820" pageHeight="260" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <mxCell id="start" value="" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#1e293b;strokeColor=none;" vertex="1" parent="1">
          <mxGeometry x="20" y="48" width="16" height="16" as="geometry" />
        </mxCell>
        
        <!-- TOP ROW STATES -->
        <mxCell id="s_boot" value="STATE_BOOTING&#xa;&lt;font style=&quot;font-size: 9px;&quot; color=&quot;#4b5563&quot;&gt;Power-On &amp; USB Init&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#3b82f6;fontStyle=1;fontSize=10;arcSize=8;" vertex="1" parent="1">
          <mxGeometry x="60" y="36" width="115" height="42" as="geometry" />
        </mxCell>
        <mxCell id="s_usb" value="STATE_USB_WAIT&#xa;&lt;font style=&quot;font-size: 9px;&quot; color=&quot;#4b5563&quot;&gt;Host Enum Δt ≥ 3.5s&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#3b82f6;fontStyle=1;fontSize=10;arcSize=8;" vertex="1" parent="1">
          <mxGeometry x="215" y="36" width="115" height="42" as="geometry" />
        </mxCell>
        <mxCell id="s_start" value="STATE_STARTUP_&#xa;PAYLOAD&#xa;&lt;font style=&quot;font-size: 8px;&quot; color=&quot;#4b5563&quot;&gt;Scenario 1 Injection&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#3b82f6;fontStyle=1;fontSize=10;arcSize=8;" vertex="1" parent="1">
          <mxGeometry x="370" y="36" width="115" height="42" as="geometry" />
        </mxCell>
        <mxCell id="s_idle" value="STATE_IDLE&#xa;&lt;font style=&quot;font-size: 9px;&quot; color=&quot;#4b5563&quot;&gt;Quiescent / Listening&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;fontStyle=1;fontSize=10;arcSize=8;" vertex="1" parent="1">
          <mxGeometry x="525" y="36" width="115" height="42" as="geometry" />
        </mxCell>
        <mxCell id="s_run" value="STATE_RUNNING&#xa;&lt;font style=&quot;font-size: 8.5px;&quot; color=&quot;#15803d&quot;&gt;Payload Execution&#xa;Quantum δt = 10ms&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dcfce7;strokeColor=#16a34a;fontStyle=1;fontSize=10;arcSize=8;" vertex="1" parent="1">
          <mxGeometry x="675" y="34" width="115" height="46" as="geometry" />
        </mxCell>

        <!-- BOTTOM ROW STATES -->
        <mxCell id="s_err" value="STATE_ERROR&#xa;&lt;font style=&quot;font-size: 9px;&quot; color=&quot;#9a3412&quot;&gt;Watchdog / Bus Fault&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffedd5;strokeColor=#ea580c;fontStyle=1;fontSize=10;arcSize=8;" vertex="1" parent="1">
          <mxGeometry x="215" y="118" width="115" height="42" as="geometry" />
        </mxCell>
        <mxCell id="s_stopd" value="STATE_STOPPED&#xa;&lt;font style=&quot;font-size: 8.5px;&quot; color=&quot;#991b1b&quot;&gt;Atomic Teardown&#xa;releaseAll() Latches&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#ef4444;fontStyle=1;fontSize=10;arcSize=8;" vertex="1" parent="1">
          <mxGeometry x="525" y="118" width="115" height="42" as="geometry" />
        </mxCell>
        <mxCell id="s_stopg" value="STATE_STOPPING&#xa;&lt;font style=&quot;font-size: 8.5px;&quot; color=&quot;#991b1b&quot;&gt;Preempt Request&#xa;Mailbox φ_stop = 1&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#ef4444;fontStyle=1;fontSize=10;arcSize=8;" vertex="1" parent="1">
          <mxGeometry x="675" y="118" width="115" height="42" as="geometry" />
        </mxCell>

        <!-- TRANSITION CONNECTORS -->
        <mxCell id="e0" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#1e293b;strokeWidth=1.5;" edge="1" parent="1" source="start" target="s_boot" />
        <mxCell id="e1" value="Init OK" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2563eb;strokeWidth=1.5;fontStyle=1;fontSize=9;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="s_boot" target="s_usb" />
        <mxCell id="e2" value="Enum OK" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2563eb;strokeWidth=1.5;fontStyle=1;fontSize=9;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="s_usb" target="s_start" />
        <mxCell id="e3" value="Done" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2563eb;strokeWidth=1.5;fontStyle=1;fontSize=9;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="s_start" target="s_idle" />
        <mxCell id="e4" value="C2 REST / Pin" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2563eb;strokeWidth=1.8;fontStyle=1;fontSize=9;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="s_idle" target="s_run" />
        <mxCell id="e5" value="Abort" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#ef4444;strokeWidth=1.8;fontStyle=1;fontSize=9;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="s_run" target="s_stopg" />
        <mxCell id="e6" value="≤ 10ms Kill" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#ef4444;strokeWidth=1.8;fontStyle=1;fontSize=9;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="s_stopg" target="s_stopd" />
        <mxCell id="e7" value="Latches Cleared" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2563eb;strokeWidth=1.5;fontStyle=1;fontSize=9;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="s_stopd" target="s_idle" />
        <mxCell id="e8" value="Enum Timeout" style="edgeStyle=orthogonalEdgeStyle;rounded=0;dashed=1;strokeColor=#ea580c;strokeWidth=1.5;fontStyle=1;fontSize=9;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="s_usb" target="s_err" />
        <mxCell id="e9" value="WDT Reboot" style="edgeStyle=orthogonalEdgeStyle;rounded=0;dashed=1;strokeColor=#ea580c;strokeWidth=1.5;fontStyle=1;fontSize=9;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="s_err" target="s_boot" />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''

drawio_path = os.path.join(FIG_SOURCE, "fig2_scenario_fsm.drawio")
with open(drawio_path, "w", encoding="utf-8") as f:
    f.write(drawio_xml)
print(f"Saved draw.io model: {drawio_path}")

# ---------------------------------------------------------------------------
# 3. Inkscape-Compliant SVG Vector Generation
# ---------------------------------------------------------------------------
svg_code = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 180" width="760" height="180" style="background:#ffffff; font-family:Helvetica, Arial, sans-serif;">
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
  <circle cx="20" cy="54" r="7" fill="#1e293b"/>
  <line x1="27" y1="54" x2="48" y2="54" stroke="#1e293b" stroke-width="1.2" marker-end="url(#arr_black)"/>

  <!-- TOP ROW STATES -->
  <!-- 1. BOOTING -->
  <rect x="52" y="34" width="112" height="40" rx="4" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.0"/>
  <text x="108" y="49" font-size="9.0" font-weight="bold" fill="#1e3a8a" text-anchor="middle">STATE_BOOTING</text>
  <text x="108" y="62" font-size="7.5" fill="#64748b" text-anchor="middle">Power-On &amp; USB Init</text>

  <!-- 2. USB_WAIT -->
  <rect x="202" y="34" width="112" height="40" rx="4" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.0"/>
  <text x="258" y="49" font-size="9.0" font-weight="bold" fill="#1e3a8a" text-anchor="middle">STATE_USB_WAIT</text>
  <text x="258" y="62" font-size="7.5" fill="#64748b" text-anchor="middle">Host Enum Δt ≥ 3.5s</text>

  <!-- 3. STARTUP_PAYLOAD -->
  <rect x="352" y="34" width="120" height="40" rx="4" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.0"/>
  <text x="412" y="45" font-size="8.0" font-weight="bold" fill="#1e3a8a" text-anchor="middle">STATE_STARTUP_</text>
  <text x="412" y="58" font-size="8.0" font-weight="bold" fill="#1e3a8a" text-anchor="middle">PAYLOAD</text>
  <text x="412" y="69" font-size="7.0" fill="#64748b" text-anchor="middle">Scenario 1 Injection</text>

  <!-- 4. IDLE -->
  <rect x="508" y="34" width="112" height="40" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1.2"/>
  <text x="564" y="49" font-size="9.0" font-weight="bold" fill="#1e40af" text-anchor="middle">STATE_IDLE</text>
  <text x="564" y="62" font-size="7.5" fill="#475569" text-anchor="middle">Quiescent / Listening</text>

  <!-- 5. RUNNING -->
  <rect x="648" y="32" width="102" height="44" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.2"/>
  <text x="699" y="46" font-size="9.0" font-weight="bold" fill="#14532d" text-anchor="middle">STATE_RUNNING</text>
  <text x="699" y="58" font-size="7.5" fill="#166534" text-anchor="middle">Payload Execution</text>
  <text x="699" y="68" font-size="7.0" fill="#15803d" text-anchor="middle">Quantum δt = 10ms</text>

  <!-- BOTTOM ROW STATES -->
  <!-- ERROR -->
  <rect x="202" y="120" width="112" height="40" rx="4" fill="#fff7ed" stroke="#ea580c" stroke-width="1.0"/>
  <text x="258" y="135" font-size="9.0" font-weight="bold" fill="#9a3412" text-anchor="middle">STATE_ERROR</text>
  <text x="258" y="148" font-size="7.5" fill="#64748b" text-anchor="middle">Watchdog / Bus Fault</text>

  <!-- STOPPED -->
  <rect x="508" y="120" width="112" height="40" rx="4" fill="#fef2f2" stroke="#ef4444" stroke-width="1.0"/>
  <text x="564" y="133" font-size="9.0" font-weight="bold" fill="#991b1b" text-anchor="middle">STATE_STOPPED</text>
  <text x="564" y="145" font-size="7.2" fill="#64748b" text-anchor="middle">Atomic Teardown</text>
  <text x="564" y="154" font-size="6.8" fill="#64748b" text-anchor="middle">releaseAll() Latches</text>

  <!-- STOPPING -->
  <rect x="648" y="120" width="102" height="40" rx="4" fill="#fef2f2" stroke="#ef4444" stroke-width="1.0"/>
  <text x="699" y="133" font-size="9.0" font-weight="bold" fill="#991b1b" text-anchor="middle">STATE_STOPPING</text>
  <text x="699" y="145" font-size="7.2" fill="#64748b" text-anchor="middle">Preempt Request</text>
  <text x="699" y="154" font-size="6.8" fill="#64748b" text-anchor="middle">Mailbox φ_stop = 1</text>

  <!-- TRANSITIONS -->
  <!-- Booting -> USB Wait -->
  <line x1="164" y1="54" x2="198" y2="54" stroke="#3b82f6" stroke-width="1.1" marker-end="url(#arr_blue)"/>
  <rect x="168" y="44" width="28" height="13" rx="2" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.5"/>
  <text x="182" y="53" font-size="6.8" fill="#1e3a8a" text-anchor="middle">Init OK</text>

  <!-- USB Wait -> Startup -->
  <line x1="314" y1="54" x2="348" y2="54" stroke="#3b82f6" stroke-width="1.1" marker-end="url(#arr_blue)"/>
  <rect x="317" y="44" width="30" height="13" rx="2" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.5"/>
  <text x="332" y="53" font-size="6.8" fill="#1e3a8a" text-anchor="middle">Enum OK</text>

  <!-- Startup -> Idle -->
  <line x1="472" y1="54" x2="504" y2="54" stroke="#3b82f6" stroke-width="1.1" marker-end="url(#arr_blue)"/>
  <rect x="477" y="44" width="23" height="13" rx="2" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.5"/>
  <text x="488" y="53" font-size="6.8" fill="#1e3a8a" text-anchor="middle">Done</text>

  <!-- Idle -> Running (Trigger) -->
  <line x1="620" y1="47" x2="644" y2="47" stroke="#2563eb" stroke-width="1.3" marker-end="url(#arr_blue)"/>
  <text x="633" y="42" font-size="6.5" font-weight="bold" fill="#1d4ed8" text-anchor="middle">REST/Pin</text>

  <!-- Running -> Idle (Normal complete) -->
  <line x1="648" y1="61" x2="624" y2="61" stroke="#16a34a" stroke-width="1.1" marker-end="url(#arr_green)"/>
  <text x="635" y="70" font-size="6.2" fill="#166534" text-anchor="middle">Complete</text>

  <!-- Running self-loop -->
  <path d="M 680,32 C 680,18 718,18 718,30" fill="none" stroke="#16a34a" stroke-width="1.0" marker-end="url(#arr_green)"/>
  <text x="699" y="16" font-size="6.5" fill="#15803d" text-anchor="middle">δt = 10ms</text>

  <!-- Running -> Stopping (Straight vertical down) -->
  <line x1="699" y1="76" x2="699" y2="116" stroke="#ef4444" stroke-width="1.3" marker-end="url(#arr_red)"/>
  <rect x="702" y="89" width="48" height="15" rx="2" fill="#ffffff" stroke="#fca5a5" stroke-width="0.5"/>
  <text x="726" y="100" font-size="7.0" font-weight="bold" fill="#991b1b" text-anchor="middle">Abort (φ_stop=1)</text>

  <!-- Stopping -> Stopped (Straight horizontal left) -->
  <line x1="648" y1="140" x2="624" y2="140" stroke="#ef4444" stroke-width="1.3" marker-end="url(#arr_red)"/>
  <rect x="618" y="133" width="36" height="14" rx="2" fill="#ffffff" stroke="#fca5a5" stroke-width="0.5"/>
  <text x="636" y="143" font-size="6.5" font-weight="bold" fill="#991b1b" text-anchor="middle">≤10ms Kill</text>

  <!-- Stopped -> Idle (Straight vertical up) -->
  <line x1="564" y1="120" x2="564" y2="78" stroke="#2563eb" stroke-width="1.3" marker-end="url(#arr_blue)"/>
  <rect x="518" y="91" width="43" height="14" rx="2" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.5"/>
  <text x="539" y="101" font-size="6.8" fill="#1e40af" text-anchor="middle">Latches Cleared</text>

  <!-- USB Wait -> Error (Timeout down) -->
  <line x1="258" y1="74" x2="258" y2="116" stroke="#ea580c" stroke-width="1.1" stroke-dasharray="3,2" marker-end="url(#arr_orange)"/>
  <rect x="261" y="90" width="46" height="14" rx="2" fill="#ffffff" stroke="#fdba74" stroke-width="0.5"/>
  <text x="284" y="100" font-size="6.8" fill="#9a3412" text-anchor="middle">Enum Timeout</text>

  <!-- Error -> Booting (WDT Reboot) -->
  <path d="M 202,140 L 108,140 L 108,78" fill="none" stroke="#ea580c" stroke-width="1.1" stroke-dasharray="3,2" marker-end="url(#arr_orange)"/>
  <rect x="135" y="133" width="46" height="14" rx="2" fill="#ffffff" stroke="#fdba74" stroke-width="0.5"/>
  <text x="158" y="143" font-size="6.8" fill="#9a3412" text-anchor="middle">WDT Reboot</text>
</svg>'''

svg_path = os.path.join(FIG_SOURCE, "fig2_scenario_fsm.svg")
with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg_code)
print(f"Saved SVG model: {svg_path}")

# ---------------------------------------------------------------------------
# 4. Vector PDF Export for IEEE Manuscript
# ---------------------------------------------------------------------------
doc = fitz.open(stream=svg_code.encode("utf-8"), filetype="svg")
pdf_bytes = doc.convert_to_pdf()
pdf_doc = fitz.open("pdf", pdf_bytes)

dst1 = os.path.join(FIG_FINAL, "fig2_scenario_fsm.pdf")
dst2 = os.path.join(PAPER_DIR, "fsm_diagram.pdf")
pdf_doc.save(dst1)
pdf_doc.save(dst2)

# Save 300 DPI preview
pix = pdf_doc[0].get_pixmap(dpi=300)
pix.save(os.path.join(FIG_FINAL, "fig2_scenario_fsm.png"))
pix.save(os.path.join(PAPER_DIR, "fsm_diagram.png"))

print(f"Exported Vector PDF: {dst1} and {dst2}")
