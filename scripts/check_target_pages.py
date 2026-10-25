import subprocess

target_pages = (
    list(range(9, 17)) +       # Front matter (9-16, printed vii-x)
    list(range(58, 69)) +      # Intro: Quotations & Text (58-68, printed lii-lxii)
    list(range(93, 99)) +      # 1 Cor 1:17-25 (93-98, printed 17-22)
    list(range(200, 207)) +    # 1 Cor 6:12-20 (200-206, printed 124-130)
    list(range(257, 265)) +    # 1 Cor 9:7-14 (257-264, printed 181-188)
    list(range(276, 285)) +    # 1 Cor 10:1-13 (276-284, printed 200-208)
    list(range(452, 458)) +    # 1 Cor 15:50-58 (452-457, printed 376-381)
    list(range(479, 483)) +    # Index I (479-482, printed 403-406)
    list(range(489, 493))      # Index I end & Index II start (489-492, printed 413-416)
)

print(f"Total pages in target derivative: {len(target_pages)}")
for p in target_pages:
    out = subprocess.check_output([
        "pdftotext", "-f", str(p), "-l", str(p), "-layout",
        "/Users/chrisrodriguez/Downloads/robertson_plummer_1911_1corinthians_icc_ia_raw.pdf", "-"
    ])
    lines = [ln.strip() for ln in out.decode("utf-8", errors="replace").split("\n") if ln.strip()]
    hdr = lines[0] if lines else "[EMPTY]"
    print(f"PDF p.{p:3d}: {hdr[:60]}")
