import os
import pymupdf

BASE_DIR = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32"
FIG_FINAL = os.path.join(BASE_DIR, "figures", "final")
PAPER_DIR = os.path.join(BASE_DIR, "paper")

figures = [
    ("Figure 1 (System Architecture)", os.path.join(FIG_FINAL, "fig1_system_architecture.pdf")),
    ("Figure 2 (Adversarial FSM)", os.path.join(FIG_FINAL, "fig2_scenario_fsm.pdf")),
    ("Figure 3 (Selective Defense)", os.path.join(FIG_FINAL, "fig3_selective_defense.pdf")),
    ("Figure 4 (IKI Distribution)", os.path.join(FIG_FINAL, "fig4_iki_distribution.pdf")),
    ("Figure 5 (Detection Latency)", os.path.join(FIG_FINAL, "fig5_detection_latency.pdf")),
]

print("=== IN-DEPTH COLLISION & BOUNDS AUDIT ===")

total_collisions = 0
total_oob = 0

for name, path in figures:
    if not os.path.exists(path):
        print(f"[MISSING] {name} at {path}")
        continue
    
    doc = pymupdf.open(path)
    page = doc[0]
    rect = page.rect
    words = page.get_text("words")
    blocks = page.get_text("blocks")
    
    # Check out-of-bounds words
    oob_words = []
    for w in words:
        x0, y0, x1, y1, text, bno, lno, wno = w
        if x0 < 0 or y0 < 0 or x1 > rect.width + 1.0 or y1 > rect.height + 1.0:
            oob_words.append((text, (x0, y0, x1, y1)))
    
    # Check pairwise word collisions
    collisions = []
    for i in range(len(words)):
        x0_i, y0_i, x1_i, y1_i, text_i, b_i, l_i, w_i = words[i]
        for j in range(i + 1, len(words)):
            x0_j, y0_j, x1_j, y1_j, text_j, b_j, l_j, w_j = words[j]
            
            # If in the same block and same line, they are normal consecutive words
            if b_i == b_j and l_i == l_j:
                continue
            
            # Intersection rectangle
            ix0 = max(x0_i, x0_j)
            iy0 = max(y0_i, y0_j)
            ix1 = min(x1_i, x1_j)
            iy1 = min(y1_i, y1_j)
            
            if ix1 > ix0 + 1.0 and iy1 > iy0 + 1.0:
                collisions.append((text_i, text_j, (ix1 - ix0) * (iy1 - iy0)))
    
    total_collisions += len(collisions)
    total_oob += len(oob_words)
    
    status = "FLAWLESS" if len(collisions) == 0 and len(oob_words) == 0 else "DEFECTS DETECTED"
    print(f"\n{name}: {status}")
    print(f"  Canvas Dimensions: {rect.width:.1f} x {rect.height:.1f} pt")
    print(f"  Words: {len(words)}, Blocks: {len(blocks)}")
    print(f"  Out of bounds: {len(oob_words)}")
    if oob_words:
        for t, b in oob_words[:5]:
            print(f"    - '{t}' at {b}")
    print(f"  Word collisions: {len(collisions)}")
    if collisions:
        for t1, t2, a in collisions[:5]:
            print(f"    - '{t1}' x '{t2}' (overlap area: {a:.2f})")

print(f"\nTOTAL OVERALL: {total_collisions} collisions, {total_oob} out-of-bounds across all figures.")
