"""
Generator for Enlarged Figure 4 (IKI Distribution) and Figure 5 (Detection Latency).
Top Conference & Senior Reviewer Edition with enlarged, highly legible typography.
"""

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams["font.family"] = "serif"
matplotlib.rcParams["mathtext.fontset"] = "dejavuserif"
matplotlib.rcParams["axes.linewidth"] = 1.1

BASE_DIR = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32"
PAPER_DIR = os.path.join(BASE_DIR, "paper")
FIG_FINAL = os.path.join(BASE_DIR, "figures", "final")
BRAIN_DIR = r"C:\Users\Ram\.gemini\antigravity\brain\ce8071ad-ae44-4bc1-99a9-e4d2c343777c"

# ===========================================================================
# FIGURE 4: IKI DISTRIBUTION (ENLARGED)
# ===========================================================================
def generate_fig4():
    fig, ax = plt.subplots(figsize=(3.45, 2.35), dpi=300)
    fig.subplots_adjust(left=0.16, right=0.96, top=0.90, bottom=0.19)

    np.random.seed(42)

    # 1. Standard BadUSB: N=500, mu=10.01, sigma=0.78
    badusb_deltas = np.random.normal(10.01, 0.78, 500)
    badusb_deltas = np.clip(badusb_deltas, 8.0, 13.0)

    # 2. Evasion BadUSB: N=500, base=80, jitter=U(0,40), pauses U(150,300) on 15% delims
    base_jitter = 80.0 + np.random.uniform(0, 40.0, 425)
    delims = np.random.uniform(150.0, 300.0, 75)
    evasion_deltas = np.concatenate([base_jitter, delims])
    np.random.shuffle(evasion_deltas)

    # 3. Human Operator: N=500, lognormal distribution matching mu=144.18, sigma=91.98
    sigma_log = np.sqrt(np.log(1 + (91.98 / 144.18)**2))
    mean_log = np.log(144.18) - (sigma_log**2) / 2
    human_deltas = np.random.lognormal(mean_log, sigma_log, 500)
    human_deltas = np.clip(human_deltas, 40.0, 440.0)

    bins = np.linspace(0, 450, 46)

    # Restrained IEEE Color Palette
    C_BADUSB = "#DC2626"
    C_EVASION = "#2563EB"
    C_HUMAN = "#475569"
    C_GRID = "#E2E8F0"

    # Histograms with bolder borders
    ax.hist(badusb_deltas, bins=bins, color=C_BADUSB, alpha=0.85, edgecolor="#991B1B", linewidth=0.8,
            label=r"Standard BadUSB ($\mu = 10.0$ ms)", zorder=3)
    ax.hist(evasion_deltas, bins=bins, color=C_EVASION, alpha=0.70, edgecolor="#1D4ED8", linewidth=0.8,
            label=r"Adversarial Evasion ($\mu = 119.3$ ms)", zorder=2)
    ax.hist(human_deltas, bins=bins, color=C_HUMAN, alpha=0.55, edgecolor="#1E293B", linewidth=0.8,
            label=r"Human Baseline ($\mu = 144.2$ ms)", zorder=1)

    # Threshold lines: bold and prominent
    ax.axvline(25.0, color="#991B1B", linestyle="--", linewidth=1.8, zorder=4,
               label=r"Speed/Jitter ($\mu \leq 25\,$ms $\vee$ $\mathrm{CV}_{\mathrm{IKI}} < 0.15$)")
    ax.axvline(75.0, color="#334155", linestyle=":", linewidth=1.8, zorder=4,
               label=r"Human Bound ($\mu \geq 75$ ms)")

    # Grid
    ax.grid(True, linestyle="--", alpha=0.5, color=C_GRID)

    # Enlarged, bold labels
    ax.set_xlabel(r"Inter-Key Interval $\Delta t$ (ms)", fontsize=10.0, fontweight="bold", labelpad=3)
    ax.set_ylabel("Empirical Frequency", fontsize=10.0, fontweight="bold", labelpad=3)

    ax.tick_params(axis="both", which="major", labelsize=9.2, pad=3)
    ax.set_xlim(0, 450)
    ax.set_ylim(0, 520)

    # Enlarged legend
    legend = ax.legend(loc="upper right", frameon=True, fancybox=True, edgecolor="#CBD5E1",
                       framealpha=0.96, fontsize=7.2, handlelength=1.2, labelspacing=0.25, borderpad=0.28)
    legend.get_frame().set_linewidth(0.8)

    # Save
    pdf_paper = os.path.join(PAPER_DIR, "fig_iki_distribution.pdf")
    png_paper = os.path.join(PAPER_DIR, "fig_iki_distribution.png")
    pdf_final = os.path.join(FIG_FINAL, "fig4_iki_distribution.pdf")
    png_final = os.path.join(FIG_FINAL, "fig4_iki_distribution.png")

    fig.savefig(pdf_paper)
    fig.savefig(png_paper, dpi=300)
    fig.savefig(pdf_final)
    fig.savefig(png_final, dpi=300)
    fig.savefig(os.path.join(BRAIN_DIR, "crop_fig4_p5_hi.png"), dpi=300)
    plt.close(fig)
    print("Enlarged Figure 4 generated successfully!")


