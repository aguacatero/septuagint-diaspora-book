import subprocess

def inspect_range(start_p, end_p, label):
    print(f"\n================ {label} (PDF pp. {start_p}-{end_p}) ================")
    out = subprocess.check_output([
        "pdftotext", "-f", str(start_p), "-l", str(end_p), "-layout",
        "/Users/chrisrodriguez/Downloads/robertson_plummer_1911_1corinthians_icc_ia_raw.pdf", "-"
    ])
    text = out.decode("utf-8", errors="replace")
    pages = text.split("\x0c")
    for idx, p in enumerate(pages[:-1]):
        pdf_p = start_p + idx
        lines = [ln.strip() for ln in p.split("\n") if ln.strip()]
        hdr = lines[0] if lines else "[EMPTY]"
        last = lines[-1] if lines else "[EMPTY]"
        print(f"--- PDF Page {pdf_p} ---")
        print(f"Header: {hdr}")
        for ln in lines[1:8]:
            print(f"  {ln}")
        print(f"Footer: {last}")

inspect_range(9, 14, "Title & Preface")
inspect_range(58, 65, "Intro: Quotations & Textual Criticism")
inspect_range(93, 97, "1 Cor 1:18-21 (B001-8)")
inspect_range(200, 206, "1 Cor 6:12-20 (B001-9)")
inspect_range(257, 263, "1 Cor 9:7-14 (B001-10)")
inspect_range(277, 283, "1 Cor 10:5-11 (B001-11)")
inspect_range(453, 458, "1 Cor 15:53-58 (15:54-55)")
