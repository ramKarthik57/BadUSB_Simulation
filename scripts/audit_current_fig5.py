import fitz

doc = fitz.open('paper/fig_detection_latency.pdf')
page = doc[0]
print('Page rect:', page.rect)
blocks = page.get_text('blocks')
for b in blocks:
    txt = b[4].strip().replace('\n', ' ').encode('ascii', errors='replace').decode()
    print(f'({b[0]:.1f}, {b[1]:.1f}, {b[2]:.1f}, {b[3]:.1f}): {repr(txt)}')

drawings = page.get_drawings()
print(f'Total drawings: {len(drawings)}')
for d in drawings:
    if d.get('fill') is not None or d.get('color') is not None:
        r = d['rect']
        if r.width > 50 and r.height > 20:
            print(f'Large rect: {r}, fill={d.get("fill")}, color={d.get("color")}')