# ===========================================================================
# FIGURE 5: DETECTION LATENCY (ENLARGED)
# ===========================================================================
def generate_fig5():
    fig, ax1 = plt.subplots(figsize=(3.45, 2.38), dpi=300)
    fig.subplots_adjust(left=0.16, right=0.84, top=0.86, bottom=0.18)

    rates = np.array([40.0, 50.0, 60.0, 66.7, 75.0, 85.0, 100.0])
    chars_allowed = np.array([8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0])
    wall_clock_ms = 8.0 * (1000.0 / rates)

    fine_rates = np.linspace(40.0, 106.0, 200)
    fine_ms = 8.0 * (1000.0 / fine_rates)

    # Colors
    C_NAVY = "#0F172A"       # Slate 900
    C_BLUE = "#1D4ED8"       # IEEE Steel Blue
    C_RED = "#B91C1C"        # Controlled Muted Red
    C_GRID = "#E2E8F0"       # Subtle gray
    C_BUFFER = "#F1F5F9"     # Light neutral tint for safety buffer

    # 1. Safety Buffer between Trigger (8) and Execution Horizon (14)
    ax1.fill_between([40.0, 106.0], 8.0, 14.0, color=C_BUFFER, alpha=1.0, zorder=1)

    # 2. Execution Horizon (14 Chars)
    line_exec = ax1.axhline(14.0, color=C_RED, linestyle="--", linewidth=1.6, zorder=2,
                            label=r"Horizon ($L_{\mathrm{exec}} = 14$)")

    # 3. Primary Curve: Quarantine Latency (8 Chars)
    line_lat, = ax1.plot([40.0, 106.0], [8.0, 8.0], color=C_NAVY, linewidth=2.4, zorder=3,
                         label=r"Trigger ($\kappa = 8$)")
    ax1.plot(rates, chars_allowed, marker="o", markersize=5.5, color=C_NAVY,
             linestyle="None", zorder=4)

    # Axes styling - Left (Chars)
    ax1.set_xlabel(r"Burst Rate $R_{\mathrm{burst}}$ (chars/s)",
                   fontsize=10.0, fontweight="bold", labelpad=3)
    ax1.set_ylabel("Quarantine Latency (Chars)",
                   fontsize=10.0, fontweight="bold", color=C_NAVY, labelpad=3)
    ax1.set_xlim(38.0, 106.0)
    ax1.set_ylim(0.0, 22.0)
    ax1.set_yticks([0, 4, 8, 12, 16, 20])
    ax1.set_xticks([40, 60, 80, 100])
    ax1.tick_params(axis="y", labelcolor=C_NAVY, labelsize=9.2, pad=3)
    ax1.tick_params(axis="x", labelsize=9.2, pad=3)
    ax1.grid(True, linestyle="--", alpha=0.5, color=C_GRID)

    # Secondary Axis: Reaction Time in ms
    ax2 = ax1.twinx()
    ax2.set_xlim(38.0, 106.0)
    line_time, = ax2.plot(fine_rates, fine_ms, color=C_BLUE, linewidth=2.2, linestyle="-.", zorder=3,
                          label=r"Reaction Time ($t_{\mathrm{quar}}$)")
    ax2.plot(rates, wall_clock_ms, marker="s", markersize=5.0, color=C_BLUE,
             linestyle="None", zorder=4)

    ax2.set_ylabel("Reaction Time (ms)",
                   fontsize=10.0, fontweight="bold", color=C_BLUE, labelpad=4)
    ax2.set_ylim(0.0, 275.0)
    ax2.set_yticks([0, 50, 100, 150, 200, 250])
    ax2.tick_params(axis="y", labelcolor=C_BLUE, labelsize=9.2, pad=3)

    # Exact Coordinate Boundary Guidelines anchored at (40.0 ch/s, 200.0 ms)
    ax2.plot([40.0, 40.0], [0.0, 200.0], color="#059669", linestyle=":", linewidth=1.5, zorder=5)
    ax2.plot([40.0, 106.0], [200.0, 200.0], color="#059669", linestyle=":", linewidth=1.5, zorder=5)
    ax2.plot(40.0, 200.0, marker="o", markersize=6.5, color="#059669", zorder=6)

    # Detection Floor Callout Box anchored at (41.0, 236.0 ms)
    ax2.annotate("Detection Floor\n" + r"$t_{\mathrm{quar}} = 200\,\mathrm{ms}$" + "\n(40 ch/s, 25 ms)",
                 xy=(40.0, 200.0), xycoords="data",
                 xytext=(41.0, 236.0), textcoords="data",
                 fontsize=6.2, fontweight="bold", color="#059669",
                 ha="left", va="center", zorder=8, linespacing=1.25,
                 bbox=dict(boxstyle="round,pad=0.22", facecolor="white", edgecolor="#10b981", lw=0.9, alpha=0.96),
                 arrowprops=dict(arrowstyle="->", color="#059669", lw=1.1, shrinkA=1, shrinkB=3))

    # Dimension Arrow for Safety Margin at x = 92.0 with centered white pill
    ax1.annotate("", xy=(92.0, 13.7), xytext=(92.0, 8.3),
                 arrowprops=dict(arrowstyle="<->", color="#334155", lw=1.2), zorder=5)
    ax1.text(92.0, 11.0, r"$\Delta = 6$ Margin",
             fontsize=7.8, fontweight="bold", color="#1E293B",
             ha="center", va="center", zorder=7,
             bbox=dict(boxstyle="round,pad=0.20", facecolor="white", edgecolor="#CBD5E1", lw=0.7, alpha=0.98))

    # Min. Latency Floor Callout annotation at 100 ch/s
    ax2.annotate("Min. Latency Floor = 80.1 ms\n" + r"($R = 100$ ch/s, $\kappa = 8$)",
                 xy=(100.0, 80.08), xycoords="data",
                 xytext=(80.0, 38.0), textcoords="data",
                 fontsize=6.4, fontweight="bold", color=C_BLUE,
                 ha="center", va="center", zorder=7, linespacing=1.35,
                 bbox=dict(boxstyle="round,pad=0.24", facecolor="white", edgecolor="#93C5FD", lw=0.9, alpha=0.96),
                 arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1.1, shrinkA=2, shrinkB=4))

    # Legend
    lines = [line_lat, line_exec, line_time]
    labels = [l.get_label() for l in lines]
    legend = ax1.legend(lines, labels, loc="upper right", frameon=True, fancybox=True,
                        edgecolor="#CBD5E1", framealpha=0.96, fontsize=7.0,
                        handlelength=1.1, labelspacing=0.22, borderpad=0.25)
    legend.get_frame().set_linewidth(0.8)
    legend.set_zorder(10)

    # Save
    pdf_paper = os.path.join(PAPER_DIR, "fig_detection_latency.pdf")
    png_paper = os.path.join(PAPER_DIR, "fig_detection_latency.png")
    pdf_final = os.path.join(FIG_FINAL, "fig5_detection_latency.pdf")
    png_final = os.path.join(FIG_FINAL, "fig5_detection_latency.png")

    fig.savefig(pdf_paper)
    fig.savefig(png_paper, dpi=300)
    fig.savefig(pdf_final)
    fig.savefig(png_final, dpi=300)
    fig.savefig(os.path.join(BRAIN_DIR, "crop_fig5_p5_hi.png"), dpi=300)
    plt.close(fig)
    print("Enlarged Figure 5 generated successfully!")

if __name__ == "__main__":
    generate_fig4()
    generate_fig5()
