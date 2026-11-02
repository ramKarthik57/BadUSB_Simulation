#include "keyboard_controller.h"
#include "mouse_controller.h"

KeyboardController KeyController;

KeyboardController::KeyboardController()
    : usbInitialized(false), lastActionTime(0),
      stealthModeEnabled(false), stealthBaseDelayMs(80), stealthJitterMs(40) {}

bool KeyboardController::begin() {
    USB.manufacturerName(USB_MANUFACTURER);
    USB.productName(USB_PRODUCT);
    USB.serialNumber(USB_SERIAL);
    USB.usbPower(USB_POWER_MA);

    keyboard.begin();
    MouseCtrl.begin();
    USB.begin();

    usbInitialized = true;
    lastActionTime = millis();
    return true;
}

bool KeyboardController::isReady() const {
    return usbInitialized;
}

void KeyboardController::releaseAll() {
    keyboard.releaseAll();
}

void KeyboardController::safeDelay(unsigned long ms, volatile bool* cancelFlag) {
    unsigned long start = millis();
    while ((millis() - start) < ms) {
        if (cancelFlag && *cancelFlag) {
            keyboard.releaseAll();
            break;
        }
        delay(10);
    }
}

bool KeyboardController::openWindowsRun(volatile bool* cancelFlag) {
    if (cancelFlag && *cancelFlag) return false;

    // Use TinyUSB raw code 0xE3 (HID_KEY_GUI_LEFT) so the HID report is immediately transmitted!
    keyboard.pressRaw(0xE3);
    safeDelay(50, cancelFlag);
    keyboard.press('r');
    safeDelay(120, cancelFlag);
    keyboard.releaseAll();

    safeDelay(STEP_PAUSE_MEDIUM_MS, cancelFlag);
    return !(cancelFlag && *cancelFlag);
}

void KeyboardController::setStealthMode(bool enabled, unsigned int baseMs, unsigned int jitterMs) {
    stealthModeEnabled = enabled;
    stealthBaseDelayMs = (baseMs > 0) ? baseMs : 80;
    stealthJitterMs = jitterMs;
}

bool KeyboardController::isStealthEnabled() const {
    return stealthModeEnabled;
}

unsigned int KeyboardController::getStealthBaseMs() const {
    return stealthBaseDelayMs;
}

unsigned int KeyboardController::getStealthJitterMs() const {
    return stealthJitterMs;
}

bool KeyboardController::typeStringWithJitter(const String& text, unsigned int baseDelayMs, unsigned int jitterRangeMs, volatile bool* cancelFlag) {
    if (!usbInitialized) return false;

    size_t len = text.length();
    if (len > MAX_TEXT_PAYLOAD_LEN) {
        len = MAX_TEXT_PAYLOAD_LEN;
    }

    for (size_t i = 0; i < len; ++i) {
        if (cancelFlag && *cancelFlag) {
            keyboard.releaseAll();
            return false;
        }

        char c = text[i];
        if (c == '\r') continue;

        if (c == '\n') {
            keyboard.write(KEY_RETURN);
        } else if (c == '\t') {
            keyboard.write(KEY_TAB);
        } else if ((uint8_t)c >= 32 && (uint8_t)c <= 126) {
            keyboard.write((uint8_t)c);
        } else {
            continue;
        }

        // Randomized inter-key interval: delta_t = baseDelayMs + random(0, jitterRangeMs)
        unsigned int delta = baseDelayMs;
        if (jitterRangeMs > 0) {
            delta += (unsigned int)random(0, jitterRangeMs + 1);
        }
        safeDelay(delta, cancelFlag);

        // Cognitive micro-pauses (150-300 ms) after spaces, punctuation, or newlines
        if (c == ' ' || c == '.' || c == ',' || c == '!' || c == '?' || c == '\n' || c == ';') {
            unsigned int pauseMs = (unsigned int)random(150, 301);
            safeDelay(pauseMs, cancelFlag);
        }
    }

    keyboard.releaseAll();
    lastActionTime = millis();
    return true;
}

