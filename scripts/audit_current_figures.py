import os
from PIL import Image

paper_dir = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper"
figs = [
    ("Figure 1", "system_architecture.png"),
    ("Figure 2", "fsm_diagram.png"),
    ("Figure 3", "defense_architecture.png"),
    ("Figure 4", "fig_iki_distribution.png"),
    ("Figure 5", "fig_detection_latency.png")
]

for name, fname in figs:
    fpath = os.path.join(paper_dir, fname)
    if not os.path.exists(fpath):
        print(f"[MISSING] {name}: {fname}")
        continue
    img = Image.open(fpath)
    print(f"[FOUND] {name}: {fname} | Size: {img.size[0]}x{img.size[1]} | Mode: {img.mode}")
