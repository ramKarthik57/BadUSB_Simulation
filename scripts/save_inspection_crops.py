import pymupdf
from PIL import Image

pdf_path = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\WHID_GUARD_2027.pdf"
doc = pymupdf.open(pdf_path)

# Render Page 2 (Figure 1)
p2 = doc[1]
pix2 = p2.get_pixmap(dpi=200)
img2 = Image.frombytes("RGB", [pix2.width, pix2.height], pix2.samples)
# Figure 1 is at top of page 2
crop_fig1 = img2.crop((0, int(pix2.height * 0.05), pix2.width, int(pix2.height * 0.52)))
crop_fig1.save(r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\check_fig1.png")

# Render Page 3 (Figure 2)
p3 = doc[2]
pix3 = p3.get_pixmap(dpi=200)
img3 = Image.frombytes("RGB", [pix3.width, pix3.height], pix3.samples)
crop_fig2 = img3.crop((0, int(pix3.height * 0.05), pix3.width, int(pix3.height * 0.45)))
crop_fig2.save(r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\check_fig2.png")

# Render Page 5 (Figure 4, 5, Table 1)
p5 = doc[4]
pix5 = p5.get_pixmap(dpi=200)
img5 = Image.frombytes("RGB", [pix5.width, pix5.height], pix5.samples)
crop_fig5 = img5.crop((0, int(pix5.height * 0.35), pix5.width, int(pix5.height * 0.85)))
crop_fig5.save(r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\check_fig5.png")

print("Saved inspection crops: check_fig1.png, check_fig2.png, check_fig5.png")
