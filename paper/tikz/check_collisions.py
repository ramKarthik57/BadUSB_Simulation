import fitz
import sys

def check_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]
    words = page.get_text('words')
    print(f"=== {pdf_path} ===")
    print(f"Total words: {len(words)}")

    overlaps = []
    for i in range(len(words)):
        for j in range(i+1, len(words)):
            w1 = words[i]
            w2 = words[j]
            r1 = fitz.Rect(w1[:4])
            r2 = fitz.Rect(w2[:4])
            inter = r1 & r2
            if not inter.is_empty and inter.width > 1.0 and inter.height > 1.0:
                overlaps.append((w1[4], w2[4], inter.width, inter.height))

    print(f"Total Overlapping Word Pairs: {len(overlaps)}")
    for t1, t2, w, h in overlaps[:20]:
        t1_s = t1.encode('ascii', 'replace').decode('ascii')
        t2_s = t2.encode('ascii', 'replace').decode('ascii')
        print(f"  COLLISION: '{t1_s}' intersects '{t2_s}' ({w:.1f}x{h:.1f} pt)")
    return len(overlaps)

if __name__ == '__main__':
    for path in sys.argv[1:]:
        check_pdf(path)
