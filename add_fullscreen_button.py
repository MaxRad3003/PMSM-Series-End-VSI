"""
add_fullscreen_button.py
Add a Fullscreen button and keyboard shortcut (F) across both Hebrew and English presentations:
1. Adds .btn-fullscreen style and :fullscreen styling to CSS.
2. Injects a Fullscreen toggle button into the header next to the slide counter.
3. Injects a Fullscreen button into the navigation footer.
4. Adds toggleFullscreen() function, 'F' key listener, and fullscreenchange event handlers.
5. Updates both presentation HTML files and generator Python scripts.
"""

from pathlib import Path
import re

PMSM_DIR = Path(r"c:\Users\maximr\OneDrive - ac.sce.ac.il\Barabi\2025 Eli & Max\PMSM")

CSS_FULLSCREEN = """
        /* Fullscreen Controls & Responsive Expansion */
        .btn-fullscreen {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: rgba(0, 210, 255, 0.12);
            border: 1px solid rgba(0, 210, 255, 0.4);
            color: var(--accent-cyan);
            padding: 5px 12px;
            border-radius: 8px;
            font-size: 12.5px;
            font-family: 'Rubik', 'Heebo', sans-serif;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.25s ease;
        }
        .btn-fullscreen:hover {
            background: rgba(0, 210, 255, 0.25);
            border-color: var(--accent-cyan);
            box-shadow: 0 0 12px rgba(0, 210, 255, 0.4);
            transform: translateY(-1px);
        }
        :fullscreen .presentation-wrapper,
        :-webkit-full-screen .presentation-wrapper {
            width: 100vw !important;
            height: 100vh !important;
            max-width: 100vw !important;
            max-height: 100vh !important;
            border-radius: 0 !important;
            border: none !important;
        }
"""

JS_FULLSCREEN = """
    // Fullscreen Navigation & Toggle
    function toggleFullscreen() {
        if (!document.fullscreenElement && !document.webkitFullscreenElement) {
            if (document.documentElement.requestFullscreen) {
                document.documentElement.requestFullscreen().catch(() => {});
            } else if (document.documentElement.webkitRequestFullscreen) {
                document.documentElement.webkitRequestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen().catch(() => {});
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            }
        }
    }

    function updateFullscreenUI() {
        const isFull = !!(document.fullscreenElement || document.webkitFullscreenElement);
        const isHe = document.documentElement.lang === 'he' || document.querySelector('html[dir="rtl"]') !== null;
        
        const headerBtn = document.getElementById('fullscreen-btn');
        const footerBtn = document.getElementById('footer-fullscreen-btn');
        const iconEl = document.getElementById('fullscreen-icon');
        const textEl = document.getElementById('fullscreen-text');

        if (iconEl) iconEl.textContent = isFull ? '🗗' : '⛶';
        if (textEl) textEl.textContent = isFull ? (isHe ? 'צא ממסך מלא' : 'Exit Fullscreen') : (isHe ? 'מסך מלא' : 'Fullscreen');
        if (footerBtn) {
            footerBtn.innerHTML = (isFull ? '🗗 ' : '⛶ ') + (isFull ? (isHe ? 'צא ממסך מלא' : 'Exit Fullscreen') : (isHe ? 'מסך מלא' : 'Fullscreen'));
        }
    }

    document.addEventListener('fullscreenchange', updateFullscreenUI);
    document.addEventListener('webkitfullscreenchange', updateFullscreenUI);
"""

