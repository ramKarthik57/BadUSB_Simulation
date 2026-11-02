/*
  BadUSB Remote Control Platform for ESP32-S3
  Combines USB HID Keyboard emulation with a Phone Wi-Fi Web Controller.
  Maintains physical BOOT button advancement and automatic startup payload.
*/

#include <Arduino.h>
#include <WiFi.h>
#include <ESPmDNS.h>

#include "config.h"
#include "keyboard_controller.h"
#include "mouse_controller.h"
#include "scenario_controller.h"
#include "web_server_handler.h"

static int lastButtonState = HIGH;
static unsigned long lastButtonPressTime = 0;

static void onWiFiEvent(WiFiEvent_t event) {
    switch (event) {
        case ARDUINO_EVENT_WIFI_STA_GOT_IP:
            Serial.printf("[BadUSB] *** CONNECTED TO HOTSPOT! IP: %s ***\n", WiFi.localIP().toString().c_str());
            break;
        case ARDUINO_EVENT_WIFI_STA_DISCONNECTED:
            Serial.println("[BadUSB] Wi-Fi STA disconnected from hotspot");
            break;
        default:
            break;
    }
}

void setup() {
    Serial.begin(115200);
    delay(100);
    Serial.println("\n[BadUSB] System starting up...");

    // 1. Configure Hardware BOOT button
    pinMode(PIN_BOOT_BUTTON, INPUT_PULLUP);

    // 2. Initialize USB HID Keyboard Stack
    Serial.println("[BadUSB] Initializing Native USB HID Keyboard...");
    KeyController.begin();
    ScenarioCtrl.begin();

    // 3. Initialize Wi-Fi in Dual Mode (AP + Station for phone hotspot)
    Serial.println("[BadUSB] Initializing Wi-Fi dual mode (AP + STA)...");
    WiFi.onEvent(onWiFiEvent);
    WiFi.mode(WIFI_AP_STA);

    // Start SoftAP (standalone controller network)
    bool apStarted = WiFi.softAP(DEFAULT_AP_SSID, DEFAULT_AP_PASS, DEFAULT_AP_CHANNEL);
    if (apStarted) {
        Serial.printf("[BadUSB] SoftAP started: %s (Password: %s)\n", DEFAULT_AP_SSID, DEFAULT_AP_PASS);
        Serial.print("[BadUSB] SoftAP IP: ");
        Serial.println(WiFi.softAPIP());
    } else {
        Serial.println("[BadUSB] SoftAP startup failed (will continue USB/STA)");
    }

    // Connect to phone's Wi-Fi hotspot in background
    Serial.printf("[BadUSB] Connecting to Hotspot SSID: %s ...\n", DEFAULT_STA_SSID);
    WiFi.begin(DEFAULT_STA_SSID, DEFAULT_STA_PASS);

    // 4. Start mDNS responder (http://badusb.local)
    if (MDNS.begin(MDNS_HOSTNAME)) {
        MDNS.addService("http", "tcp", HTTP_PORT);
        Serial.printf("[BadUSB] mDNS active: http://%s.local\n", MDNS_HOSTNAME);
    }

    // 5. Start Local Web Server
    WebHandler.begin();
    Serial.println("[BadUSB] Web controller listening on port 80");
    Serial.println("[BadUSB] Initialization complete.\n");
}

void loop() {
    // 1. Service Local Web Server requests
    WebHandler.handleClient();

    // 2. Service Scenario State Machine
    ScenarioCtrl.update();

    // 3. Physical BOOT Button Edge Detection (GPIO 0)
    int currentButtonState = digitalRead(PIN_BOOT_BUTTON);
    if (lastButtonState == HIGH && currentButtonState == LOW) {
        // Falling edge detected (button pressed)
        unsigned long now = millis();
        if ((now - lastButtonPressTime) > BUTTON_HOLD_COOLDOWN_MS) {
            lastButtonPressTime = now;
            Serial.println("[BadUSB] Physical BOOT button pressed -> Advancing scenario");

            String errorMsg;
            if (!ScenarioCtrl.requestNextScenario(errorMsg)) {
                Serial.printf("[BadUSB] Button command rejected: %s\n", errorMsg.c_str());
            }
        }
    }
    lastButtonState = currentButtonState;

    // Small yield to FreeRTOS scheduler
    delay(5);
}
