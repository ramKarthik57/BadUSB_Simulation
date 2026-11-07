import shutil
import zipfile
import os

brain_dir = "C:/Users/Ram/.gemini/antigravity/brain/ce8071ad-ae44-4bc1-99a9-e4d2c343777c"
whid_dir = "C:/Users/Ram/Desktop/BadUSB_Using_ESP32/paper/PIC2026"

# Copy PDFs to brain
shutil.copy2(os.path.join(whid_dir, "WHID_GUARD_PIC2026_CAMERA_READY.pdf"), os.path.join(brain_dir, "WHID_GUARD_PIC2026_CAMERA_READY.pdf"))
shutil.copy2(os.path.join(whid_dir, "WHID_GUARD_PIC2026_DOUBLE_BLIND.pdf"), os.path.join(brain_dir, "WHID_GUARD_PIC2026_DOUBLE_BLIND.pdf"))
print("Copied updated WHID PDFs to brain artifact directory.")

# Update ZIP
zip_path = os.path.join(whid_dir, "WHID_GUARD_PIC2026_SUBMISSION_BUNDLE.zip")
if os.path.exists(zip_path):
    os.remove(zip_path)

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(whid_dir):
        for file in files:
            if file.endswith('.zip') or file.endswith('.aux') or file.endswith('.log'):
                continue
            full_path = os.path.join(root, file)
            arc_name = os.path.relpath(full_path, whid_dir)
            zipf.write(full_path, arc_name)

print("Created WHID_GUARD_PIC2026_SUBMISSION_BUNDLE.zip successfully. Size:", os.path.getsize(zip_path))
