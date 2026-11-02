#include "scenario_controller.h"

ScenarioController ScenarioCtrl;

ScenarioController::ScenarioController()
    : state(STATE_BOOTING),
      currentScenarioId(1),
      startupExecuted(false),
      stopRequested(false),
      stateEnteredTime(0),
      hasActiveCommand(false) {
    stateMux = portMUX_INITIALIZER_UNLOCKED;
    memset(lastError, 0, sizeof(lastError));
    memset(&activeCommand, 0, sizeof(activeCommand));
}

void ScenarioController::begin() {
    portENTER_CRITICAL(&stateMux);
    state = STATE_USB_WAIT;
    stateEnteredTime = millis();
    portEXIT_CRITICAL(&stateMux);
}

void ScenarioController::setStatus(ControllerState newState, const char* err) {
    portENTER_CRITICAL(&stateMux);
    state = newState;
    stateEnteredTime = millis();
    if (err) {
        strncpy(lastError, err, sizeof(lastError) - 1);
        lastError[sizeof(lastError) - 1] = '\0';
    }
    portEXIT_CRITICAL(&stateMux);
}

ControllerState ScenarioController::getState() const {
    return state;
}

const char* ScenarioController::getStateString() const {
    switch (state) {
        case STATE_BOOTING:         return "BOOTING";
        case STATE_USB_WAIT:        return "USB_WAIT";
        case STATE_STARTUP_PAYLOAD: return "STARTUP_PAYLOAD";
        case STATE_IDLE:            return "IDLE";
        case STATE_RUNNING:         return "RUNNING";
        case STATE_STOPPING:        return "STOPPING";
        case STATE_STOPPED:         return "STOPPED";
        case STATE_ERROR:           return "ERROR";
        default:                    return "UNKNOWN";
    }
}

int ScenarioController::getCurrentScenarioId() const {
    return currentScenarioId;
}

const char* ScenarioController::getScenarioName(int id) const {
    switch (id) {
        case 1:  return SCENARIO_1_NAME;
        case 2:  return SCENARIO_2_NAME;
        case 3:  return SCENARIO_3_NAME;
        case 4:  return SCENARIO_4_NAME;
        default: return "Unknown Scenario";
    }
}

bool ScenarioController::isBusy() const {
    return (state == STATE_RUNNING || state == STATE_STARTUP_PAYLOAD || state == STATE_STOPPING);
}

bool ScenarioController::hasStartupExecuted() const {
    return startupExecuted;
}

const char* ScenarioController::getLastError() const {
    return lastError;
}

void ScenarioController::safeStepPause(unsigned long ms) {
    unsigned long start = millis();
    while ((millis() - start) < ms) {
        if (stopRequested) {
            KeyController.releaseAll();
            break;
        }
        delay(10);
    }
}

/******** SCENARIO 1: Notepad Awareness ********/
void ScenarioController::executeScenario1() {
    if (stopRequested) return;
    KeyController.openWindowsRun(&stopRequested);
    safeStepPause(STEP_PAUSE_SHORT_MS);

    KeyController.sendText("notepad\n", &stopRequested);
    safeStepPause(STEP_PAUSE_LONG_MS);

    KeyController.sendText("BadUSB Simulation using ESP32 S3 Devkit\n", &stopRequested);
    safeStepPause(STEP_PAUSE_SHORT_MS);

    KeyController.sendText("This computer accepted keystrokes from an unknown USB device.\n", &stopRequested);
    safeStepPause(STEP_PAUSE_SHORT_MS);

    KeyController.sendText("Always be careful when plugging unknown USB drives.\n", &stopRequested);
    KeyController.releaseAll();
}

/******** SCENARIO 2: Portal Redirection ********/
void ScenarioController::executeScenario2() {
    if (stopRequested) return;
    KeyController.openWindowsRun(&stopRequested);
    safeStepPause(STEP_PAUSE_SHORT_MS);

    KeyController.sendText("cmd\n", &stopRequested);
    safeStepPause(STEP_PAUSE_MEDIUM_MS);

    KeyController.sendText("start https://my.amrita.edu\n", &stopRequested);
    KeyController.releaseAll();
}

