import random
import pytest
from src.detection.keystroke_dynamics import (
    KeystrokeDynamicsEngine,
    MultiDeviceDynamicsManager,
    ThreatLevel,
)


def test_dynamics_initial_state():
    engine = KeystrokeDynamicsEngine(window_size=10)
    assert engine.total_keystrokes == 0
    assert engine.current_threat_level == ThreatLevel.SAFE
    assert len(engine.window) == 0


def test_machine_injection_detection():
    engine = KeystrokeDynamicsEngine(window_size=10, machine_threshold_ms=25.0)

    # Simulate standard high-speed BadUSB injection: 10ms intervals with minimal variance
    metrics = None
    for _ in range(12):
        metrics = engine.add_keystroke(delta_ms=10.0)

    assert metrics is not None
    assert metrics.threat_level == ThreatLevel.LOCKED_DOWN
    assert metrics.mean_iki < 25.0
    assert metrics.cv_iki < 0.15
    assert metrics.burst_rate >= 90.0


def test_human_typing_cadence():
    engine = KeystrokeDynamicsEngine(window_size=10, human_threshold_ms=75.0, human_cv_threshold=0.25)

    # Simulate realistic human typing with inter-key variations (80-160ms) and inter-word cognitive pauses (250-450ms)
    random.seed(42)
    deltas = []
    for word in ["ieee", "research", "paper", "keystroke", "firewall", "evaluation"]:
        for char in word:
            deltas.append(random.uniform(75, 150))
        deltas.append(random.uniform(280, 480))

    metrics = None
    for d in deltas:
        metrics = engine.add_keystroke(delta_ms=d)

    assert metrics is not None
    assert metrics.threat_level == ThreatLevel.SAFE
    assert metrics.mean_iki > 75.0
    assert metrics.cv_iki > 0.30


def test_multi_device_isolation():
    manager = MultiDeviceDynamicsManager(window_size=10)

    laptop_kb = "0x10075"
    badusb_hid = "0x4C06F1"

    manager.register_device(laptop_kb, name="Built-in Laptop Keyboard")
    manager.register_device(badusb_hid, name="ESP32-S3 BadUSB HID", vid="303A", pid="1001")

    # 1. Human types on laptop keyboard
    random.seed(123)
    for _ in range(12):
        m_lap, is_quar = manager.record_event(laptop_kb, delta_ms=random.uniform(90, 220))
        assert is_quar is False
        assert m_lap.threat_level in (ThreatLevel.SAFE, ThreatLevel.SUSPICIOUS)

    assert manager.is_quarantined(laptop_kb) is False

    # 2. BadUSB injects on ESP32-S3 device
    for _ in range(12):
        m_bad, is_quar = manager.record_event(badusb_hid, delta_ms=8.0)

    assert m_bad.threat_level == ThreatLevel.LOCKED_DOWN
    assert manager.is_quarantined(badusb_hid) is True

    # 3. Verify selective quarantine: BadUSB is quarantined, laptop keyboard remains authorized!
    assert manager.is_quarantined(badusb_hid) is True
    assert manager.is_quarantined(laptop_kb) is False

    # 4. Human continues typing safely while BadUSB is blocked
    m_lap2, is_quar2 = manager.record_event(laptop_kb, delta_ms=130.0)
    assert is_quar2 is False
