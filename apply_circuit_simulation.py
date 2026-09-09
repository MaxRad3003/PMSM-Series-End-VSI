import re
from circuit_code_template import get_render_circuit_code

def update_presentation_with_circuit(filepath, is_hebrew=True):
    print(f"\n==========================================")
    print(f"Applying Circuit Simulation to: {filepath} (Hebrew={is_hebrew})")
    print(f"==========================================")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Panel 2 HTML
    title_text = "<span>🔌</span> מעגל אלקטרוני חי (איור 2)" if is_hebrew else "<span>🔌</span> Live Circuit Simulation (Fig. 2)"
    tab_circuit = "מעגל חי" if is_hebrew else "Live Circuit"
    tab_matrix = "מטריצה" if is_hebrew else "Matrix"
    label_prio = "עדיפות:" if is_hebrew else "Priority:"
    label_vec = "וקטור:" if is_hebrew else "Vector:"
    label_impact = "השפעה פיזיקלית:" if is_hebrew else "Physical Impact:"
    label_norm = "נורמה:" if is_hebrew else "Norm:"

    # Locate Panel 2 in HTML
    idx_p2_start = content.find('<!-- PANEL 2: OEPC 96-LUT DECISION CORE & TRANSISTOR MATRIX -->')
    if idx_p2_start == -1:
        idx_p2_start = content.find('<!-- PANEL 2: OEPC 96-LUT DECISION CORE')
    
    idx_p3_start = content.find('<!-- PANEL 3: GATE SWITCHING TRACES & ERROR CONVERGENCE -->')
    if idx_p2_start == -1 or idx_p3_start == -1:
        print("  -> ERROR: Could not find Panel 2 / Panel 3 markers in HTML!")
        return False

    old_panel2 = content[idx_p2_start:idx_p3_start]

    # Extract the original transistor matrix card from old_panel2
    idx_matrix_start = old_panel2.find('<div class="transistor-matrix-card">')
    idx_matrix_end = old_panel2.find('<div class="demo-impact-hero">')
    if idx_matrix_start == -1 or idx_matrix_end == -1:
        print("  -> ERROR: Could not find transistor-matrix-card in old_panel2!")
        return False

    matrix_card_html = old_panel2[idx_matrix_start:idx_matrix_end].strip()

    new_panel2_html = f'''<!-- PANEL 2: OEPC 96-LUT DECISION CORE & LIVE ELECTRONIC CIRCUIT SIMULATION -->
                <div class="slide11-card">
                    <div class="slide11-card-title" style="justify-content:space-between; margin-bottom:4px;">
                        <span>{title_text}</span>
                        <div style="display:flex; gap:4px;">
                            <button id="btn-tab-circuit" class="demo-btn active-tab" onclick="setPanel2Tab('circuit')" style="padding:2px 7px; font-size:0.72rem; background:rgba(0,210,255,0.25); border-color:#00d2ff; color:#fff;">{tab_circuit}</button>
                            <button id="btn-tab-matrix" class="demo-btn" onclick="setPanel2Tab('matrix')" style="padding:2px 7px; font-size:0.72rem; opacity:0.65;">{tab_matrix}</button>
                        </div>
                    </div>

                    <!-- Compact Decision Core HUD -->
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2px;">
                        <div style="display:flex; align-items:center; gap:5px;">
                            <span style="font-size:0.75rem; color:var(--text-muted);">{label_prio}</span>
                            <div id="demo-badge-order" class="demo-order-tag" style="font-size:0.85rem; padding:0 6px;">CBA</div>
                        </div>
                        <div style="display:flex; align-items:center; gap:5px;">
                            <span style="font-size:0.75rem; color:var(--text-muted);">{label_vec}</span>
                            <span id="demo-active-vec" class="demo-vec-val" style="font-size:0.92rem; color:#f6d365; font-weight:700; font-family:monospace;">V_14</span>
                            <div id="demo-fmp-badge" class="demo-pill pill-zsc" style="font-size:0.70rem; padding:1px 6px;">Fmp=1</div>
                        </div>
                    </div>

                    <!-- 7-Bit Address Display -->
                    <div id="demo-7bit-bin" class="demo-bin-box" style="padding:2px 6px; font-size:0.92rem; margin:2px 0;">
                        <span class="bit-p">010</span><span class="bit-sep">|</span><span class="bit-s">001</span><span class="bit-sep">|</span><span class="bit-f">0</span>
                    </div>

                    <!-- VIEW 1: LIVE ELECTRONIC CIRCUIT SIMULATION (Default) -->
                    <div id="panel2-view-circuit" style="display:block;">
                        <canvas id="demo-circuit-canvas" style="width:100%; height:200px; background:#060a14; border-radius:6px; display:block; border:1px solid rgba(0,210,255,0.25);"></canvas>
                        <div style="display:flex; justify-content:space-between; font-size:0.70rem; font-family:monospace; background:rgba(0,0,0,0.45); padding:2px 8px; border-radius:5px; border:1px solid rgba(255,255,255,0.08); margin-top:3px;">
                            <span id="circuit-hud-van" style="color:#00d2ff;">v_an: +Vdc</span>
                            <span id="circuit-hud-vbn" style="color:#f6d365;">v_bn: 0V</span>
                            <span id="circuit-hud-vcn" style="color:#ff6b81;">v_cn: -Vdc</span>
                            <span id="circuit-hud-izsc" style="color:#00ff88;">i_zsc: 0.01A</span>
                        </div>
                    </div>

                    <!-- VIEW 2: 8-TRANSISTOR MATRIX (Tab Selectable) -->
                    <div id="panel2-view-matrix" style="display:none;">
                        {matrix_card_html}
                    </div>

                    <div class="demo-impact-hero" style="margin-top:2px; font-size:0.75rem; padding:2px 4px;">
                        {label_impact} <span id="demo-active-impact" class="demo-val-readout" style="color:#f6d365; font-weight:700;">-i_c, -i_0</span>
                        • {label_norm} <span id="demo-tel-norm" class="demo-val-readout" style="color:#00d2ff; font-weight:700;">0.10 A</span>
                    </div>
                </div>

                '''

    content = content[:idx_p2_start] + new_panel2_html + content[idx_p3_start:]
    print("  -> Panel 2 HTML replaced with Circuit Canvas & Tab views.")

    # 2. Add renderCircuitCanvas and tab switching function into JavaScript
    circuit_js_code = get_render_circuit_code(is_hebrew)

    tab_func_code = '''
    // Tab switching between Circuit and Matrix views in Panel 2
    window.setPanel2Tab = function(tabName) {
        const viewCirc = document.getElementById('panel2-view-circuit');
        const viewMat = document.getElementById('panel2-view-matrix');
        const btnCirc = document.getElementById('btn-tab-circuit');
        const btnMat = document.getElementById('btn-tab-matrix');

        if (tabName === 'circuit') {
            if (viewCirc) viewCirc.style.display = 'block';
            if (viewMat) viewMat.style.display = 'none';
            if (btnCirc) { btnCirc.style.background = 'rgba(0,210,255,0.25)'; btnCirc.style.borderColor = '#00d2ff'; btnCirc.style.opacity = '1'; }
            if (btnMat) { btnMat.style.background = 'rgba(0,210,255,0.12)'; btnMat.style.borderColor = 'var(--accent-cyan)'; btnMat.style.opacity = '0.65'; }
            renderCircuitCanvas();
        } else {
            if (viewCirc) viewCirc.style.display = 'none';
            if (viewMat) viewMat.style.display = 'block';
            if (btnCirc) { btnCirc.style.background = 'rgba(0,210,255,0.12)'; btnCirc.style.borderColor = 'var(--accent-cyan)'; btnCirc.style.opacity = '0.65'; }
            if (btnMat) { btnMat.style.background = 'rgba(0,210,255,0.25)'; btnMat.style.borderColor = '#00d2ff'; btnMat.style.opacity = '1'; }
        }
    };
'''

    # Insert circuit_js_code and tab_func_code before renderErrorOrbitCanvas
    idx_orbit = content.find('function renderErrorOrbitCanvas()')
    if idx_orbit == -1:
        print("  -> ERROR: function renderErrorOrbitCanvas() not found!")
        return False

    content = content[:idx_orbit] + circuit_js_code + '\n' + tab_func_code + '\n    ' + content[idx_orbit:]
    print("  -> renderCircuitCanvas and setPanel2Tab added to JS.")

    # 3. Call renderCircuitCanvas in demoLoop, stepDemoOnce, resetDemo, and initial load
    content = content.replace('renderErrorOrbitCanvas();\n            demoAnimId = requestAnimationFrame(demoLoop);',
                              'renderCircuitCanvas();\n            renderErrorOrbitCanvas();\n            demoAnimId = requestAnimationFrame(demoLoop);')
    content = content.replace('renderErrorOrbitCanvas();\n    };',
                              'renderCircuitCanvas();\n        renderErrorOrbitCanvas();\n    };')
    content = content.replace('renderGateTracesCanvas();\n        renderErrorOrbitCanvas();\n    };',
                              'renderGateTracesCanvas();\n        renderCircuitCanvas();\n        renderErrorOrbitCanvas();\n    };')
    content = content.replace('renderGateTracesCanvas();\n            renderErrorOrbitCanvas();\n        }, 500);',
                              'renderGateTracesCanvas();\n            renderCircuitCanvas();\n            renderErrorOrbitCanvas();\n        }, 500);')

    with open(filepath, 'w', encoding='utf-8') as f_out:
        f_out.write(content)
    print(f"  -> Successfully applied circuit simulation to {filepath}!")
    return True

if __name__ == '__main__':
    update_presentation_with_circuit('generate_hebrew_presentation.py', is_hebrew=True)
    update_presentation_with_circuit('generate_html_presentation.py', is_hebrew=False)
    print("\nAll files successfully updated!")
