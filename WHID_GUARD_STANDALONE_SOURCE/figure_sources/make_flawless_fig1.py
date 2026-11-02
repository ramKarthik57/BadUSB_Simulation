"""
IEEE-Grade Vector System Architecture Generator (Figure 1).
Produces publication-quality vector PDF and 300 DPI PNG.
Strictly follows IEEE Transactions / S&P formatting.
Calibrated to EXACT 1:1 IEEE textwidth scale (515.52 pt = 7.16 in).
Zero scaling distortion in LaTeX.
"""

import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
matplotlib.rcParams["mathtext.fontset"] = "dejavusans"

BASE_DIR = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32"
PAPER_DIR = os.path.join(BASE_DIR, "paper")
os.makedirs(PAPER_DIR, exist_ok=True)

fig, ax = plt.subplots(figsize=(7.16, 2.22), dpi=300)
fig.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
ax.set_xlim(0, 100)
ax.set_ylim(0, 42)
ax.axis("off")

# Professional academic palette
C_FRAME = "#94A3B8"
C_CONTAINER = "#F8FAFC"
C_CARD = "#FFFFFF"
C_NAVY = "#1E3A8A"
C_SLATE = "#334155"
C_DARK = "#0F172A"
C_RED = "#B91C1C"
C_GREEN = "#047857"
C_BLUE = "#1D4ED8"
C_MUTED = "#475569"

# ==============================================================================
# 1. TIER 1: OPERATOR CONSOLE [x: 1.0 to 27.0]
# ==============================================================================
b1 = patches.FancyBboxPatch((1.0, 1.0), 26.0, 40.0, boxstyle="round,pad=0.2,rounding_size=0.8",
                            facecolor=C_CONTAINER, edgecolor=C_SLATE, linewidth=1.3, zorder=1)
ax.add_patch(b1)
ax.text(14.0, 38.8, "TIER 1: ATTACK OPERATOR CONSOLE", fontsize=8.2, fontweight="bold",
        color=C_SLATE, ha="center", va="center")
ax.plot([2.5, 25.5], [36.8, 36.8], color="#CBD5E1", lw=0.8)

# Card 1: Web App SPA
c1 = patches.FancyBboxPatch((2.2, 25.0), 23.6, 10.5, boxstyle="round,pad=0.15,rounding_size=0.5",
                            facecolor=C_CARD, edgecolor="#CBD5E1", lw=0.8, zorder=2)
ax.add_patch(c1)
ax.text(14.0, 33.2, "Mobile Browser SPA (Web UI)", fontsize=7.6, fontweight="bold", color=C_DARK, ha="center")
ax.text(3.5, 29.8, "Virtual Keyboard: 6-row touch matrix", fontsize=6.8, color=C_DARK)
ax.text(3.5, 27.2, "Touch Delta: 60 Hz relative mouse stream", fontsize=6.8, color=C_DARK)

# Card 2: Scenarios & Jitter
c2 = patches.FancyBboxPatch((2.2, 13.0), 23.6, 10.5, boxstyle="round,pad=0.15,rounding_size=0.5",
                            facecolor=C_CARD, edgecolor="#CBD5E1", lw=0.8, zorder=2)
ax.add_patch(c2)
ax.text(14.0, 21.2, "Scenario Engine & Jitter Config", fontsize=7.6, fontweight="bold", color=C_DARK, ha="center")
ax.text(3.5, 17.8, "Attack Triggers: Scenarios 1 to 4 REST API", fontsize=6.8, color=C_DARK)
ax.text(3.5, 15.2, "Cadence Jitter: Gaussian model (80 +/- 40 ms)", fontsize=6.8, color=C_DARK)

# Card 3: Emergency Abort Switch
c3 = patches.FancyBboxPatch((2.2, 2.5), 23.6, 9.0, boxstyle="round,pad=0.15,rounding_size=0.5",
                            facecolor=C_CARD, edgecolor="#CBD5E1", lw=0.8, zorder=2)
ax.add_patch(c3)
ax.text(14.0, 9.0, "Emergency Abort Switch", fontsize=7.6, fontweight="bold", color=C_RED, ha="center")
ax.text(3.5, 6.2, "Immediate stop trigger: asserts abort flag", fontsize=6.8, color=C_DARK)
ax.text(3.5, 4.0, "Sub-10 ms cooperative loop preemption", fontsize=6.8, color=C_DARK)


# ==============================================================================
# 2. TIER 2: ESP32-S3 WEAPONIZED IMPLANT [x: 35.5 to 64.5]
# ==============================================================================
b2 = patches.FancyBboxPatch((35.5, 1.0), 29.0, 40.0, boxstyle="round,pad=0.2,rounding_size=0.8",
                            facecolor=C_CONTAINER, edgecolor=C_NAVY, linewidth=1.3, zorder=1)
