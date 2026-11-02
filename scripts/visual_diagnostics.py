import os
import pymupdf
from PIL import Image

BASE_DIR = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32"
PDF_PATH = os.path.join(BASE_DIR, "paper", "WHID_GUARD_2027.pdf")
BRAIN_DIR = r"C:\Users\Ram\.gemini\antigravity\brain\ce8071ad-ae44-4bc1-99a9-e4d2c343777c"

doc = pymupdf.open(PDF_PATH)
print(f"Loaded PDF: {PDF_PATH} ({len(doc)} pages)")

# Render all 6 pages at 300 DPI for ultra-crisp visual analysis
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=300)
    out_p = os.path.join(BRAIN_DIR, f"page_{i+1}_hi_res.png")
    pix.save(out_p)
    print(f"Saved {out_p} ({pix.width}x{pix.height})")

# Also crop each figure exactly from the page where it appears
# Page 2: Fig 1 (system_architecture.pdf)
# Page 3: Fig 2 (fsm_diagram.pdf)
# Page 4: Fig 3 (defense_architecture.pdf)
# Page 5: Fig 4 (fig_iki_distribution.pdf) and Fig 5 (fig_detection_latency.pdf)

crops = [
    (2, "crop_fig1_p2_hi.png", pymupdf.Rect(40, 45, 570, 220)),
    (3, "crop_fig2_p3_hi.png", pymupdf.Rect(40, 45, 570, 220)),
    (4, "crop_fig3_p4_hi.png", pymupdf.Rect(40, 45, 570, 225)),
    (5, "crop_fig4_p5_hi.png", pymupdf.Rect(45, 45, 300, 240)),
    (5, "crop_fig5_p5_hi.png", pymupdf.Rect(310, 45, 565, 240)),
]

for pno, name, rect in crops:
    page = doc[pno - 1]
    pix = page.get_pixmap(dpi=300, clip=rect)
    out_p = os.path.join(BRAIN_DIR, name)
    pix.save(out_p)
    print(f"Saved crop {name} ({pix.width}x{pix.height})")

print("Diagnostics rendering complete.")
