import sys
sys.stdout.reconfigure(encoding='utf-8')
from didactic_modules import (
    get_didactic_css,
    get_chapter1_html,
    get_chapter2_html,
    get_chapter4_and_5_html,
    get_chapter6_and_7_html
)

def apply_didactic_updates():
    print("Reading generate_project_book.py...")
    with open('generate_project_book.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Inject Didactic CSS if not present
    if '.didactic-box' not in content:
        css_marker = '/* Figure Display Boxes */'
        idx_css = content.find(css_marker)
        if idx_css != -1:
            content = content[:idx_css] + get_didactic_css() + '\n        ' + content[idx_css:]
            print("  [+] Didactic CSS injected!")
        else:
            print("  [-] CSS marker not found!")
    else:
        print("  [i] Didactic CSS already present.")

    # 2. Update Chapter 1
    idx_ch1 = content.find('id="ch-01"')
    idx_ch2 = content.find('id="ch-02"')
    if idx_ch1 != -1 and idx_ch2 != -1:
        content = content[:idx_ch1] + get_chapter1_html() + content[idx_ch2:]
        print("  [+] Chapter 1 updated with full pedagogical and circuit depth!")
    else:
        print("  [-] ERROR: Ch1 or Ch2 markers not found!")
        return False

    # Refresh markers after Ch1 replacement
    idx_ch2 = content.find('id="ch-02"')
    idx_ch3 = content.find('id="ch-03"')
    if idx_ch2 != -1 and idx_ch3 != -1:
        content = content[:idx_ch2] + get_chapter2_html() + content[idx_ch3:]
        print("  [+] Chapter 2 updated with 96-LUT and numerical walkthrough!")
    else:
        print("  [-] ERROR: Ch2 or Ch3 markers not found!")
        return False

    # Refresh markers for Chapters 4 & 5
    idx_ch4 = content.find('id="ch-04"')
    idx_ch6 = content.find('id="ch-06"')
    if idx_ch4 != -1 and idx_ch6 != -1:
        content = content[:idx_ch4] + get_chapter4_and_5_html() + content[idx_ch6:]
        print("  [+] Chapters 4 & 5 updated with C-HIL & ITSC analysis!")
    else:
        print("  [-] ERROR: Ch4 or Ch6 markers not found!")
        return False

    # Refresh markers for Chapters 6 & 7
    idx_ch6 = content.find('id="ch-06"')
    idx_ch8 = content.find('id="ch-08"')
    if idx_ch6 != -1 and idx_ch8 != -1:
        content = content[:idx_ch6] + get_chapter6_and_7_html() + content[idx_ch8:]
        print("  [+] Chapters 6 & 7 updated with OEMER calibration & Altium!")
    else:
        print("  [-] ERROR: Ch6 or Ch8 markers not found!")
        return False

    # Save to generate_project_book.py
    with open('generate_project_book.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] generate_project_book.py updated successfully!")

    # Now execute generate_project_book.py to generate both HTML files
    print("\nRegenerating HTML project book files...")
    import generate_project_book
    html = generate_project_book.get_book_html()
    
    with open('PMSM_Project_Book.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("  [+] Created PMSM_Project_Book.html successfully!")

    with open('ספר_סיכום_פרויקט_PMSM.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("  [+] Created ספר_סיכום_פרויקט_PMSM.html successfully!")

    return True

if __name__ == '__main__':
    apply_didactic_updates()
