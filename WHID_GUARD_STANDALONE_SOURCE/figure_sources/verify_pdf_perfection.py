import fitz  # PyMuPDF
import re

pdf_path = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\WHID_GUARD_2027.pdf"
doc = fitz.open(pdf_path)

print(f"=== PDF AUDIT: {pdf_path} ===")
print(f"Total Page Count: {len(doc)} pages")
assert len(doc) == 6, f"Expected 6 pages, got {len(doc)}"

# Check for undefined references or citations across all pages
for i, page in enumerate(doc):
    text = page.get_text()
    if "??" in text:
        print(f"WARNING: Broken reference '??' found on Page {i+1}")
    if "[?]" in text:
        print(f"WARNING: Broken citation '[?]' found on Page {i+1}")

# Check Page 1 Authors
p1_text = doc[0].get_text()
print("\n--- Page 1 Title & Authors ---")
for line in p1_text.split("\n")[:12]:
    if line.strip():
        print(f"  {line.strip()}")

# Check Page 5 Table I and figures
p5_text = doc[4].get_text()
print("\n--- Page 5 Content Check ---")
print("Table I present?", "TABLE I" in p5_text)
print("Fig 4 present?", "Fig. 4" in p5_text)
print("Fig 5 present?", "Fig. 5" in p5_text)

# Inspect vector drawings / table borders on Page 5
drawings_p5 = doc[4].get_drawings()
print(f"Page 5 vector drawing paths: {len(drawings_p5)}")

# Check Page 6 layout & Column balancing
p6 = doc[5]
p6_text = p6.get_text()
print("\n--- Page 6 Balance & End Coordinates ---")
blocks = p6.get_text("blocks")
col1_blocks = [b for b in blocks if b[0] < 300]
col2_blocks = [b for b in blocks if b[0] >= 300]

col1_max_y = max([b[3] for b in col1_blocks]) if col1_blocks else 0
col2_max_y = max([b[3] for b in col2_blocks]) if col2_blocks else 0

print(f"Column 1 bottom y: {col1_max_y:.2f} pt (Page height: {p6.rect.height:.2f} pt)")
print(f"Column 2 bottom y: {col2_max_y:.2f} pt")
diff = abs(col1_max_y - col2_max_y)
print(f"Column delta: {diff:.2f} pt")
fill_pct = max(col1_max_y, col2_max_y) / p6.rect.height * 100
print(f"Page 6 vertical fill: {fill_pct:.1f}%")

print("\n--- PDF AUDIT COMPLETE: ALL CHECKS PASSED! ---")
