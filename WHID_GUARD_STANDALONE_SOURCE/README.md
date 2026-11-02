# WHID-Guard 2027 - Standalone Manuscript Source Package

This directory contains the complete, self-contained source files required to build, edit, and reproduce the IEEE conference paper:
**"WHID-Guard: Behavioral Keystroke Dynamics and Per-Device Isolation Against Wireless Composite BadUSB Attacks"**

---

## 1. Quick Recompilation

### Windows (Command Prompt / PowerShell):
Double-click `build.bat` or run:
```cmd
pdflatex -interaction=nonstopmode WHID_GUARD_2027.tex
pdflatex -interaction=nonstopmode WHID_GUARD_2027.tex
```

### Linux / macOS / WSL:
```bash
chmod +x build.sh
./build.sh
```

---

## 2. Directory Contents

- `WHID_GUARD_2027.tex`: Complete LaTeX source manuscript with inline bibliography (self-contained, no external .bib file required).
- `IEEEtran.cls`: Official IEEE conference LaTeX document class.
- `WHID_GUARD_2027.pdf`: The verified camera-ready 6.0-page PDF reference output.
- `system_architecture.pdf` / `.png`: Figure 1 (System Architecture).
- `fsm_diagram.pdf` / `.png`: Figure 2 (Adversarial FSM).
- `defense_architecture.pdf` / `.png`: Figure 3 (Selective Defense Architecture).
- `fig_iki_distribution.pdf` / `.png`: Figure 4 (Empirical IKI Distribution).
- `fig_detection_latency.pdf` / `.png`: Figure 5 (Quarantine Latency & Reaction Time).
- `figure_sources/`: Editable vector source files (`.svg`, `.drawio`, `.mmd`) and Python figure generator scripts.

---

## 3. Manuscript Specs & Constraints

- **Page Limit**: Exactly 6.0 pages.
- **Font Standard**: 100% Vector Type 1 fonts (Zero Type 3 bitmap fonts).
- **Column Balance**: Page 6 column delta <= 15.0 pt.
