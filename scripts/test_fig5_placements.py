import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams["font.family"] = "serif"
matplotlib.rcParams["mathtext.fontset"] = "dejavuserif"
matplotlib.rcParams["axes.linewidth"] = 1.0

BRAIN_DIR = r"C:\Users\Ram\.gemini\antigravity\brain\ce8071ad-ae44-4bc1-99a9-e4d2c343777c"

def gen(arrow_x, text_pos, name):
    fig, ax1 = plt.subplots(figsize=(3.4, 2.3), dpi=300)
    fig.subplots_adjust(left=0.15, right=0.85, top=0.92, bottom=0.20)

    rates = np.array([40.0, 50.0, 60.0, 66.7, 75.0, 85.0, 100.0])
    chars_allowed = np.array([8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0])
    fine_rates = np.linspace(40.0, 106.0, 200)
    fine_ms = 8.0 * (1000.0 / fine_rates)

    C_NAVY = "#0F172A"
    C_BLUE = "#1D4ED8"
    C_RED = "#B91C1C"
    C_GRID = "#E2E8F0"
    C_BUFFER = "#F1F5F9"

    ax1.fill_between([40.0, 106.0], 8.0, 14.0, color=C_BUFFER, alpha=1.0, zorder=1)
    line_exec = ax1.axhline(14.0, color=C_RED, linestyle="--", linewidth=1.4, zorder=2,
                            label=r"Horizon ($L_{\mathrm{exec}} = 14$)")
    line_lat, = ax1.plot([40.0, 106.0], [8.0, 8.0], color=C_NAVY, linewidth=2.0, zorder=3,
                         label=r"Trigger ($\kappa = 8$)")
    ax1.plot(rates, chars_allowed, marker="o", markersize=4.8, color=C_NAVY, linestyle="None", zorder=4)

    ax1.set_xlabel(r"Burst Rate $R_{\mathrm{burst}}$ (chars/s)", fontsize=8.8, fontweight="bold", labelpad=3)
    ax1.set_ylabel("Quarantine Latency (Chars)", fontsize=8.8, fontweight="bold", color=C_NAVY, labelpad=3)
    ax1.set_xlim(38.0, 106.0)
    ax1.set_ylim(0.0, 22.0)
    ax1.set_yticks([0, 4, 8, 12, 16, 20])
    ax1.set_xticks([40, 60, 80, 100])
    ax1.tick_params(axis="y", labelcolor=C_NAVY, labelsize=8.2, pad=3)
    ax1.tick_params(axis="x", labelsize=8.2, pad=3)
    ax1.grid(True, linestyle="--", alpha=0.5, color=C_GRID)

    ax2 = ax1.twinx()
    ax2.set_xlim(38.0, 106.0)
    line_time, = ax2.plot(fine_rates, fine_ms, color=C_BLUE, linewidth=1.8, linestyle="-.", zorder=3,
                          label=r"Reaction Time ($t_{\mathrm{quar}}$)")
    ax2.plot(rates, 8.0 * (1000.0 / rates), marker="s", markersize=4.2, color=C_BLUE, linestyle="None", zorder=4)

    ax2.set_ylabel("Reaction Time (ms)", fontsize=8.8, fontweight="bold", color=C_BLUE, labelpad=4)
    ax2.set_ylim(0.0, 275.0)
    ax2.set_yticks([0, 50, 100, 150, 200, 250])
    ax2.tick_params(axis="y", labelcolor=C_BLUE, labelsize=8.2, pad=3)

    ax2.plot([40.0, 40.0], [0.0, 200.0], color="#059669", linestyle=":", linewidth=1.3, zorder=5)
    ax2.plot([40.0, 106.0], [200.0, 200.0], color="#059669", linestyle=":", linewidth=1.3, zorder=5)
    ax2.plot(40.0, 200.0, marker="o", markersize=5.5, color="#059669", zorder=6)

    ax2.annotate("Detection Floor\n" + r"$t_{\mathrm{quar}} = 200\,\mathrm{ms}$" + "\n(40 ch/s, 25 ms)",
                 xy=(40.0, 200.0), xycoords="data",
                 xytext=(41.0, 236.0), textcoords="data",
                 fontsize=5.2, fontweight="bold", color="#059669",
                 ha="left", va="center", zorder=8, linespacing=1.25,
                 bbox=dict(boxstyle="round,pad=0.20", facecolor="white", edgecolor="#10b981", lw=0.8, alpha=0.96),
                 arrowprops=dict(arrowstyle="->", color="#059669", lw=0.9, shrinkA=1, shrinkB=3))

    ax2.annotate("Min. Latency Floor = 80.1 ms\n" + r"($R = 100$ ch/s, $\kappa = 8$)",
                 xy=(100.0, 80.08), xycoords="data",
                 xytext=(82.0, 36.0), textcoords="data",
                 fontsize=5.6, fontweight="bold", color=C_BLUE,
                 ha="center", va="center", zorder=7, linespacing=1.35,
                 bbox=dict(boxstyle="round,pad=0.22", facecolor="white", edgecolor="#93C5FD", lw=0.8, alpha=0.96),
                 arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1.0, shrinkA=2, shrinkB=4))

    lines = [line_lat, line_exec, line_time]
    labels = [l.get_label() for l in lines]
    legend = ax1.legend(lines, labels, loc="upper right", frameon=True, fancybox=True,
                        edgecolor="#CBD5E1", framealpha=0.96, fontsize=6.2,
                        handlelength=1.0, labelspacing=0.20, borderpad=0.25)
    legend.get_frame().set_linewidth(0.8)
    legend.set_zorder(10)

    if arrow_x is not None:
        ax1.annotate("", xy=(arrow_x, 13.7), xytext=(arrow_x, 8.3),
                     arrowprops=dict(arrowstyle="<->", color="#334155", lw=1.0), zorder=5)
    
    tx, ty, ha, va = text_pos
    ax1.text(tx, ty, r"$\Delta = 6$ Margin",
             fontsize=6.8, fontweight="bold", color="#1E293B",
             ha=ha, va=va, zorder=7,
             bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor="#CBD5E1", lw=0.6, alpha=0.98))

    out_p = os.path.join(BRAIN_DIR, f"{name}.png")
    fig.savefig(out_p, dpi=300)
    plt.close(fig)
    print(f"Saved {out_p}")

gen(92.0, (92.0, 11.0, "center", "center"), "test_fig5_x92")
gen(48.0, (48.0, 11.0, "center", "center"), "test_fig5_x48")
gen(60.0, (60.0, 15.5, "center", "bottom"), "test_fig5_above_horizon")
