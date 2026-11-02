#include "web_server_handler.h"
#include <WiFi.h>

WebServerHandler WebHandler;

WebServerHandler::WebServerHandler() : server(HTTP_PORT) {
    strncpy(currentPin, DEFAULT_AUTH_PIN, sizeof(currentPin) - 1);
    currentPin[sizeof(currentPin) - 1] = '\0';
}

void WebServerHandler::begin() {
    // Collect custom headers
    const char* headerKeys[] = {"X-Auth-Token"};
    server.collectHeaders(headerKeys, 1);

    // Setup routes
    server.on("/", HTTP_GET, [this]() { handleRoot(); });
    server.on("/api/status", HTTP_GET, [this]() { handleStatus(); });
    server.on("/api/auth/login", HTTP_POST, [this]() { handleAuthLogin(); });

    server.on("/api/scenario/select", HTTP_POST, [this]() { handleScenarioSelect(); });
    server.on("/api/scenario/next", HTTP_POST, [this]() { handleScenarioNext(); });
    server.on("/api/scenario/stop", HTTP_POST, [this]() { handleScenarioStop(); });

    server.on("/api/keyboard/text", HTTP_POST, [this]() { handleKeyboardText(); });
    server.on("/api/keyboard/key", HTTP_POST, [this]() { handleKeyboardKey(); });
    server.on("/api/keyboard/shortcut", HTTP_POST, [this]() { handleKeyboardShortcut(); });
    server.on("/api/keyboard/release", HTTP_POST, [this]() { handleKeyboardRelease(); });

    server.on("/api/mouse/move", HTTP_POST, [this]() { handleMouseMove(); });
    server.on("/api/mouse/click", HTTP_POST, [this]() { handleMouseClick(); });
    server.on("/api/mouse/press", HTTP_POST, [this]() { handleMousePress(); });
    server.on("/api/mouse/release", HTTP_POST, [this]() { handleMouseRelease(); });
    server.on("/api/mouse/scroll", HTTP_POST, [this]() { handleMouseScroll(); });

    // Stealth / Adversarial Evasion Settings
    server.on("/api/settings/stealth", HTTP_POST, [this]() { handleSettingsStealth(); });
    server.on("/api/settings/stealth", HTTP_OPTIONS, [this]() { handlePreflight(); });

    server.onNotFound([this]() { handleNotFound(); });

    // Enable CORS header
    server.enableCORS(true);
    server.begin();
}

void WebServerHandler::handleClient() {
    server.handleClient();
}

void WebServerHandler::sendJsonResponse(int code, const String& json) {
    server.sendHeader("Access-Control-Allow-Origin", "*");
    server.sendHeader("Cache-Control", "no-cache");
    server.send(code, "application/json", json);
}

void WebServerHandler::sendErrorResponse(int code, const char* errorMsg) {
    String resp = "{\"success\":false,\"error\":\"" + String(errorMsg) + "\"}";
    sendJsonResponse(code, resp);
}

bool WebServerHandler::verifyAuth() {
    // Check header X-Auth-Token
    if (server.hasHeader("X-Auth-Token")) {
        String token = server.header("X-Auth-Token");
        if (token.equals(currentPin)) return true;
    }

    // Check JSON body if header was missing
    if (server.hasArg("plain")) {
        String body = server.arg("plain");
        String pin = extractJsonString(body, "pin");
        if (pin.length() == 0) {
            pin = extractJsonString(body, "token");
        }
        if (pin.equals(currentPin)) return true;
    }

    sendErrorResponse(401, "Unauthorized: Invalid or missing security PIN");
    return false;
}

String WebServerHandler::extractJsonString(const String& body, const char* key) {
    String searchKey = "\"" + String(key) + "\"";
    int keyIdx = body.indexOf(searchKey);
    if (keyIdx < 0) return "";

    int colonIdx = body.indexOf(':', keyIdx + searchKey.length());
    if (colonIdx < 0) return "";

    int startQuote = body.indexOf('\"', colonIdx);
    if (startQuote < 0) return "";

    int endQuote = body.indexOf('\"', startQuote + 1);
    if (endQuote < 0) return "";

    return body.substring(startQuote + 1, endQuote);
}

int WebServerHandler::extractJsonInt(const String& body, const char* key, int defaultVal) {
    String searchKey = "\"" + String(key) + "\"";
    int keyIdx = body.indexOf(searchKey);
    if (keyIdx < 0) return defaultVal;

    int colonIdx = body.indexOf(':', keyIdx + searchKey.length());
    if (colonIdx < 0) return defaultVal;

    int startIdx = colonIdx + 1;
    while (startIdx < (int)body.length() && (body[startIdx] == ' ' || body[startIdx] == '\t')) {
        startIdx++;
    }

    int endIdx = startIdx;
    while (endIdx < (int)body.length() && (isDigit(body[endIdx]) || body[endIdx] == '-')) {
        endIdx++;
    }

    if (startIdx == endIdx) return defaultVal;
    return body.substring(startIdx, endIdx).toInt();
}

