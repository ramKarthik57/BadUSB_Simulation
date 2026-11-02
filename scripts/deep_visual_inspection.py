import os
import fitz

BASE_DIR = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32"
PAPER_DIR = os.path.join(BASE_DIR, "paper")

figures = [
    ("Figure 1", os.path.join(PAPER_DIR, "system_architecture.pdf")),
    ("Figure 2", os.path.join(PAPER_DIR, "fsm_diagram.pdf")),
    ("Figure 3", os.path.join(PAPER_DIR, "defense_architecture.pdf")),
    ("Figure 4", os.path.join(PAPER_DIR, "fig_iki_distribution.pdf")),
    ("Figure 5", os.path.join(PAPER_DIR, "fig_detection_latency.pdf")),
]

for name, path in figures:
    doc = fitz.open(path)
    page = doc[0]
    words = page.get_text("words")  # (x0, y0, x1, y1, word, block_no, line_no, word_no)
    drawings = page.get_drawings()
    
    print(f"\n=======================================================")
    print(f"DEEP AUDIT FOR: {name}")
    print(f"Canvas: {page.rect}")
    print(f"=======================================================")
    
    # 1. Check text-to-text collisions
    text_boxes = [fitz.Rect(w[:4]) for w in words]
    word_strings = [w[4] for w in words]
    
    n_words = len(words)
    text_collisions = []
    for i in range(n_words):
        for j in range(i + 1, n_words):
            # Same line words usually don't overlap, check if intersect
            r1 = text_boxes[i]
            r2 = text_boxes[j]
            # Intersect with positive area
            inter = r1 & r2
            if not inter.is_empty and inter.width > 0.5 and inter.height > 0.5:
                text_collisions.append((word_strings[i], word_strings[j], inter))
                
    if text_collisions:
        print(f"  [!] TEXT COLLISIONS ({len(text_collisions)}):")
        for w1, w2, inter in text_collisions:
            print(f"      '{w1}' overlaps '{w2}' at {inter}")
    else:
        print("  [OK] Zero text-text collisions.")
        
    # 2. Check lines striking through text (excluding background fill rects)
    # Filter drawing paths that are lines or thin rects (stroke width or thin dimension)
    lines_and_strokes = []
    for d in drawings:
        # Check items in drawing
        for item in d["items"]:
            if item[0] == "l":  # line: ('l', p1, p2)
                p1, p2 = item[1], item[2]
                lines_and_strokes.append((p1, p2, d.get("color", None)))
            elif item[0] == "re":  # rect
                r = item[1]
                # If it's a thin stroke border rather than a filled container
                if d.get("fill") is None and d.get("color") is not None:
                    # 4 edges of rect
                    p1 = fitz.Point(r.x0, r.y0)
                    p2 = fitz.Point(r.x1, r.y0)
                    p3 = fitz.Point(r.x1, r.y1)
                    p4 = fitz.Point(r.x0, r.y1)
                    lines_and_strokes.extend([(p1, p2, d["color"]), (p2, p3, d["color"]),
                                              (p3, p4, d["color"]), (p4, p1, d["color"])])
                    
    # Check if any line passes through a word box (with margin)
    line_strikes = []
    for p1, p2, color in lines_and_strokes:
        line_rect = fitz.Rect(min(p1.x, p2.x), min(p1.y, p2.y), max(p1.x, p2.x), max(p1.y, p2.y))
        for i, w in enumerate(words):
            wr = fitz.Rect(w[:4])
            # If line bounding box intersects word with depth > 2 pt
            inter = line_rect & wr
            if inter.width > 3.0 and inter.height > 3.0:
                line_strikes.append((w[4], wr, (p1, p2)))
                
    if line_strikes:
        print(f"  [!] POTENTIAL LINE STRIKES THROUGH TEXT ({len(line_strikes)}):")
        for w, wr, pts in line_strikes[:10]:
            print(f"      Word '{w}' at {wr} intersected by line {pts}")
    else:
        print("  [OK] Zero line strikes through text.")

    # 3. Check out of bounds
    oob = []
    for w in words:
        wr = fitz.Rect(w[:4])
        if not page.rect.contains(wr):
            oob.append((w[4], wr))
    if oob:
        print(f"  [!] OUT OF BOUNDS ({len(oob)}):")
        for w, wr in oob:
            print(f"      Word '{w}' at {wr} outside {page.rect}")
    else:
        print("  [OK] Zero words out of bounds.")
