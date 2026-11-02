import time
import pytest
from src import firewall


class DummyHook:
    pass


def test_firewall_initial_state():
    fw = firewall.Firewall()
    assert fw.is_enabled() is False
    assert fw.hook is None
    assert fw.max_suppression_duration == firewall.Config.DEFAULT_MAX_SUPPRESSION_SECONDS


def test_firewall_enable_disable(monkeypatch):
    installed = {}

    def fake_hook(callback, suppress):
        installed['callback'] = callback
        installed['suppress'] = suppress
        installed['hook'] = DummyHook()
        return installed['hook']

    def fake_unhook(hook):
        assert hook is installed['hook']
        installed['unhooked'] = True

    monkeypatch.setattr(firewall.keyboard, 'hook', fake_hook)
    monkeypatch.setattr(firewall.keyboard, 'unhook', fake_unhook)

    fw = firewall.Firewall(max_suppression_duration=0)  # Disable timer for this test

    fw.enable()
    assert fw.is_enabled() is True
    assert isinstance(fw.hook, DummyHook)
    assert installed['callback'].__func__ is fw.blocker.__func__
    assert installed['callback'].__self__ is fw
    assert installed['suppress'] is True

    # call blocker to ensure function returns False (blocks keys)
    ev = type('E', (), {})()
    assert fw.blocker(ev) is False

    fw.disable()
    assert fw.is_enabled() is False
    assert fw.hook is None
    assert installed.get('unhooked', False) is True


def test_toggle(monkeypatch):
    monkeypatch.setattr(firewall.keyboard, 'hook', lambda cb, suppress: DummyHook())
    monkeypatch.setattr(firewall.keyboard, 'unhook', lambda hook: None)

    fw = firewall.Firewall(max_suppression_duration=0)
    fw.toggle()
    assert fw.is_enabled() is True
    fw.toggle()
    assert fw.is_enabled() is False


def test_auto_disarm_timer(monkeypatch):
    monkeypatch.setattr(firewall.keyboard, 'hook', lambda cb, suppress: DummyHook())
    monkeypatch.setattr(firewall.keyboard, 'unhook', lambda hook: None)

    disarmed = []
    fw = firewall.Firewall(max_suppression_duration=0.1)  # 100ms timeout
    fw.set_auto_disarm_callback(lambda: disarmed.append(True))

    fw.enable()
    assert fw.is_enabled() is True

    # Wait for timer to expire
    time.sleep(0.2)

    assert fw.is_enabled() is False
    assert len(disarmed) == 1
