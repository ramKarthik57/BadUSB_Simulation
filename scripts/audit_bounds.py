from PIL import ImageFont

S = 2.2
def sc(v): return int(round(v * S))

f_mono14b = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', sc(14))
f14 = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', sc(14))
f13b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', sc(13))
f12b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', sc(12))
f11b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', sc(11))

print('=== AUDITING FSM DIAGRAM (FIG 2) ===')
gap_w = sc(110)
arrow_text = 'Cleanup Complete'
tw = f11b.getbbox(arrow_text)[2] - f11b.getbbox(arrow_text)[0]
print(f'Arrow label "{arrow_text}": text_w={tw} px, gap_w={gap_w} px (margin = {gap_w - tw} px)')

print('\n=== AUDITING SYSTEM ARCHITECTURE (FIG 1) ===')
bus_w = sc(136)
labels1 = ['2.4GHz Wi-Fi', 'REST API (JSON)', 'Station / SoftAP']
for lbl in labels1:
    lw = f12b.getbbox(lbl)[2] - f12b.getbbox(lbl)[0]
    print(f'Interconnect 1 "{lbl}": text_w={lw} px, bus_w={bus_w} px (margin = {bus_w - lw} px)')

labels2 = ['USB 2.0 Full-Speed', 'GPIO 19/20 (D-/D+)', '12 Mbps CDC/HID']
for lbl in labels2:
    lw = f12b.getbbox(lbl)[2] - f12b.getbbox(lbl)[0]
    print(f'Interconnect 2 "{lbl}": text_w={lw} px, bus_w={bus_w} px (margin = {bus_w - lw} px)')

labels3 = ['Selective Gate:', 'DROPS ESP32', 'PASSES Laptop KB']
for lbl in labels3:
    lw = f12b.getbbox(lbl)[2] - f12b.getbbox(lbl)[0]
    print(f'Interconnect 3 "{lbl}": text_w={lw} px, bus_w={bus_w} px (margin = {bus_w - lw} px)')
