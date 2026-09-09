import pypdf
import sys

sys.stdout.reconfigure(encoding='utf-8')

for cat in ['7.3.1_QS_Series_Catalogue.pdf', '7.3.2_QSR_Series_Catalogue.pdf', '7.4.0_LQ_LiquidCooled_Catalogue.pdf']:
    path = rf"c:\Users\maximr\OneDrive - ac.sce.ac.il\Barabi\2025 Eli & Max\PMSM\Datasheets_and_Docs\OEMER_Catalogues\{cat}"
    reader = pypdf.PdfReader(path)
    print(f"==================== {cat} (Page 2 & Page 4) ====================")
    for p_num in [1, 2, 3]:
        if p_num < len(reader.pages):
            txt = reader.pages[p_num].extract_text()
            print(f"\n--- Page {p_num+1} ---")
            lines = [l for l in txt.split('\n') if any(w in l.lower() for w in ['pol', 'hz', 'rpm', 'frequen', 'f_n', 'speed', 'qs 100', 'qsr 100', '100s', '100m', '100l'])]
            for l in lines:
                print("  ", l)
