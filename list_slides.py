import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('OEPC_SE_VSI_PMSM_Presentation_HE.html', encoding='utf-8') as f:
    text = f.read()

slide_chunks = re.split(r'<div class="slide(?:\s+[^"]*)?"', text)
for i, chunk in enumerate(slide_chunks[1:], start=1):
    id_m = re.search(r'id="([^"]+)"', chunk[:200])
    s_id = id_m.group(1) if id_m else 'none'
    title_m = re.search(r'<div class="slide-title">(.*?)</div>', chunk, re.DOTALL)
    s_title = title_m.group(1).strip() if title_m else 'No title'
    cat_m = re.search(r'<div class="slide-category">(.*?)</div>', chunk, re.DOTALL)
    s_cat = cat_m.group(1).strip() if cat_m else 'No category'
    print(f"Slide {i} (id={s_id}): [{s_cat}] {s_title}")
