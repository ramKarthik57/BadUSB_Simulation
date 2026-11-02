"""Host-side simulation and unit tests for the ESP32-S3 BadUSB Scenario Controller,
Keyboard Command Parser, and API Contract.
"""

import time
import pytest


class MockScenarioController:
    """Python simulation matching the C++ ScenarioController state machine."""
    STATE_BOOTING = "BOOTING"
    STATE_USB_WAIT = "USB_WAIT"
    STATE_STARTUP_PAYLOAD = "STARTUP_PAYLOAD"
    STATE_IDLE = "IDLE"
    STATE_RUNNING = "RUNNING"
    STATE_STOPPING = "STOPPING"
    STATE_STOPPED = "STOPPED"
    STATE_ERROR = "ERROR"

    TOTAL_SCENARIOS = 4

    def __init__(self, usb_enum_timeout=0.05):
        self.state = self.STATE_BOOTING
        self.current_scenario_id = 1
        self.startup_executed = False
        self.stop_requested = False
        self.last_error = ""
        self.usb_enum_timeout = usb_enum_timeout
        self.boot_time = time.time()
        self.keys_held = []
        self.transmitted_text = []

    def update(self):
        now = time.time()
        if self.state == self.STATE_BOOTING:
            self.state = self.STATE_USB_WAIT
            self.boot_time = now
        elif self.state == self.STATE_USB_WAIT:
            if (now - self.boot_time) >= self.usb_enum_timeout:
                if not self.startup_executed:
                    self.state = self.STATE_STARTUP_PAYLOAD
                else:
                    self.state = self.STATE_IDLE
        elif self.state == self.STATE_STARTUP_PAYLOAD:
            self.current_scenario_id = 1
            self.transmitted_text.append("Scenario 1 (Notepad Awareness)")
            self.startup_executed = True
            self.state = self.STATE_IDLE
        elif self.state == self.STATE_STOPPING:
            self.keys_held.clear()
            self.state = self.STATE_STOPPED

    def is_busy(self):
        return self.state in (self.STATE_RUNNING, self.STATE_STARTUP_PAYLOAD, self.STATE_STOPPING)

    def request_scenario(self, scenario_id):
        if scenario_id < 1 or scenario_id > self.TOTAL_SCENARIOS:
            return False, "Invalid scenario ID (expected 1 to 4)"
        if self.is_busy():
            return False, "Controller is busy running another action"
        self.current_scenario_id = scenario_id
        self.state = self.STATE_RUNNING
        self.transmitted_text.append(f"Scenario {scenario_id}")
        self.state = self.STATE_IDLE
        return True, "Success"

    def request_next_scenario(self):
        if self.is_busy():
            return False, "Controller is busy running another action"
        next_id = self.current_scenario_id + 1
        if next_id > self.TOTAL_SCENARIOS:
            next_id = 1
        return self.request_scenario(next_id)

    def request_stop(self):
        self.stop_requested = True
        self.state = self.STATE_STOPPING
        self.update()
        return True, "Stopped"

    def send_text(self, text):
        if not text:
            return False, "Text cannot be empty"
        if len(text) > 256:
            return False, "Text exceeds maximum allowed length (256 characters)"
        if self.is_busy():
            return False, "Controller is busy running another action"
        self.transmitted_text.append(text)
        return True, "Success"


class MockKeyboardParser:
    """Python simulation matching C++ KeyboardController key and modifier mappings."""
    SPECIAL_KEYS = {
        "ENTER": 0xB0, "RETURN": 0xB0,
        "BACKSPACE": 0xB2, "BS": 0xB2,
        "TAB": 0xB3, "ESCAPE": 0xB1, "ESC": 0xB1,
        "UP": 0xDA, "DOWN": 0xD9, "LEFT": 0xD8, "RIGHT": 0xD7,
        "DELETE": 0xD4, "HOME": 0xD2, "END": 0xD5,
        "PAGEUP": 0xD3, "PAGEDOWN": 0xD6, "CAPSLOCK": 0xC1,
        "CTRL": 0x80, "CONTROL": 0x80, "SHIFT": 0x81, "ALT": 0x82,
        "WIN": 0x83, "GUI": 0x83, "WINDOWS": 0x83,
        "F1": 0xC2, "F2": 0xC3, "F3": 0xC4, "F4": 0xC5,
        "F5": 0xC6, "F6": 0xC7, "F7": 0xC8, "F8": 0xC9,
        "F9": 0xCA, "F10": 0xCB, "F11": 0xCC, "F12": 0xCD
    }

    @classmethod
    def parse_modifiers(cls, mod_str):
        if not mod_str:
            return 0
        s = mod_str.upper()
        mask = 0
        if "CTRL" in s or "CONTROL" in s: mask |= 0x01
        if "SHIFT" in s: mask |= 0x02
        if "ALT" in s: mask |= 0x04
        if "GUI" in s or "WIN" in s or "META" in s: mask |= 0x08
        return mask

    @classmethod
    def resolve_key(cls, key_name):
        if not key_name:
            return None
        k = key_name.strip().upper()
        if k in cls.SPECIAL_KEYS:
            return cls.SPECIAL_KEYS[k]
        if len(key_name) == 1 and 32 <= ord(key_name) <= 126:
            return ord(key_name)
        return None


# ============================================================
# UNIT TESTS
# ============================================================

