"""
WHID-Guard: Behavioral Keystroke Firewall & Device Isolation Engine
Module: src.firewall

Combines Windows Low-Level Hook (WH_KEYBOARD_LL) keystroke suppression
with real-time Inter-Key Interval (IKI) behavioral dynamics detection and
Windows Raw Input (WM_INPUT) per-device hardware attribution.
"""

import atexit
import datetime
import threading
import time
import tkinter as tk
from typing import Callable, Dict, Optional

import keyboard

from src.detection.keystroke_dynamics import (
    KeystrokeDynamicsEngine,
    MultiDeviceDynamicsManager,
    ThreatLevel,
    KeystrokeMetrics,
)
from src.detection.raw_input_monitor import RawInputMonitor, RawInputDeviceInfo


# ============================================================
# CONFIG MODULE
# ============================================================

class Config:
    WINDOW_WIDTH = 460
    WINDOW_HEIGHT = 460

    COLOR_BG = "#121824"
    COLOR_CARD = "#1a2332"
    COLOR_BORDER = "#2a374a"
    COLOR_TEXT = "#f1f5f9"
    COLOR_MUTED = "#94a3b8"

    COLOR_GREEN = "#10b981"
    COLOR_YELLOW = "#f59e0b"
    COLOR_RED = "#ef4444"
    COLOR_BUTTON = "#1e293b"
    COLOR_BUTTON_ACTIVE = "#334155"

    TITLE = "WHID-GUARD FIREWALL"
    SUBTITLE = "Behavioral Dynamics & Per-Device USB HID Defense"
    FOOTER = "IEEE Research Platform • Raw Input & IKI Detection Active"

    FONT_TITLE = ("Segoe UI", 13, "bold")
    FONT_SUBTITLE = ("Segoe UI", 8)
    FONT_STATUS = ("Segoe UI", 14, "bold")
    FONT_TIMER = ("Segoe UI", 9)
    FONT_BUTTON = ("Segoe UI", 10, "bold")
    FONT_METRIC_LABEL = ("Segoe UI", 8)
    FONT_METRIC_VAL = ("Consolas", 10, "bold")
    FONT_FOOTER = ("Segoe UI", 8)

    # Maximum safety duration in seconds to prevent accidental permanent lockouts
    DEFAULT_MAX_SUPPRESSION_SECONDS = 15


# ============================================================
# LOGGER MODULE
# ============================================================

class Logger:
    def __init__(self):
        self.enabled = True

    def log(self, message: str):
        if not self.enabled:
            return
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{time_str}] {message}")

    def info(self, message: str):
        self.log("[INFO] " + message)

    def warn(self, message: str):
        self.log("[WARN] " + message)

    def error(self, message: str):
        self.log("[ERROR] " + message)


logger = Logger()


# ============================================================
# FIREWALL MODULE
# ============================================================

