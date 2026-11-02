from PIL import Image, ImageFont, ImageDraw

S = 2.2
def sc(v): return int(round(v * S))

# Let's inspect Figure 2 (FSM)
f_mono14b = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', sc(14))
f14 = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', sc(14))
f13b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', sc(13))
f12b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', sc(12))

print('=== AUDITING FSM DIAGRAM (FIG 2) ===')
top_states = [
    (30, 95, 265, 235, 'STATE_BOOTING', 'Hardware init, TinyUSB\ndescriptors registered,\npull-up asserted on D+'),
    (325, 95, 595, 235, 'STATE_USB_WAIT', 'Non-blocking 3,500ms\nenumeration guard\n(tau_boot stabilization)'),
    (655, 95, 955, 235, 'STATE_STARTUP_PAYLOAD', 'Auto-executes Scenario 1\n(Notepad awareness)\nonce on initial boot'),
    (1015, 95, 1315, 235, 'STATE_IDLE', 'Steady ready state;\nawaits GPIO 0 press\nor Web API selection'),
    (1375, 95, 1770, 235, 'STATE_RUNNING', 'Executes Scenarios 1-4\nvia smartDelay(10ms)\nwith preemption polling'),
]

for x0, y0, x1, y1, name, desc in top_states:
    w = sc(x1 - x0)
    nw = f_mono14b.getbbox(name)[2] - f_mono14b.getbbox(name)[0]
    if nw > w - sc(10):
        print(f'   OVERFLOW in state title {name}: w={nw} vs box_w={w}')
    for line in desc.split('\n'):
        lw = f14.getbbox(line)[2] - f14.getbbox(line)[0]
        if lw > w - sc(16):
            print(f'   OVERFLOW in {name}: line "{line}" w={lw} vs inner_w={w - sc(16)}')

# Bottom boxes in FSM:
bot_boxes = [
    (30, 310, 560, 550, 'CONCURRENT TRIGGER SOURCES', [
        '• Physical GPIO 0 BOOT Button (50ms debounce, 600ms cooldown)',
        '• Web REST API: POST /api/scenario/select (IDs 1-4) & /api/scenario/next',
        '• FreeRTOS Spinlock Mailbox: portMUX_TYPE guards cmdPending',
        '• Eliminates race conditions between Core 0 (Web) & Core 1 (FSM)',
    ]),
    (655, 310, 1015, 550, 'STATE_STOPPED', [
        '• Entered following safe hardware abort',
        '• Verifies all modifiers & keys released',
        '• Restores clean HID bus state',
        '• Transitions back to STATE_IDLE',
    ]),
    (1085, 310, 1470, 550, 'STATE_STOPPING', [
        '• Triggered by stopRequested = true',
        '• Immediately breaks 10ms delay loop',
        '• Calls Keyboard.releaseAll() & Mouse.releaseAll()',
        '• Clears Ctrl/Alt/Win modifier latches <= 10ms',
    ]),
    (1525, 310, 1770, 550, 'STATE_ERROR', [
        '• Invalid scenario parameter',
        '• USB detachment / timeout',
        '• Auto-recovers to IDLE',
    ]),
]

for x0, y0, x1, y1, name, lines in bot_boxes:
    w = sc(x1 - x0)
    for line in lines:
        lw = f14.getbbox(line)[2] - f14.getbbox(line)[0]
        if lw > w - sc(32):
            print(f'   OVERFLOW in bot box {name}: line "{line}" w={lw} vs inner_w={w - sc(32)}')

# Check FSM arrow labels
labels = [
    ('3.5s', 595, 655, f_mono14b),
    ('Done', 955, 1015, f_mono14b),
    ('Launch', 1315, 1375, f13b),
    ('Finish', 1315, 1375, f13b),
    ('Emergency Abort (stopRequested=true)', 1280, 1560, f13b),
    ('Cleanup Done', 1015, 1085, f12b),
    ('Reset to Ready State', 840, 1160, f13b),
]
for text, x0, x1, f in labels:
    w = sc(x1 - x0)
    lw = f.getbbox(text)[2] - f.getbbox(text)[0]
    if lw > w:
        print(f'   OVERFLOW in arrow label "{text}": w={lw} vs box_w={w}')

print('=== AUDITING SYSTEM ARCHITECTURE (FIG 1) ===')
f18b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', sc(18))
f16b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', sc(16))
f14 = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', sc(14))

# Check widths of all 3 columns
c_widths = [(28, 530), (635, 1180), (1285, 1772)]
for idx, (x0, x1) in enumerate(c_widths):
    w = sc(x1 - x0)
    print(f'Col {idx+1} width: {w} px')

# Check interconnect labels:
# (c1_x1 + 10, 182, c2_x0 - 10, 230)
box1_w = sc(635 - 10 - (530 + 10))
for line in ['2.4GHz Wi-Fi', 'REST API (JSON)']:
    lw = f13b.getbbox(line)[2] - f13b.getbbox(line)[0]
    if lw > box1_w - sc(10):
        print(f'   OVERFLOW in Fig 1 Interconnect 1 "{line}": w={lw} vs box_w={box1_w - sc(10)}')

box2_w = sc(1285 - 10 - (1180 + 10))
for line in ['USB 2.0 Full-Speed', 'GPIO 19/20 (D-/D+)']:
    lw = f13b.getbbox(line)[2] - f13b.getbbox(line)[0]
    if lw > box2_w - sc(10):
        print(f'   OVERFLOW in Fig 1 Interconnect 2 "{line}": w={lw} vs box_w={box2_w - sc(10)}')

box3_w = sc(1285 - 8 - (1180 + 8))
for line in ['Selective Gate:', 'DROPS ESP32']:
    lw = f13b.getbbox(line)[2] - f13b.getbbox(line)[0]
    if lw > box3_w - sc(10):
        print(f'   OVERFLOW in Fig 1 Interconnect 3 "{line}": w={lw} vs box_w={box3_w - sc(10)}')
