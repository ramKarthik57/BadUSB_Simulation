"""
IEEE-Grade Vector FSM Diagram Generator (Figure 2).
Produces publication-quality vector PDF and 300 DPI PNG.
Strictly follows IEEE Transactions / S&P formatting.
Includes all 8 states documented in Section III-B:
  STATE_BOOTING, STATE_USB_WAIT, STATE_STARTUP, STATE_IDLE,
  STATE_RUNNING, STATE_STOPPING, STATE_STOPPED, STATE_ERROR.
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

fig, ax = plt.subplots(figsize=(7.16, 2.15), dpi=300)
fig.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
ax.set_xlim(0, 100)
ax.set_ylim(0, 42)
ax.axis("off")

C_FRAME = "#94A3B8"
C_TEXT_DARK = "#0F172A"
C_TEXT_MUTED = "#475569"
C_NAVY = "#1E3A8A"
C_BLUE = "#1D4ED8"
C_RED = "#B91C1C"
C_GREEN = "#047857"
C_SLATE = "#334155"
C_AMBER = "#B45309"

top_y0, top_h = 24.0, 16.0

def draw_state(ax, x0, y0, w, h, title, action_lines, color=C_NAVY, bg="#FFFFFF"):
    b = patches.FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.2,rounding_size=0.6",
                               facecolor=bg, edgecolor=color, linewidth=1.3, zorder=2)
    ax.add_patch(b)
    hdr = patches.FancyBboxPatch((x0, y0 + h - 5.0), w, 5.0, boxstyle="round,pad=0.2,rounding_size=0.6",
                                 facecolor=color, edgecolor=color, linewidth=0.8, zorder=3)
    ax.add_patch(hdr)
    ax.text(x0 + w/2.0, y0 + h - 2.5, title, fontsize=7.4, fontweight="bold",
            color="#FFFFFF", ha="center", va="center", zorder=4)
    for idx, txt in enumerate(action_lines):
        ax.text(x0 + w/2.0, y0 + h - 8.2 - idx * 3.8, txt, fontsize=6.8, color=C_TEXT_DARK,
                ha="center", va="center", zorder=4)

# ==============================================================================
# TOP ROW: 5 Operational States [y: 24.0 to 40.0]
# ==============================================================================
draw_state(ax, 1.0, top_y0, 16.0, top_h, "STATE_BOOTING",
           ["Power-on reset", "Peripheral init", "Start TinyUSB stack"])

draw_state(ax, 21.5, top_y0, 16.5, top_h, "STATE_USB_WAIT",
           ["Bus enumeration", "3,500 ms wait", "Driver bind sync"])

draw_state(ax, 42.5, top_y0, 16.5, top_h, "STATE_STARTUP",
           ["Scenario 1 payload", "Executes once", "Initial baseline"])

draw_state(ax, 63.5, top_y0, 16.5, top_h, "STATE_IDLE",
           ["Quiescent ready", "Awaits commands", "Mailbox polling"])

draw_state(ax, 84.0, top_y0, 15.0, top_h, "STATE_RUNNING",
           ["Injecting Scenarios 1-4", "smartDelay() 10 ms", "Cooperative loop"], color=C_BLUE)

# Sequential Top Transitions
ax.annotate("", xy=(21.5, top_y0 + top_h/2.0), xytext=(17.0, top_y0 + top_h/2.0),
            arrowprops=dict(arrowstyle="->", color=C_SLATE, lw=1.3))
ax.text(19.25, top_y0 + top_h/2.0 + 2.2, "Init", fontsize=6.6, fontweight="bold", color=C_SLATE, ha="center")

ax.annotate("", xy=(42.5, top_y0 + top_h/2.0), xytext=(38.0, top_y0 + top_h/2.0),
            arrowprops=dict(arrowstyle="->", color=C_SLATE, lw=1.3))
ax.text(40.25, top_y0 + top_h/2.0 + 2.2, "3.5 s", fontsize=6.6, fontweight="bold", color=C_SLATE, ha="center")

ax.annotate("", xy=(63.5, top_y0 + top_h/2.0), xytext=(59.0, top_y0 + top_h/2.0),
            arrowprops=dict(arrowstyle="->", color=C_SLATE, lw=1.3))
ax.text(61.25, top_y0 + top_h/2.0 + 2.2, "Done", fontsize=6.6, fontweight="bold", color=C_SLATE, ha="center")

# IDLE <-> RUNNING Dual Transitions
ax.annotate("", xy=(84.0, top_y0 + 11.5), xytext=(80.0, top_y0 + 11.5),
            arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1.4))
ax.text(82.0, top_y0 + 13.8, "Launch", fontsize=6.6, fontweight="bold", color=C_BLUE, ha="center")

ax.annotate("", xy=(80.0, top_y0 + 4.5), xytext=(84.0, top_y0 + 4.5),
            arrowprops=dict(arrowstyle="->", color=C_SLATE, lw=1.3))
ax.text(82.0, top_y0 + 2.2, "Finish", fontsize=6.4, fontweight="bold", color=C_SLATE, ha="center")


# ==============================================================================
# BOTTOM ROW: Triggers, Error, and Abort Cycle [y: 1.5 to 16.5]
# ==============================================================================
btm_y0, btm_h = 1.5, 15.0

b_trig = patches.FancyBboxPatch((1.0, btm_y0), 27.5, btm_h, boxstyle="round,pad=0.2,rounding_size=0.6",
                                facecolor="#F8FAFC", edgecolor=C_SLATE, linewidth=1.1, linestyle="--", zorder=2)
ax.add_patch(b_trig)
ax.text(14.75, btm_y0 + btm_h - 2.5, "CONCURRENT TRIGGER SOURCES", fontsize=7.4, fontweight="bold",
        color=C_SLATE, ha="center")
ax.plot([2.5, 27.0], [btm_y0 + btm_h - 4.2, btm_y0 + btm_h - 4.2], color="#CBD5E1", lw=0.6)
ax.text(2.5, btm_y0 + 7.5, "GPIO 0: 50 ms debounce, 600 ms cooldown", fontsize=6.5, color=C_TEXT_DARK)
ax.text(2.5, btm_y0 + 4.5, "REST API: POST /api/scenario/select (1-4)", fontsize=6.5, color=C_TEXT_DARK)
ax.text(2.5, btm_y0 + 1.8, "FreeRTOS Mailbox: portMUX_TYPE spinlock", fontsize=6.5, color=C_TEXT_DARK)

draw_state(ax, 34.0, btm_y0, 18.0, btm_h, "STATE_ERROR",
           ["Bus fault handler", "Stalled descriptors", "Recovery reset"], color=C_AMBER)

draw_state(ax, 63.5, btm_y0, 16.5, btm_h, "STATE_STOPPED",
           ["Atomic bus reset", "releaseAll() verified", "Ready for re-arm"], color=C_NAVY)

draw_state(ax, 84.0, btm_y0, 15.0, btm_h, "STATE_STOPPING",
           ["10 ms loop break", "Clear key latches", "Modifier queue flush"], color=C_RED)


# ==============================================================================
# ORTHOGONAL RECOVERY & TRANSITION ARROWS
# ==============================================================================
# 1. Straight DOWN: RUNNING -> STOPPING (Abort)
cx_run = (84.0 + 99.0) / 2.0
ax.annotate("", xy=(cx_run, btm_y0 + btm_h), xytext=(cx_run, top_y0),
            arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.5))
ax.text(cx_run + 0.8, (top_y0 + btm_y0 + btm_h)/2.0 + 1.5, "Abort", fontsize=6.6, fontweight="bold", color=C_RED)
ax.text(cx_run + 0.8, (top_y0 + btm_y0 + btm_h)/2.0 - 1.5, "Stop Flag", fontsize=6.4, color=C_RED)

# 2. Straight LEFT: STOPPING -> STOPPED (Release)
cy_btm = btm_y0 + btm_h / 2.0
ax.annotate("", xy=(80.0, cy_btm), xytext=(84.0, cy_btm),
            arrowprops=dict(arrowstyle="->", color=C_SLATE, lw=1.3))
ax.text(82.0, cy_btm + 2.2, "<= 10 ms", fontsize=6.2, color=C_TEXT_MUTED, ha="center")

# 3. Straight UP: STOPPED -> IDLE (Re-Arm)
cx_idle = (63.5 + 80.0) / 2.0
ax.annotate("", xy=(cx_idle, top_y0), xytext=(cx_idle, btm_y0 + btm_h),
            arrowprops=dict(arrowstyle="->", color=C_NAVY, lw=1.5))
ax.text(cx_idle + 0.8, (top_y0 + btm_y0 + btm_h)/2.0 + 1.5, "Re-Arm", fontsize=6.6, fontweight="bold", color=C_NAVY)
ax.text(cx_idle + 0.8, (top_y0 + btm_y0 + btm_h)/2.0 - 1.5, "Ready", fontsize=6.2, color=C_TEXT_MUTED)

# 4. Bus Fault into ERROR: USB_WAIT -> STATE_ERROR
ax.annotate("", xy=(40.0, btm_y0 + btm_h), xytext=(32.0, top_y0),
            arrowprops=dict(arrowstyle="->", color=C_AMBER, lw=1.2, linestyle=":"))
ax.text(32.0, 20.0, "Bus Fault", fontsize=6.2, color=C_AMBER)

# 5. Recovery Reset: STATE_ERROR -> IDLE
ax.annotate("", xy=(63.5, top_y0 + 2.5), xytext=(52.0, btm_y0 + btm_h - 2.0),
            arrowprops=dict(arrowstyle="->", color=C_AMBER, lw=1.3, connectionstyle="arc3,rad=-0.1"))
ax.text(56.0, 20.0, "Recovery Reset", fontsize=6.4, fontweight="bold", color=C_AMBER)

# 6. Trigger Event Dispatch: Triggers -> IDLE
ax.annotate("", xy=(63.5, btm_y0 + 4.0), xytext=(28.5, btm_y0 + 4.0),
            arrowprops=dict(arrowstyle="->", color=C_SLATE, lw=1.3))
ax.text(46.0, btm_y0 + 5.8, "Valid Event Dispatch", fontsize=6.6, fontweight="bold", color=C_SLATE, ha="center")

pdf_out = os.path.join(PAPER_DIR, "fsm_diagram.pdf")
png_out = os.path.join(PAPER_DIR, "fsm_diagram.png")

fig.savefig(pdf_out)
fig.savefig(png_out, dpi=300)
plt.close(fig)

print(f"Generated Vector Figure 2: {pdf_out} and {png_out}")