void WebServerHandler::handleRoot() {
    server.sendHeader("Content-Encoding", "identity");
    server.send(200, "text/html", INDEX_HTML);
}

void WebServerHandler::handleStatus() {
    String staIp = (WiFi.status() == WL_CONNECTED) ? WiFi.localIP().toString() : "";
    String apIp = WiFi.softAPIP().toString();

    String json = "{";
    json += "\"device\":\"ESP32-S3 BadUSB\",";
    json += "\"version\":\"2.0.0\",";
    json += "\"state\":\"" + String(ScenarioCtrl.getStateString()) + "\",";
    json += "\"current_scenario\":" + String(ScenarioCtrl.getCurrentScenarioId()) + ",";
    json += "\"scenario_name\":\"" + String(ScenarioCtrl.getScenarioName(ScenarioCtrl.getCurrentScenarioId())) + "\",";
    json += "\"usb_ready\":" + String(KeyController.isReady() ? "true" : "false") + ",";
    json += "\"startup_executed\":" + String(ScenarioCtrl.hasStartupExecuted() ? "true" : "false") + ",";
    json += "\"ap_ip\":\"" + apIp + "\",";
    json += "\"sta_ip\":\"" + staIp + "\",";
    json += "\"last_error\":\"" + String(ScenarioCtrl.getLastError()) + "\",";
    json += "\"stealth_enabled\":" + String(KeyController.isStealthEnabled() ? "true" : "false") + ",";
    json += "\"stealth_base_ms\":" + String(KeyController.getStealthBaseMs()) + ",";
    json += "\"stealth_jitter_ms\":" + String(KeyController.getStealthJitterMs());
    json += "}";

    sendJsonResponse(200, json);
}

void WebServerHandler::handleAuthLogin() {
    String body = server.arg("plain");
    String pin = extractJsonString(body, "pin");

    if (pin.equals(currentPin)) {
        String resp = "{\"success\":true,\"token\":\"" + pin + "\"}";
        sendJsonResponse(200, resp);
    } else {
        sendErrorResponse(401, "Invalid PIN");
    }
}

void WebServerHandler::handleScenarioSelect() {
    if (!verifyAuth()) return;

    String body = server.arg("plain");
    int scenarioId = extractJsonInt(body, "id", 0);

    String errorMsg;
    if (ScenarioCtrl.requestScenario(scenarioId, errorMsg)) {
        String resp = "{\"success\":true,\"scenario_id\":" + String(scenarioId) + "}";
        sendJsonResponse(200, resp);
    } else {
        sendErrorResponse(400, errorMsg.c_str());
    }
}

void WebServerHandler::handleScenarioNext() {
    if (!verifyAuth()) return;

    String errorMsg;
    if (ScenarioCtrl.requestNextScenario(errorMsg)) {
        String resp = "{\"success\":true,\"next_id\":" + String(ScenarioCtrl.getCurrentScenarioId()) + "}";
        sendJsonResponse(200, resp);
    } else {
        sendErrorResponse(400, errorMsg.c_str());
    }
}

void WebServerHandler::handleScenarioStop() {
    if (!verifyAuth()) return;

    String errorMsg;
    ScenarioCtrl.requestStop(errorMsg);
    sendJsonResponse(200, "{\"success\":true,\"message\":\"Stopped successfully\"}");
}

void WebServerHandler::handleKeyboardText() {
    if (!verifyAuth()) return;

    String body = server.arg("plain");
    String text = extractJsonString(body, "text");

    if (text.length() == 0) {
        sendErrorResponse(400, "Text payload cannot be empty");
        return;
    }

    String errorMsg;
    if (ScenarioCtrl.requestSendText(text.c_str(), errorMsg)) {
        sendJsonResponse(200, "{\"success\":true,\"bytes_sent\":" + String(text.length()) + "}");
    } else {
        sendErrorResponse(400, errorMsg.c_str());
    }
}

void WebServerHandler::handleKeyboardKey() {
    if (!verifyAuth()) return;

    String body = server.arg("plain");
    String keyName = extractJsonString(body, "key");

    if (keyName.length() == 0) {
        sendErrorResponse(400, "Key name cannot be empty");
        return;
    }

    String errorMsg;
    if (ScenarioCtrl.requestSendKey(keyName.c_str(), errorMsg)) {
        sendJsonResponse(200, "{\"success\":true,\"key\":\"" + keyName + "\"}");
    } else {
        sendErrorResponse(400, errorMsg.c_str());
    }
}

void WebServerHandler::handleKeyboardShortcut() {
    if (!verifyAuth()) return;

    String body = server.arg("plain");
    String modStr = extractJsonString(body, "modifiers");
    String keyName = extractJsonString(body, "key");

    if (keyName.length() == 0 && modStr.length() == 0) {
        sendErrorResponse(400, "Shortcut key or modifier cannot be empty");
        return;
    }

    uint8_t modMask = KeyboardController::parseModifiers(modStr.c_str());
    String errorMsg;
    if (ScenarioCtrl.requestSendShortcut(modMask, keyName.c_str(), errorMsg)) {
        sendJsonResponse(200, "{\"success\":true,\"modifiers\":\"" + modStr + "\",\"key\":\"" + keyName + "\"}");
    } else {
        sendErrorResponse(400, errorMsg.c_str());
    }
}

