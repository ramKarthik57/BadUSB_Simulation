"""
IEEE-Grade Vector Defense Pipeline Generator (Figure 3).
Produces publication-quality vector PDF and 300 DPI PNG.
Strictly follows IEEE Transactions / S&P formatting.
Accurately maps to Caption & Section IV:
  (1) Hardware event injection across physical bus (Rogue ESP32 vs Physical KB)
  (2) Global Win32 low-level hook interception before foreground delivery
  (3) Dynamic per-device suppression gate isolating rogue peripherals
  (4) 15-second watchdog fail-safe timer preventing operator lockout
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

fig, ax = plt.subplots(figsize=(7.16, 1.80), dpi=300)
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
C_CONTAINER = "#F8FAFC"
C_CARD = "#FFFFFF"

card_y0, card_h = 1.0, 40.0

def make_stage(ax, x0, w, num, title, col=C_SLATE):
    b = patches.FancyBboxPatch((x0, card_y0), w, card_h, boxstyle="round,pad=0.2,rounding_size=0.8",
                               facecolor=C_CONTAINER, edgecolor=col, linewidth=1.2, zorder=1)
    ax.add_patch(b)
    hdr = patches.FancyBboxPatch((x0, card_y0 + card_h - 7.0), w, 7.0, boxstyle="round,pad=0.2,rounding_size=0.8",
                                 facecolor=col, edgecolor=col, linewidth=0.8, zorder=2)
    ax.add_patch(hdr)
    ax.text(x0 + w/2.0, card_y0 + card_h - 2.5, num, fontsize=6.8, fontweight="bold",
            color="#E2E8F0", ha="center", va="center", zorder=3)
    ax.text(x0 + w/2.0, card_y0 + card_h - 5.0, title, fontsize=7.2, fontweight="bold",
            color="#FFFFFF", ha="center", va="center", zorder=3)

# ==============================================================================
# STAGE 1: HARDWARE BUS INGESTION [x: 1.0 to 22.0]
# ==============================================================================
make_stage(ax, 1.0, 21.0, "STAGE 1", "HARDWARE BUS INGESTION", C_NAVY)

c_rogue = patches.FancyBboxPatch((2.2, 19.5), 18.6, 12.0, boxstyle="round,pad=0.15,rounding_size=0.4",
                                facecolor="#FEF2F2", edgecolor="#FCA5A5", lw=0.8, zorder=3)
ax.add_patch(c_rogue)
ax.text(11.5, 28.5, "Rogue ESP32-S3", fontsize=7.4, fontweight="bold", color=C_RED, ha="center")
ax.text(3.2, 25.0, "Automated burst injection", fontsize=6.8, color=C_TEXT_DARK)
ax.text(3.2, 22.0, "High machine velocity (R <= 100 ch/s)", fontsize=6.8, color=C_TEXT_DARK)

c_phys = patches.FancyBboxPatch((2.2, 3.0), 18.6, 13.0, boxstyle="round,pad=0.15,rounding_size=0.4",
                               facecolor="#F0FDF4", edgecolor="#86EFAC", lw=0.8, zorder=3)
ax.add_patch(c_phys)
ax.text(11.5, 13.0, "Physical Laptop KB", fontsize=7.4, fontweight="bold", color=C_GREEN, ha="center")
ax.text(3.2, 9.5, "Human typing cadence", fontsize=6.8, color=C_TEXT_DARK)
ax.text(3.2, 6.5, "High natural variance (mu ~ 144 ms)", fontsize=6.8, color=C_TEXT_DARK)


# ==============================================================================
# STAGE 2: PARALLEL HOOK & RAW INPUT [x: 26.5 to 48.0]
# ==============================================================================
make_stage(ax, 26.5, 21.5, "STAGE 2", "PARALLEL HOOK & RAW INPUT", C_SLATE)

c_raw = patches.FancyBboxPatch((27.7, 19.5), 19.1, 12.0, boxstyle="round,pad=0.15,rounding_size=0.4",
                              facecolor=C_CARD, edgecolor="#CBD5E1", lw=0.8, zorder=3)
ax.add_patch(c_raw)
ax.text(37.25, 28.5, "Win32 Raw Input API", fontsize=7.4, fontweight="bold", color=C_SLATE, ha="center")
ax.text(28.7, 25.0, "WM_INPUT background telemetry", fontsize=6.8, color=C_TEXT_DARK)
ax.text(28.7, 22.0, "Binds hDevice handle to USB VID/PID", fontsize=6.8, color=C_TEXT_DARK)

c_llhook = patches.FancyBboxPatch((27.7, 3.0), 19.1, 13.0, boxstyle="round,pad=0.15,rounding_size=0.4",
                                 facecolor=C_CARD, edgecolor="#CBD5E1", lw=0.8, zorder=3)
ax.add_patch(c_llhook)
ax.text(37.25, 13.0, "Low-Level Intercept", fontsize=7.4, fontweight="bold", color=C_SLATE, ha="center")
ax.text(28.7, 9.5, "WH_KEYBOARD_LL global hook", fontsize=6.8, color=C_TEXT_DARK)
ax.text(28.7, 6.5, "Traps event before foreground app", fontsize=6.8, color=C_TEXT_DARK)


# ==============================================================================
# STAGE 3: BEHAVIORAL DYNAMICS [x: 52.5 to 74.0]
# ==============================================================================
make_stage(ax, 52.5, 21.5, "STAGE 3", "BEHAVIORAL DYNAMICS", C_SLATE)

c_stats = patches.FancyBboxPatch((53.7, 19.5), 19.1, 12.0, boxstyle="round,pad=0.15,rounding_size=0.4",
                                facecolor=C_CARD, edgecolor="#CBD5E1", lw=0.8, zorder=3)
ax.add_patch(c_stats)
ax.text(63.25, 28.5, "Sliding Window Queue", fontsize=7.4, fontweight="bold", color=C_SLATE, ha="center")
ax.text(54.7, 25.0, "Online FIFO: W = 10 events per device", fontsize=6.8, color=C_TEXT_DARK)
ax.text(54.7, 22.0, "Computes dispersion CV = sigma / mu", fontsize=6.8, color=C_TEXT_DARK)

c_rule = patches.FancyBboxPatch((53.7, 3.0), 19.1, 13.0, boxstyle="round,pad=0.15,rounding_size=0.4",
                                facecolor=C_CARD, edgecolor="#CBD5E1", lw=0.8, zorder=3)
ax.add_patch(c_rule)
ax.text(63.25, 13.0, "Anomaly Evaluation", fontsize=7.4, fontweight="bold", color=C_SLATE, ha="center")
ax.text(54.7, 9.5, "CV < 0.15 or mu < 25 ms", fontsize=6.8, color=C_RED, fontweight="bold")
ax.text(54.7, 6.5, "Sustained across kappa = 8 keystrokes", fontsize=6.8, color=C_TEXT_DARK)


# ==============================================================================
# STAGE 4: SELECTIVE QUARANTINE & WATCHDOG [x: 78.5 to 99.0]
# ==============================================================================
make_stage(ax, 78.5, 20.5, "STAGE 4", "QUARANTINE & WATCHDOG", C_NAVY)

c_gate = patches.FancyBboxPatch((79.5, 17.5), 18.5, 14.5, boxstyle="round,pad=0.15,rounding_size=0.4",
                               facecolor=C_CARD, edgecolor="#CBD5E1", lw=0.8, zorder=3)
ax.add_patch(c_gate)
ax.text(88.75, 29.0, "Selective Gate Action", fontsize=7.4, fontweight="bold", color=C_NAVY, ha="center")
ax.text(88.75, 24.5, "[DROP] Rogue USB", fontsize=7.0, fontweight="bold", color=C_RED, ha="center",
        bbox=dict(boxstyle="square,pad=0.15", facecolor="#FEF2F2", edgecolor="#FCA5A5", lw=0.6))
ax.text(88.75, 19.5, "[PASS] Physical KB", fontsize=7.0, fontweight="bold", color=C_GREEN, ha="center",
        bbox=dict(boxstyle="square,pad=0.15", facecolor="#F0FDF4", edgecolor="#86EFAC", lw=0.6))

c_wd = patches.FancyBboxPatch((79.5, 3.0), 18.5, 12.0, boxstyle="round,pad=0.15,rounding_size=0.4",
                             facecolor=C_CARD, edgecolor=C_NAVY, lw=0.8, linestyle="--", zorder=3)
ax.add_patch(c_wd)
ax.text(88.75, 12.0, "15-Second Watchdog", fontsize=7.4, fontweight="bold", color=C_NAVY, ha="center")
ax.text(80.5, 8.5, "Auto-recovery timeout", fontsize=6.8, color=C_TEXT_DARK)
ax.text(80.5, 5.5, "Prevents operator lockout trap", fontsize=6.8, color=C_TEXT_DARK)


# ==============================================================================
# PARALLEL PIPELINE ROUTING ARROWS (PROPER CLEARANCES)
# ==============================================================================
# 1 -> 2
ax.annotate("", xy=(26.5, 25.5), xytext=(22.0, 25.5),
            arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.4))
ax.annotate("", xy=(26.5, 9.5), xytext=(22.0, 9.5),
            arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=1.4))

# 2 -> 3
ax.annotate("", xy=(52.5, 25.5), xytext=(48.0, 25.5),
            arrowprops=dict(arrowstyle="->", color=C_SLATE, lw=1.4))
ax.annotate("", xy=(52.5, 9.5), xytext=(48.0, 9.5),
            arrowprops=dict(arrowstyle="->", color=C_SLATE, lw=1.4))

# 3 -> 4
ax.annotate("", xy=(78.5, 25.5), xytext=(74.0, 25.5),
            arrowprops=dict(arrowstyle="->", color=C_SLATE, lw=1.4))
ax.annotate("", xy=(78.5, 9.5), xytext=(74.0, 9.5),
            arrowprops=dict(arrowstyle="->", color=C_NAVY, lw=1.4))

pdf_out = os.path.join(PAPER_DIR, "defense_architecture.pdf")
png_out = os.path.join(PAPER_DIR, "defense_architecture.png")

fig.savefig(pdf_out)
fig.savefig(png_out, dpi=300)
plt.close(fig)

print(f"Generated Vector Figure 3: {pdf_out} and {png_out}")
