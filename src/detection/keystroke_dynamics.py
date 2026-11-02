"""
Keystroke Dynamics & Inter-Key Interval (IKI) Behavioral Detector
Module: src.detection.keystroke_dynamics

Implements real-time statistical analysis of typing cadence to distinguish
between machine-generated BadUSB injection (including stealth/jittered evasion)
and legitimate human operators.
"""

from collections import deque
from dataclasses import dataclass, field
from enum import Enum
import math
import time
from typing import Dict, List, Optional, Tuple


class ThreatLevel(str, Enum):
    SAFE = "SAFE"                          # Normal human typing cadence
    SUSPICIOUS = "SUSPICIOUS"              # Cadence anomaly or stealth evasion characteristics
    LOCKED_DOWN = "LOCKED_DOWN"            # Confirmed machine injection (BadUSB)


@dataclass
class KeystrokeMetrics:
    mean_iki: float = 0.0                  # Mean Inter-Key Interval in milliseconds
    std_iki: float = 0.0                   # Standard deviation of IKI
    cv_iki: float = 0.0                    # Coefficient of Variation (sigma / mu)
    burst_rate: float = 0.0                # Typing speed in characters per second
    threat_level: ThreatLevel = ThreatLevel.SAFE
    sample_count: int = 0
    consecutive_machine_count: int = 0
    device_id: Optional[str] = None
    last_iki_ms: float = 0.0


class KeystrokeDynamicsEngine:
    """
    Online sliding-window statistical detector for keystroke dynamics.
    """

    def __init__(
        self,
        window_size: int = 10,
        machine_threshold_ms: float = 25.0,
        machine_cv_threshold: float = 0.15,
        machine_consecutive_trigger: int = 8,
        human_threshold_ms: float = 75.0,
        human_cv_threshold: float = 0.30,
        device_id: Optional[str] = None,
    ):
        self.window_size = window_size
        self.machine_threshold_ms = machine_threshold_ms
        self.machine_cv_threshold = machine_cv_threshold
        self.machine_consecutive_trigger = machine_consecutive_trigger
        self.human_threshold_ms = human_threshold_ms
        self.human_cv_threshold = human_cv_threshold
        self.device_id = device_id

        self.window: deque = deque(maxlen=window_size)
        self.last_timestamp_ms: Optional[float] = None
        self.total_keystrokes: int = 0
        self.consecutive_machine_count: int = 0
        self.current_threat_level: ThreatLevel = ThreatLevel.SAFE
        self.last_metrics: KeystrokeMetrics = KeystrokeMetrics(device_id=device_id)

    def reset(self) -> None:
        """Reset sliding window and behavioral state."""
        self.window.clear()
        self.last_timestamp_ms = None
        self.total_keystrokes = 0
        self.consecutive_machine_count = 0
        self.current_threat_level = ThreatLevel.SAFE
        self.last_metrics = KeystrokeMetrics(device_id=self.device_id)

    def add_keystroke(
        self,
        timestamp_ms: Optional[float] = None,
        delta_ms: Optional[float] = None,
    ) -> KeystrokeMetrics:
        """
        Record a keystroke event and compute real-time dynamics.
        Can supply either timestamp_ms (epoch/monotonic) or direct delta_ms.
        """
        now_ms = timestamp_ms if timestamp_ms is not None else (time.perf_counter() * 1000.0)

        if delta_ms is None:
            if self.last_timestamp_ms is None:
                self.last_timestamp_ms = now_ms
                self.total_keystrokes += 1
                self.last_metrics = KeystrokeMetrics(
                    threat_level=ThreatLevel.SAFE,
                    sample_count=1,
                    device_id=self.device_id,
                )
                return self.last_metrics
            computed_delta = now_ms - self.last_timestamp_ms
        else:
            computed_delta = delta_ms

        # Clamp negative deltas due to timer anomalies
        computed_delta = max(0.1, float(computed_delta))
        self.last_timestamp_ms = now_ms
        self.total_keystrokes += 1

        # Push to sliding window
        self.window.append(computed_delta)
        n = len(self.window)

        # Compute online statistics
        mean_iki = sum(self.window) / n
        if n > 1:
            variance = sum((x - mean_iki) ** 2 for x in self.window) / n
            std_iki = math.sqrt(variance)
        else:
            std_iki = 0.0

        cv_iki = (std_iki / mean_iki) if mean_iki > 0.0 else 0.0
        burst_rate = (1000.0 / mean_iki) if mean_iki > 0.0 else 0.0

        # Decision Rule Evaluation
        # If mean IKI < 25ms OR CV < 0.15 over 8 consecutive keystrokes: MACHINE_INJECTION
        is_machine_instant = (mean_iki < self.machine_threshold_ms) or (n >= 4 and cv_iki < self.machine_cv_threshold)

        if is_machine_instant:
            self.consecutive_machine_count += 1
        else:
            self.consecutive_machine_count = max(0, self.consecutive_machine_count - 1)

        if self.consecutive_machine_count >= self.machine_consecutive_trigger:
            threat_level = ThreatLevel.LOCKED_DOWN
        elif mean_iki > self.human_threshold_ms and cv_iki > self.human_cv_threshold:
            threat_level = ThreatLevel.SAFE
            self.consecutive_machine_count = 0
        else:
            # Intermediate / transition region (e.g. stealth evasion or rapid human burst)
            threat_level = ThreatLevel.SUSPICIOUS

        self.current_threat_level = threat_level
        self.last_metrics = KeystrokeMetrics(
            mean_iki=round(mean_iki, 2),
            std_iki=round(std_iki, 2),
            cv_iki=round(cv_iki, 4),
            burst_rate=round(burst_rate, 2),
            threat_level=threat_level,
            sample_count=self.total_keystrokes,
            consecutive_machine_count=self.consecutive_machine_count,
            device_id=self.device_id,
            last_iki_ms=round(computed_delta, 2),
        )
        return self.last_metrics


