import fitz

doc = fitz.open(r"C:\Users\Ram\.gemini\antigravity\brain\ce8071ad-ae44-4bc1-99a9-e4d2c343777c\fig5_clean.pdf")
page = doc[0]
print('Page rect:', page.rect)
blocks = page.get_text('blocks')
for b in blocks:
    text = b[4].strip().encode('ascii', errors='backslashreplace').decode('ascii')
    print('Block:', [round(x, 1) for x in b[:4]], repr(text))
