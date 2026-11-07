import fitz

pdf_path = 'paper/WHID_GUARD_2027.pdf'
doc = fitz.open(pdf_path)

for pno, r_clip, figname in [
    (1, fitz.Rect(40, 40, 572, 245), 'Page 2 Fig 1'),
    (2, fitz.Rect(40, 40, 572, 235), 'Page 3 Fig 2'),
    (3, fitz.Rect(40, 40, 572, 245), 'Page 4 Fig 3'),
    (4, fitz.Rect(40, 40, 572, 275), 'Page 5 Figs 4 & 5')
]:
    page = doc[pno]
    words = page.get_text('words', clip=r_clip)
    rects = [fitz.Rect(w[:4]) for w in words]
    collisions = 0
    for a in range(len(rects)):
        for b in range(a + 1, len(rects)):
            r_int = rects[a] & rects[b]
            if not r_int.is_empty and r_int.width > 0.5 and r_int.height > 0.5:
                collisions += 1
                w1 = words[a][4].encode('ascii', errors='replace').decode()
                w2 = words[b][4].encode('ascii', errors='replace').decode()
                print(f'[{figname}] Collision between "{w1}" and "{w2}": {r_int}')
    print(f'{figname}: {len(words)} words, {collisions} text collisions')
