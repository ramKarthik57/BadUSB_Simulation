# Usage Guide

1. Activate Python virtual environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Start the app: `python firewall.py`.
4. Click TOGGLE to switch block mode.
5. Watch console logs.

## Programmatic usage

```python
from firewall import Firewall

fw = Firewall()
fw.enable()
# now keyboard state is blocked while hook is active
fw.disable()
```
