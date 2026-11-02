"""
Draw.io & Inkscape SVG Generator for Figure 3: Selective Ingestion Defense Architecture
Creates:
  1. figures/source/fig3_selective_defense.drawio (Native draw.io XML)
  2. figures/source/fig3_selective_defense.svg (Inkscape-compliant SVG)
  3. paper/defense_architecture.pdf & figures/final/fig3_selective_defense.pdf (Vector PDF)
"""

import os
import fitz

BASE_DIR = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32"
FIG_SOURCE = os.path.join(BASE_DIR, "figures", "source")
FIG_FINAL = os.path.join(BASE_DIR, "figures", "final")
PAPER_DIR = os.path.join(BASE_DIR, "paper")

# ---------------------------------------------------------------------------
# 1. Native draw.io XML Definition
# ---------------------------------------------------------------------------
drawio_xml = '''<mxfile host="app.diagrams.net" modified="2026-11-02T08:50:00.000Z" agent="PipeJack/WHID-Guard Defense Designer" version="24.0.0" type="device">
  <diagram id="fig3_defense" name="Selective Defense Architecture">
    <mxGraphModel dx="1200" dy="500" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="820" pageHeight="260" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- Physical Devices -->
        <mxCell id="d_legit" value="Physical Keyboard&#xa;&lt;font style=&quot;font-size: 9px;&quot; color=&quot;#4b5563&quot;&gt;Genuine HID (h_legit)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#3b82f6;fontStyle=1;fontSize=10;arcSize=6;" vertex="1" parent="1">
          <mxGeometry x="15" y="32" width="115" height="40" as="geometry" />
        </mxCell>
        <mxCell id="d_rogue" value="Rogue ESP32-S3&#xa;&lt;font style=&quot;font-size: 9px;&quot; color=&quot;#991b1b&quot;&gt;BadUSB (h_rogue)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fef2f2;strokeColor=#ef4444;fontStyle=1;fontSize=10;arcSize=6;" vertex="1" parent="1">
          <mxGeometry x="15" y="112" width="115" height="40" as="geometry" />
        </mxCell>

        <!-- USB Root Hub -->
        <mxCell id="hub" value="USB Root Hub" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f1f5f9;strokeColor=#64748b;fontStyle=1;fontSize=10;rotation=-90;arcSize=6;" vertex="1" parent="1">
          <mxGeometry x="120" y="70" width="80" height="24" as="geometry" />
        </mxCell>
        
        <!-- Host OS Container -->
        <mxCell id="host_box" value="Host OS Defense Daemon (WHID-Guard)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#94a3b8;fontColor=#475569;fontStyle=1;fontSize=11;dashed=1;rounded=1;arcSize=4;startSize=24;" vertex="1" parent="1">
          <mxGeometry x="195" y="10" width="555" height="162" as="geometry" />
        </mxCell>
        
        <!-- Modules -->
        <mxCell id="m_hook" value="Low-Level Hook&#xa;&lt;font style=&quot;font-size: 9px;&quot; color=&quot;#4b5563&quot;&gt;WH_KEYBOARD_LL&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3b82f6;fontStyle=1;fontSize=10;arcSize=6;" vertex="1" parent="host_box">
          <mxGeometry x="15" y="24" width="115" height="38" as="geometry" />
        </mxCell>
        <mxCell id="m_raw" value="Raw Input Monitor&#xa;&lt;font style=&quot;font-size: 9px;&quot; color=&quot;#4b5563&quot;&gt;WM_INPUT (h_dev)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3b82f6;fontStyle=1;fontSize=10;arcSize=6;" vertex="1" parent="host_box">
          <mxGeometry x="15" y="104" width="115" height="38" as="geometry" />
        </mxCell>
        <mxCell id="m_eng" value="Dynamics Engine&#xa;&lt;font style=&quot;font-size: 8.5px;&quot; color=&quot;#4b5563&quot;&gt;Sliding Window (W=10)&#xa;Metrics: mu_IKI, CV_IKI&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3b82f6;fontStyle=1;fontSize=10;arcSize=6;" vertex="1" parent="host_box">
          <mxGeometry x="160" y="101" width="125" height="44" as="geometry" />
        </mxCell>
        <mxCell id="m_gate" value="Selective Filter Gate&#xa;&lt;font style=&quot;font-size: 8.5px;&quot; color=&quot;#1e3a8a&quot;&gt;Match h_origin in Q_quarantine&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;fontStyle=1;fontSize=10;arcSize=6;" vertex="1" parent="host_box">
          <mxGeometry x="320" y="24" width="125" height="38" as="geometry" />
        </mxCell>
        <mxCell id="m_qtab" value="Quarantine Table&#xa;&lt;font style=&quot;font-size: 8.5px;&quot; color=&quot;#991b1b&quot;&gt;Blacklist: h_rogue&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fef2f2;strokeColor=#ef4444;fontStyle=1;fontSize=10;arcSize=6;" vertex="1" parent="host_box">
          <mxGeometry x="320" y="66" width="125" height="32" as="geometry" />
        </mxCell>
        <mxCell id="m_dec" value="Decision Boundary&#xa;&lt;font style=&quot;font-size: 8.5px;&quot; color=&quot;#6b21a8&quot;&gt;mu &lt; 25ms or CV &lt; 0.15&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#faf5ff;strokeColor=#a855f7;fontStyle=1;fontSize=10;arcSize=6;" vertex="1" parent="host_box">
          <mxGeometry x="320" y="104" width="125" height="38" as="geometry" />
        </mxCell>
        <mxCell id="m_wdt" value="15s Watchdog Timer&#xa;&lt;font style=&quot;font-size: 8px;&quot; color=&quot;#9a3412&quot;&gt;Auto-Release on Idle&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;dashed=1;fillColor=#fff7ed;strokeColor=#ea580c;fontStyle=1;fontSize=9;arcSize=6;" vertex="1" parent="host_box">
          <mxGeometry x="320" y="146" width="125" height="24" as="geometry" />
        </mxCell>
        
        <!-- Outputs -->
        <mxCell id="o_drop" value="[DROP EVENT]&#xa;&lt;font style=&quot;font-size: 8px;&quot;&gt;Suppress Scancode&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#ef4444;fontStyle=1;fontSize=9;fontColor=#991b1b;arcSize=6;" vertex="1" parent="host_box">
          <mxGeometry x="465" y="20" width="80" height="28" as="geometry" />
        </mxCell>
        <mxCell id="o_pass" value="[PASS EVENT]&#xa;&lt;font style=&quot;font-size: 8px;&quot;&gt;Allow Keystroke&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dcfce7;strokeColor=#16a34a;fontStyle=1;fontSize=9;fontColor=#166534;arcSize=6;" vertex="1" parent="host_box">
          <mxGeometry x="465" y="56" width="80" height="28" as="geometry" />
        </mxCell>
        <mxCell id="o_app" value="Active Window&#xa;&lt;font style=&quot;font-size: 8px;&quot; color=&quot;#4b5563&quot;&gt;Foreground Target&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#cbd5e1;fontStyle=1;fontSize=9;arcSize=6;" vertex="1" parent="host_box">
          <mxGeometry x="465" y="98" width="80" height="32" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''

drawio_path = os.path.join(FIG_SOURCE, "fig3_selective_defense.drawio")
with open(drawio_path, "w", encoding="utf-8") as f:
    f.write(drawio_xml)
print(f"Saved draw.io model: {drawio_path}")

# ---------------------------------------------------------------------------
# 2. Inkscape-Compliant SVG Vector Generation
# ---------------------------------------------------------------------------
svg_code = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 180" width="760" height="180" style="background:#ffffff; font-family:Helvetica, Arial, sans-serif;">
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

  <!-- COLUMN 1: Physical Peripherals -->
  <rect x="12" y="32" width="112" height="38" rx="4" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.0"/>
  <text x="68" y="46" font-size="9.0" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Physical Keyboard</text>
  <text x="68" y="58" font-size="7.5" fill="#64748b" text-anchor="middle">Genuine HID (h_legit)</text>

  <rect x="12" y="112" width="112" height="38" rx="4" fill="#fef2f2" stroke="#ef4444" stroke-width="1.0"/>
  <text x="68" y="126" font-size="9.0" font-weight="bold" fill="#991b1b" text-anchor="middle">Rogue ESP32-S3</text>
  <text x="68" y="138" font-size="7.5" fill="#64748b" text-anchor="middle">BadUSB (h_rogue)</text>

  <!-- COLUMN 2: USB Root Hub -->
  <rect x="146" y="24" width="22" height="134" rx="3" fill="#f1f5f9" stroke="#64748b" stroke-width="1.0"/>
  <text x="157" y="94" font-size="8.5" font-weight="bold" fill="#334155" text-anchor="middle" transform="rotate(-90 157 94)">USB Root Hub</text>

  <line x1="124" y1="51" x2="144" y2="51" stroke="#2563eb" stroke-width="1.1" marker-end="url(#arr_blue)"/>
  <line x1="124" y1="131" x2="144" y2="131" stroke="#ef4444" stroke-width="1.1" marker-end="url(#arr_red)"/>

  <!-- HOST OS CONTAINER -->
  <rect x="182" y="8" width="568" height="164" rx="5" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.0" stroke-dasharray="4,3"/>
  <text x="194" y="22" font-size="8.5" font-weight="bold" fill="#475569">Host OS Defense Daemon (WHID-Guard)</text>

  <!-- COLUMN 3: Ingestion Channels -->
  <rect x="194" y="32" width="112" height="38" rx="4" fill="#ffffff" stroke="#3b82f6" stroke-width="1.0"/>
  <text x="250" y="46" font-size="9.0" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Low-Level Hook</text>
  <text x="250" y="58" font-size="7.5" fill="#64748b" text-anchor="middle">WH_KEYBOARD_LL</text>

  <rect x="194" y="112" width="112" height="38" rx="4" fill="#ffffff" stroke="#3b82f6" stroke-width="1.0"/>
  <text x="250" y="126" font-size="9.0" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Raw Input Monitor</text>
  <text x="250" y="138" font-size="7.5" fill="#64748b" text-anchor="middle">WM_INPUT (h_dev)</text>

  <line x1="168" y1="51" x2="192" y2="51" stroke="#2563eb" stroke-width="1.1" marker-end="url(#arr_blue)"/>
  <line x1="168" y1="131" x2="192" y2="131" stroke="#2563eb" stroke-width="1.1" marker-end="url(#arr_blue)"/>

  <!-- COLUMN 4: Dynamics Engine -->
  <rect x="336" y="108" width="124" height="44" rx="4" fill="#ffffff" stroke="#3b82f6" stroke-width="1.0"/>
  <text x="398" y="122" font-size="9.0" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Dynamics Engine</text>
  <text x="398" y="133" font-size="7.2" fill="#64748b" text-anchor="middle">Sliding Window (W = 10)</text>
  <text x="398" y="144" font-size="7.2" fill="#64748b" text-anchor="middle">Metrics: mu_IKI, CV_IKI</text>

  <line x1="306" y1="131" x2="334" y2="131" stroke="#2563eb" stroke-width="1.1" marker-end="url(#arr_blue)"/>

  <!-- COLUMN 5: Defense Stack -->
  <!-- Top: Filter Gate -->
  <rect x="490" y="32" width="134" height="38" rx="4" fill="#dbeafe" stroke="#2563eb" stroke-width="1.2"/>
  <text x="557" y="46" font-size="8.8" font-weight="bold" fill="#1e40af" text-anchor="middle">Selective Filter Gate</text>
  <text x="557" y="58" font-size="7.2" fill="#1e3a8a" text-anchor="middle">Match h_origin in Q_quar</text>

  <!-- Middle: Quarantine Table -->
  <rect x="490" y="74" width="134" height="28" rx="4" fill="#fef2f2" stroke="#ef4444" stroke-width="1.0"/>
  <text x="557" y="86" font-size="8.5" font-weight="bold" fill="#991b1b" text-anchor="middle">Quarantine Table</text>
  <text x="557" y="96" font-size="7.0" fill="#b91c1c" text-anchor="middle">Blacklist: h_rogue</text>

  <!-- Bottom: Decision Boundary -->
  <rect x="490" y="106" width="134" height="36" rx="4" fill="#faf5ff" stroke="#a855f7" stroke-width="1.0"/>
  <text x="557" y="120" font-size="8.5" font-weight="bold" fill="#6b21a8" text-anchor="middle">Decision Boundary</text>
  <text x="557" y="132" font-size="7.0" fill="#7e22ce" text-anchor="middle">mu &lt; 25ms or CV &lt; 0.15</text>

  <!-- Watchdog Timer -->
  <rect x="490" y="146" width="134" height="22" rx="3" fill="#fff7ed" stroke="#ea580c" stroke-width="0.9" stroke-dasharray="3,2"/>
  <text x="557" y="157" font-size="7.8" font-weight="bold" fill="#9a3412" text-anchor="middle">15s Watchdog (Auto-Clear)</text>

  <!-- Connectors in Stack -->
  <line x1="306" y1="51" x2="488" y2="51" stroke="#2563eb" stroke-width="1.1" marker-end="url(#arr_blue)"/>
  <rect x="368" y="42" width="68" height="15" rx="2" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.5"/>
  <text x="402" y="52" font-size="7.0" fill="#1e3a8a" text-anchor="middle">Scancode Stream</text>

  <line x1="460" y1="128" x2="488" y2="128" stroke="#9333ea" stroke-width="1.1" marker-end="url(#arr_purple)"/>

  <!-- Decision -> Q-Tab -->
  <line x1="557" y1="106" x2="557" y2="103" stroke="#ef4444" stroke-width="1.1" marker-end="url(#arr_red)"/>
  <!-- Q-Tab -> Gate -->
  <line x1="557" y1="74" x2="557" y2="71" stroke="#ef4444" stroke-width="1.1" marker-end="url(#arr_red)"/>
  <rect x="428" y="80" width="58" height="14" rx="2" fill="#ffffff" stroke="#fca5a5" stroke-width="0.5"/>
  <text x="457" y="90" font-size="6.5" font-weight="bold" fill="#991b1b" text-anchor="middle">Lockdown (κ≥8)</text>

  <!-- WDT -> Decision -->
  <line x1="557" y1="146" x2="557" y2="143" stroke="#ea580c" stroke-width="0.9" stroke-dasharray="2,2" marker-end="url(#arr_orange)"/>

  <!-- COLUMN 6: Enforcement Outputs -->
  <!-- Drop -->
  <rect x="646" y="26" width="94" height="28" rx="3.5" fill="#fee2e2" stroke="#ef4444" stroke-width="1.0"/>
  <text x="693" y="38" font-size="8.0" font-weight="bold" fill="#991b1b" text-anchor="middle">[DROP EVENT]</text>
  <text x="693" y="48" font-size="6.8" fill="#b91c1c" text-anchor="middle">Suppress Scancode</text>

  <!-- Pass -->
  <rect x="646" y="60" width="94" height="28" rx="3.5" fill="#dcfce7" stroke="#16a34a" stroke-width="1.0"/>
  <text x="693" y="72" font-size="8.0" font-weight="bold" fill="#166534" text-anchor="middle">[PASS EVENT]</text>
  <text x="693" y="82" font-size="6.8" fill="#15803d" text-anchor="middle">Allow Keystroke</text>

  <!-- Active Window -->
  <rect x="646" y="104" width="94" height="34" rx="3.5" fill="#f8fafc" stroke="#cbd5e1" stroke-width="0.9"/>
  <text x="693" y="118" font-size="8.0" font-weight="bold" fill="#334155" text-anchor="middle">Active Window</text>
  <text x="693" y="129" font-size="6.8" fill="#64748b" text-anchor="middle">Foreground App Target</text>

  <!-- Routing from Gate to Outputs -->
  <path d="M 624,40 L 638,40 L 638,40 L 644,40" fill="none" stroke="#ef4444" stroke-width="1.1" marker-end="url(#arr_red)"/>
  <path d="M 624,56 L 638,56 L 638,74 L 644,74" fill="none" stroke="#16a34a" stroke-width="1.1" marker-end="url(#arr_green)"/>
  <line x1="693" y1="88" x2="693" y2="102" stroke="#16a34a" stroke-width="0.9" marker-end="url(#arr_green)"/>
</svg>'''

svg_path = os.path.join(FIG_SOURCE, "fig3_selective_defense.svg")
with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg_code)
print(f"Saved SVG model: {svg_path}")

# ---------------------------------------------------------------------------
# 3. Vector PDF Export for IEEE Manuscript
# ---------------------------------------------------------------------------
doc = fitz.open(stream=svg_code.encode("utf-8"), filetype="svg")
pdf_bytes = doc.convert_to_pdf()
pdf_doc = fitz.open("pdf", pdf_bytes)

dst1 = os.path.join(FIG_FINAL, "fig3_selective_defense.pdf")
dst2 = os.path.join(PAPER_DIR, "defense_architecture.pdf")
pdf_doc.save(dst1)
pdf_doc.save(dst2)

# Save 300 DPI preview
pix = pdf_doc[0].get_pixmap(dpi=300)
pix.save(os.path.join(FIG_FINAL, "fig3_selective_defense.png"))
pix.save(os.path.join(PAPER_DIR, "defense_architecture.png"))

print(f"Exported Vector PDF: {dst1} and {dst2}")
