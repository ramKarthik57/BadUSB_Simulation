#pragma once

#include <Arduino.h>
#include "USB.h"
#include "USBHIDKeyboard.h"
#include "config.h"

// Modifier bitmask flags
enum ModifierMask {
    MOD_NONE  = 0x00,
    MOD_CTRL  = 0x01,
    MOD_SHIFT = 0x02,
    MOD_ALT   = 0x04,
    MOD_GUI   = 0x08
};

class KeyboardController {
public:
    KeyboardController();

    // Initialization & lifecycle
    bool begin();
    bool isReady() const;
    void releaseAll();

    // Text transmission with cancellation check
    bool sendText(const char* text, volatile bool* cancelFlag = nullptr);

    // Special key transmission
    bool sendKey(const char* keyName, volatile bool* cancelFlag = nullptr);

    // Modifier + key combination
    bool sendShortcut(uint8_t modifiers, const char* keyName, volatile bool* cancelFlag = nullptr);

    // Helper utilities
    static uint8_t parseModifiers(const char* modStr);
    static uint8_t getSpecialKeyCode(const char* keyName, bool& isPrintable, char& printableChar);

    // Low level Windows Run dialog helper (Win + R)
    bool openWindowsRun(volatile bool* cancelFlag = nullptr);

    // Stealth / Adversarial Evasion configuration (Human Cadence Emulation)
    void setStealthMode(bool enabled, unsigned int baseMs = 80, unsigned int jitterMs = 40);
    bool isStealthEnabled() const;
    unsigned int getStealthBaseMs() const;
    unsigned int getStealthJitterMs() const;
    bool typeStringWithJitter(const String& text, unsigned int baseDelayMs, unsigned int jitterRangeMs, volatile bool* cancelFlag = nullptr);

private:
    USBHIDKeyboard keyboard;
    bool usbInitialized;
    unsigned long lastActionTime;

    // Evasion / Stealth mode variables
    bool stealthModeEnabled;
    unsigned int stealthBaseDelayMs;
    unsigned int stealthJitterMs;

    void safeDelay(unsigned long ms, volatile bool* cancelFlag);
};

extern KeyboardController KeyController;
