import fitz

svg_code = '''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="150" viewBox="0 0 300 150">
    <rect width="300" height="150" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" rx="8"/>
    <text x="150" y="80" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="bold" fill="#1e293b" text-anchor="middle">PyMuPDF Vector SVG to PDF</text>
</svg>'''

doc = fitz.open(stream=svg_code.encode("utf-8"), filetype="svg")
pdf_bytes = doc.convert_to_pdf()
pdf_doc = fitz.open("pdf", pdf_bytes)
out_path = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\test_svg.pdf"
pdf_doc.save(out_path)
print("SUCCESS! Page rect:", pdf_doc[0].rect, "Saved to:", out_path)
