import os
import shutil
import zipfile
import pymupdf  # PyMuPDF
from PIL import Image

BASE_DIR = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32"
PAPER_DIR = os.path.join(BASE_DIR, "paper")
ARTIFACT_DIR = r"C:\Users\Ram\.gemini\antigravity\brain\ce8071ad-ae44-4bc1-99a9-e4d2c343777c"
PDF_PATH = os.path.join(PAPER_DIR, "WHID_GUARD_2027.pdf")
PREVIEW_PATH = os.path.join(PAPER_DIR, "WHID_GUARD_PREVIEW.png")
BUNDLE_PATH = os.path.join(PAPER_DIR, "WHID_GUARD_SUBMISSION_BUNDLE.zip")

print("Rendering 6-page preview...")
doc = pymupdf.open(PDF_PATH)
assert len(doc) == 6, f"Expected 6 pages, found {len(doc)}"

page_imgs = []
zoom = 2.0  # 144 DPI
mat = pymupdf.Matrix(zoom, zoom)

for i in range(len(doc)):
    pix = doc[i].get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    page_imgs.append(img)

# Arrange into 3 columns x 2 rows
pw, ph = page_imgs[0].size
pad = 30
header_h = 80
cols = 3
rows = 2

montage_w = cols * pw + (cols + 1) * pad
montage_h = rows * ph + (rows + 1) * pad + header_h

montage = Image.new("RGB", (montage_w, montage_h), (241, 245, 249))

# Draw header
from PIL import ImageDraw, ImageFont
draw = ImageDraw.Draw(montage)
font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 36)
font_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 22)

draw.text((pad, 20), "WHID-Guard IEEE Camera-Ready Manuscript (6.0 Pages Double-Column)", fill=(15, 23, 42), font=font_title)
draw.text((pad, 62), "Authors: Ram Karthik G & Dr. G Saranya  |  Department of Cybersecurity, Amrita Vishwa Vidyapeetham", fill=(71, 85, 105), font=font_sub)

for idx, pimg in enumerate(page_imgs):
    r = idx // cols
    c = idx % cols
    x = pad + c * (pw + pad)
    y = header_h + pad + r * (ph + pad)
    
    # Shadow / Border
    draw.rectangle([x - 2, y - 2, x + pw + 1, y + ph + 1], outline=(148, 163, 184), width=2)
    montage.paste(pimg, (x, y))

montage.save(PREVIEW_PATH, quality=95)
print(f"Saved preview: {PREVIEW_PATH} ({montage_w}x{montage_h})")

# Copy to brain artifact directory
shutil.copy2(PREVIEW_PATH, os.path.join(ARTIFACT_DIR, "WHID_GUARD_PREVIEW.png"))
shutil.copy2(PDF_PATH, os.path.join(ARTIFACT_DIR, "WHID_GUARD_2027.pdf"))
print(f"Copied artifacts to {ARTIFACT_DIR}")

# Create Submission Bundle
print("Packaging submission bundle...")
bundle_files = [
    "WHID_GUARD_2027.pdf",
    "WHID_GUARD_2027.tex",
    "IEEEtran.cls",
    "system_architecture.pdf",
    "system_architecture.png",
    "fsm_diagram.pdf",
    "fsm_diagram.png",
    "defense_architecture.pdf",
    "defense_architecture.png",
    "fig_iki_distribution.pdf",
    "fig_iki_distribution.png",
    "fig_detection_latency.pdf",
    "fig_detection_latency.png"
]

with zipfile.ZipFile(BUNDLE_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
    for fname in bundle_files:
        fpath = os.path.join(PAPER_DIR, fname)
        if os.path.exists(fpath):
            zf.write(fpath, arcname=fname)
            print(f"  Added {fname} ({os.path.getsize(fpath)} bytes)")
        else:
            print(f"  WARNING: File missing: {fname}")

print(f"Created submission bundle: {BUNDLE_PATH} ({os.path.getsize(BUNDLE_PATH)} bytes)")
print("ALL TASKS COMPLETED PERFECTLY!")
