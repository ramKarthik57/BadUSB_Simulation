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

def build_spotless_fig5():
    fig, ax1 = plt.subplots(figsize=(3.45, 2.30), dpi=300)
    fig.subplots_adjust(left=0.17, right=0.83, top=0.92, bottom=0.22)

    rates = np.array([40.0, 50.0, 60.0, 66.7, 75.0, 85.0, 100.0])
    chars_allowed = np.array([8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0])
    wall_clock_ms = 8.0 * (1000.0 / rates)

    fine_rates = np.linspace(35.0, 105.0, 250)
    fine_ms = 8.0 * (1000.0 / fine_rates)

    C_NAVY = "#0F172A"       # Primary Keystroke Trigger (Navy)
    C_BLUE = "#1D4ED8"       # Reaction Time (Steel Blue)
    C_RED = "#DC2626"        # Execution Horizon (Red)
    C_GREEN = "#059669"      # Safety Buffer (Emerald)
    C_GRID = "#E2E8F0"

    # 1. Shaded Safety Buffer Band (soft emerald tint, indicating safe pre-execution window)
    ax1.fill_between([35.0, 105.0], 8.0, 14.0, color="#ECFDF5", alpha=0.95, zorder=1)

    # 2. Execution Horizon & Trigger Lines on Left Axis (Keystrokes: 0 to 20)
    line_exec = ax1.axhline(14.0, color=C_RED, linestyle="--", linewidth=1.5, zorder=2,
                            label=r"Horizon ($L_{\mathrm{exec}} = 14$)")
    line_lat, = ax1.plot([35.0, 105.0], [8.0, 8.0], color=C_NAVY, linewidth=2.0, zorder=3,
                         label=r"Trigger ($\kappa = 8$)")
    ax1.plot(rates, chars_allowed, marker="o", markersize=4.8, color=C_NAVY, linestyle="None", zorder=4)

    # 3. Clean Safety Buffer Dimensioning at x = 94.0
    ax1.annotate("", xy=(95.0, 8.0), xytext=(95.0, 14.0),
                 arrowprops=dict(arrowstyle="<->", color=C_GREEN, lw=1.2, shrinkA=1, shrinkB=1), zorder=5)
    ax1.text(93.5, 11.0, r"$\Delta = 6$ chars",
             fontsize=6.8, fontweight="bold", color="#065f46",
             ha="right", va="center", zorder=6,
             bbox=dict(boxstyle="round,pad=0.20", facecolor="white", edgecolor="#10b981", lw=0.6, alpha=0.98))

    ax1.set_xlabel(r"Burst Injection Rate $R_{\mathrm{burst}}$ (chars/s)", fontsize=8.4, fontweight="bold", labelpad=5)
    ax1.set_ylabel("Quarantine Latency (Keystrokes)", fontsize=8.4, fontweight="bold", color=C_NAVY, labelpad=4)
    ax1.set_xlim(35.0, 105.0)
    ax1.set_ylim(0.0, 20.0)
    ax1.set_yticks([0, 4, 8, 12, 16, 20])
    ax1.set_xticks([40, 60, 80, 100])
    ax1.tick_params(axis="y", labelcolor=C_NAVY, labelsize=7.8, pad=2)
    ax1.tick_params(axis="x", labelsize=7.8, pad=2)
    ax1.grid(True, linestyle="--", alpha=0.5, color=C_GRID)

    # 4. Right Axis: Wall-Clock Reaction Time (ms: 0 to 250)
    ax2 = ax1.twinx()
    ax2.set_xlim(35.0, 105.0)
    line_time, = ax2.plot(fine_rates, fine_ms, color=C_BLUE, linewidth=1.9, linestyle="-.", zorder=3,
                          label=r"Reaction Time ($t_{\mathrm{quar}}$)")
    ax2.plot(rates, wall_clock_ms, marker="s", markersize=4.8, color=C_BLUE, linestyle="None", zorder=4)
    ax2.set_ylabel(r"Wall-Clock Latency $t_{\mathrm{quar}}$ (ms)", fontsize=8.4, fontweight="bold", color=C_BLUE, labelpad=4)
    ax2.set_ylim(0.0, 250.0)
    ax2.set_yticks([0, 50, 100, 150, 200, 250])
    ax2.tick_params(axis="y", labelcolor=C_BLUE, labelsize=7.8, pad=2)

    # 5. Non-colliding Endpoint Labels at Key Operating Limits
    # Point 1: (40 ch/s, 200 ms) -> placed above-right of marker at (41.5, 208.0)
    ax2.text(41.5, 208.0, r"$\mathbf{200.0\,\mathrm{ms}}$ (at $40\,\mathrm{ch/s}$)",
             fontsize=6.4, fontweight="bold", color=C_BLUE,
             ha="left", va="bottom", zorder=7,
             bbox=dict(boxstyle="round,pad=0.20", facecolor="white", edgecolor="#93c5fd", lw=0.6, alpha=0.96))

    # Point 2: (100 ch/s, 80.1 ms) -> placed safely below marker at (101.0, 58.0)
    ax2.text(101.0, 58.0, r"$\mathbf{80.1\,\mathrm{ms}}$ (at $100\,\mathrm{ch/s}$)",
             fontsize=6.4, fontweight="bold", color=C_BLUE,
             ha="right", va="top", zorder=7,
             bbox=dict(boxstyle="round,pad=0.20", facecolor="white", edgecolor="#93c5fd", lw=0.6, alpha=0.96))

    # 6. Upper-Right Compact Legend in Clear White Space
    lines = [line_exec, line_lat, line_time]
    labels = [l.get_label() for l in lines]
    leg = ax2.legend(lines, labels, loc="upper right", fontsize=6.2, framealpha=0.98, edgecolor="#CBD5E1",
                     borderpad=0.35, labelspacing=0.65, handlelength=1.5)
    leg.get_frame().set_linewidth(0.6)

    out_pdf = os.path.join(BRAIN_DIR, "fig5_spotless.pdf")
    out_png = os.path.join(BRAIN_DIR, "fig5_spotless.png")
    fig.savefig(out_pdf, format="pdf")
    fig.savefig(out_png, format="png", dpi=300)
    plt.close(fig)

    # Audit collisions
    doc = fitz.open(out_pdf)
    words = doc[0].get_text("words")
    rects = [fitz.Rect(w[:4]) for w in words]
    coll = 0
    for a in range(len(rects)):
        for b in range(a + 1, len(rects)):
            r_int = rects[a] & rects[b]
            if not r_int.is_empty and r_int.width > 0.5 and r_int.height > 0.5:
                coll += 1
                w1 = words[a][4].encode("ascii", errors="replace").decode()
                w2 = words[b][4].encode("ascii", errors="replace").decode()
                print(f"Collision between '{w1}' and '{w2}': {r_int}")
    print(f"=== fig5_spotless: {len(words)} words, {coll} collisions ===")

build_spotless_fig5()
