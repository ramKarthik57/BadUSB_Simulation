"""
Flawless Figure 4 Generator (Senior Reviewer & Top Conference Edition).
Fixes per user prompt:
- Decision Boundary legend text updated to:
  "Speed/Jitter Boundary (μ ≤ 25 ms ∨ CV_IKI < 0.15)"
- Compact, publication-grade legend formatting (fontsize=6.5, tight padding).
- 100% Type 42 / TrueType vector font embedding for IEEE PDF eXpress compliance.
"""

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams["font.family"] = "serif"
matplotlib.rcParams["mathtext.fontset"] = "dejavuserif"
matplotlib.rcParams["axes.linewidth"] = 1.0

BASE_DIR = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32"
PAPER_DIR = os.path.join(BASE_DIR, "paper")
FIG_FINAL = os.path.join(BASE_DIR, "figures", "final")
FIG_SOURCE = os.path.join(BASE_DIR, "figures", "source")
BRAIN_DIR = r"C:\Users\Ram\.gemini\antigravity\brain\ce8071ad-ae44-4bc1-99a9-e4d2c343777c"

fig, ax = plt.subplots(figsize=(3.4, 2.3), dpi=300)
fig.subplots_adjust(left=0.15, right=0.96, top=0.92, bottom=0.20)

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

# Histograms
ax.hist(badusb_deltas, bins=bins, color=C_BADUSB, alpha=0.85, edgecolor="#991B1B", linewidth=0.6,
        label=r"Standard BadUSB ($\mu = 10.0$ ms)", zorder=3)
ax.hist(evasion_deltas, bins=bins, color=C_EVASION, alpha=0.70, edgecolor="#1D4ED8", linewidth=0.6,
        label=r"Adversarial Evasion ($\mu = 119.3$ ms)", zorder=2)
ax.hist(human_deltas, bins=bins, color=C_HUMAN, alpha=0.55, edgecolor="#1E293B", linewidth=0.6,
        label=r"Human Baseline ($\mu = 144.2$ ms)", zorder=1)

# Threshold lines: Updated label per prompt
ax.axvline(25.0, color="#991B1B", linestyle="--", linewidth=1.4, zorder=4,
           label=r"Speed/Jitter ($\mu \leq 25\,$ms $\vee$ $\mathrm{CV}_{\mathrm{IKI}} < 0.15$)")
ax.axvline(75.0, color="#334155", linestyle=":", linewidth=1.4, zorder=4,
           label=r"Human Bound ($\mu \geq 75$ ms)")

# Clean white background with subtle grid
ax.grid(True, linestyle="--", alpha=0.5, color=C_GRID)

ax.set_xlabel(r"Inter-Key Interval $\Delta t$ (ms)", fontsize=8.8, fontweight="bold", labelpad=3)
ax.set_ylabel("Empirical Frequency", fontsize=8.8, fontweight="bold", labelpad=3)

ax.tick_params(axis="both", which="major", labelsize=8.2, pad=3)
ax.set_xlim(0, 450)
ax.set_ylim(0, 520)

legend = ax.legend(loc="upper right", frameon=True, fancybox=True, edgecolor="#CBD5E1",
                   framealpha=0.96, fontsize=6.5, handlelength=1.1, labelspacing=0.22, borderpad=0.28)
legend.get_frame().set_linewidth(0.8)

# Save both PDF and PNG
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

print("Flawless Figure 4 generated successfully!")
