# ESP32-S3 Hardware Setup & Firmware Flashing Guide

This guide details the physical hardware setup, toolchain requirements, compilation commands, and flashing procedure for the **ESP32-S3 BadUSB Remote Control Platform**.

---

## 1. Board & Hardware Identification

### Physical Ports on the ESP32-S3 DevKit
Most ESP32-S3 DevKit boards (such as the `ESP32-S3-DevKitC-1`) feature **TWO Type-C USB ports**:

| Port Label | Internal Chip Connection | Purpose in this Project |
| :--- | :--- | :--- |
| **COM / UART** | CP2102 or CH340 USB-to-UART bridge | Used for **firmware flashing** and Serial Monitor debugging (e.g. `COM5`). |
| **USB / OTG** | Direct on-chip ESP32-S3 USB peripheral (GPIO 19/20) | Used for the **BadUSB attack vector** (enumerates as a native USB HID keyboard). |

> [!IMPORTANT]
> To flash the device, plug your USB cable into the **UART / COM** port.
> When demonstrating the BadUSB attack, plug your USB cable into the **USB / OTG** port. During development, you can connect both simultaneously with two cables.

### Physical Buttons
- **BOOT Button (GPIO 0)**: Used in this project to cycle through educational payloads (`1 -> 2 -> 3 -> 4`). Also used during power-on to enter ROM download mode if the board fails to respond.
- **RST / EN Button**: Resets the ESP32-S3 microcontroller.

---

## 2. Toolchain Prerequisites

### Arduino IDE 2.x or Arduino CLI
- **Installed Core**: `esp32` by Espressif Systems (version `2.0.17` or `3.x`).
- **Target Board FQBN**: `esp32:esp32:esp32s3`
- **Critical Board Option**: `USBMode=default` (Enables native USB-OTG TinyUSB stack).

### Arduino CLI Executable Location
On this machine, the bundled CLI is located at:
```
C:\Users\Ram\AppData\Local\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe
```

---

## 3. Firmware Build Procedure

### Option A: Using Arduino CLI (Terminal)
Open PowerShell in the project directory:

```powershell
arduino-cli compile `
  --fqbn esp32:esp32:esp32s3:CDCOnBoot=cdc,USBMode=hwcdc `
  "badusb_firmware"
```

Expected output:
```text
Sketch uses 844581 bytes (64%) of program storage space. Maximum is 1310720 bytes.
Global variables use 59304 bytes (18%) of dynamic memory.
```

### Flashing Firmware:
```powershell
arduino-cli upload -p COM5 `
  --fqbn esp32:esp32:esp32s3:CDCOnBoot=cdc,USBMode=hwcdc `
  "badusb_firmware"
```

### Option B: Using Arduino IDE GUI
1. Launch Arduino IDE.
2. Open file: `badusb_firmware/badusb_firmware.ino` (or from your Arduino sketchbook at `Documents/Arduino/badusb_firmware`).
3. Under **Tools** menu, configure:
   - **Board**: `ESP32S3 Dev Module`
   - **USB Mode**: `USB-OTG (TinyUSB)` *(Crucial: do not leave on Hardware CDC)*
   - **USB CDC On Boot**: `Disabled` (or `Enabled` if you wish to see logs on the OTG port)
   - **Upload Speed**: `921600`
   - **Port**: Select your detected COM port (e.g. `COM5`)
4. Click the **Verify** (Checkmark) button.

---

## 4. Manual Flashing Procedure

> [!NOTE]
> Per project safety guidelines, automatic flashing is not performed. Execute the manual command below when you are ready to write to the physical microcontroller.

### Uploading via Arduino CLI
Run the following command while the ESP32-S3 is plugged into `COM5`:

```powershell
& "C:\Users\Ram\AppData\Local\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe" upload `
  -p COM5 `
  --fqbn esp32:esp32:esp32s3:USBMode=default `
  "c:\Users\Ram\Desktop\BadUSB_Using_ESP32\badusb_firmware"
```

### Uploading via esptool.py Directly
If you prefer raw `esptool.exe`:
```powershell
& "C:\Users\Ram\AppData\Local\Arduino15\packages\esp32\tools\esptool_py\4.5.1\esptool.exe" `
  --chip esp32s3 `
  --port COM5 `
  --baud 921600 `
  write_flash -z 0x10000 "c:\Users\Ram\Desktop\BadUSB_Using_ESP32\badusb_firmware\build\badusb_firmware.ino.bin"
```

---

## 5. Troubleshooting & Recovery

### 1. Board Not Responding to Flash Commands (`A fatal error occurred: Failed to connect`)
- **Fix**: Force the ESP32-S3 into ROM Bootloader Mode:
  1. Hold down the physical **BOOT** button.
  2. Press and release the physical **RST / EN** button once.
  3. Release the **BOOT** button.
  4. Re-run the flash command.

### 2. Laptop Does Not Recognize USB Keyboard on Native Port
- Check that the USB cable supports **data lines** (some cheap cables are power-only charging cables).
- Ensure the cable is plugged into the port labelled **USB** (not UART).
- Inspect Windows Device Manager under `Keyboards` for `"HID Keyboard Device"` (Hardware ID `VID_303A&PID_0002` or `TinyUSB BadUSB Demo`).

### 3. Keystrokes Not Typing in Applications
- BadUSB devices send blind keystrokes to whichever window has active focus on the host OS.
- Click inside an open Notepad window or terminal to ensure it has input focus.
