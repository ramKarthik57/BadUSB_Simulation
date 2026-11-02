#pragma once

#include <Arduino.h>

static const char INDEX_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>BadUSB Remote Controller</title>
<style>
  :root {
    --bg: #0b0f19;
    --card: #151e32;
    --border: #243250;
    --text: #f1f5f9;
    --muted: #94a3b8;
    --accent: #10b981;
    --accent-glow: rgba(16, 185, 129, 0.2);
    --danger: #ef4444;
    --danger-glow: rgba(239, 68, 68, 0.2);
    --warning: #f59e0b;
    --blue: #3b82f6;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    padding: 12px;
    max-width: 540px;
    margin: 0 auto;
    font-size: 14px;
  }
  header {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 12px;
  }
  .header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }
  .title { font-weight: 700; font-size: 17px; letter-spacing: 0.5px; display: flex; align-items: center; gap: 8px; }
  .badge {
    padding: 4px 8px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .badge-idle { background: #1e293b; color: var(--accent); border: 1px solid var(--accent); }
  .badge-running { background: #7c2d12; color: #ffedd5; border: 1px solid #f97316; animation: pulse 1.5s infinite; }
  .badge-stopped { background: #450a0a; color: #fecaca; border: 1px solid var(--danger); }
  @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.6; } 100% { opacity: 1; } }
  .meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    font-size: 12px;
    color: var(--muted);
  }
  .meta-item b { color: var(--text); }
  
  .tabs {
    display: flex;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    margin-bottom: 12px;
  }
  .tab-btn {
    flex: 1;
    padding: 10px 4px;
    border: none;
    border-radius: 8px;
    background: transparent;
    color: var(--muted);
    font-weight: 600;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .tab-btn.active {
    background: var(--border);
    color: var(--text);
  }
  .tab-pane { display: none; }
  .tab-pane.active { display: block; }

  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 12px;
  }
  .card-title {
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .btn {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    font-weight: 600;
    border-radius: 8px;
    border: 1px solid transparent;
    cursor: pointer;
    transition: transform 0.05s ease, background 0.15s ease;
    user-select: none;
  }
  .btn:active { transform: scale(0.97); }
  .btn-primary { background: var(--blue); color: white; border-color: #2563eb; }
  .btn-accent { background: var(--accent); color: #022c22; font-weight: 700; }
  .btn-danger { background: var(--danger); color: white; }
  .btn-secondary { background: #1e293b; color: var(--text); border-color: var(--border); }
  .btn-block { width: 100%; padding: 12px; }

  .scenario-card {
    background: #0f172a;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 10px;
  }
  .scenario-card.active-scenario {
    border-color: var(--accent);
    box-shadow: 0 0 10px var(--accent-glow);
  }
  .scenario-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
  }
  .scenario-name { font-weight: 600; font-size: 14px; }
  .scenario-desc { font-size: 12px; color: var(--muted); margin-bottom: 10px; }

  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
  .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; }

  textarea {
    width: 100%;
    height: 85px;
    background: #0b0f19;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px;
    color: var(--text);
    font-size: 14px;
    resize: none;
    margin-bottom: 6px;
    outline: none;
  }
  textarea:focus { border-color: var(--blue); }
  .char-count { text-align: right; font-size: 11px; color: var(--muted); margin-bottom: 8px; }

  .key-btn {
    padding: 10px 4px;
    font-size: 12px;
    background: #1e293b;
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 6px;
  }
  .key-btn:active { background: #334155; }
  .key-btn.danger { background: #450a0a; border-color: var(--danger); color: #fecaca; }

  .mod-btn {
    padding: 10px 4px;
    font-size: 13px;
    font-weight: 700;
    background: #1e293b;
    color: #94a3b8;
    border: 1px solid var(--border);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .mod-btn.active-mod {
    background: #0284c7;
    color: #ffffff;
    border-color: #38bdf8;
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
  }
  .win-direct-btn {
    background: linear-gradient(135deg, #1e3a8a, #2563eb);
    color: white;
    font-weight: 700;
    border: 1px solid #3b82f6;
  }
  .win-direct-btn:active { background: #1d4ed8; }

  .sub-tabs {
    display: flex;
    background: #0f172a;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 3px;
    gap: 3px;
    margin-bottom: 12px;
  }
  .sub-tab-btn {
    flex: 1;
    padding: 8px 2px;
    border: none;
    border-radius: 6px;
    background: transparent;
    color: var(--muted);
    font-weight: 600;
    font-size: 11px;
    cursor: pointer;
    text-align: center;
    transition: all 0.15s ease;
  }
  .sub-tab-btn.active {
    background: var(--border);
    color: var(--text);
  }
  .sub-pane { display: none; }
  .sub-pane.active { display: block; }

  /* Virtual Keyboard */
  .vk-box {
    background: #0b0f19;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 6px 3px;
    margin-bottom: 10px;
  }
  .vk-row {
    display: flex;
    gap: 2px;
    margin-bottom: 3px;
    justify-content: stretch;
  }
  .vk-k {
    flex: 1;
    min-width: 0;
    height: 35px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #1e293b;
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    user-select: none;
    transition: transform 0.05s ease, background 0.1s ease;
    padding: 0;
  }
  .vk-k:active {
    transform: scale(0.92);
    background: var(--blue);
    color: white;
  }
  .vk-k.w-12 { flex: 1.25; }
  .vk-k.w-15 { flex: 1.5; }
  .vk-k.w-18 { flex: 1.8; }
  .vk-k.w-20 { flex: 2; }
  .vk-k.w-space { flex: 4.8; }
  .vk-k.k-fn { background: #0f172a; font-size: 9px; color: var(--muted); }
  .vk-k.k-mod { background: #1e3a5f; color: #93c5fd; }
  .vk-k.k-act { background: #0284c7; color: white; border-color: #38bdf8; }
  .vk-k.k-del { background: #450a0a; color: #fecaca; }

  .live-box {
    background: #0b0f19;
    border: 1px dashed var(--blue);
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 12px;
  }
  .live-input {
    width: 100%;
    padding: 10px;
    background: #151e32;
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text);
    font-size: 13px;
    outline: none;
    margin-top: 6px;
  }
  .live-input:focus { border-color: var(--accent); }

  .input-field {
    width: 100%;
    padding: 10px;
    background: #0b0f19;
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text);
    font-size: 14px;
    margin-bottom: 10px;
  }

  .toast {
    position: fixed;
    bottom: 16px;
    left: 50%;
    transform: translateX(-50%);
    background: #1e293b;
    border: 1px solid var(--border);
    color: white;
    padding: 10px 18px;
    border-radius: 9999px;
    font-size: 13px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.25s ease;
    z-index: 9999;
  }
  .toast.show { opacity: 1; }
  .toast.success { border-color: var(--accent); color: #6ee7b7; background: #064e3b; }
  .toast.error { border-color: var(--danger); color: #fca5a5; background: #450a0a; }
  /* Touchpad & Mouse Styles */
  .touchpad-box {
    background: #0b0f19;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 12px;
  }
  .touchpad-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    font-size: 12px;
  }
  .touchpad {
    width: 100%;
    height: 230px;
    background: radial-gradient(circle at center, #172554 0%, #090d16 100%);
    border: 2px dashed #2563eb;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    touch-action: none;
    user-select: none;
    cursor: crosshair;
    position: relative;
    transition: border-color 0.15s ease, background 0.15s ease;
    margin-bottom: 10px;
  }
  .touchpad.active {
    border-color: var(--accent);
    background: radial-gradient(circle at center, #064e3b 0%, #090d16 100%);
  }
  .touchpad.drag-mode {
    border-color: var(--warning);
    background: radial-gradient(circle at center, #78350f 0%, #090d16 100%);
  }
  .touchpad-hint {
    color: var(--muted);
    font-size: 11px;
    text-align: center;
    pointer-events: none;
    line-height: 1.5;
  }
  .mouse-btn-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 8px;
  }
  .mouse-btn-primary {
    height: 52px;
    font-size: 15px;
    font-weight: 700;
    border-radius: 8px;
  }
  .mouse-btn-left {
    background: #1e40af;
    color: white;
    border-color: #3b82f6;
  }
  .mouse-btn-left:active { background: #2563eb; }
  .mouse-btn-right {
    background: #1e293b;
    color: var(--text);
    border-color: var(--border);
  }
  .mouse-btn-right:active { background: #334155; }
</style>
</head>
<body>

<header>
  <div class="header-top">
    <div class="title">
      <span>⚡ BadUSB Controller</span>
    </div>
    <span id="statusBadge" class="badge badge-idle">IDLE</span>
  </div>
  <div class="meta-grid">
    <div class="meta-item">USB HID: <b id="usbStatus">Ready</b></div>
    <div class="meta-item">Scenario: <b id="currentScenLabel">#1 (Notepad)</b></div>
    <div class="meta-item">STA IP: <b id="staIpLabel">...</b></div>
    <div class="meta-item">AP IP: <b>192.168.4.1</b></div>
  </div>
</header>

<div class="tabs">
  <button class="tab-btn active" onclick="switchTab('tabScenarios', this)">Scenarios</button>
  <button class="tab-btn" onclick="switchTab('tabKeyboard', this)">Keyboard</button>
  <button class="tab-btn" onclick="switchTab('tabMouse', this)">Mouse</button>
  <button class="tab-btn" onclick="switchTab('tabSettings', this)">Settings</button>
</div>

<!-- TAB 1: SCENARIOS -->
<div id="tabScenarios" class="tab-pane active">
  <div class="card">
    <div class="card-title">
      <span>Educational Demonstrations</span>
      <span style="font-size:12px; color:var(--muted)">Direct Launch</span>
    </div>

    <div class="scenario-card" id="cardScen1">
      <div class="scenario-head">
        <span class="scenario-name">1. Notepad Awareness</span>
        <button class="btn btn-accent" style="padding:6px 12px; font-size:12px" onclick="runScenario(1)">Launch</button>
      </div>
      <div class="scenario-desc">Simulates opening Notepad and auto-typing security advice.</div>
    </div>

    <div class="scenario-card" id="cardScen2">
      <div class="scenario-head">
        <span class="scenario-name">2. Portal Redirection</span>
        <button class="btn btn-accent" style="padding:6px 12px; font-size:12px" onclick="runScenario(2)">Launch</button>
      </div>
      <div class="scenario-desc">Opens command line and launches university portal in browser.</div>
    </div>

    <div class="scenario-card" id="cardScen3">
      <div class="scenario-head">
        <span class="scenario-name">3. Ransomware Awareness</span>
        <button class="btn btn-accent" style="padding:6px 12px; font-size:12px" onclick="runScenario(3)">Launch</button>
      </div>
      <div class="scenario-desc">Launches ransomware awareness education dialog.</div>
    </div>

    <div class="scenario-card" id="cardScen4">
      <div class="scenario-head">
        <span class="scenario-name">4. Wi-Fi Reconnaissance</span>
        <button class="btn btn-accent" style="padding:6px 12px; font-size:12px" onclick="runScenario(4)">Launch</button>
      </div>
      <div class="scenario-desc">Displays list of saved Wi-Fi profile names (non-destructive).</div>
    </div>

    <div class="grid-2" style="margin-top:12px">
      <button class="btn btn-secondary" style="padding:12px" onclick="nextScenario()">▶ Next (Physical Sync)</button>
      <button class="btn btn-danger" style="padding:12px" onclick="stopExecution()">⏹ Stop / Abort</button>
    </div>

    <!-- Adversarial Evasion / Stealth Cadence Toggle -->
    <div style="margin-top:14px; padding:12px; background:#0f172a; border:1px solid var(--border); border-radius:8px">
      <div style="display:flex; justify-content:space-between; align-items:center">
        <div>
          <div style="font-size:12px; font-weight:700; color:var(--text)">Adversarial Evasion (Stealth Mode)</div>
          <div style="font-size:11px; color:var(--muted)">Human Cadence Emulation with IKI Jitter</div>
        </div>
        <input type="checkbox" id="stealthModeToggle" onchange="toggleStealthMode(this.checked)" style="width:20px; height:20px; accent-color:var(--blue); cursor:pointer">
      </div>
      <div id="stealthParamsBox" style="margin-top:8px; display:none; font-size:11px; color:var(--muted); border-top:1px solid #1e293b; padding-top:6px">
        <div style="display:flex; justify-content:space-between; margin-bottom:3px">
          <span>Base Delay: <b id="stealthBaseLabel" style="color:var(--text)">80ms</b></span>
          <span>Jitter: <b id="stealthJitterLabel" style="color:var(--text)">±40ms</b></span>
        </div>
        <div style="font-size:10px; color:#94a3b8">Applies 150–300ms cognitive micro-pauses at spaces & punctuation.</div>
      </div>
    </div>
  </div>
</div>

<!-- TAB 2: REMOTE KEYBOARD -->
<div id="tabKeyboard" class="tab-pane">
  <!-- Pinned Sticky Modifiers & Win Header -->
  <div class="card" style="margin-bottom:8px">
    <div class="card-title">
      <span>Hardware Modifiers</span>
      <span id="activeModsLabel" style="font-size:12px; font-weight:700; color:var(--muted)">None</span>
    </div>
    <div class="grid-4" style="margin-bottom:6px">
      <button id="modBtn_ctrl" class="btn mod-btn" onclick="toggleModifier('ctrl')">Ctrl</button>
      <button id="modBtn_alt" class="btn mod-btn" onclick="toggleModifier('alt')">Alt</button>
      <button id="modBtn_shift" class="btn mod-btn" onclick="toggleModifier('shift')">Shift</button>
      <button id="modBtn_win" class="btn mod-btn" onclick="toggleModifier('win')">Win ⊞</button>
    </div>
    <div style="display:flex; justify-content:space-between; align-items:center; font-size:11px; color:var(--muted)">
      <label style="display:flex; align-items:center; gap:5px; cursor:pointer">
        <input type="checkbox" id="autoReleaseCheck" checked style="accent-color:var(--blue)">
        <span>Auto-release modifier</span>
      </label>
      <div style="display:flex; gap:6px">
        <button class="btn btn-secondary" style="padding:4px 8px; font-size:11px" onclick="clearModifiers()">Clear</button>
        <button class="btn btn-danger" style="padding:4px 8px; font-size:11px" onclick="releaseAllKeys()">Release All</button>
      </div>
    </div>
  </div>

  <!-- Sub-Navigation for Keyboard Views -->
  <div class="sub-tabs">
    <button class="sub-tab-btn active" id="btnSubFullKbd" onclick="switchSubTab('subFullKbd', this)">Full Layout</button>
    <button class="sub-tab-btn" id="btnSubShortcuts" onclick="switchSubTab('subShortcuts', this)">Shortcuts</button>
    <button class="sub-tab-btn" id="btnSubLiveText" onclick="switchSubTab('subLiveText', this)">Text & Live</button>
    <button class="sub-tab-btn" id="btnSubNavNum" onclick="switchSubTab('subNavNum', this)">Numpad</button>
  </div>

  <!-- SUB-PANE 1: FULL ON-SCREEN LAPTOP KEYBOARD -->
  <div id="subFullKbd" class="sub-pane active">
    <div class="vk-box">
      <!-- Function Row -->
      <div class="vk-row">
        <button class="vk-k k-fn" onclick="sendKeyOrCombo('ESCAPE')">Esc</button>
        <button class="vk-k k-fn" onclick="sendKeyOrCombo('F1')">F1</button>
        <button class="vk-k k-fn" onclick="sendKeyOrCombo('F2')">F2</button>
        <button class="vk-k k-fn" onclick="sendKeyOrCombo('F3')">F3</button>
        <button class="vk-k k-fn" onclick="sendKeyOrCombo('F4')">F4</button>
        <button class="vk-k k-fn" onclick="sendKeyOrCombo('F5')">F5</button>
        <button class="vk-k k-fn" onclick="sendKeyOrCombo('F6')">F6</button>
        <button class="vk-k k-fn" onclick="sendKeyOrCombo('F7')">F7</button>
        <button class="vk-k k-fn" onclick="sendKeyOrCombo('F8')">F8</button>
        <button class="vk-k k-fn" onclick="sendKeyOrCombo('F9')">F9</button>
        <button class="vk-k k-fn" onclick="sendKeyOrCombo('F10')">F10</button>
        <button class="vk-k k-fn" onclick="sendKeyOrCombo('F11')">F11</button>
        <button class="vk-k k-fn" onclick="sendKeyOrCombo('F12')">F12</button>
        <button class="vk-k k-del" onclick="sendKeyOrCombo('DELETE')">Del</button>
      </div>

      <!-- Number Row -->
      <div class="vk-row">
        <button class="vk-k" id="vk_grave" onclick="vkChar('`')">`</button>
        <button class="vk-k" id="vk_1" onclick="vkChar('1')">1</button>
        <button class="vk-k" id="vk_2" onclick="vkChar('2')">2</button>
        <button class="vk-k" id="vk_3" onclick="vkChar('3')">3</button>
        <button class="vk-k" id="vk_4" onclick="vkChar('4')">4</button>
        <button class="vk-k" id="vk_5" onclick="vkChar('5')">5</button>
        <button class="vk-k" id="vk_6" onclick="vkChar('6')">6</button>
        <button class="vk-k" id="vk_7" onclick="vkChar('7')">7</button>
        <button class="vk-k" id="vk_8" onclick="vkChar('8')">8</button>
        <button class="vk-k" id="vk_9" onclick="vkChar('9')">9</button>
        <button class="vk-k" id="vk_0" onclick="vkChar('0')">0</button>
        <button class="vk-k" id="vk_minus" onclick="vkChar('-')">-</button>
        <button class="vk-k" id="vk_equal" onclick="vkChar('=')">=</button>
        <button class="vk-k w-15 k-del" onclick="sendKeyOrCombo('BACKSPACE')">⌫</button>
      </div>

      <!-- QWERTY Row -->
      <div class="vk-row">
        <button class="vk-k w-12 k-mod" onclick="sendKeyOrCombo('TAB')">Tab</button>
        <button class="vk-k" id="vk_q" onclick="vkChar('q')">Q</button>
        <button class="vk-k" id="vk_w" onclick="vkChar('w')">W</button>
        <button class="vk-k" id="vk_e" onclick="vkChar('e')">E</button>
        <button class="vk-k" id="vk_r" onclick="vkChar('r')">R</button>
        <button class="vk-k" id="vk_t" onclick="vkChar('t')">T</button>
        <button class="vk-k" id="vk_y" onclick="vkChar('y')">Y</button>
        <button class="vk-k" id="vk_u" onclick="vkChar('u')">U</button>
        <button class="vk-k" id="vk_i" onclick="vkChar('i')">I</button>
        <button class="vk-k" id="vk_o" onclick="vkChar('o')">O</button>
        <button class="vk-k" id="vk_p" onclick="vkChar('p')">P</button>
        <button class="vk-k" id="vk_lbracket" onclick="vkChar('[')">[</button>
        <button class="vk-k" id="vk_rbracket" onclick="vkChar(']')">]</button>
        <button class="vk-k" id="vk_backslash" onclick="vkChar('\\')">\</button>
      </div>

      <!-- Home Row -->
      <div class="vk-row">
        <button class="vk-k w-15" id="vk_caps" onclick="toggleCaps()">Caps</button>
        <button class="vk-k" id="vk_a" onclick="vkChar('a')">A</button>
        <button class="vk-k" id="vk_s" onclick="vkChar('s')">S</button>
        <button class="vk-k" id="vk_d" onclick="vkChar('d')">D</button>
        <button class="vk-k" id="vk_f" onclick="vkChar('f')">F</button>
        <button class="vk-k" id="vk_g" onclick="vkChar('g')">G</button>
        <button class="vk-k" id="vk_h" onclick="vkChar('h')">H</button>
        <button class="vk-k" id="vk_j" onclick="vkChar('j')">J</button>
        <button class="vk-k" id="vk_k" onclick="vkChar('k')">K</button>
        <button class="vk-k" id="vk_l" onclick="vkChar('l')">L</button>
        <button class="vk-k" id="vk_semicolon" onclick="vkChar(';')">;</button>
        <button class="vk-k" id="vk_quote" onclick="vkChar('\'')">'</button>
        <button class="vk-k w-18 k-mod" style="background:#1e3a8a; color:white" onclick="sendKeyOrCombo('ENTER')">Enter ↵</button>
      </div>

      <!-- Shift Row -->
      <div class="vk-row">
        <button class="vk-k w-18 k-mod" onclick="toggleModifier('shift')">⇧ Shift</button>
        <button class="vk-k" id="vk_z" onclick="vkChar('z')">Z</button>
        <button class="vk-k" id="vk_x" onclick="vkChar('x')">X</button>
        <button class="vk-k" id="vk_c" onclick="vkChar('c')">C</button>
        <button class="vk-k" id="vk_v" onclick="vkChar('v')">V</button>
        <button class="vk-k" id="vk_b" onclick="vkChar('b')">B</button>
        <button class="vk-k" id="vk_n" onclick="vkChar('n')">N</button>
        <button class="vk-k" id="vk_m" onclick="vkChar('m')">M</button>
        <button class="vk-k" id="vk_comma" onclick="vkChar(',')">,</button>
        <button class="vk-k" id="vk_dot" onclick="vkChar('.')">.</button>
        <button class="vk-k" id="vk_slash" onclick="vkChar('/')">/</button>
        <button class="vk-k w-18 k-mod" onclick="toggleModifier('shift')">⇧ Shift</button>
      </div>

      <!-- Bottom Control Row -->
      <div class="vk-row">
        <button class="vk-k k-mod" onclick="toggleModifier('ctrl')">Ctrl</button>
        <button class="vk-k k-mod" onclick="sendDirectWin()">⊞ Win</button>
        <button class="vk-k k-mod" onclick="toggleModifier('alt')">Alt</button>
        <button class="vk-k w-space" onclick="sendKeyOrCombo('SPACE')">Spacebar</button>
        <button class="vk-k k-mod" onclick="toggleModifier('alt')">Alt</button>
        <button class="vk-k k-fn" onclick="sendKeyOrCombo('MENU')">Menu ▤</button>
        <button class="vk-k k-mod" onclick="toggleModifier('ctrl')">Ctrl</button>
      </div>
    </div>
  </div>

  <!-- SUB-PANE 2: SHORTCUTS LIBRARY -->
  <div id="subShortcuts" class="sub-pane">
    <div class="card">
      <div class="card-title"><span>Windows System & Navigation</span></div>
      <div class="grid-3" style="margin-bottom:6px">
        <button class="btn key-btn" onclick="sendDirectWin()">⊞ Start Menu</button>
        <button class="btn key-btn" onclick="sendShortcut('GUI', 'r')">Win + R (Run)</button>
        <button class="btn key-btn" onclick="sendShortcut('GUI', 'd')">Win + D (Desktop)</button>
      </div>
      <div class="grid-3" style="margin-bottom:6px">
        <button class="btn key-btn" onclick="sendShortcut('GUI', 'e')">Win + E (Explorer)</button>
        <button class="btn key-btn" onclick="sendShortcut('GUI', 'l')">Win + L (Lock)</button>
        <button class="btn key-btn" onclick="sendShortcut('GUI', 'x')">Win + X (Power)</button>
      </div>
      <div class="grid-3" style="margin-bottom:6px">
        <button class="btn key-btn" onclick="sendShortcut('GUI', 'v')">Win + V (Clips)</button>
        <button class="btn key-btn" onclick="sendShortcut('GUI', 'i')">Win + I (Settings)</button>
        <button class="btn key-btn" onclick="sendShortcut('GUI', 'TAB')">Win + Tab</button>
      </div>
      <div class="grid-3">
        <button class="btn key-btn" onclick="sendShortcut('GUI+SHIFT', 's')">Win+Shift+S (Snip)</button>
        <button class="btn key-btn" onclick="sendShortcut('GUI', '.')">Win + . (Emoji)</button>
        <button class="btn key-btn" onclick="sendShortcut('GUI', 'UP')">Win + ↑ (Max)</button>
      </div>
    </div>

    <div class="card">
      <div class="card-title"><span>Process & Window Management</span></div>
      <div class="grid-3" style="margin-bottom:6px">
        <button class="btn key-btn" onclick="sendShortcut('ALT', 'TAB')">Alt + Tab</button>
        <button class="btn key-btn" onclick="sendShortcut('ALT', 'F4')">Alt + F4</button>
        <button class="btn key-btn" onclick="sendShortcut('CTRL+SHIFT', 'ESCAPE')">Ctrl+Shift+Esc</button>
      </div>
      <div class="grid-3">
        <button class="btn key-btn" onclick="sendShortcut('CTRL+ALT', 'DELETE')">Ctrl+Alt+Del</button>
        <button class="btn key-btn" onclick="sendKeyOrCombo('PRINTSCREEN')">PrtScn</button>
        <button class="btn key-btn" onclick="sendKeyOrCombo('MENU')">Menu ▤</button>
      </div>
    </div>

    <div class="card">
      <div class="card-title"><span>Editing & Clipboard</span></div>
      <div class="grid-3" style="margin-bottom:6px">
        <button class="btn key-btn" onclick="sendShortcut('CTRL', 'c')">Ctrl + C (Copy)</button>
        <button class="btn key-btn" onclick="sendShortcut('CTRL', 'v')">Ctrl + V (Paste)</button>
        <button class="btn key-btn" onclick="sendShortcut('CTRL', 'x')">Ctrl + X (Cut)</button>
      </div>
      <div class="grid-3" style="margin-bottom:6px">
        <button class="btn key-btn" onclick="sendShortcut('CTRL', 'a')">Ctrl + A (All)</button>
        <button class="btn key-btn" onclick="sendShortcut('CTRL', 'z')">Ctrl + Z (Undo)</button>
        <button class="btn key-btn" onclick="sendShortcut('CTRL', 'y')">Ctrl + Y (Redo)</button>
      </div>
      <div class="grid-3">
        <button class="btn key-btn" onclick="sendShortcut('CTRL', 's')">Ctrl + S (Save)</button>
        <button class="btn key-btn" onclick="sendShortcut('CTRL', 'f')">Ctrl + F (Find)</button>
        <button class="btn key-btn" onclick="sendShortcut('CTRL', 'p')">Ctrl + P (Print)</button>
      </div>
    </div>

    <div class="card">
      <div class="card-title"><span>Browser Controls</span></div>
      <div class="grid-3" style="margin-bottom:6px">
        <button class="btn key-btn" onclick="sendShortcut('CTRL', 't')">Ctrl + T (Tab)</button>
        <button class="btn key-btn" onclick="sendShortcut('CTRL', 'w')">Ctrl + W (Close)</button>
        <button class="btn key-btn" onclick="sendShortcut('CTRL+SHIFT', 't')">Reopen Tab</button>
      </div>
      <div class="grid-3" style="margin-bottom:6px">
        <button class="btn key-btn" onclick="sendKeyOrCombo('F5')">F5 (Refresh)</button>
        <button class="btn key-btn" onclick="sendShortcut('CTRL', 'F5')">Ctrl + F5</button>
        <button class="btn key-btn" onclick="sendKeyOrCombo('F11')">F11 (Full)</button>
      </div>
      <div class="grid-3">
        <button class="btn key-btn" onclick="sendShortcut('ALT', 'LEFT')">Alt + ← (Back)</button>
        <button class="btn key-btn" onclick="sendShortcut('ALT', 'RIGHT')">Alt + → (Fwd)</button>
        <button class="btn key-btn" onclick="sendShortcut('CTRL', 'n')">Ctrl + N (New)</button>
      </div>
    </div>

    <div class="card">
      <div class="card-title"><span>Custom Shortcut Runner</span></div>
      <div style="display:flex; gap:6px; margin-bottom:8px">
        <input type="text" id="custModInput" class="input-field" placeholder="Mods (e.g. CTRL+SHIFT)" style="margin-bottom:0; flex:1">
        <input type="text" id="custKeyInput" class="input-field" placeholder="Key (e.g. s, F12)" style="margin-bottom:0; width:100px">
      </div>
      <button class="btn btn-primary btn-block" onclick="runCustomShortcut()">Send Custom Shortcut</button>
    </div>
  </div>

  <!-- SUB-PANE 3: TEXT & LIVE PHONE TYPING -->
  <div id="subLiveText" class="sub-pane">
    <div class="live-box">
      <div style="font-weight:700; font-size:13px; color:#38bdf8; margin-bottom:4px">🔴 Live Wireless Typing</div>
      <p style="font-size:11px; color:var(--muted)">Tap the box below: your phone keyboard opens & keystrokes type directly into your laptop live.</p>
      <input type="text" id="liveTypeInput" class="live-input" placeholder="Tap here to type on laptop live..." autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
    </div>

    <div class="card">
      <div class="card-title">
        <span>Bulk Text Transmitter</span>
        <span style="font-size:12px; color:var(--muted)">Max 256 chars</span>
      </div>
      <textarea id="textPayload" placeholder="Paste or type text to send in bulk (e.g., commands, notes, URLs)..." oninput="updateCharCount()"></textarea>
      <div class="char-count"><span id="charCount">0</span> / 256</div>
      <div class="grid-2">
        <button class="btn btn-primary" style="padding:11px" onclick="sendCustomText(false)">Send Text</button>
        <button class="btn btn-accent" style="padding:11px" onclick="sendCustomText(true)">Send + Enter ↵</button>
      </div>
    </div>
  </div>

  <!-- SUB-PANE 4: NAVIGATION & NUMPAD -->
  <div id="subNavNum" class="sub-pane">
    <div class="card">
      <div class="card-title"><span>Cursor & Navigation Pad</span></div>
      <div style="display:flex; flex-direction:column; align-items:center; gap:6px; margin-bottom:12px">
        <button class="btn key-btn" style="width:70px; height:40px; font-size:16px" onclick="sendKeyOrCombo('UP')">▲</button>
        <div style="display:flex; gap:6px">
          <button class="btn key-btn" style="width:70px; height:40px; font-size:16px" onclick="sendKeyOrCombo('LEFT')">◀</button>
          <button class="btn key-btn" style="width:70px; height:40px; font-size:16px" onclick="sendKeyOrCombo('DOWN')">▼</button>
          <button class="btn key-btn" style="width:70px; height:40px; font-size:16px" onclick="sendKeyOrCombo('RIGHT')">▶</button>
        </div>
      </div>
      <div class="grid-3" style="margin-bottom:6px">
        <button class="btn key-btn" onclick="sendKeyOrCombo('HOME')">Home</button>
        <button class="btn key-btn" onclick="sendKeyOrCombo('END')">End</button>
        <button class="btn key-btn" onclick="sendKeyOrCombo('INSERT')">Insert</button>
      </div>
      <div class="grid-3" style="margin-bottom:6px">
        <button class="btn key-btn" onclick="sendKeyOrCombo('PAGEUP')">Page Up</button>
        <button class="btn key-btn" onclick="sendKeyOrCombo('PAGEDOWN')">Page Down</button>
        <button class="btn key-btn danger" onclick="sendKeyOrCombo('DELETE')">Delete</button>
      </div>
      <div class="grid-3">
        <button class="btn key-btn" onclick="sendShortcut('CTRL', 'LEFT')">Ctrl + ◀ (Word)</button>
        <button class="btn key-btn" onclick="sendShortcut('CTRL', 'RIGHT')">Ctrl + ▶ (Word)</button>
        <button class="btn key-btn" onclick="sendShortcut('CTRL', 'BACKSPACE')">Ctrl + ⌫</button>
      </div>
    </div>

    <div class="card">
      <div class="card-title"><span>Numeric Keypad (Numpad)</span></div>
      <div class="grid-4" style="margin-bottom:6px">
        <button class="btn key-btn" onclick="sendKeyOrCombo('CAPSLOCK')">NumLock</button>
        <button class="btn key-btn" onclick="sendKeyOrCombo('/')">/</button>
        <button class="btn key-btn" onclick="sendKeyOrCombo('*')">*</button>
        <button class="btn key-btn" onclick="sendKeyOrCombo('-')">-</button>
      </div>
      <div class="grid-4" style="margin-bottom:6px">
        <button class="btn key-btn" onclick="sendKeyOrCombo('7')">7</button>
        <button class="btn key-btn" onclick="sendKeyOrCombo('8')">8</button>
        <button class="btn key-btn" onclick="sendKeyOrCombo('9')">9</button>
        <button class="btn key-btn" onclick="sendKeyOrCombo('+')">+</button>
      </div>
      <div class="grid-4" style="margin-bottom:6px">
        <button class="btn key-btn" onclick="sendKeyOrCombo('4')">4</button>
        <button class="btn key-btn" onclick="sendKeyOrCombo('5')">5</button>
        <button class="btn key-btn" onclick="sendKeyOrCombo('6')">6</button>
        <button class="btn key-btn" onclick="sendKeyOrCombo('BACKSPACE')">⌫</button>
      </div>
      <div class="grid-4" style="margin-bottom:6px">
        <button class="btn key-btn" onclick="sendKeyOrCombo('1')">1</button>
        <button class="btn key-btn" onclick="sendKeyOrCombo('2')">2</button>
        <button class="btn key-btn" onclick="sendKeyOrCombo('3')">3</button>
        <button class="btn key-btn key-accent" onclick="sendKeyOrCombo('ENTER')">↵ Enter</button>
      </div>
      <div class="grid-2">
        <button class="btn key-btn" style="padding:10px" onclick="sendKeyOrCombo('0')">0</button>
        <button class="btn key-btn" style="padding:10px" onclick="sendKeyOrCombo('.')">.</button>
      </div>
    </div>
  </div>
</div>

<!-- TAB 3: MOUSE CONTROL -->
<div id="tabMouse" class="tab-pane">
  <div class="touchpad-box">
    <div class="touchpad-head">
      <span><b>Touchpad Trackpad</b></span>
      <span id="dragLockStatus" style="font-weight:700; color:var(--muted)">Normal Mode</span>
    </div>
    <div id="trackpadSurface" class="touchpad">
      <div style="font-size:24px; margin-bottom:4px">🖱️</div>
      <div class="touchpad-hint">
        <b>Drag finger:</b> Move cursor<br>
        <b>Tap:</b> Left Click &nbsp;|&nbsp; <b>2-Finger Tap:</b> Right Click<br>
        <b>2-Finger Drag:</b> Scroll Wheel
      </div>
    </div>

    <!-- Main Left / Right Click buttons -->
    <div class="mouse-btn-row">
      <button class="btn mouse-btn-primary mouse-btn-left" onclick="sendMouseClick('left')">Left Click</button>
      <button class="btn mouse-btn-primary mouse-btn-right" onclick="sendMouseClick('right')">Right Click</button>
    </div>

    <!-- Secondary Click & Drag Lock Options -->
    <div class="grid-4" style="margin-bottom:8px">
      <button class="btn key-btn" onclick="sendMouseClick('double')">Double ↵↵</button>
      <button class="btn key-btn" onclick="sendMouseClick('middle')">Middle ⊙</button>
      <button id="dragLockBtn" class="btn key-btn" onclick="toggleDragLock()">🔒 Drag Lock</button>
      <button class="btn key-btn danger" onclick="releaseMouseAll()">Release ↺</button>
    </div>

    <!-- Sensitivity Slider -->
    <div style="margin-top:10px; background:#151e32; padding:10px; border-radius:8px; border:1px solid var(--border)">
      <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px">
        <span>Cursor Sensitivity:</span>
        <b id="sensLabel" style="color:var(--blue)">1.8x</b>
      </div>
      <input type="range" id="sensSlider" min="0.5" max="3.5" step="0.1" value="1.8" style="width:100%; accent-color:var(--blue)" oninput="updateSensitivity()">
    </div>
  </div>

  <!-- SCROLL WHEEL & DIRECTIONAL NUDGE PAD -->
  <div class="card">
    <div class="card-title">
      <span>Scroll & Precision Nudge</span>
      <span style="font-size:12px; color:var(--muted)">Step: <b id="nudgeStepLabel">20px</b></span>
    </div>

    <!-- Scroll Ribbon -->
    <div class="grid-2" style="margin-bottom:12px">
      <button class="btn btn-secondary" style="padding:12px" onclick="sendMouseScroll(4)">▲ Scroll Up (Wheel)</button>
      <button class="btn btn-secondary" style="padding:12px" onclick="sendMouseScroll(-4)">▼ Scroll Down (Wheel)</button>
    </div>

    <!-- Pixel-by-Pixel Directional Nudge Pad -->
    <div style="display:flex; flex-direction:column; align-items:center; gap:6px; margin-bottom:12px">
      <button class="btn key-btn" style="width:65px; height:38px; font-size:16px" onclick="nudgeMouse(0, -1)">▲</button>
      <div style="display:flex; gap:6px">
        <button class="btn key-btn" style="width:65px; height:38px; font-size:16px" onclick="nudgeMouse(-1, 0)">◀</button>
        <button class="btn key-btn" style="width:65px; height:38px; font-size:13px; font-weight:700" onclick="sendMouseClick('left')">CLICK</button>
        <button class="btn key-btn" style="width:65px; height:38px; font-size:16px" onclick="nudgeMouse(1, 0)">▶</button>
      </div>
      <button class="btn key-btn" style="width:65px; height:38px; font-size:16px" onclick="nudgeMouse(0, 1)">▼</button>
    </div>

    <!-- Nudge Step Presets -->
    <div class="grid-3">
      <button class="btn key-btn" onclick="setNudgeStep(5)">Precision (5px)</button>
      <button class="btn key-btn" style="border-color:var(--blue)" onclick="setNudgeStep(20)">Normal (20px)</button>
      <button class="btn key-btn" onclick="setNudgeStep(50)">Fast (50px)</button>
    </div>
  </div>
</div>

<!-- TAB 4: SETTINGS -->
<div id="tabSettings" class="tab-pane">
  <div class="card">
    <div class="card-title"><span>Authentication</span></div>
    <label style="font-size:12px; color:var(--muted); display:block; margin-bottom:4px;">Security PIN</label>
    <input type="password" id="authPin" class="input-field" placeholder="Enter PIN" value="badusb123">
    <button class="btn btn-secondary btn-block" onclick="savePin()">Set PIN & Authenticate</button>
  </div>

  <div class="card">
    <div class="card-title"><span>Network Details</span></div>
    <p style="font-size:12px; color:var(--muted); line-height:1.6; margin-bottom:8px">
      • <b>Access Point Mode:</b> SSID: <code style="color:var(--text)">BadUSB-Controller</code> (IP: 192.168.4.1)<br>
      • <b>Station Mode:</b> Connects to your phone hotspot so laptop and phone can stay on the same hotspot subnet.<br>
      • <b>mDNS Address:</b> <a href="http://badusb.local" style="color:var(--blue)">http://badusb.local</a>
    </p>
    <button class="btn btn-secondary btn-block" onclick="refreshStatus()">Refresh Device State</button>
  </div>
</div>

<div id="toast" class="toast">Command sent</div>

<script>
  let authToken = sessionStorage.getItem('badusb_token') || 'badusb123';
  const stickyMods = { ctrl: false, alt: false, shift: false, win: false };
  let capsLock = false;

  function toggleModifier(mod) {
    stickyMods[mod] = !stickyMods[mod];
    updateModifierUI();
    updateKeyboardLabels();
  }

  function clearModifiers() {
    stickyMods.ctrl = false;
    stickyMods.alt = false;
    stickyMods.shift = false;
    stickyMods.win = false;
    updateModifierUI();
    updateKeyboardLabels();
  }

  function toggleCaps() {
    capsLock = !capsLock;
    const btn = document.getElementById('vk_caps');
    if (btn) btn.classList.toggle('k-act', capsLock);
    sendKey('CAPSLOCK');
    updateKeyboardLabels();
  }

  function getActiveModifiersString() {
    const list = [];
    if (stickyMods.ctrl) list.push('CTRL');
    if (stickyMods.alt) list.push('ALT');
    if (stickyMods.shift) list.push('SHIFT');
    if (stickyMods.win) list.push('GUI');
    return list.join('+');
  }

  function updateModifierUI() {
    ['ctrl', 'alt', 'shift', 'win'].forEach(m => {
      const btn = document.getElementById('modBtn_' + m);
      if (btn) {
        btn.classList.toggle('active-mod', !!stickyMods[m]);
      }
    });
    const label = document.getElementById('activeModsLabel');
    const act = getActiveModifiersString();
    if (label) {
      label.innerText = act ? act : 'None';
      label.style.color = act ? '#38bdf8' : 'var(--muted)';
    }
  }

  function updateKeyboardLabels() {
    const shiftOn = stickyMods.shift;
    const upper = shiftOn || capsLock;

    const symShift = {
      'vk_grave': ['`', '~'], 'vk_1': ['1', '!'], 'vk_2': ['2', '@'], 'vk_3': ['3', '#'],
      'vk_4': ['4', '$'], 'vk_5': ['5', '%'], 'vk_6': ['6', '^'], 'vk_7': ['7', '&'],
      'vk_8': ['8', '*'], 'vk_9': ['9', '('], 'vk_0': ['0', ')'], 'vk_minus': ['-', '_'],
      'vk_equal': ['=', '+'], 'vk_lbracket': ['[', '{'], 'vk_rbracket': [']', '}'],
      'vk_backslash': ['\\', '|'], 'vk_semicolon': [';', ':'], 'vk_quote': ["'", '"'],
      'vk_comma': [',', '<'], 'vk_dot': ['.', '>'], 'vk_slash': ['/', '?']
    };

    for (const [id, [norm, sh]] of Object.entries(symShift)) {
      const el = document.getElementById(id);
      if (el) el.innerText = shiftOn ? sh : norm;
    }

    const letters = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m'];
    letters.forEach(ch => {
      const el = document.getElementById('vk_' + ch);
      if (el) el.innerText = upper ? ch.toUpperCase() : ch.toLowerCase();
    });
  }

  function vkChar(baseChar) {
    const shiftOn = stickyMods.shift;
    const upper = shiftOn || capsLock;
    let charToSend = baseChar;

    const symMap = {
      '`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&',
      '8': '*', '9': '(', '0': ')', '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|',
      ';': ':', "'": '"', ',': '<', '.': '>', '/': '?'
    };

    if (shiftOn && symMap[baseChar]) {
      charToSend = symMap[baseChar];
    } else if (upper && baseChar >= 'a' && baseChar <= 'z') {
      charToSend = baseChar.toUpperCase();
    }

    sendKeyOrCombo(charToSend);
  }

  function switchTab(tabId, btn) {
    document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    const pane = document.getElementById(tabId);
    if (pane) pane.classList.add('active');
    if (btn) {
      btn.classList.add('active');
    } else {
      const activeBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick')?.includes(tabId));
      if (activeBtn) activeBtn.classList.add('active');
    }
  }

  function switchSubTab(subId, btn) {
    document.querySelectorAll('.sub-pane').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.sub-tab-btn').forEach(el => el.classList.remove('active'));
    const pane = document.getElementById(subId);
    if (pane) pane.classList.add('active');
    if (btn) {
      btn.classList.add('active');
    } else {
      const activeBtn = Array.from(document.querySelectorAll('.sub-tab-btn')).find(b => b.getAttribute('onclick')?.includes(subId));
      if (activeBtn) activeBtn.classList.add('active');
    }
  }

  function runCustomShortcut() {
    const mod = (document.getElementById('custModInput').value || '').trim();
    const key = (document.getElementById('custKeyInput').value || '').trim();
    if (!key && !mod) {
      showToast('Enter modifier or key', true);
      return;
    }
    if (mod) {
      sendShortcut(mod, key);
    } else {
      sendKey(key);
    }
  }

  function showToast(msg, isError = false) {
    const t = document.getElementById('toast');
    t.innerText = msg;
    t.className = 'toast show ' + (isError ? 'error' : 'success');
    setTimeout(() => { t.className = 'toast'; }, 2200);
  }

  function updateCharCount() {
    const len = document.getElementById('textPayload').value.length;
    document.getElementById('charCount').innerText = len;
  }

  async function apiPost(endpoint, data = {}) {
    try {
      const token = authToken || 'badusb123';
      data.token = token;
      data.pin = token;

      const res = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Auth-Token': token
        },
        body: JSON.stringify(data)
      });
      const json = await res.json();
      if (!res.ok) {
        showToast(json.error || 'Request failed', true);
        return null;
      }
      return json;
    } catch (e) {
      showToast('Network error', true);
      return null;
    }
  }

  async function refreshStatus() {
    try {
      const res = await fetch('/api/status');
      if (!res.ok) return;
      const data = await res.json();

      const badge = document.getElementById('statusBadge');
      badge.innerText = data.state;
      badge.className = 'badge badge-' + (data.state === 'RUNNING' ? 'running' : (data.state === 'STOPPED' ? 'stopped' : 'idle'));

      document.getElementById('usbStatus').innerText = data.usb_ready ? 'Ready' : 'Waiting';
      document.getElementById('currentScenLabel').innerText = '#' + data.current_scenario + ' (' + data.scenario_name + ')';
      document.getElementById('staIpLabel').innerText = data.sta_ip || 'Disconnected';

      document.querySelectorAll('.scenario-card').forEach(el => el.classList.remove('active-scenario'));
      const activeCard = document.getElementById('cardScen' + data.current_scenario);
      if (activeCard) activeCard.classList.add('active-scenario');

      if (typeof data.stealth_enabled !== 'undefined') {
        const tgl = document.getElementById('stealthModeToggle');
        const box = document.getElementById('stealthParamsBox');
        if (tgl && document.activeElement !== tgl) {
          tgl.checked = !!data.stealth_enabled;
          if (box) box.style.display = tgl.checked ? 'block' : 'none';
        }
      }
    } catch(e) {}
  }

  async function runScenario(id) {
    const res = await apiPost('/api/scenario/select', { id: id });
    if (res && res.success) {
      showToast('Started Scenario ' + id);
      refreshStatus();
    }
  }

  async function nextScenario() {
    const res = await apiPost('/api/scenario/next');
    if (res && res.success) {
      showToast('Advanced to Scenario ' + res.next_id);
      refreshStatus();
    }
  }

  async function stopExecution() {
    const res = await apiPost('/api/scenario/stop');
    if (res && res.success) {
      showToast('Stopped and released keys');
      refreshStatus();
    }
  }

  async function toggleStealthMode(enabled) {
    const res = await apiPost('/api/settings/stealth', { enabled: enabled, baseMs: 80, jitterMs: 40 });
    const box = document.getElementById('stealthParamsBox');
    if (box) box.style.display = enabled ? 'block' : 'none';
    if (res && res.success) {
      showToast(enabled ? 'Stealth Evasion Armed (Cadence Jitter Active)' : 'Stealth Mode Disabled (Standard BadUSB)');
    }
  }

  async function sendCustomText(withEnter = false) {
    const ta = document.getElementById('textPayload');
    let text = ta.value;
    if (!text) {
      showToast('Please type text first', true);
      return;
    }
    if (withEnter) {
      text += '\n';
    }
    const res = await apiPost('/api/keyboard/text', { text: text });
    if (res && res.success) {
      showToast('Text transmitted to laptop');
      ta.value = '';
      updateCharCount();
    }
  }

  async function sendDirectWin() {
    const res = await apiPost('/api/keyboard/key', { key: 'WIN' });
    if (res && res.success) {
      showToast('Windows Key Tapped (Start Menu)');
    }
  }

  async function sendKey(name) {
    const res = await apiPost('/api/keyboard/key', { key: name });
    if (res && res.success) {
      showToast('Sent: ' + name);
    }
  }

  async function sendShortcut(mod, key) {
    const res = await apiPost('/api/keyboard/shortcut', { modifiers: mod, key: key });
    if (res && res.success) {
      showToast('Shortcut: ' + mod + '+' + key);
    }
  }

  async function sendKeyOrCombo(keyName) {
    const act = getActiveModifiersString();
    if (act) {
      await sendShortcut(act, keyName);
      const autoRel = document.getElementById('autoReleaseCheck');
      if (autoRel && autoRel.checked) {
        clearModifiers();
      }
    } else {
      await sendKey(keyName);
    }
  }

  async function releaseAllKeys() {
    const res = await apiPost('/api/keyboard/release');
    if (res && res.success) {
      clearModifiers();
      showToast('Emergency Release Complete');
    }
  }

  function savePin() {
    const pin = document.getElementById('authPin').value;
    if (pin) {
      authToken = pin;
      sessionStorage.setItem('badusb_token', pin);
      showToast('PIN saved');
    }
  }

  // --- Mouse Controller State & Functions ---
  let mouseSens = 1.8;
  let dragLock = false;
  let nudgeStep = 20;

  function updateSensitivity() {
    mouseSens = parseFloat(document.getElementById('sensSlider').value);
    document.getElementById('sensLabel').innerText = mouseSens.toFixed(1) + 'x';
  }

  function setNudgeStep(step) {
    nudgeStep = step;
    document.getElementById('nudgeStepLabel').innerText = step + 'px';
  }

  async function sendMouseMove(dx, dy, wheel = 0) {
    return await apiPost('/api/mouse/move', { x: Math.round(dx), y: Math.round(dy), wheel: Math.round(wheel) });
  }

  async function sendMouseClick(btn) {
    const res = await apiPost('/api/mouse/click', { button: btn });
    if (res && res.success) {
      showToast(btn.toUpperCase() + ' Click');
    }
  }

  async function sendMouseScroll(wheel) {
    const res = await apiPost('/api/mouse/scroll', { wheel: wheel });
    if (res && res.success) {
      showToast(wheel > 0 ? 'Scrolled Up' : 'Scrolled Down');
    }
  }

  async function toggleDragLock() {
    dragLock = !dragLock;
    const btn = document.getElementById('dragLockBtn');
    const badge = document.getElementById('dragLockStatus');
    const pad = document.getElementById('trackpadSurface');

    if (dragLock) {
      await apiPost('/api/mouse/press', { button: 'left' });
      btn.style.background = '#78350f';
      btn.style.borderColor = 'var(--warning)';
      btn.style.color = '#fef08a';
      badge.innerText = '🔒 Dragging (Left Held)';
      badge.style.color = 'var(--warning)';
      pad.classList.add('drag-mode');
      showToast('Drag Lock Active (Left Click Held)');
    } else {
      await apiPost('/api/mouse/release', { button: 'left' });
      btn.style.background = '';
      btn.style.borderColor = '';
      btn.style.color = '';
      badge.innerText = 'Normal Mode';
      badge.style.color = 'var(--muted)';
      pad.classList.remove('drag-mode');
      showToast('Drag Lock Released');
    }
  }

  async function releaseMouseAll() {
    dragLock = false;
    const btn = document.getElementById('dragLockBtn');
    const badge = document.getElementById('dragLockStatus');
    const pad = document.getElementById('trackpadSurface');
    btn.style.background = '';
    btn.style.borderColor = '';
    btn.style.color = '';
    badge.innerText = 'Normal Mode';
    badge.style.color = 'var(--muted)';
    pad.classList.remove('drag-mode');

    const res = await apiPost('/api/mouse/release', { button: 'all' });
    if (res && res.success) {
      showToast('All Mouse Buttons Released');
    }
  }

  function nudgeMouse(dirX, dirY) {
    sendMouseMove(dirX * nudgeStep, dirY * nudgeStep);
  }

  // Trackpad Touch Gestures
  function initTrackpad() {
    const pad = document.getElementById('trackpadSurface');
    if (!pad) return;

    let startX = 0, startY = 0;
    let lastX = 0, lastY = 0;
    let startTime = 0;
    let touchMoved = false;
    let isTwoFinger = false;
    let lastTapTime = 0;
    let moveThrottle = false;
    let queuedX = 0, queuedY = 0, queuedWheel = 0;

    function flushMovement() {
      if (queuedX !== 0 || queuedY !== 0 || queuedWheel !== 0) {
        sendMouseMove(queuedX, queuedY, queuedWheel);
        queuedX = 0;
        queuedY = 0;
        queuedWheel = 0;
      }
      moveThrottle = false;
    }

    pad.addEventListener('touchstart', (e) => {
      pad.classList.add('active');
      const touches = e.touches;
      startTime = Date.now();
      touchMoved = false;

      if (touches.length === 1) {
        isTwoFinger = false;
        startX = touches[0].clientX;
        startY = touches[0].clientY;
        lastX = startX;
        lastY = startY;
      } else if (touches.length >= 2) {
        isTwoFinger = true;
        startY = (touches[0].clientY + touches[1].clientY) / 2;
        lastY = startY;
      }
    }, { passive: false });

    pad.addEventListener('touchmove', (e) => {
      e.preventDefault();
      const touches = e.touches;
      touchMoved = true;

      if (touches.length === 1 && !isTwoFinger) {
        const curX = touches[0].clientX;
        const curY = touches[0].clientY;
        const rawDx = (curX - lastX) * mouseSens;
        const rawDy = (curY - lastY) * mouseSens;
        lastX = curX;
        lastY = curY;

        queuedX += rawDx;
        queuedY += rawDy;

        if (!moveThrottle) {
          moveThrottle = true;
          setTimeout(flushMovement, 22);
        }
      } else if (touches.length >= 2) {
        const curY = (touches[0].clientY + touches[1].clientY) / 2;
        const dy = curY - lastY;
        lastY = curY;

        const scrollDelta = Math.round(dy / 8);
        if (scrollDelta !== 0) {
          queuedWheel += scrollDelta;
          if (!moveThrottle) {
            moveThrottle = true;
            setTimeout(flushMovement, 35);
          }
        }
      }
    }, { passive: false });

    pad.addEventListener('touchend', (e) => {
      pad.classList.remove('active');
      flushMovement();

      const duration = Date.now() - startTime;
      if (!touchMoved && duration < 240) {
        if (isTwoFinger) {
          sendMouseClick('right');
        } else {
          const now = Date.now();
          if ((now - lastTapTime) < 280) {
            sendMouseClick('double');
            lastTapTime = 0;
          } else {
            sendMouseClick('left');
            lastTapTime = now;
          }
        }
      }
    });
  }

  // Initialize both live typing and trackpad
  window.addEventListener('DOMContentLoaded', () => {
    initTrackpad();

    const liveInp = document.getElementById('liveTypeInput');
    if (liveInp) {
      liveInp.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace') {
          e.preventDefault();
          sendKeyOrCombo('BACKSPACE');
        } else if (e.key === 'Enter') {
          e.preventDefault();
          sendKeyOrCombo('ENTER');
        } else if (e.key === 'Tab') {
          e.preventDefault();
          sendKeyOrCombo('TAB');
        } else if (e.key === 'Escape') {
          e.preventDefault();
          sendKeyOrCombo('ESCAPE');
        }
      });

      liveInp.addEventListener('input', (e) => {
        const val = e.data || e.target.value;
        if (val) {
          for (let i = 0; i < val.length; i++) {
            sendKeyOrCombo(val[i]);
          }
        }
        e.target.value = '';
      });
    }
  });

  setInterval(refreshStatus, 1500);
  refreshStatus();
</script>
</body>
</html>
)rawliteral";
