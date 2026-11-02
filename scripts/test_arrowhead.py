import pymupdf

svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <line x1="10" y1="50" x2="80" y2="50" stroke="#2563eb" stroke-width="2"/>
  <polygon points="74,46 82,50 74,54" fill="#2563eb"/>
</svg>"""

doc = pymupdf.open(stream=svg.encode("utf-8"), filetype="svg")
pdf_bytes = doc.convert_to_pdf()
doc_pdf = pymupdf.open(stream=pdf_bytes, filetype="pdf")
drawings = doc_pdf[0].get_drawings()
print(f"Test drawings count: {len(drawings)}")
for d in drawings:
    print(d["type"], d.get("color"), d.get("fill"))
