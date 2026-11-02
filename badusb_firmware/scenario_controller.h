#pragma once

#include <Arduino.h>
#include "keyboard_controller.h"
#include "config.h"

enum ControllerState {
    STATE_BOOTING = 0,
    STATE_USB_WAIT,
    STATE_STARTUP_PAYLOAD,
    STATE_IDLE,
    STATE_RUNNING,
    STATE_STOPPING,
    STATE_STOPPED,
    STATE_ERROR
};

enum CommandType {
    CMD_NONE = 0,
    CMD_START_SCENARIO,
    CMD_NEXT_SCENARIO,
    CMD_STOP,
    CMD_SEND_TEXT,
    CMD_SEND_KEY,
    CMD_SEND_SHORTCUT
};

struct ControllerCommand {
    CommandType type;
    int scenarioId;
    char text[MAX_TEXT_PAYLOAD_LEN + 1];
    char keyName[16];
    uint8_t modifiers;
};

class ScenarioController {
public:
    ScenarioController();

    // Lifecycle
    void begin();
    void update(); // Called from main task/loop or dedicated FreeRTOS worker

    // Public actions (thread-safe command submission)
    bool requestScenario(int id, String& errorMsg);
    bool requestNextScenario(String& errorMsg);
    bool requestStop(String& errorMsg);
    bool requestSendText(const char* text, String& errorMsg);
    bool requestSendKey(const char* keyName, String& errorMsg);
    bool requestSendShortcut(uint8_t modifiers, const char* keyName, String& errorMsg);

    // State queries
    ControllerState getState() const;
    const char* getStateString() const;
    int getCurrentScenarioId() const;
    const char* getScenarioName(int id) const;
    bool isBusy() const;
    bool hasStartupExecuted() const;
    const char* getLastError() const;

private:
    ControllerState state;
    int currentScenarioId;
    bool startupExecuted;
    volatile bool stopRequested;
    char lastError[64];
    unsigned long stateEnteredTime;

    ControllerCommand activeCommand;
    bool hasActiveCommand;
    portMUX_TYPE stateMux;

    // Internal scenario execution routines
    void executeScenario1(); // Notepad Awareness
    void executeScenario2(); // Portal Redirection
    void executeScenario3(); // Ransomware Awareness
    void executeScenario4(); // Wi-Fi Reconnaissance

    void setStatus(ControllerState newState, const char* err = nullptr);
    void safeStepPause(unsigned long ms);
};

extern ScenarioController ScenarioCtrl;
