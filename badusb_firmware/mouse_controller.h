#pragma once

#include <Arduino.h>
#include "USBHIDMouse.h"

class MouseController {
public:
    MouseController();

    bool begin();
    bool isReady() const;

    void move(int8_t x, int8_t y, int8_t wheel = 0);
    void click(uint8_t button = MOUSE_LEFT);
    void doubleClick(uint8_t button = MOUSE_LEFT);
    void press(uint8_t button = MOUSE_LEFT);
    void release(uint8_t button = MOUSE_LEFT);
    void releaseAll();
    bool isPressed(uint8_t button = MOUSE_LEFT);

    static uint8_t parseButton(const char* btnStr);

private:
    USBHIDMouse mouse;
    bool mouseInitialized;
};

extern MouseController MouseCtrl;
