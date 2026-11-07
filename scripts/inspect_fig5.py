import fitz

doc = fitz.open('paper/fig_detection_latency.pdf')
page = doc[0]
print('Page rect:', page.rect)
blocks = page.get_text('blocks')
for b in blocks:
    text = b[4].strip().encode('ascii', errors='backslashreplace').decode('ascii')
    print('Block:', [round(x, 1) for x in b[:4]], repr(text))

print("\n--- WORDS ---")
words = page.get_text('words')
for w in words:
    text = w[4].encode('ascii', errors='backslashreplace').decode('ascii')
    print(f"Word at {[round(x, 1) for x in w[:4]]}: {repr(text)}")
