import os
from PIL import Image

paper_dir = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper"
figs = [
    "system_architecture.png",
    "fsm_diagram.png",
    "defense_architecture.png",
    "fig_iki_distribution.png",
    "fig_detection_latency.png"
]

print("=== IMAGE INTEGRITY VERIFICATION ===")
for f in figs:
    path = os.path.join(paper_dir, f)
    if not os.path.exists(path):
        print(f"[FAIL] Missing {f}")
        continue
    img = Image.open(path)
    print(f"[PASS] {f}: {img.size} ({img.format}, {img.mode}) - OK")
