import os

FIG_SOURCE = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\figures\source"

# 1. Mermaid Fig 2 (Adversarial FSM)
mmd_fig2 = """stateDiagram-v2
    [*] --> STATE_BOOTING: Power-On
    STATE_BOOTING --> STATE_USB_WAIT: Init OK
    STATE_USB_WAIT --> STATE_STARTUP_PAYLOAD: Enum OK (Δt ≥ 3.5s)
    STATE_USB_WAIT --> STATE_ERROR: Enum Timeout
    STATE_ERROR --> STATE_BOOTING: WDT Reboot
    STATE_STARTUP_PAYLOAD --> STATE_IDLE: Injection Done
    STATE_IDLE --> STATE_RUNNING: REST Command (Authenticated)
    STATE_RUNNING --> STATE_IDLE: Complete
    STATE_RUNNING --> STATE_RUNNING: δt = 10ms Quantum
    STATE_RUNNING --> STATE_USB_WAIT: USB Disconnect / Bus Drop
    STATE_RUNNING --> STATE_STOPPING: Abort (φ_stop = 1)
    STATE_STOPPING --> STATE_STOPPED: ≤10ms Kill
    STATE_STOPPED --> STATE_IDLE: Deassert Software Flags (State Clear)
"""
with open(os.path.join(FIG_SOURCE, "fig2_scenario_fsm.mmd"), "w", encoding="utf-8") as f:
    f.write(mmd_fig2)

# 2. Mermaid Fig 3 (Selective Defense Pipeline)
mmd_fig3 = """graph LR
    subgraph USB_Bus["USB Physical Layer"]
        KB["Physical Keyboard (h_legit)"] --> HUB["USB Root Hub"]
        ESP["Rogue ESP32-S3 (h_rogue)"] --> HUB
    end

    subgraph Host_Daemon["Host OS Defense Daemon (WHID-Guard Framework)"]
        HUB --> HOOK["Selective Filter Hook (WH_KEYBOARD_LL)"]
        HUB --> RAW["Raw Input Pre-Filter (WM_INPUT, RIDEV_INPUTSINK)"]

        HOOK -->|"Scancode Stream"| GATE["Selective Filter Gate"]
        RAW --> DYN["Dynamics Engine (W = 5)"]
        DYN --> DEC["Decision Boundary (μ < 25ms ∨ CV < 0.15)"]
        DEC -->|"Lockdown (κ ≥ 8)"| QUAR["Quarantine Table (Blacklist)"]
        QUAR -->|"Filter Origin"| GATE
        WDT["15s Watchdog (Auto-Reset)"] -.->|"Trigger Flush"| OVR["Global Pipeline Flush & Gate Override"]
        OVR -.->|"Flush Q_quar & Restore Gate"| QUAR
    end

    GATE -->|"Match: h_origin ∈ Q_quar"| DROP["[DROP EVENT] Suppress Scancode"]
    GATE -->|"Match: h_origin ∉ Q_quar"| PASS["[PASS EVENT] Allow Keystroke"]
    PASS --> WIN["Active Foreground Window"]
"""
with open(os.path.join(FIG_SOURCE, "fig3_selective_defense.mmd"), "w", encoding="utf-8") as f:
    f.write(mmd_fig3)