def update_file(file_path: Path, is_hebrew: bool):
    print(f"Adding fullscreen button to {file_path.name}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add CSS
    if "/* Fullscreen Controls & Responsive Expansion */" not in content:
        p_style = content.find("</style>")
        if p_style != -1:
            content = content[:p_style] + CSS_FULLSCREEN + "\n    " + content[p_style:]
            print(f"  [+] Injected Fullscreen CSS into {file_path.name}")

    # 2. Update Header HTML
    # Search for slide-counter in pres-header
    if 'id="fullscreen-btn"' not in content:
        btn_text = "מסך מלא" if is_hebrew else "Fullscreen"
        title_text = "מסך מלא (F)" if is_hebrew else "Fullscreen (F)"
        
        header_old = re.search(r'(<div class="slide-counter">.*?</div>\s*</div>)', content, re.DOTALL)
        if header_old:
            btn_html = f"""<div style="display: flex; align-items: center; gap: 12px;">
            <button class="btn-fullscreen" id="fullscreen-btn" onclick="toggleFullscreen()" title="{title_text}">
                <span id="fullscreen-icon">⛶</span>
                <span id="fullscreen-text">{btn_text}</span>
            </button>
            """
            content = content[:header_old.start()] + btn_html + header_old.group(1)[:-6] + "</div>\n    </div>" + content[header_old.end():]
            print(f"  [+] Injected Fullscreen button into Header in {file_path.name}")

    # 3. Update Footer HTML
    if 'id="footer-fullscreen-btn"' not in content:
        btn_text = "מסך מלא" if is_hebrew else "Fullscreen"
        title_text = "מסך מלא (F)" if is_hebrew else "Fullscreen (F)"
        kbd_text = "| מסך מלא <kbd>F</kbd>" if is_hebrew else "| Fullscreen <kbd>F</kbd>"

        # Update keyboard hint
        m_hint = re.search(r'(<div class="keyboard-hint">.*?)(</div>)', content, re.DOTALL)
        if m_hint:
            if "kbd>F</kbd>" not in m_hint.group(1):
                new_hint = m_hint.group(1).rstrip() + f" {kbd_text}" + m_hint.group(2)
                content = content[:m_hint.start()] + new_hint + content[m_hint.end():]
                print(f"  [+] Updated Keyboard hint in {file_path.name}")

        # Add button to nav-controls
        m_nav = re.search(r'<div class="nav-controls">', content)
        if m_nav:
            insert_pos = m_nav.end()
            footer_btn_html = f"""
            <button class="btn-nav" id="footer-fullscreen-btn" onclick="toggleFullscreen()" title="{title_text}" style="background: rgba(0, 210, 255, 0.12); border-color: rgba(0, 210, 255, 0.35); color: var(--accent-cyan);">
                ⛶ {btn_text}
            </button>"""
            content = content[:insert_pos] + footer_btn_html + content[insert_pos:]
            print(f"  [+] Injected Fullscreen button into Footer in {file_path.name}")

    # 4. Update JavaScript (key F and toggleFullscreen)
    if "function toggleFullscreen()" not in content:
        # Insert JS_FULLSCREEN before </script> in navigation script block
        # Look for updateSlide function or document.addEventListener('keydown'
        m_keydown = re.search(r"document\.addEventListener\('keydown',\s*\(e\)\s*=>\s*\{", content)
        if m_keydown:
            # Add 'F' key to keydown listener
            f_key_snippet = """        if (e.key === 'f' || e.key === 'F') {
            toggleFullscreen();
            return;
        }\n"""
            insert_pos = m_keydown.end()
            content = content[:insert_pos] + "\n" + f_key_snippet + content[insert_pos:]
            print(f"  [+] Added 'F' key listener into {file_path.name}")

        # Add function toggleFullscreen()
        m_script_end = content.find("</script>\n\n\n<script>\n/* =====================================================================")
        if m_script_end == -1:
            m_script_end = content.find("</script>\n<script>\n/* =====================================================================")
        if m_script_end == -1:
            m_script_end = content.find("</script>")

        if m_script_end != -1:
            content = content[:m_script_end] + "\n" + JS_FULLSCREEN + "\n" + content[m_script_end:]
            print(f"  [+] Injected toggleFullscreen() JS into {file_path.name}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [DONE] Saved {file_path.name}\n")

def main():
    files = [
        (PMSM_DIR / "OEPC_SE_VSI_PMSM_Presentation_HE.html", True),
        (PMSM_DIR / "generate_hebrew_presentation.py", True),
        (PMSM_DIR / "OEPC_SE_VSI_PMSM_Presentation.html", False),
        (PMSM_DIR / "generate_html_presentation.py", False),
    ]

    for p, is_he in files:
        if p.exists():
            update_file(p, is_he)
        else:
            print(f"File not found: {p}")

if __name__ == "__main__":
    main()
