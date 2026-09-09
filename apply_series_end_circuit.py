import os
import sys
from circuit_code_template import get_render_circuit_code

def update_presentation(filepath, is_hebrew=True):
    print(f"Updating {filepath} (Hebrew={is_hebrew})...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Title & Note
    old_title_he = "<span>🔌</span> מעגל אלקטרוני חי (איור 2)"
    old_title_en = "<span>🔌</span> Live Circuit Simulation (Fig. 2)"
    new_title_he = "<span>🔌</span> מעגל Series-End VSI וסלילים טוריים (איור 2)"
    new_title_en = "<span>🔌</span> Series-End VSI & Open-End Windings (Fig. 2)"

    target_title = old_title_he if is_hebrew else old_title_en
    rep_title = new_title_he if is_hebrew else new_title_en

    if target_title in content:
        content = content.replace(target_title, rep_title)
        print("  [+] Title updated!")
    elif (new_title_he in content) or (new_title_en in content):
        print("  [i] Title already modern.")

    # 2. Update subtitle / explanatory note
    note_he = '<div style="font-size:0.68rem; color:var(--text-muted); text-align:center; margin-top:2px; font-weight:500;">חיבור סלילים טורי בין ענפי הממיר L1-L4 (ללא כוכב וללא משולש)</div>'
    note_en = '<div style="font-size:0.68rem; color:var(--text-muted); text-align:center; margin-top:2px; font-weight:500;">Series Windings between Inverter Legs L1-L4 (Open-End, No Star/Delta)</div>'
    chosen_note = note_he if is_hebrew else note_en

    # Check if subtitle already exists
    if "חיבור סלילים טורי בין ענפי הממיר" not in content and "Series Windings between Inverter Legs" not in content:
        c_idx = content.find('id="demo-circuit-canvas"')
        if c_idx != -1:
            end_c = content.find('></canvas>', c_idx)
            if end_c != -1:
                content = content[:end_c + 10] + f'\n                        {chosen_note}' + content[end_c + 10:]
                print("  [+] Subtitle note added!")

    # 3. Inject JS circuit code
    s = content.find('// Canvas 4: Dynamic Electronic Circuit Simulation')
    if s == -1:
        s = content.find('function renderCircuitCanvas()')
    e = content.find('function renderErrorOrbitCanvas()')

    if s != -1 and e != -1:
        code = get_render_circuit_code(is_hebrew).strip() + "\n\n    "
        content = content[:s] + code + content[e:]
        print("  [+] Circuit JS code injected!")
    else:
        print(f"  [-] ERROR: markers not found: s={s}, e={e}")
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [OK] Successfully saved {filepath}!")
    return True

if __name__ == '__main__':
    update_presentation('generate_hebrew_presentation.py', True)
    update_presentation('generate_html_presentation.py', False)
