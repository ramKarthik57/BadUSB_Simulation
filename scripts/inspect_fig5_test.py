import fitz

doc = fitz.open(r"C:\Users\Ram\.gemini\antigravity\brain\ce8071ad-ae44-4bc1-99a9-e4d2c343777c\fig5_perfect_test.pdf")
page = doc[0]
print('Page rect:', page.rect)
blocks = page.get_text('blocks')
for b in blocks:
    text = b[4].strip().encode('ascii', errors='backslashreplace').decode('ascii')
    print('Block:', [round(x, 1) for x in b[:4]], repr(text))

words = page.get_text('words')
rects = [fitz.Rect(w[:4]) for w in words]
coll = 0
for a in range(len(rects)):
    for b in range(a + 1, len(rects)):
        r_int = rects[a] & rects[b]
        if not r_int.is_empty and r_int.width > 0.5 and r_int.height > 0.5:
            coll += 1
            w1 = words[a][4].encode("ascii", errors="replace").decode()
            w2 = words[b][4].encode("ascii", errors="replace").decode()
            print(f"Collision between '{w1}' and '{w2}': {r_int}")
print(f"=== Words: {len(words)}, Collisions: {coll} ===")