def test_startup_executes_payload_1_once():
    ctrl = MockScenarioController(usb_enum_timeout=0.01)
    ctrl.update() # Booting -> USB_WAIT
    assert ctrl.state == MockScenarioController.STATE_USB_WAIT

    time.sleep(0.02)
    ctrl.update() # USB_WAIT -> STARTUP_PAYLOAD
    assert ctrl.state == MockScenarioController.STATE_STARTUP_PAYLOAD

    ctrl.update() # Executes payload 1 -> IDLE
    assert ctrl.state == MockScenarioController.STATE_IDLE
    assert ctrl.current_scenario_id == 1
    assert ctrl.startup_executed is True
    assert len(ctrl.transmitted_text) == 1

    # Subsequent updates must NOT re-run payload 1
    ctrl.update()
    assert ctrl.state == MockScenarioController.STATE_IDLE
    assert len(ctrl.transmitted_text) == 1


def test_sequential_boot_button_advance():
    ctrl = MockScenarioController(usb_enum_timeout=0.0)
    ctrl.state = MockScenarioController.STATE_IDLE
    ctrl.current_scenario_id = 1

    # Step to 2
    ok, _ = ctrl.request_next_scenario()
    assert ok and ctrl.current_scenario_id == 2

    # Step to 3
    ok, _ = ctrl.request_next_scenario()
    assert ok and ctrl.current_scenario_id == 3

    # Step to 4
    ok, _ = ctrl.request_next_scenario()
    assert ok and ctrl.current_scenario_id == 4

    # Step wraps to 1 cleanly
    ok, _ = ctrl.request_next_scenario()
    assert ok and ctrl.current_scenario_id == 1


def test_direct_scenario_selection():
    ctrl = MockScenarioController(usb_enum_timeout=0.0)
    ctrl.state = MockScenarioController.STATE_IDLE
    ctrl.current_scenario_id = 1

    # Jump directly from Scenario 1 to Scenario 4 without executing 2 or 3
    ok, msg = ctrl.request_scenario(4)
    assert ok is True
    assert ctrl.current_scenario_id == 4
    assert ctrl.transmitted_text[-1] == "Scenario 4"


def test_invalid_scenario_rejection():
    ctrl = MockScenarioController(usb_enum_timeout=0.0)
    ctrl.state = MockScenarioController.STATE_IDLE

    ok, msg = ctrl.request_scenario(0)
    assert ok is False
    assert "Invalid scenario ID" in msg

    ok, msg = ctrl.request_scenario(5)
    assert ok is False
    assert "Invalid scenario ID" in msg


def test_emergency_stop():
    ctrl = MockScenarioController(usb_enum_timeout=0.0)
    ctrl.state = MockScenarioController.STATE_RUNNING
    ctrl.keys_held = ["CTRL", "ALT", "r"]

    ok, _ = ctrl.request_stop()
    assert ok is True
    assert ctrl.state == MockScenarioController.STATE_STOPPED
    assert len(ctrl.keys_held) == 0  # Keys released


def test_keyboard_text_bounds():
    ctrl = MockScenarioController(usb_enum_timeout=0.0)
    ctrl.state = MockScenarioController.STATE_IDLE

    # Valid message
    ok, _ = ctrl.send_text("Hi i am ram")
    assert ok is True
    assert ctrl.transmitted_text[-1] == "Hi i am ram"

    # Empty text rejected
    ok, msg = ctrl.send_text("")
    assert ok is False
    assert "cannot be empty" in msg

    # Oversized text (> 256 chars) rejected
    oversized = "A" * 300
    ok, msg = ctrl.send_text(oversized)
    assert ok is False
    assert "exceeds maximum allowed length" in msg


def test_keyboard_key_mapping():
    assert MockKeyboardParser.resolve_key("ENTER") == 0xB0
    assert MockKeyboardParser.resolve_key("enter") == 0xB0
    assert MockKeyboardParser.resolve_key("BACKSPACE") == 0xB2
    assert MockKeyboardParser.resolve_key("WIN") == 0x83
    assert MockKeyboardParser.resolve_key("CTRL") == 0x80
    assert MockKeyboardParser.resolve_key("ALT") == 0x82
    assert MockKeyboardParser.resolve_key("SHIFT") == 0x81
    assert MockKeyboardParser.resolve_key("F1") == 0xC2
    assert MockKeyboardParser.resolve_key("F12") == 0xCD
    assert MockKeyboardParser.resolve_key("a") == ord("a")
    assert MockKeyboardParser.resolve_key("A") == ord("A")
    assert MockKeyboardParser.resolve_key("UNKNOWN_KEY_NAME") is None


def test_keyboard_modifier_parsing():
    assert MockKeyboardParser.parse_modifiers("CTRL") == 0x01
    assert MockKeyboardParser.parse_modifiers("SHIFT") == 0x02
    assert MockKeyboardParser.parse_modifiers("ALT") == 0x04
    assert MockKeyboardParser.parse_modifiers("GUI") == 0x08
    assert MockKeyboardParser.parse_modifiers("WIN") == 0x08
    assert MockKeyboardParser.parse_modifiers("CTRL+ALT") == 0x05
    assert MockKeyboardParser.parse_modifiers("CTRL+SHIFT+GUI") == 0x0B
    assert MockKeyboardParser.parse_modifiers("") == 0x00
