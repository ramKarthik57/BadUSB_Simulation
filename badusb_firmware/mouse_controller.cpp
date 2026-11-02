#include "mouse_controller.h"

MouseController MouseCtrl;

MouseController::MouseController()
    : mouseInitialized(false) {}

bool MouseController::begin() {
    mouse.begin();
    mouseInitialized = true;
    return true;
}

bool MouseController::isReady() const {
    return mouseInitialized;
}

void MouseController::move(int8_t x, int8_t y, int8_t wheel) {
    mouse.move(x, y, wheel);
}

void MouseController::click(uint8_t button) {
    mouse.click(button);
}

void MouseController::doubleClick(uint8_t button) {
    mouse.click(button);
    delay(50);
    mouse.click(button);
}

void MouseController::press(uint8_t button) {
    mouse.press(button);
}

void MouseController::release(uint8_t button) {
    mouse.release(button);
}

void MouseController::releaseAll() {
    mouse.release(MOUSE_ALL);
}

bool MouseController::isPressed(uint8_t button) {
    return mouse.isPressed(button);
}

uint8_t MouseController::parseButton(const char* btnStr) {
    if (!btnStr) return MOUSE_LEFT;
    String s = String(btnStr);
    s.toUpperCase();
    if (s.indexOf("RIGHT") >= 0) return MOUSE_RIGHT;
    if (s.indexOf("MIDDLE") >= 0) return MOUSE_MIDDLE;
    if (s.indexOf("BACK") >= 0) return MOUSE_BACKWARD;
    if (s.indexOf("FORWARD") >= 0) return MOUSE_FORWARD;
    return MOUSE_LEFT;
}
