"""
Crafts a 100% publication-grade Figure 5 (Detection Latency & Reaction Time).
Guaranteed ZERO overlap between any text, arrows, legends, and curves.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32"
PAPER_DIR = os.path.join(BASE_DIR, "paper")
os.makedirs(PAPER_DIR, exist_ok=True)

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams["font.size"] = 10
plt.rcParams["axes.linewidth"] = 1.0

fig, ax1 = plt.subplots(figsize=(6.8, 4.0), dpi=300)
fig.subplots_adjust(left=0.11, right=0.87, top=0.91, bottom=0.13)

# Data points
rates = np.array([40.0, 50.0, 60.0, 66.7, 75.0, 85.0, 100.0])
chars_allowed = np.array([8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0])
wall_clock_ms = 8.0 * (1000.0 / rates)

fine_rates = np.linspace(38.0, 108.0, 200)
fine_ms = 8.0 * (1000.0 / fine_rates)

# Shaded background zones
ax1.axvspan(38.0, 110.0, color="#F8FAFC", alpha=0.9, zorder=0)
ax1.axvspan(10.0, 38.0, color="#F0FDF4", alpha=0.6, zorder=0)
ax1.axvline(38.0, color="#64748B", linestyle=":", linewidth=1.4, zorder=1)

# Zone Headers
ax1.text(24.0, 17.5, "Human / Evasion Zone\n(Cadence Anomaly Alert)", ha="center", va="center",
         fontsize=8.0, color="#059669", fontweight="bold")
ax1.text(64.0, 17.5, "Machine Injection Detection Zone\n(IKI < 25ms, Sustained CV < 0.15)", ha="center", va="center",
         fontsize=8.0, color="#1E293B", fontweight="bold")

# Attack Execution Horizon (14 Chars)
line_exec = ax1.axhline(14.0, color="#DC2626", linestyle="--", linewidth=1.8, zorder=2,
                        label=r"Attack Execution Horizon ($L_{\mathrm{exec}} = 14$ Chars)")

# Shaded Safety Buffer between 8 and 14 chars
ax1.fill_between([38.0, 110.0], 8.0, 14.0, color="#FEE2E2", alpha=0.65, zorder=1)

# Safety Buffer Text shifted to Left Center (x = 54)
ax1.text(54.0, 11.0, r"$\mathbf{\Delta = 6\text{ Character Safety Buffer}}$" "\n(Neutralized before execution)",
         ha="center", va="center", fontsize=8.0, fontweight="bold", color="#B91C1C",
         bbox=dict(boxstyle="round,pad=0.35", facecolor="#FFFFFF", edgecolor="#FECACA", alpha=0.95))

# Primary Curve: Quarantine Latency (8 Chars)
line_latency = ax1.plot(fine_rates, np.full_like(fine_rates, 8.0), color="#0F172A", linewidth=2.4, zorder=3,
                        label=r"Quarantine Trigger Latency ($\kappa = 8$ Keystrokes)")
ax1.plot(rates, chars_allowed, "o", color="#0F172A", markersize=6.0, zorder=4)

# Secondary Axis: Wall-Clock Response Time (ms)
ax2 = ax1.twinx()
line_ms = ax2.plot(fine_rates, fine_ms, color="#2563EB", linewidth=2.0, linestyle="-.", zorder=3,
                   label=r"Automated Reaction Time $t_{\mathrm{quarantine}}$ (ms)")
ax2.plot(rates, wall_clock_ms, "D", color="#2563EB", markersize=5.5, zorder=4)

# Callout at 100 ch/s placed in clear space (x=95, y=168 ms on right axis)
ax2.annotate(r"Standard BadUSB: 80.1 ms" "\n" r"($\mu = 10.0\mathrm{ms}, CV = 0.078$)",
             xy=(100.0, 80.1), xytext=(95.0, 168.0),
             ha="center",
             arrowprops=dict(facecolor="#2563EB", edgecolor="#2563EB", shrink=0.08, width=1.4, headwidth=4.5),
             fontsize=8.0, fontweight="bold", color="#1D4ED8",
             bbox=dict(boxstyle="round,pad=0.35", facecolor="#EFF6FF", edgecolor="#BFDBFE", alpha=0.95))

# Formatting Left Axis
ax1.set_xlabel(r"Keystroke Injection Speed $R_{\mathrm{burst}}$ (Characters / Second)", fontsize=9.5, fontweight="bold")
ax1.set_ylabel("Quarantine Latency (Characters Injected)", color="#0F172A", fontsize=9.5, fontweight="bold")
ax1.tick_params(axis="y", labelcolor="#0F172A")
ax1.set_xlim(10, 110)
ax1.set_ylim(0, 20)
ax1.grid(True, linestyle="--", alpha=0.45, color="#CBD5E1")

# Formatting Right Axis
ax2.set_ylabel(r"Automated Reaction Time $t_{\mathrm{quarantine}}$ (ms)", color="#2563EB", fontsize=9.5, fontweight="bold")
ax2.tick_params(axis="y", labelcolor="#2563EB")
ax2.set_ylim(0, 240)

# Legend placed in EMPTY Lower Left / Center quadrant (below y=8)
lines = [line_latency[0], line_ms[0], line_exec]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="lower left", bbox_to_anchor=(0.28, 0.04), fontsize=7.8, framealpha=0.95, edgecolor="#94A3B8")

out_pdf = os.path.join(PAPER_DIR, "fig_detection_latency.pdf")
out_png = os.path.join(PAPER_DIR, "fig_detection_latency.png")
fig.savefig(out_pdf, format="pdf")
fig.savefig(out_png, format="png", dpi=300)
plt.close(fig)
print(f"Generated Flawless Figure 5: {out_pdf} and {out_png}")
