import pymupdf

doc = pymupdf.open(r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\WHID_GUARD_2027.pdf")
for pno in range(len(doc)):
    page = doc[pno]
    words = page.get_text('words')
    overlaps = []
    for i in range(len(words)):
        for j in range(i+1, len(words)):
            w1 = words[i]
            w2 = words[j]
            r1 = pymupdf.Rect(w1[:4])
            r2 = pymupdf.Rect(w2[:4])
            inter = r1 & r2
            if not inter.is_empty and inter.width > 1.5 and inter.height > 1.5:
                overlaps.append((w1[4], w2[4], inter.width, inter.height, r1, r2))
    print(f"Page {pno+1}: {len(overlaps)} collisions")
    for t1, t2, w, h, r1, r2 in overlaps:
        t1_s = t1.encode('ascii', 'replace').decode('ascii')
        t2_s = t2.encode('ascii', 'replace').decode('ascii')
        print(f"  P{pno+1}: '{t1_s}' vs '{t2_s}' ({w:.1f}x{h:.1f} pt)")
        print(f"     r1: {r1}")
        print(f"     r2: {r2}")