bool KeyboardController::sendText(const char* text, volatile bool* cancelFlag) {
    if (!text || !usbInitialized) return false;

    if (stealthModeEnabled) {
        return typeStringWithJitter(String(text), stealthBaseDelayMs, stealthJitterMs, cancelFlag);
    }

    size_t len = strlen(text);
    if (len > MAX_TEXT_PAYLOAD_LEN) {
        len = MAX_TEXT_PAYLOAD_LEN;
    }

    for (size_t i = 0; i < len; ++i) {
        if (cancelFlag && *cancelFlag) {
            keyboard.releaseAll();
            return false;
        }

        char c = text[i];
        if (c == '\r') continue; // Skip carriage return, handle newline

        if (c == '\n') {
            keyboard.write(KEY_RETURN);
        } else if (c == '\t') {
            keyboard.write(KEY_TAB);
        } else if ((uint8_t)c >= 32 && (uint8_t)c <= 126) {
            keyboard.write((uint8_t)c);
        } else {
            // Unsupported/extended character: skip safely without breaking state
            continue;
        }

        safeDelay(KEY_PRESS_DELAY_MS, cancelFlag);
    }

    keyboard.releaseAll();
    lastActionTime = millis();
    return true;
}

uint8_t KeyboardController::getSpecialKeyCode(const char* keyName, bool& isPrintable, char& printableChar) {
    isPrintable = false;
    printableChar = 0;
    if (!keyName || strlen(keyName) == 0) return 0;

    String k = String(keyName);
    k.toUpperCase();
    k.trim();

    if (k == "ENTER" || k == "RETURN") return KEY_RETURN;
    if (k == "BACKSPACE" || k == "BS") return KEY_BACKSPACE;
    if (k == "TAB") return KEY_TAB;
    if (k == "ESCAPE" || k == "ESC") return KEY_ESC;
    if (k == "SPACE") { isPrintable = true; printableChar = ' '; return 0; }
    if (k == "UP" || k == "UP_ARROW") return KEY_UP_ARROW;
    if (k == "DOWN" || k == "DOWN_ARROW") return KEY_DOWN_ARROW;
    if (k == "LEFT" || k == "LEFT_ARROW") return KEY_LEFT_ARROW;
    if (k == "RIGHT" || k == "RIGHT_ARROW") return KEY_RIGHT_ARROW;
    if (k == "DELETE" || k == "DEL") return KEY_DELETE;
    if (k == "INSERT" || k == "INS") return KEY_INSERT;
    if (k == "HOME") return KEY_HOME;
    if (k == "END") return KEY_END;
    if (k == "PAGEUP" || k == "PAGE_UP") return KEY_PAGE_UP;
    if (k == "PAGEDOWN" || k == "PAGE_DOWN") return KEY_PAGE_DOWN;
    if (k == "CAPSLOCK" || k == "CAPS_LOCK") return KEY_CAPS_LOCK;

    // Special keys using TinyUSB scancodes
    if (k == "PRINTSCREEN" || k == "PRTSC" || k == "PRINT_SCREEN") return 0x46; // HID_KEY_PRINT_SCREEN
    if (k == "SCROLLLOCK" || k == "SCROLL_LOCK") return 0x47; // HID_KEY_SCROLL_LOCK
    if (k == "PAUSE" || k == "BREAK") return 0x48; // HID_KEY_PAUSE
    if (k == "MENU" || k == "APP" || k == "APPLICATION") return 0x65; // HID_KEY_APPLICATION

    // Modifier keys as individual triggers
    if (k == "CTRL" || k == "CONTROL" || k == "LCTRL") return KEY_LEFT_CTRL;
    if (k == "ALT" || k == "LALT") return KEY_LEFT_ALT;
    if (k == "SHIFT" || k == "LSHIFT") return KEY_LEFT_SHIFT;
    if (k == "WIN" || k == "GUI" || k == "WINDOWS" || k == "SUPER") return KEY_LEFT_GUI;

    // Function keys
    if (k == "F1") return KEY_F1;
    if (k == "F2") return KEY_F2;
    if (k == "F3") return KEY_F3;
    if (k == "F4") return KEY_F4;
    if (k == "F5") return KEY_F5;
    if (k == "F6") return KEY_F6;
    if (k == "F7") return KEY_F7;
    if (k == "F8") return KEY_F8;
    if (k == "F9") return KEY_F9;
    if (k == "F10") return KEY_F10;
    if (k == "F11") return KEY_F11;
    if (k == "F12") return KEY_F12;

    // Single printable character
    if (k.length() == 1) {
        char ch = keyName[0]; // Preserve original case
        if (ch >= 32 && ch <= 126) {
            isPrintable = true;
            printableChar = ch;
            return 0;
        }
    }

    return 0;
}

