import fitz

def test_svg(font_size, box_x, box_w):
    center_x = box_x + box_w / 2
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 224" width="760" height="224" style="background:#ffffff; font-family:Helvetica, Arial, sans-serif;">
  <rect x="{box_x}" y="8" width="{box_w}" height="208" rx="6" fill="#faf5ff" stroke="#a855f7" stroke-width="1.3"/>
  <text x="{center_x}" y="25" font-size="{font_size}" font-weight="bold" fill="#6b21a8" text-anchor="middle">Tier 1: Mobile C2 Controller</text>
</svg>"""
    doc = fitz.open(stream=svg.encode("utf-8"), filetype="svg")
    pdf_bytes = doc.convert_to_pdf()
    pdf_doc = fitz.open("pdf", pdf_bytes)
    page = pdf_doc[0]
    blocks = page.get_text("blocks")
    t_box = blocks[0]
    text_x0, text_x1 = t_box[0], t_box[2]
    left_margin = text_x0 - box_x
    right_margin = (box_x + box_w) - text_x1
    print(f"Font {font_size}, box [{box_x}, {box_x + box_w}] (w={box_w}):")
    print(f"  Text bbox: [{text_x0:.2f}, {text_x1:.2f}] (w={text_x1 - text_x0:.2f})")
    print(f"  Left margin: {left_margin:.2f} pt | Right margin: {right_margin:.2f} pt")
    doc.close()
    pdf_doc.close()

print("Original:")
test_svg(9.6, 10, 116)

print("\nCandidate 1: font 8.8, box [8, 134] (w=126):")
test_svg(8.8, 8, 126)

print("\nCandidate 2: font 8.5, box [8, 134] (w=126):")
test_svg(8.5, 8, 126)

print("\nCandidate 3: font 8.6, box [6, 134] (w=128):")
test_svg(8.6, 6, 128)
