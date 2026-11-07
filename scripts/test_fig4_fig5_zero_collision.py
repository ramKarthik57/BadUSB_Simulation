import os
import fitz
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32"
PAPER_DIR = os.path.join(BASE_DIR, "paper")

def build_fig5(bottom=0.24, labelpad=6, lspace=0.70, callout_linespace=1.6):
    fig, ax1 = plt.subplots(figsize=(3.45, 2.38), dpi=300)
    fig.subplots_adjust(left=0.18, right=0.82, top=0.90, bottom=bottom)

    rates = np.array([40.0, 50.0, 60.0, 66.7, 75.0, 85.0, 100.0])
    chars_allowed = np.array([8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0])
    wall_clock_ms = 8.0 * (1000.0 / rates)

    fine_rates = np.linspace(40.0, 106.0, 200)
    fine_ms = 8.0 * (1000.0 / fine_rates)

    C_NAVY = "#0F172A"
    C_BLUE = "#1D4ED8"
    C_RED = "#B91C1C"
    C_GRID = "#E2E8F0"
    C_BUFFER = "#F1F5F9"

    # 1. Safety Buffer
    ax1.fill_between([40.0, 106.0], 8.0, 14.0, color=C_BUFFER, alpha=1.0, zorder=1)

    # 2. Execution Horizon
    line_exec = ax1.axhline(14.0, color=C_RED, linestyle="--", linewidth=1.5, zorder=2,
                            label=r"Horizon ($L_{\mathrm{exec}} = 14$)")

    # 3. Trigger Line
    line_lat, = ax1.plot([40.0, 106.0], [8.0, 8.0], color=C_NAVY, linewidth=2.2, zorder=3,
                         label=r"Trigger ($\kappa = 8$)")
    ax1.plot(rates, chars_allowed, marker="o", markersize=5.0, color=C_NAVY,
             linestyle="None", zorder=4)

    # Left Y-Axis
    ax1.set_xlabel(r"Burst Rate $R_{\mathrm{burst}}$ (chars/s)",
                   fontsize=8.5, fontweight="bold", labelpad=labelpad)
    ax1.set_ylabel("Quarantine Latency (Chars)",
                   fontsize=8.5, fontweight="bold", color=C_NAVY, labelpad=4)
    ax1.set_xlim(38.0, 106.0)
    ax1.set_ylim(0.0, 22.0)
    ax1.set_yticks([0, 4, 8, 12, 16, 20])
    ax1.set_xticks([40, 60, 80, 100])
    ax1.tick_params(axis="y", labelcolor=C_NAVY, labelsize=7.8, pad=2)
    ax1.tick_params(axis="x", labelsize=7.8, pad=2)
    ax1.grid(True, linestyle="--", alpha=0.5, color=C_GRID)

    # Right Y-Axis
    ax2 = ax1.twinx()
    ax2.set_xlim(38.0, 106.0)
    line_time, = ax2.plot(fine_rates, fine_ms, color=C_BLUE, linewidth=2.0, linestyle="-.", zorder=3,
                          label=r"Reaction Time ($t_{\mathrm{quar}}$)")
    ax2.plot(rates, wall_clock_ms, marker="s", markersize=4.8, color=C_BLUE,
             linestyle="None", zorder=4)

    ax2.set_ylabel("Reaction Time (ms)",
                   fontsize=8.5, fontweight="bold", color=C_BLUE, labelpad=4)
    ax2.set_ylim(0.0, 275.0)
    ax2.set_yticks([0, 50, 100, 150, 200, 250])
    ax2.tick_params(axis="y", labelcolor=C_BLUE, labelsize=7.8, pad=2)

    # Guidelines
    ax2.plot([40.0, 40.0], [0.0, 200.0], color="#059669", linestyle=":", linewidth=1.4, zorder=5)
    ax2.plot([40.0, 106.0], [200.0, 200.0], color="#059669", linestyle=":", linewidth=1.4, zorder=5)
    ax2.plot(40.0, 200.0, marker="o", markersize=6.0, color="#059669", zorder=6)

    # Detection floor: compact, distinct from legend
    ax2.annotate("Detection Floor\n" + r"$t_{\mathrm{quar}} = 200\,\mathrm{ms}$" + "\n(40 ch/s, 25 ms)",
                 xy=(40.0, 200.0), xycoords="data",
                 xytext=(41.0, 226.0), textcoords="data",
                 fontsize=5.0, fontweight="bold", color="#059669",
                 ha="left", va="center", zorder=8, linespacing=2.4,
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#10b981", lw=0.8, alpha=1.0),
                 arrowprops=dict(arrowstyle="->", color="#059669", lw=1.0, shrinkA=1, shrinkB=3))

    # Delta = 6 Margin
    ax1.annotate("", xy=(90.0, 13.8), xytext=(90.0, 12.5),
                 arrowprops=dict(arrowstyle="->", color="#334155", lw=1.1), zorder=5)
    ax1.annotate("", xy=(90.0, 8.2), xytext=(90.0, 9.5),
                 arrowprops=dict(arrowstyle="->", color="#334155", lw=1.1), zorder=5)
    ax1.text(90.0, 11.0, r"$\Delta = 6$ Margin",
             fontsize=7.0, fontweight="bold", color="#1E293B",
             ha="center", va="center", zorder=7,
             bbox=dict(boxstyle="round,pad=0.40", facecolor="white", edgecolor="#CBD5E1", lw=0.6, alpha=1.0))

    # Min latency floor
    ax2.annotate("Min. Latency Floor = 80.1 ms\n" + r"($R = 100$ ch/s, $\kappa = 8$)",
                 xy=(100.0, 80.08), xycoords="data",
                 xytext=(75.0, 36.0), textcoords="data",
                 fontsize=5.5, fontweight="bold", color=C_BLUE,
                 ha="center", va="center", zorder=7, linespacing=callout_linespace,
                 bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="#93C5FD", lw=0.8, alpha=1.0),
                 arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1.0, shrinkA=2, shrinkB=4))

    # Legend
    lines = [line_lat, line_exec, line_time]
    labels = [l.get_label() for l in lines]
    legend = ax1.legend(lines, labels, loc="upper right", frameon=True, fancybox=True,
                        facecolor="white", edgecolor="#CBD5E1", framealpha=1.0, fontsize=6.0,
                        handlelength=1.0, labelspacing=lspace, borderpad=0.45)
    legend.get_frame().set_linewidth(0.8)
    legend.set_zorder(12)

    pdf_p = os.path.join(PAPER_DIR, "fig_detection_latency.pdf")
    fig.savefig(pdf_p)
    plt.close(fig)

    # Check collisions
    doc = fitz.open(pdf_p)
    page = doc[0]
    words = page.get_text("words")
    text_boxes = [fitz.Rect(w[:4]) for w in words]
    collisions = []
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            inter = text_boxes[i] & text_boxes[j]
            if not inter.is_empty and inter.width > 0.5 and inter.height > 0.5:
                collisions.append((words[i][4], words[j][4], inter))
    return len(collisions), collisions

for b in [0.25, 0.26]:
    for lp in [6, 7]:
        for ls in [0.70, 0.80]:
            for cls in [1.8, 2.0, 2.2]:
                n, cols = build_fig5(bottom=b, labelpad=lp, lspace=ls, callout_linespace=cls)
                if n == 0:
                    print(f"Fig 5 zero collisions found! bottom={b}, labelpad={lp}, lspace={ls}, callout_linespace={cls}")
                    break
            if n == 0:
                break
        if n == 0:
            break
    if n == 0:
        break
if n > 0:
    print(f"Fig 5 remaining collisions ({n}):")
    for c in cols[:5]:
        print(" ", c)