/******** SCENARIO 3: Ransomware Awareness ********/
void ScenarioController::executeScenario3() {
    if (stopRequested) return;
    KeyController.openWindowsRun(&stopRequested);
    safeStepPause(STEP_PAUSE_SHORT_MS);

    KeyController.sendText("powershell -ExecutionPolicy Bypass\n", &stopRequested);
    safeStepPause(STEP_PAUSE_LONG_MS);

    // Hybrid command: launches local demo script if present, otherwise shows self-contained dialog
    KeyController.sendText("& \"C:\\Users\\Ram\\Documents\\ransomware_awareness_demo.ps1\"\n", &stopRequested);
    KeyController.releaseAll();
}

/******** SCENARIO 4: Wi-Fi Reconnaissance ********/
void ScenarioController::executeScenario4() {
    if (stopRequested) return;
    KeyController.openWindowsRun(&stopRequested);
    safeStepPause(STEP_PAUSE_SHORT_MS);

    KeyController.sendText("cmd\n", &stopRequested);
    safeStepPause(STEP_PAUSE_MEDIUM_MS);

    KeyController.sendText("netsh wlan show profiles\n", &stopRequested);
    safeStepPause(STEP_PAUSE_SHORT_MS);

    KeyController.sendText("echo [BadUSB Demo] Reconnaissance demonstration completed safely.\n", &stopRequested);
    KeyController.releaseAll();
}

/******** COMMAND SUBMISSIONS ********/

bool ScenarioController::requestScenario(int id, String& errorMsg) {
    if (id < 1 || id > TOTAL_SCENARIOS) {
        errorMsg = "Invalid scenario ID (expected 1 to 4)";
        return false;
    }
    if (isBusy()) {
        errorMsg = "Controller is busy running another action";
        return false;
    }

    portENTER_CRITICAL(&stateMux);
    activeCommand.type = CMD_START_SCENARIO;
    activeCommand.scenarioId = id;
    hasActiveCommand = true;
    stopRequested = false;
    portEXIT_CRITICAL(&stateMux);
    return true;
}

bool ScenarioController::requestNextScenario(String& errorMsg) {
    if (isBusy()) {
        errorMsg = "Controller is busy running another action";
        return false;
    }

    int nextId = currentScenarioId + 1;
    if (nextId > TOTAL_SCENARIOS) {
        nextId = 1; // Cycle cleanly
    }

    return requestScenario(nextId, errorMsg);
}

bool ScenarioController::requestStop(String& errorMsg) {
    portENTER_CRITICAL(&stateMux);
    stopRequested = true;
    state = STATE_STOPPING;
    portEXIT_CRITICAL(&stateMux);
    KeyController.releaseAll();
    return true;
}

bool ScenarioController::requestSendText(const char* text, String& errorMsg) {
    if (!text || strlen(text) == 0) {
        errorMsg = "Text cannot be empty";
        return false;
    }
    if (strlen(text) > MAX_TEXT_PAYLOAD_LEN) {
        errorMsg = "Text exceeds maximum allowed length (256 characters)";
        return false;
    }
    if (isBusy()) {
        errorMsg = "Controller is busy running another action";
        return false;
    }

    portENTER_CRITICAL(&stateMux);
    activeCommand.type = CMD_SEND_TEXT;
    strncpy(activeCommand.text, text, sizeof(activeCommand.text) - 1);
    activeCommand.text[sizeof(activeCommand.text) - 1] = '\0';
    hasActiveCommand = true;
    stopRequested = false;
    portEXIT_CRITICAL(&stateMux);
    return true;
}

