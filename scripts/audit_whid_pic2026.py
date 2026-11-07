import fitz
import os

def audit_whid(pdf_path, name):
    print(f"\n==========================================")
    print(f"AUDITING: {name} ({pdf_path})")
    print(f"==========================================")
    doc = fitz.open(pdf_path)
    print(f"Page Count: {len(doc)} pages")
    
    # 1. Font Audit
    has_type3 = False
    all_fonts = []
    for i, page in enumerate(doc):
        fonts = page.get_fonts()
        for f in fonts:
            font_type = f[2]
            font_name = f[3]
            all_fonts.append((font_name, font_type))
            if font_type.lower() == 'type3':
                has_type3 = True
                print(f"  [!] Type 3 font detected on page {i+1}: {font_name}")
    if not has_type3:
        print(f"  [PASS] ZERO Type 3 fonts detected! (Total embedded fonts: {len(set(all_fonts))})")
        
    # 2. Text Collision Audit
    total_collisions = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        words = page.get_text("words")
        collisions = []
        for i in range(len(words)):
            w1 = words[i]
            r1 = fitz.Rect(w1[0], w1[1], w1[2], w1[3])
            for j in range(i + 1, min(i + 30, len(words))):
                w2 = words[j]
                r2 = fitz.Rect(w2[0], w2[1], w2[2], w2[3])
                inter = r1 & r2
                if not inter.is_empty and inter.width > 2.5 and inter.height > 2.5:
                    collisions.append((w1[4], w2[4], inter))
        if collisions:
            print(f"  [!] Page {page_num + 1} has {len(collisions)} collision(s): {collisions[:3]}")
            total_collisions += len(collisions)
        else:
            print(f"  [PASS] Page {page_num + 1}: 0 text collisions")
            
    # 3. Page 6 Column Balance
    p6 = doc[-1]
    blocks = p6.get_text("blocks")
    col1_y1, col2_y1 = 0, 0
    for b in blocks:
        if b[0] < 300:
            col1_y1 = max(col1_y1, b[3])
        else:
            col2_y1 = max(col2_y1, b[3])
    delta = abs(col1_y1 - col2_y1)
    print(f"  Page 6 Column 1 bottom: {col1_y1:.1f} pt, Column 2 bottom: {col2_y1:.1f} pt (Delta: {delta:.1f} pt)")
    if delta < 40:
        print(f"  [PASS] Last page columns are beautifully balanced!")

base_dir = "C:/Users/Ram/Desktop/BadUSB_Using_ESP32/paper/PIC2026"
audit_whid(os.path.join(base_dir, "WHID_GUARD_PIC2026_CAMERA_READY.pdf"), "Camera-Ready")
audit_whid(os.path.join(base_dir, "WHID_GUARD_PIC2026_DOUBLE_BLIND.pdf"), "Double-Blind")
