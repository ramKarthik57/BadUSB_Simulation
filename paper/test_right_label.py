import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import fitz

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['mathtext.fontset'] = 'dejavuserif'
matplotlib.rcParams['axes.linewidth'] = 1.0

labels = [
    'Reaction Time (ms)',
    r'Latency $t_{\mathrm{quar}}$ (ms)',
    'Wall-Clock Latency (ms)',
    r'Reaction Time $t_{\mathrm{quar}}$ (ms)'
]

for lbl in labels:
    fig, ax1 = plt.subplots(figsize=(3.4, 2.3), dpi=300)
    fig.subplots_adjust(left=0.17, right=0.82, top=0.89, bottom=0.20)
    ax2 = ax1.twinx()
    ax2.set_ylabel(lbl, fontsize=9.0, fontweight='bold', color='#1D4ED8', labelpad=4)
    ax2.set_ylim(0.0, 250.0)
    
    test_pdf = 'C:/Users/Ram/Desktop/BadUSB_Using_ESP32/paper/test_lbl.pdf'
    fig.savefig(test_pdf)
    plt.close(fig)
    
    doc = fitz.open(test_pdf)
    page = doc[0]
    words = [w for w in page.get_text('words') if w[0] > 200]
    y_min = min(w[1] for w in words)
    y_max = max(w[3] for w in words)
    in_bounds = (y_min >= 0 and y_max <= page.rect.height)
    print(f'Label \"{lbl}\": y=[{y_min:.1f}, {y_max:.1f}] on height {page.rect.height:.1f} (in bounds: {in_bounds})')