# 3. Native draw.io XML for Fig 1
drawio_fig1 = """<mxfile host="Electron" modified="2026-11-02T10:50:00.000Z" agent="PipeJack Diagram Engine" version="24.0.0">
  <diagram id="fig1" name="Fig1_System_Architecture">
    <mxGraphModel dx="760" dy="180" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="760" pageHeight="180" background="#ffffff">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- Tier 1 -->
        <mxCell id="t1" value="Tier 1: Mobile C2 Controller" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#faf5ff;strokeColor=#a855f7;strokeWidth=1.2;fontStyle=1;fontColor=#6b21a8;verticalAlign=top;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="14" y="8" width="172" height="164" as="geometry" />
        </mxCell>
        <mxCell id="t1_b1" value="Touch Web Console&#xa;&lt;font color='#64748b' style='font-size:7.5px'&gt;Single-Page App (SPA)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#c084fc;fontStyle=1;fontSize=9;fontColor=#1e293b;" vertex="1" parent="1">
          <mxGeometry x="24" y="34" width="152" height="34" as="geometry" />
        </mxCell>
        <mxCell id="t1_b2" value="REST Attack Engine&#xa;&lt;font color='#64748b' style='font-size:7.5px'&gt;Scenarios 1–4, Cadence Jitter&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#c084fc;fontStyle=1;fontSize=9;fontColor=#1e293b;" vertex="1" parent="1">
          <mxGeometry x="24" y="78" width="152" height="34" as="geometry" />
        </mxCell>
        <mxCell id="t1_b3" value="802.11 b/g/n Station&#xa;&lt;font color='#64748b' style='font-size:7.5px'&gt;Station Link (192.168.4.2)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#c084fc;fontStyle=1;fontSize=9;fontColor=#1e293b;" vertex="1" parent="1">
          <mxGeometry x="24" y="122" width="152" height="34" as="geometry" />
        </mxCell>
        <!-- Tier 2 -->
        <mxCell id="t2" value="Tier 2: Weaponized ESP32-S3 Hardware Implant" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f0fdf4;strokeColor=#22c55e;strokeWidth=1.2;fontStyle=1;fontColor=#15803d;verticalAlign=top;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="246" y="8" width="268" height="164" as="geometry" />
        </mxCell>
        <mxCell id="t2_c0" value="Core 0: Network&#xa;&lt;font color='#64748b' style='font-size:7.2px'&gt;SoftAP &amp; Web Server&#xa;Gateway IP: 192.168.4.1&#xa;TCP/IP Baseband&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#4ade80;fontStyle=1;fontSize=8.8;fontColor=#1e293b;" vertex="1" parent="1">
          <mxGeometry x="256" y="27" width="118" height="49" as="geometry" />
        </mxCell>
        <mxCell id="t2_c1" value="Core 1: HID Engine&#xa;&lt;font color='#64748b' style='font-size:7.2px'&gt;8-State Scenario FSM&#xa;Native TinyUSB HID&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#4ade80;fontStyle=1;fontSize=8.8;fontColor=#1e293b;" vertex="1" parent="1">
          <mxGeometry x="386" y="27" width="118" height="49" as="geometry" />
        </mxCell>
        <mxCell id="t2_mb" value="Lock-Free Atomic Ring Buffer (Non-blocking Shared Mailbox)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dcfce7;strokeColor=#16a34a;fontStyle=1;fontSize=7.4;fontColor=#14532d;" vertex="1" parent="1">
          <mxGeometry x="256" y="80" width="248" height="24" as="geometry" />
        </mxCell>
        <mxCell id="t2_ant" value="2.4 GHz Antenna&#xa;&lt;font color='#64748b' style='font-size:7.2px'&gt;SoftAP Transceiver&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#4ade80;fontStyle=1;fontSize=8.8;fontColor=#1e293b;" vertex="1" parent="1">
          <mxGeometry x="256" y="116" width="118" height="38" as="geometry" />
        </mxCell>
        <mxCell id="t2_usb" value="Native USB OTG PHY&#xa;&lt;font color='#ea580c' style='font-size:7.2px'&gt;GPIO 19/20 (D+/D-)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff7ed;strokeColor=#ea580c;fontStyle=1;fontSize=8.8;fontColor=#9a3412;" vertex="1" parent="1">
          <mxGeometry x="386" y="116" width="118" height="38" as="geometry" />
        </mxCell>
        <!-- Tier 3 -->
        <mxCell id="t3" value="Tier 3: Windows Host (WHID-Guard)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#3b82f6;strokeWidth=1.2;fontStyle=1;fontColor=#1d4ed8;verticalAlign=top;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="574" y="8" width="172" height="164" as="geometry" />
        </mxCell>
        <mxCell id="t3_b1" value="Selective Filter Hook (WH_KEYBOARD_LL)&#xa;&lt;font color='#1d4ed8' style='font-size:6.8px'&gt;[PASS] Operator / [DROP] Rogue&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3b82f6;fontStyle=1;fontSize=8.0;fontColor=#1e3a8a;" vertex="1" parent="1">
          <mxGeometry x="584" y="32" width="152" height="26" as="geometry" />
        </mxCell>
        <mxCell id="t3_b2" value="Quarantine Table &amp; Policy Gate&#xa;&lt;font color='#64748b' style='font-size:6.8px'&gt;Isolates Rogue h_rogue (15s Reset)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3b82f6;fontStyle=1;fontSize=8.2;fontColor=#1e3a8a;" vertex="1" parent="1">
          <mxGeometry x="584" y="66" width="152" height="26" as="geometry" />
        </mxCell>
        <mxCell id="t3_b3" value="Behavioral Dynamics Engine (W=5)&#xa;&lt;font color='#64748b' style='font-size:6.8px'&gt;mu &lt; 25ms or CV &lt; 0.15&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3b82f6;fontStyle=1;fontSize=8.2;fontColor=#1e3a8a;" vertex="1" parent="1">
          <mxGeometry x="584" y="100" width="152" height="26" as="geometry" />
        </mxCell>
        <mxCell id="t3_b4" value="Raw Input Monitor (WM_INPUT)&#xa;&lt;font color='#64748b' style='font-size:6.8px'&gt;Pre-Hook Device Attribution (h_dev)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3b82f6;fontStyle=1;fontSize=8.2;fontColor=#1e3a8a;" vertex="1" parent="1">
          <mxGeometry x="584" y="134" width="152" height="26" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
with open(os.path.join(FIG_SOURCE, "fig1_system_architecture.drawio"), "w", encoding="utf-8") as f:
    f.write(drawio_fig1)

# 4. Native draw.io XML for Fig 2
drawio_fig2 = """<mxfile host="Electron" modified="2026-11-02T10:50:00.000Z" agent="PipeJack Diagram Engine" version="24.0.0">
  <diagram id="fig2" name="Fig2_Scenario_FSM">
    <mxGraphModel dx="760" dy="180" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="760" pageHeight="180" background="#ffffff">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="s_boot" value="STATE_BOOTING&#xa;&lt;font color='#64748b' style='font-size:7.2px'&gt;Power-On &amp; USB Init&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#3b82f6;fontStyle=1;fontSize=8.8;fontColor=#1e3a8a;" vertex="1" parent="1">
          <mxGeometry x="44" y="32" width="108" height="40" as="geometry" />
        </mxCell>
        <mxCell id="s_wait" value="STATE_USB_WAIT&#xa;&lt;font color='#64748b' style='font-size:7.2px'&gt;Host Enum Δt ≥ 3.5s&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#3b82f6;fontStyle=1;fontSize=8.8;fontColor=#1e3a8a;" vertex="1" parent="1">
          <mxGeometry x="190" y="32" width="112" height="40" as="geometry" />
        </mxCell>
        <mxCell id="s_start" value="STATE_STARTUP_PAYLOAD&#xa;&lt;font color='#64748b' style='font-size:7.2px'&gt;Scenario 1 Injection&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#3b82f6;fontStyle=1;fontSize=8.0;fontColor=#1e3a8a;" vertex="1" parent="1">
          <mxGeometry x="340" y="32" width="136" height="40" as="geometry" />
        </mxCell>
        <mxCell id="s_idle" value="STATE_IDLE&#xa;&lt;font color='#475569' style='font-size:7.2px'&gt;Quiescent / Ready&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;fontStyle=1;fontSize=8.8;fontColor=#1e40af;" vertex="1" parent="1">
          <mxGeometry x="504" y="32" width="96" height="40" as="geometry" />
        </mxCell>
        <mxCell id="s_run" value="STATE_RUNNING&#xa;&lt;font color='#166534' style='font-size:7.2px'&gt;Payload Active&#xa;Quantum δt = 10ms&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dcfce7;strokeColor=#16a34a;fontStyle=1;fontSize=8.8;fontColor=#14532d;" vertex="1" parent="1">
          <mxGeometry x="664" y="32" width="88" height="42" as="geometry" />
        </mxCell>
        <mxCell id="s_err" value="STATE_ERROR&#xa;&lt;font color='#64748b' style='font-size:7.2px'&gt;Watchdog / Fault&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff7ed;strokeColor=#ea580c;fontStyle=1;fontSize=8.8;fontColor=#9a3412;" vertex="1" parent="1">
          <mxGeometry x="190" y="122" width="112" height="40" as="geometry" />
        </mxCell>
        <mxCell id="s_stopd" value="STATE_STOPPED&#xa;&lt;font color='#991b1b' style='font-size:6.0px'&gt;Deassert Software Flags (State Clear)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fef2f2;strokeColor=#ef4444;fontStyle=1;fontSize=8.8;fontColor=#991b1b;" vertex="1" parent="1">
          <mxGeometry x="504" y="122" width="118" height="40" as="geometry" />
        </mxCell>
        <mxCell id="s_stopg" value="STATE_STOPPING&#xa;&lt;font color='#64748b' style='font-size:7.0px'&gt;Preempt Request&#xa;Mailbox φ_stop = 1&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fef2f2;strokeColor=#ef4444;fontStyle=1;fontSize=8.8;fontColor=#991b1b;" vertex="1" parent="1">
          <mxGeometry x="664" y="122" width="88" height="40" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
