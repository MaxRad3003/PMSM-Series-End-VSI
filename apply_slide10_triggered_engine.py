import re

def update_file(filename, is_hebrew=True):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update the Controls Bar HTML: Add the Scope Mode Trigger Button
    # Search for demo-controls-bar
    btn_scope_html = (
        '<button id="btn-demo-scope-mode" class="demo-btn" onclick="toggleDemoScopeMode()" style="background:rgba(0,255,136,0.15); border-color:#00ff88; color:#00ff88; font-size:0.78rem;" title="ייצוב גל נעול טריגר (2 מחזורים סטציונריים) או גלילה איטית">\n'
        '                            📌 גל מיוצב (נעול טריגר)\n'
        '                        </button>'
        if is_hebrew else
        '<button id="btn-demo-scope-mode" class="demo-btn" onclick="toggleDemoScopeMode()" style="background:rgba(0,255,136,0.15); border-color:#00ff88; color:#00ff88; font-size:0.78rem;" title="Trigger-locked stationary 2-cycle view or gentle slow roll">\n'
        '                            📌 Trigger-Locked Scope\n'
        '                        </button>'
    )

    # Let's replace the controls bar section around playback & speed slider
    old_ctrl_pattern = r'(<div class="demo-btn-group">\s*<button id="btn-demo-play".*?🔄[^<]*?</button>\s*</div>)'
    match_ctrl = re.search(old_ctrl_pattern, content, re.DOTALL)
    if match_ctrl:
        new_ctrl = match_ctrl.group(1) + '\n\n                        ' + btn_scope_html
        content = content[:match_ctrl.start()] + new_ctrl + content[match_ctrl.end():]
        print(f"[{filename}] Controls bar updated with Scope Mode Button.")
    else:
        print(f"[{filename}] WARNING: Could not find demo-btn-group in controls bar!")

    # 2. Locate the Slide 10 script block and replace the simulation & canvas render engine
    start_tag = '// --- 3. SLIDE 11: OEPC SWITCHING & CLOSED-LOOP ERROR CORRECTION ENGINE ---'
    if start_tag not in content:
        start_tag = 'SLIDE 11: OEPC SWITCHING'
    
    idx_start = content.find(start_tag)
    if idx_start == -1:
        print(f"[{filename}] ERROR: start tag not found!")
        return False

    # Find the end of the IIFE
    end_tag = '// Slide 9 Interactive Dynamic Simulation Engine'
    if end_tag not in content:
        end_tag = 'slide-dynamic-sim'
    
    # Or find the closing of IIFE: })();
    idx_iife_end = content.find('})();', idx_start)
    if idx_iife_end == -1:
        print(f"[{filename}] ERROR: IIFE closing not found!")
        return False
    idx_iife_end += 5 # include })();

    # Read the full replacement JS engine code
    with open('slide10_engine_replacement.js', 'r', encoding='utf-8') as f_js:
        new_engine_js = f_js.read()

    # Substitute is_hebrew text if needed
    if not is_hebrew:
        new_engine_js = new_engine_js.replace("📌 גל מיוצב (נעול טריגר)", "📌 Trigger-Locked Scope")
        new_engine_js = new_engine_js.replace("🌊 גלילה איטית", "🌊 Slow Rolling Scope")
        new_engine_js = new_engine_js.replace("📌 גל מיוצב (TRIG LOCKED • 2 CYCLES)", "📌 TRIG LOCKED • 2 CYCLES (Stationary)")
        new_engine_js = new_engine_js.replace("🌊 גלילה איטית (SLOW ROLL 0.25X)", "🌊 SLOW ROLL 0.25X")
        new_engine_js = new_engine_js.replace("שגיאות e_x וזרם סדרה אפס i_zsc", "Phase Errors e_x & Zero-Sequence Current i_zsc")
        new_engine_js = new_engine_js.replace("2 מחזורים סטציונריים @ 50 Hz", "2 Stationary Cycles @ 50 Hz")

    content = content[:idx_start] + new_engine_js + content[idx_iife_end:]

    with open(filename, 'w', encoding='utf-8') as f_out:
        f_out.write(content)
    print(f"[{filename}] Successfully updated with Triggered Scope Engine!")
    return True

print("Ready to run apply_slide10_triggered_engine.py after writing slide10_engine_replacement.js")
