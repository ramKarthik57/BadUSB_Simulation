import os
import shutil
import pymupdf
from PIL import Image

BASE_DIR = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32"
PAPER_DIR = os.path.join(BASE_DIR, "paper")
TIKZ_DIR = os.path.join(PAPER_DIR, "tikz")
ARTIFACT_DIR = r"C:\Users\Ram\.gemini\antigravity\brain\ce8071ad-ae44-4bc1-99a9-e4d2c343777c"
PDF_PATH = os.path.join(PAPER_DIR, "WHID_GUARD_2027.pdf")

doc = pymupdf.open(PDF_PATH)
print(f"Exporting inspection crops and pages from {PDF_PATH} ({len(doc)} pages)...")

# 1. Export each page at 200 DPI
for idx in range(len(doc)):
    page = doc[idx]
    pix = page.get_pixmap(dpi=200)
    page_img_path = os.path.join(ARTIFACT_DIR, f"page_{idx+1}.png")
    pix.save(page_img_path)
    print(f"Saved {page_img_path}")

# 2. Extract crops for individual figures directly from page renders
# Fig 1 is at top of Page 2
p2_img = Image.open(os.path.join(ARTIFACT_DIR, "page_2.png"))
crop_fig1 = p2_img.crop((0, int(p2_img.height * 0.04), p2_img.width, int(p2_img.height * 0.38)))
crop_fig1.save(os.path.join(ARTIFACT_DIR, "crop_fig1_p2.png"))

# Fig 2 is at top of Page 3
p3_img = Image.open(os.path.join(ARTIFACT_DIR, "page_3.png"))
crop_fig2 = p3_img.crop((0, int(p3_img.height * 0.04), p3_img.width, int(p3_img.height * 0.36)))
crop_fig2.save(os.path.join(ARTIFACT_DIR, "crop_fig2_p3.png"))

# Fig 3 is at top of Page 4
p4_img = Image.open(os.path.join(ARTIFACT_DIR, "page_4.png"))
crop_fig3 = p4_img.crop((0, int(p4_img.height * 0.04), p4_img.width, int(p4_img.height * 0.40)))
crop_fig3.save(os.path.join(ARTIFACT_DIR, "crop_fig3_p4.png"))

# Figs 4 & 5 on Page 5
p5_img = Image.open(os.path.join(ARTIFACT_DIR, "page_5.png"))
crop_fig4_5 = p5_img.crop((0, int(p5_img.height * 0.04), p5_img.width, int(p5_img.height * 0.45)))
crop_fig4_5.save(os.path.join(ARTIFACT_DIR, "crop_fig4_p5.png"))

# 3. Copy standalone native vector renders
shutil.copy2(os.path.join(TIKZ_DIR, "fig1_p3_preview-1.png"), os.path.join(ARTIFACT_DIR, "fig1_p3_inspect.png"))
shutil.copy2(os.path.join(TIKZ_DIR, "fig2_p3_preview-1.png"), os.path.join(ARTIFACT_DIR, "fig2_p3_inspect.png"))
shutil.copy2(os.path.join(TIKZ_DIR, "fig3_p_preview-1.png"), os.path.join(ARTIFACT_DIR, "fig3_p_inspect.png"))

print("All inspection artifacts exported successfully!")