uint8_t KeyboardController::parseModifiers(const char* modStr) {
    if (!modStr) return MOD_NONE;
    String s = String(modStr);
    s.toUpperCase();

    uint8_t mask = MOD_NONE;
    if (s.indexOf("CTRL") >= 0 || s.indexOf("CONTROL") >= 0) mask |= MOD_CTRL;
    if (s.indexOf("SHIFT") >= 0) mask |= MOD_SHIFT;
    if (s.indexOf("ALT") >= 0) mask |= MOD_ALT;
    if (s.indexOf("GUI") >= 0 || s.indexOf("WIN") >= 0 || s.indexOf("META") >= 0) mask |= MOD_GUI;
    return mask;
}

bool KeyboardController::sendKey(const char* keyName, volatile bool* cancelFlag) {
    if (cancelFlag && *cancelFlag) return false;

    bool isPrintable = false;
    char printableChar = 0;
    uint8_t code = getSpecialKeyCode(keyName, isPrintable, printableChar);

    if (code != 0) {
        if (code >= 0x80 && code <= 0x87) {
            // Standalone modifier key press (e.g. WIN, CTRL, ALT, SHIFT):
            // In ESP32 Arduino USBHIDKeyboard::press(code), modifier keys (>=0x80) call pressRaw(0)
            // which exits early without calling sendReport().
            // We use TinyUSB raw modifier code (0xE0 + offset) so sendReport() is guaranteed!
            uint8_t rawMod = 0xE0 + (code - 0x80);
            keyboard.pressRaw(rawMod);
            safeDelay(120, cancelFlag);
            keyboard.releaseRaw(rawMod);
            safeDelay(40, cancelFlag);
        } else if (code == 0x46 || code == 0x47 || code == 0x48 || code == 0x65) {
            // Special raw hardware keys: PrintScreen, ScrollLock, Pause, Menu
            keyboard.pressRaw(code);
            safeDelay(80, cancelFlag);
            keyboard.releaseRaw(code);
            safeDelay(30, cancelFlag);
        } else {
            keyboard.press(code);
            safeDelay(70, cancelFlag);
            keyboard.release(code);
            safeDelay(20, cancelFlag);
        }
    } else if (isPrintable) {
        keyboard.write((uint8_t)printableChar);
        safeDelay(20, cancelFlag);
    } else {
        return false; // Unknown key
    }

    keyboard.releaseAll();
    lastActionTime = millis();
    return true;
}

bool KeyboardController::sendShortcut(uint8_t modifiers, const char* keyName, volatile bool* cancelFlag) {
    if (cancelFlag && *cancelFlag) return false;

    // Press modifier keys using pressRaw to guarantee HID reports are sent to host!
    if (modifiers & MOD_CTRL)  keyboard.pressRaw(0xE0); // Left Ctrl
    if (modifiers & MOD_SHIFT) keyboard.pressRaw(0xE1); // Left Shift
    if (modifiers & MOD_ALT)   keyboard.pressRaw(0xE2); // Left Alt
    if (modifiers & MOD_GUI)   keyboard.pressRaw(0xE3); // Left GUI / Windows

    safeDelay(50, cancelFlag);

    // If a key name is provided, press it
    if (keyName && strlen(keyName) > 0) {
        bool isPrintable = false;
        char printableChar = 0;
        uint8_t code = getSpecialKeyCode(keyName, isPrintable, printableChar);

        if (code != 0) {
            if (code >= 0x80 && code <= 0x87) {
                keyboard.pressRaw(0xE0 + (code - 0x80));
            } else if (code == 0x46 || code == 0x47 || code == 0x48 || code == 0x65) {
                keyboard.pressRaw(code);
            } else {
                keyboard.press(code);
            }
            safeDelay(100, cancelFlag);
        } else if (isPrintable) {
            // If Shift is not active, normalize uppercase letter to lowercase
            // to avoid USBHIDKeyboard's asciimap inadvertently adding Shift!
            if (!(modifiers & MOD_SHIFT) && printableChar >= 'A' && printableChar <= 'Z') {
                printableChar = tolower(printableChar);
            }
            keyboard.press((uint8_t)printableChar);
            safeDelay(100, cancelFlag);
        }
    } else {
        // Only modifiers requested (hold duration for tap)
        safeDelay(100, cancelFlag);
    }

    // Always release all keys safely
    keyboard.releaseAll();
    safeDelay(30, cancelFlag);
    lastActionTime = millis();
    return true;
}
