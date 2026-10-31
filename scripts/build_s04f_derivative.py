#!/usr/bin/env python3
"""Build authentic source-faithful derivative PDF for S04F (Lightfoot 1914 Galatians)."""

import hashlib
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

RAW_PDF = Path("/Users/chrisrodriguez/Downloads/lightfoot_1914_galatians_ia_raw.pdf")
TARGET_PDF = Path("/Users/chrisrodriguez/Downloads/lightfoot_1914_galatians.pdf")

TARGET_PAGES = (
    list(range(9, 21)) +       # Front matter (PDF 9-20, printed vii-xiv: half-title, title, preface, contents)
    list(range(77, 89)) +      # Intro IV & V (PDF 77-88, printed 57-68: Genuineness, Character & Contents)
    list(range(134, 144)) +    # Gal 2:15-21 (PDF 134-143, printed 114-123: Gal 2:16 on Ps 143:2, Gal 2:21)
    list(range(153, 185)) +    # Gal 3 complete (PDF 153-184, printed 133-164: Gal 3:6 Gen 15:6, Gal 3:10 Deut 27:26, Gal 3:11 Hab 2:4, Gal 3:12 Lev 18:5, Gal 3:13 Deut 21:23, Gal 3:16 Gen 13:15, and 3 Excursuses pp. 152-164)
    list(range(199, 206)) +    # Gal 4:21-31 (PDF 199-205, printed 179-185: Hagar/Sarah allegory, Gal 4:27 Isa 54:1)
    list(range(213, 221)) +    # Excursuses on Hagar & Philo (PDF 213-220, printed 193-200)
    list(range(395, 405))      # Complete Index (PDF 395-404, printed 375-384)
)

def build_derivative():
    if not RAW_PDF.is_file():
        raise FileNotFoundError(f"Raw PDF not found: {RAW_PDF}")

    print(f"Building S04F derivative from {len(TARGET_PAGES)} selected pages...")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # 1. Extract each selected page
        page_files = []
        for idx, p in enumerate(TARGET_PAGES):
            out_page = tmp_path / f"page_{idx+1:03d}.pdf"
            subprocess.run([
                "pdfseparate", "-f", str(p), "-l", str(p),
                str(RAW_PDF), str(out_page)
            ], check=True)
            page_files.append(str(out_page))

        # 2. Unite into uncompressed derivative
        raw_united = tmp_path / "united.pdf"
        subprocess.run(["pdfunite"] + page_files + [str(raw_united)], check=True)
        raw_size = raw_united.stat().st_size
        print(f"United PDF size: {raw_size:,} bytes ({raw_size/(1024*1024):.2f} MB)")

        # 3. Optimize via Ghostscript (-dPDFSETTINGS=/ebook)
        gs_cmd = [
            "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS=/ebook", "-dNOPAUSE", "-dQUIET", "-dBATCH",
            f"-sOutputFile={TARGET_PDF}", str(raw_united)
        ]
        print("Optimizing with Ghostscript...")
        subprocess.run(gs_cmd, check=True)

    final_size = TARGET_PDF.stat().st_size
    final_sha = hashlib.sha256(TARGET_PDF.read_bytes()).hexdigest()
    print(f"\nSUCCESS: Generated {TARGET_PDF.name}")
    print(f"  Pages: {len(TARGET_PAGES)}")
    print(f"  Size:  {final_size:,} bytes ({final_size/(1024*1024):.2f} MB)")
    print(f"  SHA256: {final_sha}")

if __name__ == "__main__":
    build_derivative()
