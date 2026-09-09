# 1. Sync generate_hebrew_presentation.py
with open('OEPC_SE_VSI_PMSM_Presentation_HE.html', encoding='utf-8') as f:
    he_html = f.read()

with open('generate_hebrew_presentation.py', encoding='utf-8') as f:
    py_he = f.read()

start_marker_he = 'html_he_content = r"""'
end_marker_he = '\n"""\n\n# Write Hebrew HTML presentation'

p1 = py_he.find(start_marker_he) + len(start_marker_he)
p2 = py_he.find(end_marker_he)
if p1 != -1 and p2 != -1:
    new_py_he = py_he[:p1] + he_html + py_he[p2:]
    with open('generate_hebrew_presentation.py', 'w', encoding='utf-8') as f:
        f.write(new_py_he)
    print("[OK] Synced generate_hebrew_presentation.py successfully!")
else:
    print("[FAIL] Markers not found in generate_hebrew_presentation.py")

# 2. Sync generate_html_presentation.py
with open('OEPC_SE_VSI_PMSM_Presentation.html', encoding='utf-8') as f:
    en_html = f.read()

with open('generate_html_presentation.py', encoding='utf-8') as f:
    py_en = f.read()

start_marker_en = 'html_content = r"""'
end_marker_en = '\n"""\n\nwith open(PMSM_DIR / "OEPC_SE_VSI_PMSM_Presentation.html"'

p1_en = py_en.find(start_marker_en) + len(start_marker_en)
p2_en = py_en.find(end_marker_en)
if p1_en != -1 and p2_en != -1:
    new_py_en = py_en[:p1_en] + en_html + py_en[p2_en:]
    with open('generate_html_presentation.py', 'w', encoding='utf-8') as f:
        f.write(new_py_en)
    print("[OK] Synced generate_html_presentation.py successfully!")
else:
    print("[FAIL] Markers not found in generate_html_presentation.py")