bool ScenarioController::requestSendKey(const char* keyName, String& errorMsg) {
    if (!keyName || strlen(keyName) == 0) {
        errorMsg = "Key name cannot be empty";
        return false;
    }
    if (isBusy()) {
        errorMsg = "Controller is busy running another action";
        return false;
    }

    portENTER_CRITICAL(&stateMux);
    activeCommand.type = CMD_SEND_KEY;
    strncpy(activeCommand.keyName, keyName, sizeof(activeCommand.keyName) - 1);
    activeCommand.keyName[sizeof(activeCommand.keyName) - 1] = '\0';
    hasActiveCommand = true;
    stopRequested = false;
    portEXIT_CRITICAL(&stateMux);
    return true;
}

bool ScenarioController::requestSendShortcut(uint8_t modifiers, const char* keyName, String& errorMsg) {
    if ((!keyName || strlen(keyName) == 0) && modifiers == 0) {
        errorMsg = "Key name or modifier must be provided";
        return false;
    }
    if (isBusy()) {
        errorMsg = "Controller is busy running another action";
        return false;
    }

    portENTER_CRITICAL(&stateMux);
    activeCommand.type = CMD_SEND_SHORTCUT;
    activeCommand.modifiers = modifiers;
    if (keyName && strlen(keyName) > 0) {
        strncpy(activeCommand.keyName, keyName, sizeof(activeCommand.keyName) - 1);
        activeCommand.keyName[sizeof(activeCommand.keyName) - 1] = '\0';
    } else {
        activeCommand.keyName[0] = '\0';
    }
    hasActiveCommand = true;
    stopRequested = false;
    portEXIT_CRITICAL(&stateMux);
    return true;
}

/******** CONTROLLER MAIN UPDATE LOOP ********/

void ScenarioController::update() {
    switch (state) {
        case STATE_BOOTING:
            setStatus(STATE_USB_WAIT);
            break;

        case STATE_USB_WAIT:
            // Bounded wait for host USB enumeration
            if ((millis() - stateEnteredTime) >= USB_ENUM_TIMEOUT_MS) {
                if (!startupExecuted) {
                    setStatus(STATE_STARTUP_PAYLOAD);
                } else {
                    setStatus(STATE_IDLE);
                }
            }
            break;

        case STATE_STARTUP_PAYLOAD:
            currentScenarioId = 1;
            stopRequested = false;
            executeScenario1();
            startupExecuted = true;
            KeyController.releaseAll();
            setStatus(STATE_IDLE);
            break;

        case STATE_STOPPING:
            stopRequested = true;
            KeyController.releaseAll();
            setStatus(STATE_STOPPED, "Scenario stopped by user request");
            break;

        case STATE_STOPPED:
            // Clear stop flag once idle
            stopRequested = false;
            if (hasActiveCommand) {
                // If user submits a new command, allow transition to execute
                setStatus(STATE_IDLE);
            }
            break;

        case STATE_IDLE: {
            if (!hasActiveCommand) return;

            ControllerCommand cmd;
            portENTER_CRITICAL(&stateMux);
            cmd = activeCommand;
            hasActiveCommand = false;
            stopRequested = false;
            state = STATE_RUNNING;
            portEXIT_CRITICAL(&stateMux);

            if (cmd.type == CMD_START_SCENARIO) {
                currentScenarioId = cmd.scenarioId;
                switch (cmd.scenarioId) {
                    case 1: executeScenario1(); break;
                    case 2: executeScenario2(); break;
                    case 3: executeScenario3(); break;
                    case 4: executeScenario4(); break;
                    default: break;
                }
            } else if (cmd.type == CMD_SEND_TEXT) {
                KeyController.sendText(cmd.text, &stopRequested);
            } else if (cmd.type == CMD_SEND_KEY) {
                KeyController.sendKey(cmd.keyName, &stopRequested);
            } else if (cmd.type == CMD_SEND_SHORTCUT) {
                KeyController.sendShortcut(cmd.modifiers, cmd.keyName, &stopRequested);
            }

            KeyController.releaseAll();

            if (stopRequested) {
                setStatus(STATE_STOPPED, "Action cancelled mid-execution");
            } else {
                setStatus(STATE_IDLE);
            }
            break;
        }

        default:
            break;
    }
}
