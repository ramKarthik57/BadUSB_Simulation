import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams["font.family"] = "serif"
matplotlib.rcParams["mathtext.fontset"] = "dejavuserif"
matplotlib.rcParams["axes.linewidth"] = 1.0
import matplotlib.pyplot as plt
import fitz

BRAIN_DIR = r"C:\Users\Ram\.gemini\antigravity\brain\ce8071ad-ae44-4bc1-99a9-e4d2c343777c"

def test_fig5_candidate(variant_name, band_color, pill_pos, annot_style):
    fig, ax1 = plt.subplots(figsize=(3.45, 2.30), dpi=300)
    fig.subplots_adjust(left=0.17, right=0.83, top=0.92, bottom=0.22)

    rates = np.array([40.0, 50.0, 60.0, 66.7, 75.0, 85.0, 100.0])
    chars_allowed = np.array([8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0])
    wall_clock_ms = 8.0 * (1000.0 / rates)

    fine_rates = np.linspace(38.0, 104.0, 200)
    fine_ms = 8.0 * (1000.0 / fine_rates)

    C_NAVY = "#0F172A"
    C_BLUE = "#1D4ED8"
    C_RED = "#DC2626"
    C_GREEN = "#059669"
    C_GRID = "#E2E8F0"

    # Shaded band
    ax1.fill_between([38.0, 104.0], 8.0, 14.0, color=band_color, alpha=0.55, zorder=1)

    # Lines on ax1
    line_exec = ax1.axhline(14.0, color=C_RED, linestyle="--", linewidth=1.4, zorder=2,
                            label=r"Horizon ($L_{\mathrm{exec}} = 14$)")
    line_lat, = ax1.plot([38.0, 104.0], [8.0, 8.0], color=C_NAVY, linewidth=2.0, zorder=3,
                         label=r"Trigger ($\kappa = 8$)")
    ax1.plot(rates, chars_allowed, marker="o", markersize=4.8, color=C_NAVY, linestyle="None", zorder=4)

    # Safety margin label
    px, py = pill_pos
    ax1.text(px, py, r"Safety Buffer ($\Delta = 6$ chars)",
             fontsize=6.8, fontweight="bold", color="#065f46",
             ha="center", va="center", zorder=5,
             bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#10b981", lw=0.6, alpha=1.0))

    ax1.set_xlabel(r"Burst Injection Rate $R_{\mathrm{burst}}$ (chars/s)", fontsize=8.2, fontweight="bold", labelpad=5)
    ax1.set_ylabel("Quarantine Latency (Chars)", fontsize=8.2, fontweight="bold", color=C_NAVY, labelpad=4)
    ax1.set_xlim(38.0, 104.0)
    ax1.set_ylim(0.0, 22.0)
    ax1.set_yticks([0, 4, 8, 12, 16, 20])
    ax1.set_xticks([40, 60, 80, 100])
    ax1.tick_params(axis="y", labelcolor=C_NAVY, labelsize=7.8, pad=2)
    ax1.tick_params(axis="x", labelsize=7.8, pad=2)
    ax1.grid(True, linestyle="--", alpha=0.5, color=C_GRID)

    # Right axis
    ax2 = ax1.twinx()
    ax2.set_xlim(38.0, 104.0)
    line_time, = ax2.plot(fine_rates, fine_ms, color=C_BLUE, linewidth=1.8, linestyle="-.", zorder=3,
                          label=r"Reaction Time ($t_{\mathrm{quar}}$)")
    ax2.plot(rates, wall_clock_ms, marker="s", markersize=4.5, color=C_BLUE, linestyle="None", zorder=4)
    ax2.set_ylabel("Reaction Time (ms)", fontsize=8.2, fontweight="bold", color=C_BLUE, labelpad=4)
    ax2.set_ylim(0.0, 250.0)
    ax2.set_yticks([0, 50, 100, 150, 200, 250])
    ax2.tick_params(axis="y", labelcolor=C_BLUE, labelsize=7.8, pad=2)

    if annot_style == "clean_badge":
        # Direct clean badges without long diagonal arrows
        ax2.text(40.0, 214.0, "200 ms", fontsize=6.4, fontweight="bold", color="#047857",
                 ha="center", va="center", zorder=6,
                 bbox=dict(boxstyle="round,pad=0.22", facecolor="white", edgecolor="#10b981", lw=0.6))
        ax2.text(100.0, 95.0, "80.1 ms", fontsize=6.4, fontweight="bold", color="#047857",
                 ha="center", va="center", zorder=6,
                 bbox=dict(boxstyle="round,pad=0.22", facecolor="white", edgecolor="#10b981", lw=0.6))

    lines = [line_exec, line_lat, line_time]
    labels = [l.get_label() for l in lines]
    leg = ax2.legend(lines, labels, loc="upper right", fontsize=6.2, framealpha=0.96, edgecolor="#CBD5E1",
                     borderpad=0.35, labelspacing=0.65, handlelength=1.5)
    leg.get_frame().set_linewidth(0.6)

    out_pdf = os.path.join(BRAIN_DIR, f"{variant_name}.pdf")
    out_png = os.path.join(BRAIN_DIR, f"{variant_name}.png")
    fig.savefig(out_pdf, format="pdf")
    fig.savefig(out_png, format="png", dpi=300)
    plt.close(fig)

    # Check collision
    doc = fitz.open(out_pdf)
    words = doc[0].get_text("words")
    rects = [fitz.Rect(w[:4]) for w in words]
    coll = 0
    for a in range(len(rects)):
        for b in range(a + 1, len(rects)):
            r_int = rects[a] & rects[b]
            if not r_int.is_empty and r_int.width > 0.5 and r_int.height > 0.5:
                coll += 1
    print(f"{variant_name}: {len(words)} words, {coll} collisions")

test_fig5_candidate("test_fig5_v5", "#d1fae5", (54.0, 11.0), "clean_badge")
test_fig5_candidate("test_fig5_v6", "#e0e7ff", (55.0, 11.0), "clean_badge")
test_fig5_candidate("test_fig5_v7", "#f1f5f9", (54.0, 11.0), "clean_badge")
