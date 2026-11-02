from PIL import Image

im = Image.open(r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\fsm_diagram.png")
# Let's crop the bottom area between STATE_STOPPED and STATE_STOPPING, and save it
crop1 = im.crop((1600, 480, 3100, 750))
crop1.save(r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32\paper\debug_fsm_arrows.png")
print("Saved debug_fsm_arrows.png")