class Firewall:
    """
    Core defensive keystroke firewall. Supports:
    1. Global low-level hook suppression (WH_KEYBOARD_LL)
    2. Online Keystroke Dynamics behavioral detection (IKI sliding window)
    3. Per-device hardware attribution via Windows Raw Input (WM_INPUT)
    4. Selective per-device quarantine and suppression
    """

    def __init__(
        self,
        max_suppression_duration=Config.DEFAULT_MAX_SUPPRESSION_SECONDS,
        start_monitor: bool = False,
    ):
        self.enabled = False  # Manual full-block state
        self.auto_guard_enabled = True  # Behavioral detection & selective suppression
        self.hook = None
        self.max_suppression_duration = max_suppression_duration
        self._watchdog_timer = None
        self._on_auto_disarm_callback = None
        self._on_metrics_updated_callback = None

        # Behavioral Dynamics & Raw Input Managers
        self.dynamics_manager = MultiDeviceDynamicsManager(window_size=10)
        self.global_engine = KeystrokeDynamicsEngine(window_size=10)
        self.raw_monitor = RawInputMonitor(on_event_callback=self._on_raw_input_event)

        # Fallback device handle if raw input is inactive/mocked
        self.fallback_device_id = "0xPRIMARY"
        self.dynamics_manager.register_device(
            self.fallback_device_id,
            name="Primary System Keyboard",
        )

        if start_monitor and self.raw_monitor.is_windows:
            self.raw_monitor.start()

        # Failsafe cleanup on process termination
        atexit.register(self.disable)
        logger.info(
            f"WHID-Guard Firewall initialized (timeout: {self.max_suppression_duration}s, Auto-Guard: active)"
        )

    def start_monitor(self):
        """Start the Windows Raw Input hardware attribution listener."""
        if self.raw_monitor and self.raw_monitor.is_windows:
            self.raw_monitor.start()

    def stop_monitor(self):
        """Stop the Windows Raw Input hardware attribution listener."""
        if self.raw_monitor:
            self.raw_monitor.stop()

    def _on_raw_input_event(self, handle_hex: str, timestamp_ms: float):
        """Callback invoked by RawInputMonitor thread upon WM_INPUT."""
        dev_info = self.raw_monitor.devices.get(handle_hex)
        name = dev_info.name if dev_info else "Keyboard Device"
        vid = dev_info.vid if dev_info else None
        pid = dev_info.pid if dev_info else None

        self.dynamics_manager.register_device(handle_hex, name=name, vid=vid, pid=pid)

    def blocker(self, event):
        """
        Low-level keyboard hook callback.
        Returning False suppresses the keystroke on the host operating system.
        Returning None / True allows the keystroke to pass to the foreground window.
        """
        now_ms = time.perf_counter() * 1000.0

        # Determine device ID from Raw Input or fallback
        active_dev = self.raw_monitor.active_device_id or self.fallback_device_id

        # Update behavioral metrics
        metrics, is_quarantined = self.dynamics_manager.record_event(
            active_dev,
            timestamp_ms=now_ms,
        )
        self.global_engine.add_keystroke(timestamp_ms=now_ms)

        # Notify UI of new metrics
        if self._on_metrics_updated_callback:
            try:
                self._on_metrics_updated_callback(metrics, active_dev)
            except Exception:
                pass

        # 1. Manual full BLOCKING mode -> drop all keystrokes
        if self.enabled:
            return False

        # 2. Behavioral Quarantine mode -> drop keystrokes only from quarantined devices
        if self.auto_guard_enabled and is_quarantined:
            logger.warn(f"WHID-Guard: Suppressed keystroke from quarantined device {active_dev}")
            return False

        # Legitimate keystroke permitted
        return None

    def set_auto_disarm_callback(self, callback: Callable):
        self._on_auto_disarm_callback = callback

    def set_metrics_callback(self, callback: Callable):
        self._on_metrics_updated_callback = callback

    def install_hook(self):
        if self.hook is None:
            logger.info("Installing keyboard suppression hook")
            self.hook = keyboard.hook(self.blocker, suppress=True)

    def remove_hook(self):
        if self.hook is not None:
            logger.info("Removing keyboard suppression hook")
            try:
                keyboard.unhook(self.hook)
            except Exception as e:
                logger.warn(f"Exception during unhook: {e}")
            self.hook = None

    def _on_timeout(self):
        logger.warn("Watchdog timeout reached: Automatically disarming keystroke firewall for safety")
        self.disable()
        if self._on_auto_disarm_callback:
            try:
                self._on_auto_disarm_callback()
            except Exception:
                pass

    def enable(self):
        logger.info("Enable firewall")
        self.enabled = True
        self.install_hook()

        # Start safety watchdog timer
        if self._watchdog_timer is not None:
            self._watchdog_timer.cancel()
        if self.max_suppression_duration and self.max_suppression_duration > 0:
            self._watchdog_timer = threading.Timer(self.max_suppression_duration, self._on_timeout)
            self._watchdog_timer.daemon = True
            self._watchdog_timer.start()

    def disable(self):
        logger.info("Disable firewall")
        self.enabled = False

        if self._watchdog_timer is not None:
            self._watchdog_timer.cancel()
            self._watchdog_timer = None

        self.remove_hook()

    def toggle(self):
        logger.info("Toggle firewall")
        if self.enabled:
            self.disable()
        else:
            self.enable()

    def is_enabled(self):
        return self.enabled

    def reset_behavioral_state(self):
        """Clear all quarantines and reset sliding-window detectors."""
        self.dynamics_manager.clear_all_quarantines()
        self.global_engine.reset()
        logger.info("Behavioral state reset: All device quarantines released")