with open(os.path.join(FIG_SOURCE, "fig2_scenario_fsm.drawio"), "w", encoding="utf-8") as f:
    f.write(drawio_fig2)

# 5. Native draw.io XML for Fig 3
drawio_fig3 = """<mxfile host="Electron" modified="2026-11-02T10:50:00.000Z" agent="PipeJack Diagram Engine" version="24.0.0">
  <diagram id="fig3" name="Fig3_Selective_Defense">
    <mxGraphModel dx="760" dy="180" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="760" pageHeight="180" background="#ffffff">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="kb" value="Physical Keyboard&#xa;&lt;font color='#64748b' style='font-size:7.2px'&gt;Genuine HID (h_legit)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#3b82f6;fontStyle=1;fontSize=8.8;fontColor=#1e3a8a;" vertex="1" parent="1">
          <mxGeometry x="12" y="32" width="108" height="38" as="geometry" />
        </mxCell>
        <mxCell id="esp" value="Rogue ESP32-S3&#xa;&lt;font color='#64748b' style='font-size:7.2px'&gt;BadUSB (h_rogue)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fef2f2;strokeColor=#ef4444;fontStyle=1;fontSize=8.8;fontColor=#991b1b;" vertex="1" parent="1">
          <mxGeometry x="12" y="112" width="108" height="38" as="geometry" />
        </mxCell>
        <mxCell id="hub" value="USB Root Hub" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f1f5f9;strokeColor=#64748b;fontStyle=1;fontSize=8.5;fontColor=#334155;rotation=-90;" vertex="1" parent="1">
          <mxGeometry x="138" y="24" width="24" height="134" as="geometry" />
        </mxCell>
        <mxCell id="host" value="Host OS Defense Daemon (WHID-Guard Framework)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#94a3b8;strokeWidth=1.0;strokeDashed=1;fontStyle=1;fontColor=#475569;verticalAlign=top;spacingTop=4;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="180" y="8" width="448" height="166" as="geometry" />
        </mxCell>
        <mxCell id="hook" value="Selective Filter Hook&#xa;&lt;font color='#64748b' style='font-size:7.0px'&gt;(WH_KEYBOARD_LL Hook)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3b82f6;fontStyle=1;fontSize=8.0;fontColor=#1e3a8a;" vertex="1" parent="1">
          <mxGeometry x="194" y="32" width="118" height="38" as="geometry" />
        </mxCell>
        <mxCell id="raw" value="Raw Input Pre-Filter&#xa;&lt;font color='#64748b' style='font-size:6.8px'&gt;WM_INPUT (RIDEV_INPUTSINK)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3b82f6;fontStyle=1;fontSize=8.0;fontColor=#1e3a8a;" vertex="1" parent="1">
          <mxGeometry x="194" y="112" width="118" height="38" as="geometry" />
        </mxCell>
        <mxCell id="dyn" value="Dynamics Engine&#xa;&lt;font color='#64748b' style='font-size:7.0px'&gt;Sliding Window (W = 5)&#xa;mu_IKI &amp; CV_IKI&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#3b82f6;fontStyle=1;fontSize=8.8;fontColor=#1e3a8a;" vertex="1" parent="1">
          <mxGeometry x="338" y="108" width="118" height="44" as="geometry" />
        </mxCell>
        <mxCell id="gate" value="Selective Filter Gate&#xa;&lt;font color='#1e3a8a' style='font-size:7.0px'&gt;Inspects h_origin in Q_quar&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;fontStyle=1;fontSize=8.8;fontColor=#1e40af;" vertex="1" parent="1">
          <mxGeometry x="480" y="28" width="138" height="32" as="geometry" />
        </mxCell>
        <mxCell id="quar" value="Quarantine Table (Blacklist)&#xa;&lt;font color='#b91c1c' style='font-size:6.8px'&gt;Isolates Handle h_rogue&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fef2f2;strokeColor=#ef4444;fontStyle=1;fontSize=8.2;fontColor=#991b1b;" vertex="1" parent="1">
          <mxGeometry x="480" y="72" width="138" height="26" as="geometry" />
        </mxCell>
        <mxCell id="dec" value="Decision Boundary&#xa;&lt;font color='#7e22ce' style='font-size:7.0px'&gt;mu &lt; 25ms or CV &lt; 0.15&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#faf5ff;strokeColor=#a855f7;fontStyle=1;fontSize=8.5;fontColor=#6b21a8;" vertex="1" parent="1">
          <mxGeometry x="480" y="110" width="138" height="32" as="geometry" />
        </mxCell>
        <mxCell id="wdt" value="15s Watchdog (Auto-Reset)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff7ed;strokeColor=#ea580c;strokeDashed=1;fontStyle=1;fontSize=7.2;fontColor=#9a3412;" vertex="1" parent="1">
          <mxGeometry x="480" y="150" width="138" height="18" as="geometry" />
        </mxCell>
        <mxCell id="ovr" value="Global Pipeline Flush&#xa;&lt;font color='#c2410c' style='font-size:6.8px'&gt;&amp; Gate Override&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff7ed;strokeColor=#ea580c;fontStyle=1;fontSize=7.2;fontColor=#9a3412;" vertex="1" parent="1">
          <mxGeometry x="646" y="142" width="96" height="26" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
with open(os.path.join(FIG_SOURCE, "fig3_selective_defense.drawio"), "w", encoding="utf-8") as f:
    f.write(drawio_fig3)

print("Updated Mermaid and draw.io source models successfully.")
