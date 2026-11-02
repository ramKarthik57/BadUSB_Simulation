import os
import shutil
import zipfile

src_root = r"C:\Users\Ram\Desktop\BadUSB_Using_ESP32"
paper_dir = os.path.join(src_root, "paper")
figures_source_dir = os.path.join(src_root, "figures", "source")
scripts_dir = os.path.join(src_root, "scripts")

dest_dirs = [
    os.path.join(src_root, "WHID_GUARD_STANDALONE_SOURCE"),
    r"C:\Users\Ram\Desktop\WHID_GUARD_STANDALONE_SOURCE",
]

for dest in dest_dirs:
    os.makedirs(dest, exist_ok=True)
    fig_dest = os.path.join(dest, "figure_sources")
    os.makedirs(fig_dest, exist_ok=True)

    # 1. LaTeX core files
    shutil.copy2(os.path.join(paper_dir, "WHID_GUARD_2027.tex"), dest)
    shutil.copy2(os.path.join(paper_dir, "IEEEtran.cls"), dest)
    shutil.copy2(os.path.join(paper_dir, "WHID_GUARD_2027.pdf"), dest)

    # 2. Figures used directly by pdflatex
    fig_names = [
        "system_architecture.pdf",
        "system_architecture.png",
        "fsm_diagram.pdf",
        "fsm_diagram.png",
        "defense_architecture.pdf",
        "defense_architecture.png",
        "fig_iki_distribution.pdf",
        "fig_iki_distribution.png",
        "fig_detection_latency.pdf",
        "fig_detection_latency.png",
    ]
    for fn in fig_names:
        src_path = os.path.join(paper_dir, fn)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest)

    # 3. Figure source models (.svg, .drawio, .mmd)
    if os.path.exists(figures_source_dir):
        for f in os.listdir(figures_source_dir):
            shutil.copy2(os.path.join(figures_source_dir, f), fig_dest)

    # 4. Figure generation Python scripts
    gen_scripts = [
        "rectify_all_inconsistencies.py",
        "make_flawless_fig1.py",
        "make_flawless_fig2.py",
        "make_flawless_fig3.py",
        "make_flawless_fig4.py",
        "make_flawless_fig5.py",
        "update_drawio_and_mmd.py",
        "audit_all_figures.py",
        "verify_pdf_perfection.py",
    ]
    for gs in gen_scripts:
        src_path = os.path.join(scripts_dir, gs)
        if os.path.exists(src_path):
            shutil.copy2(src_path, fig_dest)

    # 5. Build scripts
    build_bat = (
        "@echo off\n"
        "echo ========================================================\n"
        "echo Compiling WHID-Guard 2027 IEEE Paper...\n"
        "echo ========================================================\n"
        "pdflatex -interaction=nonstopmode WHID_GUARD_2027.tex\n"
        "pdflatex -interaction=nonstopmode WHID_GUARD_2027.tex\n"
        "echo Done! Output generated: WHID_GUARD_2027.pdf\n"
        "pause\n"
    )
    with open(os.path.join(dest, "build.bat"), "w", encoding="utf-8") as f:
        f.write(build_bat)

    build_sh = (
        "#!/bin/bash\n"
        "set -e\n"
        "echo '========================================================'\n"
        "echo 'Compiling WHID-Guard 2027 IEEE Paper...'\n"
        "echo '========================================================'\n"
        "pdflatex -interaction=nonstopmode WHID_GUARD_2027.tex\n"
        "pdflatex -interaction=nonstopmode WHID_GUARD_2027.tex\n"
        "echo 'Done! Output generated: WHID_GUARD_2027.pdf'\n"
    )
    with open(
        os.path.join(dest, "build.sh"), "w", encoding="utf-8", newline="\n"
    ) as f:
        f.write(build_sh)

    # 6. Comprehensive README.md
    readme_content = """# WHID-Guard 2027 - Standalone Manuscript Source Package

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
"""
    with open(os.path.join(dest, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"Populated {dest}")

# Create a zip archive of the desktop standalone package
desktop_pkg = r"C:\Users\Ram\Desktop\WHID_GUARD_STANDALONE_SOURCE"
zip_dest = r"C:\Users\Ram\Desktop\WHID_GUARD_STANDALONE_SOURCE.zip"
with zipfile.ZipFile(zip_dest, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(desktop_pkg):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, desktop_pkg)
            z.write(full_path, rel_path)

print(
    f"Created standalone zip archive: {zip_dest} ({os.path.getsize(zip_dest)} bytes)"
)
