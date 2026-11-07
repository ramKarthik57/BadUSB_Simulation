import fitz

doc = fitz.open(r'C:\Users\Ram\.gemini\antigravity\brain\ce8071ad-ae44-4bc1-99a9-e4d2c343777c\test_fig5_v5.pdf')
words = doc[0].get_text('words')
rects = [fitz.Rect(w[:4]) for w in words]
for a in range(len(rects)):
    for b in range(a + 1, len(rects)):
        r_int = rects[a] & rects[b]
        if not r_int.is_empty and r_int.width > 0.5 and r_int.height > 0.5:
            w1 = words[a][4].encode('ascii', errors='replace').decode()
            w2 = words[b][4].encode('ascii', errors='replace').decode()
            print(f'Collision between "{w1}" and "{w2}": {r_int}')