# ============================================================
# UI MODULE
# ============================================================

class UI:
    def __init__(self, firewall: Firewall):
        self.firewall = firewall
        self.root: Optional[tk.Tk] = None

        self.status_var: Optional[tk.StringVar] = None
        self.status_label: Optional[tk.Label] = None
        self.timer_var: Optional[tk.StringVar] = None
        self.timer_label: Optional[tk.Label] = None

        # Telemetry panel variables
        self.device_name_var: Optional[tk.StringVar] = None
        self.threat_var: Optional[tk.StringVar] = None
        self.threat_label: Optional[tk.Label] = None
        self.speed_var: Optional[tk.StringVar] = None
        self.mean_iki_var: Optional[tk.StringVar] = None
        self.cv_var: Optional[tk.StringVar] = None
        self.quarantine_var: Optional[tk.StringVar] = None

        self._countdown_remaining = 0
        self.firewall.set_auto_disarm_callback(self._on_auto_disarm)
        self.firewall.set_metrics_callback(self._on_metrics_updated)
        logger.info("UI created")

    def create_window(self):
        self.root = tk.Tk()
        self.root.title("WHID-Guard: Behavioral Keystroke Firewall")
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.configure(bg=Config.COLOR_BG)
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_title(self):
        title = tk.Label(
            self.root,
            text=Config.TITLE,
            font=Config.FONT_TITLE,
            fg=Config.COLOR_TEXT,
            bg=Config.COLOR_BG,
        )
        title.pack(pady=(12, 1))

        sub = tk.Label(
            self.root,
            text=Config.SUBTITLE,
            font=Config.FONT_SUBTITLE,
            fg=Config.COLOR_MUTED,
            bg=Config.COLOR_BG,
        )
        sub.pack(pady=(0, 6))

    def create_status(self):
        self.status_var = tk.StringVar(value="ALLOW")
        self.status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=Config.FONT_STATUS,
            fg=Config.COLOR_GREEN,
            bg=Config.COLOR_BG,
        )
        self.status_label.pack(pady=2)

        self.timer_var = tk.StringVar(value="Auto-Guard: Monitoring Dynamics (WH_KEYBOARD_LL Active)")
        self.timer_label = tk.Label(
            self.root,
            textvariable=self.timer_var,
            font=Config.FONT_TIMER,
            fg="#94a3b8",
            bg=Config.COLOR_BG,
        )
        self.timer_label.pack(pady=(0, 6))

    def create_telemetry_card(self):
        """Telemetry Card showing real-time Keystroke Dynamics & Raw Input device info."""
        card = tk.Frame(
            self.root,
            bg=Config.COLOR_CARD,
            bd=1,
            relief="solid",
            highlightbackground=Config.COLOR_BORDER,
            highlightthickness=1,
        )
        card.pack(fill="x", padx=16, pady=4)

        # Header: Threat Level & Active Device
        top_frame = tk.Frame(card, bg=Config.COLOR_CARD)
        top_frame.pack(fill="x", padx=10, pady=(8, 4))

        tk.Label(
            top_frame,
            text="ATTRIBUTED DEVICE:",
            font=Config.FONT_METRIC_LABEL,
            fg=Config.COLOR_MUTED,
            bg=Config.COLOR_CARD,
        ).pack(side="left")

        self.threat_var = tk.StringVar(value="SAFE")
        self.threat_label = tk.Label(
            top_frame,
            textvariable=self.threat_var,
            font=("Segoe UI", 9, "bold"),
            fg=Config.COLOR_GREEN,
            bg="#064e3b",
            padx=6,
            pady=1,
        )
        self.threat_label.pack(side="right")

        self.device_name_var = tk.StringVar(value="Listening for USB / PS/2 Keystrokes...")
        tk.Label(
            card,
            textvariable=self.device_name_var,
            font=("Segoe UI", 9, "bold"),
            fg=Config.COLOR_TEXT,
            bg=Config.COLOR_CARD,
            anchor="w",
        ).pack(fill="x", padx=10, pady=(0, 6))

        # Metrics Grid
        grid_frame = tk.Frame(card, bg=Config.COLOR_CARD)
        grid_frame.pack(fill="x", padx=10, pady=4)

        # Speed
        f1 = tk.Frame(grid_frame, bg=Config.COLOR_CARD)
        f1.pack(side="left", expand=True, fill="x")
        tk.Label(f1, text="BURST SPEED", font=Config.FONT_METRIC_LABEL, fg=Config.COLOR_MUTED, bg=Config.COLOR_CARD).pack(anchor="w")
        self.speed_var = tk.StringVar(value="0.0 ch/s")
        tk.Label(f1, textvariable=self.speed_var, font=Config.FONT_METRIC_VAL, fg=Config.COLOR_TEXT, bg=Config.COLOR_CARD).pack(anchor="w")

        # Mean IKI
        f2 = tk.Frame(grid_frame, bg=Config.COLOR_CARD)
        f2.pack(side="left", expand=True, fill="x")
        tk.Label(f2, text="MEAN IKI", font=Config.FONT_METRIC_LABEL, fg=Config.COLOR_MUTED, bg=Config.COLOR_CARD).pack(anchor="w")
        self.mean_iki_var = tk.StringVar(value="0.0 ms")
        tk.Label(f2, textvariable=self.mean_iki_var, font=Config.FONT_METRIC_VAL, fg=Config.COLOR_TEXT, bg=Config.COLOR_CARD).pack(anchor="w")

        # CV
        f3 = tk.Frame(grid_frame, bg=Config.COLOR_CARD)
        f3.pack(side="left", expand=True, fill="x")
        tk.Label(f3, text="CADENCE CV", font=Config.FONT_METRIC_LABEL, fg=Config.COLOR_MUTED, bg=Config.COLOR_CARD).pack(anchor="w")
        self.cv_var = tk.StringVar(value="0.0000")
        tk.Label(f3, textvariable=self.cv_var, font=Config.FONT_METRIC_VAL, fg=Config.COLOR_TEXT, bg=Config.COLOR_CARD).pack(anchor="w")

        # Quarantine Status
        q_frame = tk.Frame(card, bg=Config.COLOR_CARD)
        q_frame.pack(fill="x", padx=10, pady=(4, 8))
        tk.Label(q_frame, text="ISOLATION STATUS:", font=Config.FONT_METRIC_LABEL, fg=Config.COLOR_MUTED, bg=Config.COLOR_CARD).pack(side="left")
        self.quarantine_var = tk.StringVar(value="All Devices Authorized")
        tk.Label(q_frame, textvariable=self.quarantine_var, font=("Segoe UI", 8, "bold"), fg=Config.COLOR_GREEN, bg=Config.COLOR_CARD).pack(side="right")

    def create_buttons(self):
        btn_frame = tk.Frame(self.root, bg=Config.COLOR_BG)
        btn_frame.pack(fill="x", padx=16, pady=6)

        # Toggle Button
        btn_toggle = tk.Button(
            btn_frame,
            text="MANUAL OVERRIDE",
            command=self.on_toggle,
            font=Config.FONT_BUTTON,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            height=1,
            bd=0,
            cursor="hand2",
        )
        btn_toggle.pack(side="left", expand=True, fill="x", padx=(0, 4))

        # Reset / Clear Button
        btn_reset = tk.Button(
            btn_frame,
            text="RESET DETECTOR",
            command=self.on_reset,
            font=Config.FONT_BUTTON,
            bg=Config.COLOR_BUTTON,
            fg="white",
            activebackground=Config.COLOR_BUTTON_ACTIVE,
            activeforeground="white",
            height=1,
            bd=0,
            cursor="hand2",
        )
        btn_reset.pack(side="right", expand=True, fill="x", padx=(4, 0))

    def create_footer(self):
        footer = tk.Label(
            self.root,
            text=Config.FOOTER,
            font=Config.FONT_FOOTER,
            fg="#64748b",
            bg=Config.COLOR_BG,
        )
        footer.pack(side="bottom", pady=6)

    def _on_metrics_updated(self, metrics: KeystrokeMetrics, dev_id: str):
        """Thread-safe UI update from firewall blocker callback."""
        if not self.root:
            return

        def _update():
            # Update active device
            dev_info = self.firewall.raw_monitor.devices.get(dev_id)
            if dev_info:
                name_str = f"{dev_info.name} [{dev_id}]"
            else:
                name_str = f"Device {dev_id}"
            if self.device_name_var:
                self.device_name_var.set(name_str)

            # Update Metrics
            if self.speed_var:
                self.speed_var.set(f"{metrics.burst_rate:.1f} ch/s")
            if self.mean_iki_var:
                self.mean_iki_var.set(f"{metrics.mean_iki:.1f} ms")
            if self.cv_var:
                self.cv_var.set(f"{metrics.cv_iki:.4f}")

            # Update Threat Label & Quarantine
            if self.threat_var and self.threat_label:
                t = metrics.threat_level
                if t == ThreatLevel.LOCKED_DOWN:
                    self.threat_var.set("MACHINE INJECTION")
                    self.threat_label.config(fg="#fecaca", bg="#7f1d1d")
                elif t == ThreatLevel.SUSPICIOUS:
                    self.threat_var.set("SUSPICIOUS")
                    self.threat_label.config(fg="#fef3c7", bg="#78350f")
                else:
                    self.threat_var.set("SAFE (HUMAN)")
                    self.threat_label.config(fg=Config.COLOR_GREEN, bg="#064e3b")

            if self.quarantine_var:
                quarantined = self.firewall.dynamics_manager.quarantined_devices
                if quarantined:
                    q_list = ", ".join(quarantined)
                    self.quarantine_var.set(f"QUARANTINED: {q_list}")
                else:
                    self.quarantine_var.set("All Devices Authorized")

        try:
            self.root.after(0, _update)
        except Exception:
            pass

    def set_allow(self):
        self.status_var.set("ALLOW")
        self.status_label.config(fg=Config.COLOR_GREEN)
        self.timer_var.set("Auto-Guard: Monitoring Dynamics (WH_KEYBOARD_LL Active)")
        self._countdown_remaining = 0

    def set_block(self):
        self.status_var.set("BLOCKING")
        self.status_label.config(fg=Config.COLOR_RED)
        self._countdown_remaining = self.firewall.max_suppression_duration
        self._update_countdown()

    def _update_countdown(self):
        if self.firewall.is_enabled() and self._countdown_remaining > 0:
            self.timer_var.set(f"Manual Override Safety Timer: {self._countdown_remaining}s")
            self._countdown_remaining -= 1
            if self.root:
                self.root.after(1000, self._update_countdown)
        elif not self.firewall.is_enabled():
            self.set_allow()

    def _on_auto_disarm(self):
        if self.root:
            self.root.after(0, self.set_allow)

    def on_toggle(self):
        logger.info("Manual toggle pressed")
        self.firewall.toggle()
        if self.firewall.is_enabled():
            self.set_block()
        else:
            self.set_allow()

    def on_reset(self):
        logger.info("Reset detector button pressed")
        self.firewall.reset_behavioral_state()
        if self.speed_var:
            self.speed_var.set("0.0 ch/s")
        if self.mean_iki_var:
            self.mean_iki_var.set("0.0 ms")
        if self.cv_var:
            self.cv_var.set("0.0000")
        if self.threat_var and self.threat_label:
            self.threat_var.set("SAFE")
            self.threat_label.config(fg=Config.COLOR_GREEN, bg="#064e3b")
        if self.quarantine_var:
            self.quarantine_var.set("All Devices Authorized")

    def on_close(self):
        logger.info("Closing application window, releasing active hooks and threads")
        self.firewall.disable()
        self.firewall.stop_monitor()
        if self.root:
            self.root.destroy()

    def build(self):
        self.create_window()
        self.create_title()
        self.create_status()
        self.create_telemetry_card()
        self.create_buttons()
        self.create_footer()

    def run(self):
        logger.info("UI started")
        self.firewall.start_monitor()
        self.root.mainloop()


# ============================================================
# APPLICATION MODULE
# ============================================================

class App:
    def __init__(self):
        logger.info("App starting")
        self.firewall = Firewall()
        self.ui = UI(self.firewall)

    def setup(self):
        logger.info("Setup")
        self.ui.build()

    def run(self):
        logger.info("Run")
        self.ui.run()


# ============================================================
# MAIN
# ============================================================

def main():
    logger.info("Main")
    app = App()
    app.setup()
    app.run()


if __name__ == "__main__":
    main()
