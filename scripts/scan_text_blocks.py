import pymupdf
import sys
sys.stdout.reconfigure(encoding='utf-8')

figures = ['system_architecture', 'fsm_diagram', 'defense_architecture', 'fig_iki_distribution', 'fig_detection_latency']

for name in figures:
    p = pymupdf.open(f'C:/Users/Ram/Desktop/BadUSB_Using_ESP32/paper/{name}.pdf')[0]
    print(f'=== {name} ===')
    for b in p.get_text('blocks'):
        txt = b[4].strip().replace('\n', ' ')
        non_ascii = [f"U+{ord(c):04X}('{c}')" for c in txt if ord(c) > 127]
        if non_ascii:
            print(f"  [{b[0]:.1f}, {b[1]:.1f}, {b[2]:.1f}, {b[3]:.1f}] Non-ASCII: {non_ascii} in '{txt}'")
        if '\ufffd' in txt:
            print(f"  *** REPLACEMENT CHAR (BAD ENCODING) in '{txt}' ***")
