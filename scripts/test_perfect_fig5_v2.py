import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams["font.family"] = "serif"
matplotlib.rcParams["mathtext.fontset"] = "dejavuserif"
matplotlib.rcParams["axes.linewidth"] = 0.9
import matplotlib.pyplot as plt
import fitz

BRAIN_DIR = r"C:\Users\Ram\.gemini\antigravity\brain\ce8071ad-ae44-4bc1-99a9-e4d2c343777c"

def make_perfect_fig5():
    # Width 3.35 in, Height 2.25 in
    fig, ax1 = plt.subplots(figsize=(3.35, 2.25), dpi=300)
    # Margins: left=0.15, right=0.85, top=0.88, bottom=0.18
    # This leaves plenty of room so y-labels never clip top or bottom!
    fig.subplots_adjust(left=0.15, right=0.85, top=0.88, bottom=0.18)

    rates = np.array([40.0, 50.0, 60.0, 66.7, 75.0, 85.0, 100.0])
    chars_allowed = np.array([8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0])
    wall_clock_ms = 8.0 * (1000.0 / rates)

    fine_rates = np.linspace(38.0, 102.0, 250)
    fine_ms = 8.0 * (1000.0 / fine_rates)

    C_NAVY = "#0F172A"       # Primary Keystroke Trigger (Navy)
    C_BLUE = "#1D4ED8"       # Reaction Time (Steel Blue)
    C_RED = "#DC2626"        # Execution Horizon (Red)
    C_GREEN = "#059669"      # Safety Buffer (Emerald)
    C_GRID = "#E2E8F0"

    # Set left axis range to 0..24
    # With ylim(0, 24):
    # - Trigger is at y=8 (33% height)
    # - Execution Horizon is at y=14 (58% height)
    # - The entire upper band y in [16, 24] (top 33% of the plot) is completely clear!
    # - Perfect place for the legend without touching ANY line!
    ax1.set_xlim(36.0, 104.0)
    ax1.set_ylim(0.0, 24.0)
    ax1.set_yticks([0, 4, 8, 12, 16, 20, 24])
    ax1.set_xticks([40, 60, 80, 100])

    # Right axis: range 0..300 ms
    # 24 chars at left corresponds to 300 ms at right: exactly 6 ticks each!
    # Left ticks: 0, 4, 8, 12, 16, 20, 24 (step 4)
    # Right ticks: 0, 50, 100, 150, 200, 250, 300 (step 50)
    # Every grid line aligns 100% horizontally!
    ax2 = ax1.twinx()
    ax2.set_xlim(36.0, 104.0)
    ax2.set_ylim(0.0, 300.0)
    ax2.set_yticks([0, 50, 100, 150, 200, 250, 300])

    # 1. Shaded Safety Buffer Band (soft emerald tint)
    ax1.fill_between([36.0, 104.0], 8.0, 14.0, color="#ECFDF5", alpha=0.95, zorder=1)

    # Text inside safety buffer band on the left (x=50, y=11)
    # At x=50, reaction time is 160 ms (y1 = 12.8 in scale 0..24).
    # Wait, at x=94, reaction time is 85 ms (y1 = 6.8, below the band!).
    # So at x=94, the band between 8 and 14 is 100% EMPTY!
    ax1.text(94.0, 11.0, r"Safety Margin ($\Delta = 6$)",
             fontsize=6.8, fontweight="bold", color="#065f46",
             ha="center", va="center", zorder=5,
             bbox=dict(boxstyle="round,pad=0.22", facecolor="#ffffff", edgecolor="#10b981", lw=0.6, alpha=0.98))

    # 2. Execution Horizon & Trigger Lines on Left Axis
    line_exec = ax1.axhline(14.0, color=C_RED, linestyle="--", linewidth=1.4, zorder=2,
                            label=r"Execution Horizon ($L_{\mathrm{exec}} = 14$)")
    line_lat, = ax1.plot([36.0, 104.0], [8.0, 8.0], color=C_NAVY, linewidth=1.8, zorder=3,
                         label=r"Quarantine Trigger ($\kappa = 8$)")
    ax1.plot(rates, chars_allowed, marker="o", markersize=4.2, color=C_NAVY, linestyle="None", zorder=4)

    # 3. Right Axis Line: Wall-Clock Reaction Time (ms)
    line_time, = ax2.plot(fine_rates, fine_ms, color=C_BLUE, linewidth=1.8, linestyle="-.", zorder=3,
                          label=r"Reaction Time ($t_{\mathrm{quar}}$)")
    ax2.plot(rates, wall_clock_ms, marker="s", markersize=4.2, color=C_BLUE, linestyle="None", zorder=4)

    # 4. Clean compact callouts for endpoints
    # At (40, 200): marker is at (40, 200). Put text at (42.0, 215)
    ax2.annotate(r"$\mathbf{200\,\mathrm{ms}}$", xy=(40.0, 200.0), xytext=(43.0, 222.0),
                 fontsize=6.5, fontweight="bold", color=C_BLUE, zorder=6,
                 arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=0.8, shrinkA=0, shrinkB=2),
                 bbox=dict(boxstyle="round,pad=0.18", facecolor="#ffffff", edgecolor="#93c5fd", lw=0.5, alpha=0.95))

    # At (100, 80.1): marker is at (100, 80.1). Put text at (96.0, 48.0)
    ax2.annotate(r"$\mathbf{80.1\,\mathrm{ms}}$", xy=(100.0, 80.1), xytext=(94.0, 42.0),
                 fontsize=6.5, fontweight="bold", color=C_BLUE, zorder=6,
                 arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=0.8, shrinkA=0, shrinkB=2),
                 bbox=dict(boxstyle="round,pad=0.18", facecolor="#ffffff", edgecolor="#93c5fd", lw=0.5, alpha=0.95))

    # Labels and Grid
    ax1.set_xlabel(r"Burst Injection Rate (chars/s)", fontsize=8.2, fontweight="bold", labelpad=3)
    ax1.set_ylabel("Quarantine Latency (Chars)", fontsize=8.2, fontweight="bold", color=C_NAVY, labelpad=2)
    ax2.set_ylabel(r"Reaction Time $t_{\mathrm{quar}}$ (ms)", fontsize=8.2, fontweight="bold", color=C_BLUE, labelpad=2)

    ax1.tick_params(axis="y", labelcolor=C_NAVY, labelsize=7.5, pad=2)
    ax1.tick_params(axis="x", labelsize=7.5, pad=2)
    ax2.tick_params(axis="y", labelcolor=C_BLUE, labelsize=7.5, pad=2)
    ax1.grid(True, linestyle="--", alpha=0.45, color=C_GRID)

    # 5. Legend in Upper Right (y1 in [16..24], completely above L_exec=14 and all data!)
    lines = [line_exec, line_lat, line_time]
    labels = [l.get_label() for l in lines]
    leg = ax1.legend(lines, labels, loc="upper right", fontsize=6.0, framealpha=0.98, edgecolor="#CBD5E1",
                     borderpad=0.28, labelspacing=0.45, handlelength=1.4)
    leg.get_frame().set_linewidth(0.5)

    out_pdf = os.path.join(BRAIN_DIR, "fig5_perfect_test.pdf")
    out_png = os.path.join(BRAIN_DIR, "fig5_perfect_test.png")
    fig.savefig(out_pdf, format="pdf")
    fig.savefig(out_png, format="png", dpi=300)
    plt.close(fig)
    print("Fig 5 generated to brain dir.")

make_perfect_fig5()
