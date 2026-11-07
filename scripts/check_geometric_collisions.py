import fitz

targets = [
    ('paper/fig1_system_architecture.pdf', 'Fig 1'),
    ('paper/fig2_fsm_diagram.pdf', 'Fig 2'),
    ('paper/fig3_selective_defense.pdf', 'Fig 3')
]

for pdf, label in targets:
    doc = fitz.open(pdf)
    page = doc[0]
    drawings = page.get_drawings()
    rect_paths = [d['rect'] for d in drawings if d.get('fill') is not None or d.get('color') is not None]
    words = page.get_text('words')
    
    tight = 0
    for w in words:
        w_rect = fitz.Rect(w[:4])
        for r in rect_paths:
            if r.contains(w_rect):
                margin = min(w_rect.x0 - r.x0, r.x1 - w_rect.x1, w_rect.y0 - r.y0, r.y1 - w_rect.y1)
                if margin < 1.0:
                    tight += 1
                    w_txt = w[4].encode('ascii', errors='replace').decode()
                    print(f'[{label}] Tight margin ({margin:.2f} pt) for word "{w_txt}" inside rect {r}')
    print(f'[{label}] Checked {len(words)} words across {len(rect_paths)} vector shapes. Tight margins (<1.0 pt): {tight}')
