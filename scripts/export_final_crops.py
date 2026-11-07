import os
import fitz

BRAIN_DIR = r"C:\Users\Ram\.gemini\antigravity\brain\ce8071ad-ae44-4bc1-99a9-e4d2c343777c"
PDF_PATH = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\WHID_GUARD_2027.pdf"

doc = fitz.open(PDF_PATH)

# Page 2: Fig 1
p2 = doc[1]
pix1 = p2.get_pixmap(dpi=300, clip=fitz.Rect(36, 40, 576, 260))
pix1.save(os.path.join(BRAIN_DIR, "pdf_crop_fig1.png"))

# Page 3: Fig 2
p3 = doc[2]
pix2 = p3.get_pixmap(dpi=300, clip=fitz.Rect(36, 40, 576, 260))
pix2.save(os.path.join(BRAIN_DIR, "pdf_crop_fig2.png"))

# Page 4: Fig 3
p4 = doc[3]
pix3 = p4.get_pixmap(dpi=300, clip=fitz.Rect(36, 40, 576, 260))
pix3.save(os.path.join(BRAIN_DIR, "pdf_crop_fig3.png"))

# Page 5: Fig 4 & Fig 5
p5 = doc[4]
pix45 = p5.get_pixmap(dpi=300, clip=fitz.Rect(36, 40, 576, 260))
pix45.save(os.path.join(BRAIN_DIR, "pdf_crop_fig4_fig5.png"))

# Also save standalone high-res images of each figure
shutil_copy = [
    (r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\fig1_system_architecture.png", "fig1_final.png"),
    (r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\fig2_fsm_diagram.png", "fig2_final.png"),
    (r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\fig3_selective_defense.png", "fig3_final.png"),
    (r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\fig_iki_distribution.png", "fig4_final.png"),
    (r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\fig_detection_latency.png", "fig5_final.png"),
]
import shutil
for src, dst in shutil_copy:
    shutil.copyfile(src, os.path.join(BRAIN_DIR, dst))

print("All high-res crops and standalone images exported to brain directory.")
