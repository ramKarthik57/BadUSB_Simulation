import fitz

def check_figure_geometry(pdf_path, name):
    doc = fitz.open(pdf_path)
    page = doc[0]
    drawings = page.get_drawings()
    words = page.get_text("words")
    
    print(f"\n=======================================================")
    print(f"GEOMETRY INSPECTION: {name}")
    print(f"Page Rect: {page.rect}")
    print(f"=======================================================")
    
    # Extract filled/stroked paths and their bounding rects
    drawn_rects = []
    lines = []
    for d in drawings:
        r = fitz.Rect(d["rect"])
        # If it's a visible shape (has fill or stroke)
        if d.get("fill") is not None or d.get("color") is not None:
            drawn_rects.append((r, d.get("fill"), d.get("color"), d.get("width", 1.0)))
        for item in d["items"]:
            if item[0] == "l":
                lines.append((item[1], item[2], d.get("color")))
                
    # 1. Check all text against all lines (excluding background fills)
    print(f"Total words: {len(words)}, Total paths: {len(drawings)}, Total line segments: {len(lines)}")
    
    # Check text against drawn boxes
    # Find which box contains which text, and check if text touches box border (padding < 1.5 pt)
    tight_padding = []
    for w in words:
        w_rect = fitz.Rect(w[:4])
        for r, fill, stroke, lw in drawn_rects:
            # Check if text is mostly inside the rect
            if r.contains(w_rect) and r.width < page.rect.width * 0.9:
                # Check distances to all 4 edges of containing rect
                pad_l = w_rect.x0 - r.x0
                pad_r = r.x1 - w_rect.x1
                pad_t = w_rect.y0 - r.y0
                pad_b = r.y1 - w_rect.y1
                min_pad = min(pad_l, pad_r, pad_t, pad_b)
                if min_pad < 1.0:
                    w_safe = w[4].encode('ascii', 'backslashreplace').decode('ascii')
                    tight_padding.append((w_safe, w_rect, r, min_pad))
                    
    if tight_padding:
        print(f"  [!] Tight padding (text touching box border < 1.0 pt) ({len(tight_padding)}):")
        for word, wr, br, pad in tight_padding[:10]:
            print(f"      '{word}' at {wr} is only {pad:.2f} pt from box {br}")
    else:
        print("  [OK] All text has >= 1.0 pt padding from containing box borders.")
        
    # Check for colliding non-nested boxes
    box_overlaps = []
    for i in range(len(drawn_rects)):
        for j in range(i + 1, len(drawn_rects)):
            r1, f1, s1, _ = drawn_rects[i]
            r2, f2, s2, _ = drawn_rects[j]
            # Ignore identical or full-page backgrounds
            if r1 == r2 or r1.contains(r2) or r2.contains(r1):
                continue
            inter = r1 & r2
            if not inter.is_empty and inter.width > 1.0 and inter.height > 1.0:
                box_overlaps.append((r1, r2, inter))
                
    if box_overlaps:
        print(f"  [!] Non-nested box overlaps ({len(box_overlaps)}):")
        for r1, r2, inter in box_overlaps[:10]:
            print(f"      Box {r1} overlaps Box {r2} by area {inter}")
    else:
        print("  [OK] Zero non-nested box collisions.")

check_figure_geometry(r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\system_architecture.pdf", "Fig 1")
check_figure_geometry(r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\fsm_diagram.pdf", "Fig 2")
check_figure_geometry(r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\defense_architecture.pdf", "Fig 3")
check_figure_geometry(r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\fig_iki_distribution.pdf", "Fig 4")
check_figure_geometry(r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\fig_detection_latency.pdf", "Fig 5")
