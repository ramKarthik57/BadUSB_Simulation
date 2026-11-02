"""Simple simulation script for Firewall module."""

from firewall import Firewall
import time

fw = Firewall()
print("Initial enabled:", fw.is_enabled())

print("Enabling firewall...")
fw.enable()
print("Enabled:", fw.is_enabled())

print("Sleeping 2 seconds while firewall would block keys...")
time.sleep(2)

print("Disabling firewall...")
fw.disable()
print("Enabled:", fw.is_enabled())
