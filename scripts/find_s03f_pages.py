import subprocess
import re

def search_loci():
    loci_targets = {
        "1 Cor 1:19": [r"Isa\.\s*xxix\.\s*14", r"ἀπολῶ\s*τὴν\s*σοφίαν", r"γέγραπται\s*γάρ"],
        "1 Cor 6:16": [r"Gen\.\s*ii\.\s*24", r"εἰς\s*σάρκα\s*μίαν", r"ἔσονται\s*γάρ"],
        "1 Cor 9:9": [r"Deut\.\s*xxv\.\s*4", r"φιμώσεις", r"βοῦν\s*ἀλοῶντα"],
        "1 Cor 10:7": [r"Exod\.\s*xxxii\.\s*6", r"ἐκάθισεν\s*ὁ\s*λαὸς", r"παίζειν"],
        "1 Cor 15:54-55": [r"Isa\.\s*xxv\.\s*8", r"Hos\.\s*xiii\.\s*14", r"κατεπόθη\s*ὁ\s*θάνατος", r"ποῦ\s*σου\s*θάνατε"]
    }
    
    out = subprocess.check_output(["pdftotext", "-layout", "/Users/chrisrodriguez/Downloads/robertson_plummer_1911_1corinthians_icc_ia_raw.pdf", "-"])
    pages = out.decode("utf-8", errors="replace").split("\x0c")
    print(f"Total pages extracted: {len(pages)}")
    
    for locus, patterns in loci_targets.items():
        print(f"\n=== Searching for {locus} ===")
        seen_pages = set()
        for p_idx, page_text in enumerate(pages):
            for pat in patterns:
                if re.search(pat, page_text, re.IGNORECASE):
                    if p_idx + 1 not in seen_pages:
                        seen_pages.add(p_idx + 1)
                        lines = [ln.strip() for ln in page_text.split("\n") if ln.strip()]
                        hdr = lines[0] if lines else ""
                        print(f"  PDF Page {p_idx + 1} (Header: {hdr[:50]}): pattern '{pat}'")

if __name__ == "__main__":
    search_loci()
