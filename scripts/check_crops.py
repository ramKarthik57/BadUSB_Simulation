import os
from PIL import Image

paper_dir = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper"
for f in ["check_fig1.png", "check_fig2.png", "check_fig5.png"]:
    p = os.path.join(paper_dir, f)
    if os.path.exists(p):
        im = Image.open(p)
        print(f"{f}: {im.size}")
