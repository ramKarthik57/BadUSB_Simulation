#pragma once

#include <Arduino.h>
#include <WebServer.h>
#include "config.h"
#include "scenario_controller.h"
#include "keyboard_controller.h"
#include "mouse_controller.h"
#include "web_assets.h"

class WebServerHandler {
public:
    WebServerHandler();

    void begin();
    void handleClient();

private:
    WebServer server;
    char currentPin[32];

    bool verifyAuth();
    void sendJsonResponse(int code, const String& json);
    void sendErrorResponse(int code, const char* errorMsg);

    // Route handlers
    void handleRoot();
    void handleStatus();
    void handleAuthLogin();
    void handleScenarioSelect();
    void handleScenarioNext();
    void handleScenarioStop();
    void handleKeyboardText();
    void handleKeyboardKey();
    void handleKeyboardShortcut();
    void handleKeyboardRelease();

    // Stealth / Evasion route handler
    void handleSettingsStealth();
    void handlePreflight();

    // Mouse route handlers
    void handleMouseMove();
    void handleMouseClick();
    void handleMousePress();
    void handleMouseRelease();
    void handleMouseScroll();

    void handleNotFound();

    // Helper JSON extractors
    static String extractJsonString(const String& body, const char* key);
    static int extractJsonInt(const String& body, const char* key, int defaultVal = 0);
};

extern WebServerHandler WebHandler;
