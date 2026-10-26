import hashlib
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

RAW_PDF = Path("/Users/chrisrodriguez/Downloads/robertson_plummer_1911_1corinthians_icc_ia_raw.pdf")
TARGET_PDF = Path("/Users/chrisrodriguez/Downloads/robertson_plummer_1911_1corinthians_icc.pdf")

TARGET_PAGES = (
    list(range(9, 17)) +       # Front matter (9-16, printed vii-x)
    list(range(58, 69)) +      # Intro: Quotations & Text (58-68, printed lii-lxii)
    list(range(77, 80)) +      # 1 Cor 1:1-3 (77-79, printed 1-3: Joel 2:32 / Rom 10:12-13 on 1:2)
    list(range(93, 99)) +      # 1 Cor 1:17-25 (93-98, printed 17-22: Isa 29:14 on 1:19)
    list(range(124, 129)) +    # 1 Cor 2:13-3:4 (124-128, printed 48-52: Isa 40:13 / Rom 11:34 on 2:16)
    list(range(200, 207)) +    # 1 Cor 6:12-20 (200-206, printed 124-130: Gen 2:24 on 6:16)
    list(range(257, 265)) +    # 1 Cor 9:7-14 (257-264, printed 181-188: Deut 25:4 on 9:9)
    list(range(276, 285)) +    # 1 Cor 10:1-13 (276-284, printed 200-208: Exod 32:6 on 10:7)
    list(range(452, 458)) +    # 1 Cor 15:50-58 (452-457, printed 376-381: Isa 25:8 / Hos 13:14 on 15:54-55)
    list(range(479, 483)) +    # Index I (479-482, printed 403-406)
    list(range(489, 493))      # Index I end & Index II start (489-492, printed 413-416)
)

def build_derivative():
    if not RAW_PDF.is_file():
        raise FileNotFoundError(f"Raw PDF not found: {RAW_PDF}")
        
    print(f"Building S03F derivative from {len(TARGET_PAGES)} selected pages...")
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
    
    # 4. Verify page count of final derivative
    info_out = subprocess.check_output(["pdfinfo", str(TARGET_PDF)]).decode()
    pages_line = [ln for ln in info_out.split("\n") if ln.startswith("Pages:")][0]
    
    print(f"SUCCESS: Built {TARGET_PDF.name}")
    print(f"  {pages_line.strip()}")
    print(f"  Size: {final_size:,} bytes ({final_size/(1024*1024):.2f} MB)")
    print(f"  SHA-256: {final_sha}")

if __name__ == "__main__":
    build_derivative()