void WebServerHandler::handleKeyboardRelease() {
    if (!verifyAuth()) return;

    KeyController.releaseAll();
    sendJsonResponse(200, "{\"success\":true,\"message\":\"All keys released\"}");
}

void WebServerHandler::handleMouseMove() {
    if (!verifyAuth()) return;

    String body = server.arg("plain");
    int x = extractJsonInt(body, "x", 0);
    int y = extractJsonInt(body, "y", 0);
    int wheel = extractJsonInt(body, "wheel", 0);

    if (x < -127) x = -127;
    if (x > 127) x = 127;
    if (y < -127) y = -127;
    if (y > 127) y = 127;
    if (wheel < -127) wheel = -127;
    if (wheel > 127) wheel = 127;

    MouseCtrl.move((int8_t)x, (int8_t)y, (int8_t)wheel);
    sendJsonResponse(200, "{\"success\":true,\"x\":" + String(x) + ",\"y\":" + String(y) + "}");
}

void WebServerHandler::handleMouseClick() {
    if (!verifyAuth()) return;

    String body = server.arg("plain");
    String btnStr = extractJsonString(body, "button");
    if (btnStr.length() == 0) btnStr = "left";

    btnStr.toLowerCase();
    if (btnStr == "double") {
        MouseCtrl.doubleClick(MOUSE_LEFT);
    } else {
        uint8_t btn = MouseController::parseButton(btnStr.c_str());
        MouseCtrl.click(btn);
    }

    sendJsonResponse(200, "{\"success\":true,\"button\":\"" + btnStr + "\"}");
}

void WebServerHandler::handleMousePress() {
    if (!verifyAuth()) return;

    String body = server.arg("plain");
    String btnStr = extractJsonString(body, "button");
    uint8_t btn = MouseController::parseButton(btnStr.c_str());

    MouseCtrl.press(btn);
    sendJsonResponse(200, "{\"success\":true,\"pressed\":\"" + btnStr + "\"}");
}

void WebServerHandler::handleMouseRelease() {
    if (!verifyAuth()) return;

    String body = server.arg("plain");
    String btnStr = extractJsonString(body, "button");
    btnStr.toLowerCase();

    if (btnStr == "all" || btnStr.length() == 0) {
        MouseCtrl.releaseAll();
    } else {
        uint8_t btn = MouseController::parseButton(btnStr.c_str());
        MouseCtrl.release(btn);
    }

    sendJsonResponse(200, "{\"success\":true,\"released\":\"" + btnStr + "\"}");
}

void WebServerHandler::handleMouseScroll() {
    if (!verifyAuth()) return;

    String body = server.arg("plain");
    int wheel = extractJsonInt(body, "wheel", 0);
    if (wheel < -127) wheel = -127;
    if (wheel > 127) wheel = 127;

    MouseCtrl.move(0, 0, (int8_t)wheel);
    sendJsonResponse(200, "{\"success\":true,\"wheel\":" + String(wheel) + "}");
}

void WebServerHandler::handlePreflight() {
    server.sendHeader("Access-Control-Allow-Origin", "*");
    server.sendHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS");
    server.sendHeader("Access-Control-Allow-Headers", "Content-Type, X-Auth-Token");
    server.send(204);
}

void WebServerHandler::handleSettingsStealth() {
    if (!verifyAuth()) return;

    String body = server.arg("plain");
    bool enabled = false;
    if (body.indexOf("\"enabled\":true") >= 0 || body.indexOf("\"enabled\": 1") >= 0 || body.indexOf("\"enabled\":true") >= 0 || server.arg("enabled") == "1" || server.arg("enabled") == "true") {
        enabled = true;
    }

    int baseMs = extractJsonInt(body, "baseMs", 80);
    int jitterMs = extractJsonInt(body, "jitterMs", 40);
    if (server.hasArg("baseMs")) baseMs = server.arg("baseMs").toInt();
    if (server.hasArg("jitterMs")) jitterMs = server.arg("jitterMs").toInt();

    KeyController.setStealthMode(enabled, baseMs, jitterMs);

    String resp = "{";
    resp += "\"success\":true,";
    resp += "\"stealth_enabled\":" + String(enabled ? "true" : "false") + ",";
    resp += "\"stealth_base_ms\":" + String(KeyController.getStealthBaseMs()) + ",";
    resp += "\"stealth_jitter_ms\":" + String(KeyController.getStealthJitterMs());
    resp += "}";
    sendJsonResponse(200, resp);
}

void WebServerHandler::handleNotFound() {
    if (server.method() == HTTP_OPTIONS) {
        server.sendHeader("Access-Control-Allow-Origin", "*");
        server.sendHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
        server.sendHeader("Access-Control-Allow-Headers", "Content-Type, X-Auth-Token");
        server.send(204);
        return;
    }
    server.send(404, "application/json", "{\"error\":\"Not Found\"}");
}
