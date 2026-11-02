import subprocess
import fitz

def check_collisions(pdf_path):
    doc = fitz.open(pdf_path)
    p = doc[0]
    words = p.get_text('words')
    overlaps = []
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            w1, w2 = words[i], words[j]
            r1 = fitz.Rect(w1[:4])
            r2 = fitz.Rect(w2[:4])
            intersect = r1.intersect(r2)
            if not intersect.is_empty and intersect.width > 0.5 and intersect.height > 0.5:
                overlaps.append((w1[4], w2[4], intersect))
    return overlaps

print("Testing Fig 2...")