class MultiDeviceDynamicsManager:
    """
    Manages per-device keystroke dynamics engines to isolate and selectively
    suppress malicious USB devices while allowing legitimate human keyboards.
    """

    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.engines: Dict[str, KeystrokeDynamicsEngine] = {}
        self.quarantined_devices: set = set()
        self.device_info: Dict[str, Dict[str, str]] = {}
        self.last_active_device_id: Optional[str] = None

    def register_device(
        self,
        device_id: str,
        name: str = "Unknown Keyboard",
        vid: Optional[str] = None,
        pid: Optional[str] = None,
    ) -> None:
        """Register hardware device metadata."""
        self.device_info[device_id] = {
            "name": name,
            "vid": vid or "UNKNOWN",
            "pid": pid or "UNKNOWN",
            "registered_at": time.strftime("%H:%M:%S"),
        }
        if device_id not in self.engines:
            self.engines[device_id] = KeystrokeDynamicsEngine(
                window_size=self.window_size,
                device_id=device_id,
            )

    def get_or_create_engine(self, device_id: str) -> KeystrokeDynamicsEngine:
        """Retrieve or create an engine for the specified device handle/ID."""
        if device_id not in self.engines:
            self.engines[device_id] = KeystrokeDynamicsEngine(
                window_size=self.window_size,
                device_id=device_id,
            )
        return self.engines[device_id]

    def record_event(
        self,
        device_id: str,
        timestamp_ms: Optional[float] = None,
        delta_ms: Optional[float] = None,
    ) -> Tuple[KeystrokeMetrics, bool]:
        """
        Record a key event from a device.
        Returns: (metrics, is_quarantined)
        """
        self.last_active_device_id = device_id
        engine = self.get_or_create_engine(device_id)
        metrics = engine.add_keystroke(timestamp_ms=timestamp_ms, delta_ms=delta_ms)

        # Automatic quarantine transition on machine injection detection
        if metrics.threat_level == ThreatLevel.LOCKED_DOWN:
            self.quarantined_devices.add(device_id)

        is_quarantined = device_id in self.quarantined_devices
        return metrics, is_quarantined

    def quarantine_device(self, device_id: str) -> None:
        self.quarantined_devices.add(device_id)

    def release_device(self, device_id: str) -> None:
        self.quarantined_devices.discard(device_id)
        if device_id in self.engines:
            self.engines[device_id].reset()

    def clear_all_quarantines(self) -> None:
        self.quarantined_devices.clear()
        for engine in self.engines.values():
            engine.reset()

    def is_quarantined(self, device_id: str) -> bool:
        return device_id in self.quarantined_devices

    def get_summary(self) -> Dict[str, dict]:
        """Return status summary for all monitored devices."""
        summary = {}
        for dev_id, eng in self.engines.items():
            info = self.device_info.get(dev_id, {})
            m = eng.last_metrics
            summary[dev_id] = {
                "name": info.get("name", "Keyboard"),
                "vid": info.get("vid", ""),
                "pid": info.get("pid", ""),
                "threat": m.threat_level.value,
                "mean_iki_ms": m.mean_iki,
                "cv": m.cv_iki,
                "burst_rate": m.burst_rate,
                "quarantined": dev_id in self.quarantined_devices,
                "samples": m.sample_count,
            }
        return summary