ax.add_patch(b2)
ax.text(50.0, 38.8, "TIER 2: ESP32-S3 WEAPONIZED IMPLANT", fontsize=8.2, fontweight="bold",
        color=C_NAVY, ha="center", va="center")
ax.plot([37.0, 63.0], [36.8, 36.8], color="#CBD5E1", lw=0.8)

# Core 0: Network & Core 1: Payload (top half)
c_c0 = patches.FancyBboxPatch((36.7, 25.0), 13.0, 10.5, boxstyle="round,pad=0.15,rounding_size=0.5",
                              facecolor=C_CARD, edgecolor="#CBD5E1", lw=0.8, zorder=2)
ax.add_patch(c_c0)
ax.text(43.2, 33.2, "Core 0: Wi-Fi/C2", fontsize=7.4, fontweight="bold", color=C_NAVY, ha="center")
ax.text(37.5, 29.8, "SoftAP & Station", fontsize=6.8, color=C_DARK)
ax.text(37.5, 27.2, "HTTP REST API", fontsize=6.8, color=C_DARK)

c_c1 = patches.FancyBboxPatch((50.5, 25.0), 13.0, 10.5, boxstyle="round,pad=0.15,rounding_size=0.5",
                              facecolor=C_CARD, edgecolor="#CBD5E1", lw=0.8, zorder=2)
ax.add_patch(c_c1)
ax.text(57.0, 33.2, "Core 1: Payload", fontsize=7.4, fontweight="bold", color=C_NAVY, ha="center")
ax.text(51.3, 29.8, "8-State FSM Loop", fontsize=6.8, color=C_DARK)
ax.text(51.3, 27.2, "10 ms smartDelay()", fontsize=6.8, color=C_DARK)

# FreeRTOS Spinlock Mailbox
c_mb = patches.FancyBboxPatch((36.7, 14.5), 26.8, 8.5, boxstyle="round,pad=0.15,rounding_size=0.5",
                              facecolor=C_CARD, edgecolor=C_NAVY, lw=0.9, linestyle="--", zorder=2)
ax.add_patch(c_mb)
ax.text(50.1, 20.5, "FreeRTOS Spinlock Mailbox (portMUX_TYPE)", fontsize=7.2, fontweight="bold", color=C_NAVY, ha="center")
ax.text(50.1, 17.5, "Thread-safe inter-core queue serializing async C2 commands", fontsize=6.7, color=C_MUTED, ha="center")

# TinyUSB Native Hardware OTG
c_usb = patches.FancyBboxPatch((36.7, 2.5), 26.8, 10.0, boxstyle="round,pad=0.15,rounding_size=0.5",
                               facecolor=C_CARD, edgecolor="#CBD5E1", lw=0.8, zorder=2)
ax.add_patch(c_usb)
ax.text(50.1, 9.8, "Native TinyUSB Composite OTG (GPIO 19/20)", fontsize=7.4, fontweight="bold", color=C_NAVY, ha="center")
ax.text(38.0, 6.8, "Full-Speed 12 Mbps PHY Differential Bus (D- / D+)", fontsize=6.8, color=C_DARK)
ax.text(38.0, 4.4, "Composite HID Endpoints: 104-Key KB + 3-Button Mouse", fontsize=6.8, color=C_DARK)


# ==============================================================================
# 3. TIER 3: WORKSTATION DEFENSE SUBSYSTEM [x: 73.0 to 99.0]
# ==============================================================================
b3 = patches.FancyBboxPatch((73.0, 1.0), 26.0, 40.0, boxstyle="round,pad=0.2,rounding_size=0.8",
                            facecolor=C_CONTAINER, edgecolor=C_SLATE, linewidth=1.3, zorder=1)
ax.add_patch(b3)
ax.text(86.0, 38.8, "TIER 3: WORKSTATION DEFENSE SUBSYSTEM", fontsize=8.0, fontweight="bold",
        color=C_SLATE, ha="center", va="center")
ax.plot([74.5, 97.5], [36.8, 36.8], color="#CBD5E1", lw=0.8)

# Stage A: Ingestion Layer (Top)
c_raw = patches.FancyBboxPatch((74.2, 27.0), 23.6, 8.8, boxstyle="round,pad=0.15,rounding_size=0.5",
                               facecolor=C_CARD, edgecolor="#CBD5E1", lw=0.8, zorder=2)
ax.add_patch(c_raw)
ax.text(86.0, 33.2, "Win32 Raw Input Ingestion", fontsize=7.6, fontweight="bold", color=C_DARK, ha="center")
ax.text(75.5, 30.2, "RegisterRawInputDevices() background hook", fontsize=6.8, color=C_DARK)
ax.text(75.5, 28.0, "Resolves per-device hDevice hardware handle", fontsize=6.8, color=C_DARK)

