import os
from PIL import Image

p1 = 'C:/Users/Ram/Desktop/BadUSB_Using_ESP32/paper/system_architecture.png'
p2 = 'C:/Users/Ram/Desktop/BadUSB_Using_ESP32/paper/fsm_diagram.png'
p5 = 'C:/Users/Ram/Desktop/BadUSB_Using_ESP32/paper/fig_detection_latency.png'
p5_pdf = 'C:/Users/Ram/Desktop/BadUSB_Using_ESP32/paper/fig_detection_latency.pdf'

for p in [p1, p2, p5, p5_pdf]:
    if os.path.exists(p):
        if p.endswith('.png'):
            im = Image.open(p)
            print(f'{os.path.basename(p)}: size={im.size}, mode={im.mode}')
        else:
            print(f'{os.path.basename(p)}: bytes={os.path.getsize(p)}')
    else:
        print(f'MISSING: {p}')
