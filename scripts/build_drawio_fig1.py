"""
Draw.io & Inkscape SVG Generator for Figure 1: System Architecture
Creates:
  1. figures/source/fig1_system_architecture.drawio (Native draw.io XML)
  2. figures/source/fig1_system_architecture.svg (Inkscape-compliant SVG)
  3. paper/system_architecture.pdf & figures/final/fig1_system_architecture.pdf (Vector PDF)
"""

import os
import xml.etree.ElementTree as ET
import fitz

BASE_DIR = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32"
FIG_SOURCE = os.path.join(BASE_DIR, "figures", "source")
FIG_FINAL = os.path.join(BASE_DIR, "figures", "final")
PAPER_DIR = os.path.join(BASE_DIR, "paper")

for d in [FIG_SOURCE, FIG_FINAL, PAPER_DIR]:
    os.makedirs(d, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Native draw.io XML Definition
# ---------------------------------------------------------------------------
drawio_xml = '''<mxfile host="app.diagrams.net" modified="2026-11-02T08:50:00.000Z" agent="PipeJack/WHID-Guard Architecture Designer" version="24.0.0" type="device">
  <diagram id="fig1_arch" name="System Architecture">
    <mxGraphModel dx="1200" dy="500" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="820" pageHeight="260" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- TIER 1 CONTAINER -->
        <mxCell id="tier1" value="Tier 1: Mobile C2 Controller" style="swimlane;whiteSpace=wrap;html=1;fillColor=#faf5ff;strokeColor=#9333ea;fontColor=#581c87;fontStyle=1;fontSize=12;rounded=1;arcSize=4;startSize=26;" vertex="1" parent="1">
          <mxGeometry x="20" y="20" width="180" height="200" as="geometry" />
        </mxCell>
        <mxCell id="c2_web" value="Touch Web Console&#xa;&lt;font style=&quot;font-size: 10px;&quot; color=&quot;#4b5563&quot;&gt;Single-Page App (SPA)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#a855f7;fontStyle=1;fontSize=11;arcSize=6;" vertex="1" parent="tier1">
          <mxGeometry x="15" y="38" width="150" height="42" as="geometry" />
        </mxCell>
        <mxCell id="c2_api" value="REST Attack Engine&#xa;&lt;font style=&quot;font-size: 10px;&quot; color=&quot;#4b5563&quot;&gt;Scenarios 1–4, Cadence Jitter&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#a855f7;fontStyle=1;fontSize=11;arcSize=6;" vertex="1" parent="tier1">
          <mxGeometry x="15" y="94" width="150" height="42" as="geometry" />
        </mxCell>
        <mxCell id="c2_wifi" value="802.11 b/g/n Client&#xa;&lt;font style=&quot;font-size: 10px;&quot; color=&quot;#4b5563&quot;&gt;Station Link (192.168.4.1)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#a855f7;fontStyle=1;fontSize=11;arcSize=6;" vertex="1" parent="tier1">
          <mxGeometry x="15" y="148" width="150" height="42" as="geometry" />
        </mxCell>
        <mxCell id="e_c2_1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#a855f7;strokeWidth=1.5;" edge="1" parent="tier1" source="c2_web" target="c2_api">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_c2_2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#a855f7;strokeWidth=1.5;" edge="1" parent="tier1" source="c2_api" target="c2_wifi">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- TIER 2 CONTAINER -->
        <mxCell id="tier2" value="Tier 2: Weaponized ESP32-S3 Hardware Implant" style="swimlane;whiteSpace=wrap;html=1;fillColor=#f0fdf4;strokeColor=#16a34a;fontColor=#14532d;fontStyle=1;fontSize=12;rounded=1;arcSize=4;startSize=26;" vertex="1" parent="1">
          <mxGeometry x="270" y="20" width="270" height="200" as="geometry" />
        </mxCell>
        <mxCell id="core0" value="Core 0: Network&#xa;&lt;font style=&quot;font-size: 9px;&quot; color=&quot;#4b5563&quot;&gt;SoftAP, HTTP Server&#xa;TCP/IP Baseband Stack&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#22c55e;fontStyle=1;fontSize=11;arcSize=6;" vertex="1" parent="tier2">
          <mxGeometry x="12" y="38" width="118" height="48" as="geometry" />
        </mxCell>
        <mxCell id="core1" value="Core 1: HID Engine&#xa;&lt;font style=&quot;font-size: 9px;&quot; color=&quot;#4b5563&quot;&gt;8-State Scenario FSM&#xa;Native TinyUSB HID&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#22c55e;fontStyle=1;fontSize=11;arcSize=6;" vertex="1" parent="tier2">
          <mxGeometry x="140" y="38" width="118" height="48" as="geometry" />
        </mxCell>
        <mxCell id="ipc" value="FreeRTOS Spinlock Mailbox (portMUX_TYPE, Ring Buffer)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dcfce7;strokeColor=#16a34a;fontStyle=1;fontSize=10;arcSize=6;" vertex="1" parent="tier2">
          <mxGeometry x="12" y="98" width="246" height="30" as="geometry" />
        </mxCell>
        <mxCell id="ant_hw" value="2.4 GHz Antenna&#xa;&lt;font style=&quot;font-size: 9px;&quot; color=&quot;#4b5563&quot;&gt;SoftAP RF Transceiver&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#22c55e;fontStyle=1;fontSize=11;arcSize=6;" vertex="1" parent="tier2">
          <mxGeometry x="12" y="142" width="118" height="44" as="geometry" />
        </mxCell>
        <mxCell id="usb_hw" value="Native USB OTG PHY&#xa;&lt;font style=&quot;font-size: 9px;&quot; color=&quot;#4b5563&quot;&gt;GPIO 19/20 &amp; BOOT Pin&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff7ed;strokeColor=#ea580c;fontStyle=1;fontSize=11;arcSize=6;" vertex="1" parent="tier2">
          <mxGeometry x="140" y="142" width="118" height="44" as="geometry" />
        </mxCell>
        
        <!-- TIER 3 CONTAINER -->
        <mxCell id="tier3" value="Tier 3: Windows Host Workstation (WHID-Guard)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#2563eb;fontColor=#1e3a8a;fontStyle=1;fontSize=12;rounded=1;arcSize=4;startSize=26;" vertex="1" parent="1">
          <mxGeometry x="610" y="20" width="220" height="200" as="geometry" />
        </mxCell>
        <mxCell id="h_gate" value="Selective Filter Gate (WH_KEYBOARD_LL)&#xa;&lt;font style=&quot;font-size: 9px;&quot; color=&quot;#dc2626&quot;&gt;[PASS] Operator Keys / [DROP] Rogue BadUSB&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fef2f2;strokeColor=#ef4444;fontStyle=1;fontSize=10;arcSize=6;" vertex="1" parent="tier3">
          <mxGeometry x="12" y="34" width="196" height="34" as="geometry" />
        </mxCell>
        <mxCell id="h_qtab" value="Quarantine Table &amp; Policy Gate&#xa;&lt;font style=&quot;font-size: 9px;&quot; color=&quot;#4b5563&quot;&gt;Isolates Rogue Handle h_rogue (15s Auto-Reset)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#ef4444;fontStyle=1;fontSize=10;arcSize=6;" vertex="1" parent="tier3">
          <mxGeometry x="12" y="74" width="196" height="32" as="geometry" />
        </mxCell>
        <mxCell id="h_eng" value="Behavioral Dynamics Engine (W=10)&#xa;&lt;font style=&quot;font-size: 9px;&quot; color=&quot;#4b5563&quot;&gt;Metric Eval (mu &lt; 25 ms or CV &lt; 0.15)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3b82f6;fontStyle=1;fontSize=10;arcSize=6;" vertex="1" parent="tier3">
          <mxGeometry x="12" y="112" width="196" height="34" as="geometry" />
        </mxCell>
        <mxCell id="h_raw" value="Raw Input Monitor (WM_INPUT)&#xa;&lt;font style=&quot;font-size: 9px;&quot; color=&quot;#4b5563&quot;&gt;Per-Device Hardware Attribution to Origin h_dev&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3b82f6;fontStyle=1;fontSize=10;arcSize=6;" vertex="1" parent="tier3">
          <mxGeometry x="12" y="152" width="196" height="34" as="geometry" />
        </mxCell>
        
        <!-- INTER-TIER CONNECTORS -->
        <mxCell id="link_wifi" value="2.4 GHz SoftAP&#xa;&lt;font style=&quot;font-size: 9px;&quot;&gt;REST Commands&lt;/font&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;strokeColor=#9333ea;strokeWidth=2;fontStyle=1;fontSize=10;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="c2_wifi" target="ant_hw">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="link_usb" value="USB 2.0 Bus&#xa;&lt;font style=&quot;font-size: 9px;&quot;&gt;12 Mbps HID&lt;/font&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#2563eb;strokeWidth=2;fontStyle=1;fontSize=10;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="usb_hw" target="h_raw">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''

drawio_path = os.path.join(FIG_SOURCE, "fig1_system_architecture.drawio")
with open(drawio_path, "w", encoding="utf-8") as f:
    f.write(drawio_xml)
print(f"Saved draw.io model: {drawio_path}")

# ---------------------------------------------------------------------------
# 2. Inkscape-Compliant SVG Vector Generation
# ---------------------------------------------------------------------------
svg_code = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 180" width="760" height="180" style="background:#ffffff; font-family:Helvetica, Arial, sans-serif;">
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

  <!-- TIER 1 CONTAINER -->
  <rect x="10" y="8" width="165" height="164" rx="5" fill="#faf5ff" stroke="#a855f7" stroke-width="1.2"/>
  <text x="92" y="24" font-size="10.5" font-weight="bold" fill="#6b21a8" text-anchor="middle">Tier 1: Mobile C2 Controller</text>
  
  <rect x="20" y="34" width="145" height="36" rx="3.5" fill="#ffffff" stroke="#c084fc" stroke-width="0.9"/>
  <text x="92" y="48" font-size="9.5" font-weight="bold" fill="#1e293b" text-anchor="middle">Touch Web Console</text>
  <text x="92" y="61" font-size="8.0" fill="#64748b" text-anchor="middle">Single-Page App (SPA)</text>
  
  <rect x="20" y="78" width="145" height="36" rx="3.5" fill="#ffffff" stroke="#c084fc" stroke-width="0.9"/>
  <text x="92" y="92" font-size="9.5" font-weight="bold" fill="#1e293b" text-anchor="middle">REST Attack Engine</text>
  <text x="92" y="105" font-size="8.0" fill="#64748b" text-anchor="middle">Scenarios 1–4, Cadence Jitter</text>
  
  <rect x="20" y="122" width="145" height="36" rx="3.5" fill="#ffffff" stroke="#c084fc" stroke-width="0.9"/>
  <text x="92" y="136" font-size="9.5" font-weight="bold" fill="#1e293b" text-anchor="middle">802.11 b/g/n Client</text>
  <text x="92" y="149" font-size="8.0" fill="#64748b" text-anchor="middle">Station Link (192.168.4.1)</text>

  <line x1="92" y1="70" x2="92" y2="76" stroke="#a855f7" stroke-width="1.0" marker-end="url(#arr_purple)"/>
  <line x1="92" y1="114" x2="92" y2="120" stroke="#a855f7" stroke-width="1.0" marker-end="url(#arr_purple)"/>

  <!-- TIER 2 CONTAINER -->
  <rect x="245" y="8" width="248" height="164" rx="5" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.2"/>
  <text x="369" y="24" font-size="10.5" font-weight="bold" fill="#15803d" text-anchor="middle">Tier 2: Weaponized ESP32-S3 Hardware Implant</text>

  <rect x="255" y="34" width="110" height="40" rx="3.5" fill="#ffffff" stroke="#4ade80" stroke-width="0.9"/>
  <text x="310" y="48" font-size="9.0" font-weight="bold" fill="#1e293b" text-anchor="middle">Core 0: Network</text>
  <text x="310" y="59" font-size="7.5" fill="#64748b" text-anchor="middle">SoftAP, HTTP Server</text>
  <text x="310" y="69" font-size="7.5" fill="#64748b" text-anchor="middle">TCP/IP Baseband Stack</text>

  <rect x="373" y="34" width="110" height="40" rx="3.5" fill="#ffffff" stroke="#4ade80" stroke-width="0.9"/>
  <text x="428" y="48" font-size="9.0" font-weight="bold" fill="#1e293b" text-anchor="middle">Core 1: HID Engine</text>
  <text x="428" y="59" font-size="7.5" fill="#64748b" text-anchor="middle">8-State Scenario FSM</text>
  <text x="428" y="69" font-size="7.5" fill="#64748b" text-anchor="middle">Native TinyUSB HID</text>

  <!-- Mailbox -->
  <rect x="255" y="82" width="228" height="24" rx="3.5" fill="#dcfce7" stroke="#16a34a" stroke-width="0.9"/>
  <text x="369" y="97" font-size="8.5" font-weight="bold" fill="#14532d" text-anchor="middle">FreeRTOS Spinlock Mailbox (portMUX_TYPE, Ring Buffer)</text>

  <rect x="255" y="114" width="110" height="34" rx="3.5" fill="#ffffff" stroke="#4ade80" stroke-width="0.9"/>
  <text x="310" y="128" font-size="9.0" font-weight="bold" fill="#1e293b" text-anchor="middle">2.4 GHz Antenna</text>
  <text x="310" y="140" font-size="7.5" fill="#64748b" text-anchor="middle">SoftAP RF Transceiver</text>

  <rect x="373" y="114" width="110" height="34" rx="3.5" fill="#fff7ed" stroke="#ea580c" stroke-width="0.9"/>
  <text x="428" y="128" font-size="9.0" font-weight="bold" fill="#9a3412" text-anchor="middle">Native USB OTG PHY</text>
  <text x="428" y="140" font-size="7.5" fill="#64748b" text-anchor="middle">GPIO 19/20 &amp; BOOT Pin</text>

  <!-- Connectors in Tier 2 -->
  <line x1="310" y1="74" x2="310" y2="80" stroke="#16a34a" stroke-width="1.0" marker-end="url(#arr_green)"/>
  <line x1="428" y1="74" x2="428" y2="80" stroke="#16a34a" stroke-width="1.0" marker-end="url(#arr_green)"/>
  <line x1="310" y1="108" x2="310" y2="112" stroke="#16a34a" stroke-width="1.0" marker-end="url(#arr_green)"/>
  <line x1="428" y1="106" x2="428" y2="112" stroke="#ea580c" stroke-width="1.0" marker-end="url(#arr_orange)"/>

  <!-- TIER 3 CONTAINER -->
  <rect x="555" y="8" width="195" height="164" rx="5" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.2"/>
  <text x="652" y="24" font-size="9.5" font-weight="bold" fill="#1d4ed8" text-anchor="middle">Tier 3: Windows Host (WHID-Guard)</text>

  <rect x="565" y="32" width="175" height="30" rx="3.5" fill="#fef2f2" stroke="#ef4444" stroke-width="0.9"/>
  <text x="652" y="44" font-size="8.5" font-weight="bold" fill="#991b1b" text-anchor="middle">Selective Filter Gate (WH_KEYBOARD_LL)</text>
  <text x="652" y="55" font-size="7.2" fill="#b91c1c" text-anchor="middle">[PASS] Operator Keys / [DROP] Rogue BadUSB</text>

  <rect x="565" y="68" width="175" height="28" rx="3.5" fill="#ffffff" stroke="#ef4444" stroke-width="0.9"/>
  <text x="652" y="80" font-size="8.5" font-weight="bold" fill="#991b1b" text-anchor="middle">Quarantine Table &amp; Policy Gate</text>
  <text x="652" y="90" font-size="7.2" fill="#64748b" text-anchor="middle">Isolates Rogue Handle h_rogue (15s Auto-Reset)</text>

  <rect x="565" y="102" width="175" height="28" rx="3.5" fill="#ffffff" stroke="#60a5fa" stroke-width="0.9"/>
  <text x="652" y="114" font-size="8.5" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Behavioral Dynamics Engine (W=10)</text>
  <text x="652" y="124" font-size="7.2" fill="#64748b" text-anchor="middle">Metric Eval (mu &lt; 25 ms or CV &lt; 0.15)</text>

  <rect x="565" y="136" width="175" height="28" rx="3.5" fill="#ffffff" stroke="#60a5fa" stroke-width="0.9"/>
  <text x="652" y="148" font-size="8.5" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Raw Input Monitor (WM_INPUT)</text>
  <text x="652" y="158" font-size="7.2" fill="#64748b" text-anchor="middle">Per-Device Hardware Attribution to Origin h_dev</text>

  <!-- Connectors in Tier 3 -->
  <line x1="652" y1="136" x2="652" y2="132" stroke="#3b82f6" stroke-width="1.0" marker-end="url(#arr_blue)"/>
  <line x1="652" y1="102" x2="652" y2="98" stroke="#ef4444" stroke-width="1.0" marker-end="url(#arr_red)"/>
  <line x1="652" y1="68" x2="652" y2="64" stroke="#ef4444" stroke-width="1.0" marker-end="url(#arr_red)"/>

  <!-- INTER-TIER CONNECTORS -->
  <!-- Link 1: Wi-Fi -->
  <line x1="165" y1="140" x2="252" y2="140" stroke="#9333ea" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arr_purple)"/>
  <rect x="175" y="126" width="65" height="24" rx="2.5" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.5"/>
  <text x="207" y="136" font-size="7.5" font-weight="bold" fill="#7e22ce" text-anchor="middle">2.4 GHz SoftAP</text>
  <text x="207" y="146" font-size="6.8" fill="#475569" text-anchor="middle">REST Commands</text>

  <!-- Link 2: USB -->
  <line x1="483" y1="140" x2="562" y2="140" stroke="#2563eb" stroke-width="1.5" marker-end="url(#arr_blue)"/>
  <rect x="491" y="126" width="62" height="24" rx="2.5" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.5"/>
  <text x="522" y="136" font-size="7.5" font-weight="bold" fill="#1d4ed8" text-anchor="middle">USB 2.0 Bus</text>
  <text x="522" y="146" font-size="6.8" fill="#475569" text-anchor="middle">12 Mbps HID</text>
</svg>'''

svg_path = os.path.join(FIG_SOURCE, "fig1_system_architecture.svg")
with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg_code)
print(f"Saved SVG model: {svg_path}")

# ---------------------------------------------------------------------------
# 3. Vector PDF Export for IEEE Manuscript
# ---------------------------------------------------------------------------
doc = fitz.open(stream=svg_code.encode("utf-8"), filetype="svg")
pdf_bytes = doc.convert_to_pdf()
pdf_doc = fitz.open("pdf", pdf_bytes)

# Save to figures/final and paper/
dst1 = os.path.join(FIG_FINAL, "fig1_system_architecture.pdf")
dst2 = os.path.join(PAPER_DIR, "system_architecture.pdf")
pdf_doc.save(dst1)
pdf_doc.save(dst2)

# Save 300 DPI preview
pix = pdf_doc[0].get_pixmap(dpi=300)
pix.save(os.path.join(FIG_FINAL, "fig1_system_architecture.png"))
pix.save(os.path.join(PAPER_DIR, "system_architecture.png"))

print(f"Exported Vector PDF: {dst1} and {dst2}")