# Downward flow arrow 1
ax.annotate("", xy=(86.0, 25.5), xytext=(86.0, 27.0),
            arrowprops=dict(arrowstyle="->", color=C_SLATE, lw=1.2))

# Stage B: Dynamics Engine (Middle)
c_dyn = patches.FancyBboxPatch((74.2, 15.5), 23.6, 9.5, boxstyle="round,pad=0.15,rounding_size=0.5",
                               facecolor=C_CARD, edgecolor="#CBD5E1", lw=0.8, zorder=2)
ax.add_patch(c_dyn)
ax.text(86.0, 22.5, "Sliding-Window Dynamics Engine", fontsize=7.6, fontweight="bold", color=C_DARK, ha="center")
ax.text(75.5, 19.5, "Online FIFO: W = 10 keystrokes per hDevice", fontsize=6.8, color=C_DARK)
ax.text(75.5, 17.0, "Computes mean latency and dispersion CV = sigma / mu", fontsize=6.8, color=C_DARK)

# Downward flow arrow 2
ax.annotate("", xy=(86.0, 14.0), xytext=(86.0, 15.5),
            arrowprops=dict(arrowstyle="->", color=C_SLATE, lw=1.2))

# Stage C: Selective Enforcement Gate (Bottom)
c_gate = patches.FancyBboxPatch((74.2, 2.5), 23.6, 11.0, boxstyle="round,pad=0.15,rounding_size=0.5",
                                facecolor=C_CARD, edgecolor="#CBD5E1", lw=0.8, zorder=2)
ax.add_patch(c_gate)
ax.text(86.0, 11.2, "Selective Low-Level Hook Gate", fontsize=7.6, fontweight="bold", color=C_DARK, ha="center")
ax.text(75.5, 8.8, "WH_KEYBOARD_LL per-event interception", fontsize=6.8, color=C_DARK)

ax.text(79.5, 5.0, "[DROP] Rogue USB", fontsize=7.0, fontweight="bold", color=C_RED, ha="center",
        bbox=dict(boxstyle="square,pad=0.2", facecolor="#FEF2F2", edgecolor="#FCA5A5", lw=0.7))
ax.text(92.5, 5.0, "[PASS] Physical KB", fontsize=7.0, fontweight="bold", color=C_GREEN, ha="center",
        bbox=dict(boxstyle="square,pad=0.2", facecolor="#F0FDF4", edgecolor="#86EFAC", lw=0.7))


# ==============================================================================
# 4. CHANNELS & PROPER ARROW ROUTING
# ==============================================================================
# Channel 1: Wi-Fi [x: 27.0 to 35.5] (8.5-unit corridor at y = 30.0)
ax.annotate("", xy=(35.5, 30.0), xytext=(27.0, 30.0),
            arrowprops=dict(arrowstyle="<->", color=C_SLATE, lw=1.6))
ax.text(31.25, 33.5, "2.4 GHz Wi-Fi", fontsize=7.2, fontweight="bold", color=C_SLATE, ha="center")
ax.text(31.25, 26.5, "REST / JSON", fontsize=6.8, color=C_MUTED, ha="center")

# Channel 2: USB [x: 64.5 to 73.0]
# TinyUSB is at y=2.5..12.5. Routes up to Tier 3 Ingestion at y=31.0!
ax.annotate("", xy=(73.0, 31.0), xytext=(64.5, 7.5),
            arrowprops=dict(arrowstyle="->", color=C_NAVY, lw=1.7,
                            connectionstyle="angle,angleA=0,angleB=90,rad=4"))
ax.text(68.75, 19.5, "USB 2.0 PHY\n12 Mbps HID", fontsize=7.0, fontweight="bold", color=C_NAVY,
        ha="center", va="center", bbox=dict(boxstyle="square,pad=0.2", facecolor="#FFFFFF", edgecolor="#CBD5E1", lw=0.6))

# Physical Keyboard Input entering Tier 3 Ingestion
ax.annotate("", xy=(97.0, 31.0), xytext=(99.8, 31.0),
            arrowprops=dict(arrowstyle="<-", color=C_GREEN, lw=1.5))
ax.text(98.5, 33.8, "Host KB", fontsize=6.2, fontweight="bold", color=C_GREEN, ha="center")

pdf_out = os.path.join(PAPER_DIR, "system_architecture.pdf")
png_out = os.path.join(PAPER_DIR, "system_architecture.png")

fig.savefig(pdf_out)
fig.savefig(png_out, dpi=300)
plt.close(fig)

print(f"Generated Vector Figure 1: {pdf_out} and {png_out}")
