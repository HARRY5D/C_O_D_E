"""
Script to move existing PDFs from data/ root to data/raw/
"""
import shutil
from pathlib import Path

data_dir = Path("data")
raw_dir = data_dir / "raw"
raw_dir.mkdir(exist_ok=True)

pdfs = list(data_dir.glob("*.pdf"))
print(f"Found {len(pdfs)} PDFs to move:")
for pdf in pdfs:
    dest = raw_dir / pdf.name
    if not dest.exists():
        shutil.move(str(pdf), str(dest))
        print(f"  [OK] Moved: {pdf.name}")
    else:
        print(f"  [SKIP] Already exists: {pdf.name}")

print(f"\nAll PDFs are now in: {raw_dir}")
