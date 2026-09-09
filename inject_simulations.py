"""
Inject JSXGraph and Dynamic Simulation slides into OEPC presentations (Hebrew & English).
"""

import os
from pathlib import Path
from build_interactive_engine import INTERACTIVE_JS

PMSM_DIR = Path(r"c:\Users\maximr\OneDrive - ac.sce.ac.il\Barabi\2025 Eli & Max\PMSM")

# 1. JSXGraph Head Scripts
JSX_HEAD = """
    <!-- JSXGraph Mathematical & Dynamic Visualizer -->
    <link rel="stylesheet" type="text/css" href="presentation_assets/jsxgraph.css" />
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/jsxgraph/distrib/jsxgraph.css" />
    <script type="text/javascript" src="presentation_assets/jsxgraphcore.js"></script>
    <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/jsxgraph/distrib/jsxgraphcore.js"></script>
"""

# 2. Interactive CSS
INTERACTIVE_CSS = """
        /* =====================================================================
           INTERACTIVE JSXGRAPH & DYNAMIC SIMULATION STYLES
           ===================================================================== */
        .sim-container {
            display: grid;
            grid-template-columns: 380px 1fr;
            gap: 18px;
            height: calc(100% - 75px);
            margin-top: 8px;
        }
        .sim-controls-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 11px;
            overflow-y: auto;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }
        .sim-control-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        .sim-control-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 13px;
            color: var(--text-secondary);
            font-weight: 500;
        }
        .sim-val-badge {
            font-family: 'Fira Code', monospace;
            color: var(--accent-cyan);
            font-weight: 700;
            background: rgba(0, 210, 255, 0.12);
            padding: 2px 7px;
            border-radius: 5px;
            font-size: 12px;
            direction: ltr;
            unicode-bidi: isolate;
        }
        .sim-slider {
            -webkit-appearance: none;
            appearance: none;
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: rgba(255,255,255,0.12);
            outline: none;
            transition: background 0.2s;
        }
        .sim-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: var(--accent-cyan);
            cursor: pointer;
            box-shadow: 0 0 10px rgba(0, 210, 255, 0.7);
            border: 2px solid #fff;
        }
        .sim-btn-group {
            display: flex;
            gap: 6px;
        }
        .sim-btn {
            flex: 1;
            padding: 7px 8px;
            border-radius: 8px;
            font-size: 12px;
            font-family: 'Rubik', 'Heebo', sans-serif;
            font-weight: 600;
            cursor: pointer;
            border: 1px solid var(--border-color);
            background: rgba(255,255,255,0.05);
            color: var(--text-primary);
            transition: all 0.2s;
            text-align: center;
        }
        .sim-btn:hover {
            background: rgba(0, 210, 255, 0.15);
            border-color: var(--accent-cyan);
        }
        .sim-btn.active {
            background: linear-gradient(135deg, #00d2ff, #3a7bd5);
            color: #fff;
            border-color: transparent;
            box-shadow: 0 0 14px rgba(0, 210, 255, 0.45);
        }
        .sim-display-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }
        .sim-canvas-box {
            position: relative;
            flex: 1;
            min-height: 240px;
            background: #060913;
            border: 1px solid rgba(64, 120, 240, 0.25);
            border-radius: 10px;
            overflow: hidden;
        }
        .jxgbox {
            width: 100%;
            height: 100%;
            border-radius: 10px;
            background: #060913 !important;
            border: none !important;
        }
        .telemetry-bar {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }
        .telemetry-chip {
            background: rgba(10, 15, 29, 0.95);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 8px 12px;
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .telemetry-lbl {
            font-size: 11px;
            color: var(--text-muted);
            font-family: 'Rubik', sans-serif;
        }
        .telemetry-val {
            font-family: 'Fira Code', monospace;
            font-size: 15px;
            font-weight: 700;
            color: var(--accent-cyan);
            direction: ltr;
            unicode-bidi: isolate;
        }
        .priority-badge-row {
            display: flex;
            gap: 6px;
            margin-top: 2px;
        }
        .p-badge {
            flex: 1;
            padding: 6px 6px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            text-align: center;
            display: flex;
            flex-direction: column;
            gap: 2px;
            font-family: 'Rubik', sans-serif;
        }
        .p-prime {
            background: rgba(255, 75, 75, 0.2);
            border: 1px solid rgba(255, 75, 75, 0.5);
            color: #ff6b6b;
        }
        .p-sec {
            background: rgba(246, 211, 101, 0.2);
            border: 1px solid rgba(246, 211, 101, 0.5);
            color: #f6d365;
        }
        .p-minor {
            background: rgba(64, 120, 240, 0.2);
            border: 1px solid rgba(64, 120, 240, 0.5);
            color: #70a1ff;
        }
        .lut-match-box {
            background: rgba(0, 210, 255, 0.08);
            border: 1px solid rgba(0, 210, 255, 0.35);
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 13px;
            line-height: 1.5;
            color: var(--text-primary);
        }
        .dual-screen-grid {
            display: grid;
            grid-template-columns: 1.7fr 1fr;
            gap: 12px;
            flex: 1;
            min-height: 250px;
        }
"""

# 3. Hebrew Slides HTML
HE_SLIDE_OP_PRINCIPLE = """
        <!-- SLIDE: Interactive OEPC Operating Principle & Priority LUT Decoder -->
        <div class="slide" id="slide-oepc-principle">
            <div class="slide-category">הדמיה אינטראקטיבית • JSXGraph</div>
            <div class="slide-title">מפענח עקרון הפעולה של OEPC – מיפוי שגיאות, תעדוף ובחירת וקטורי LUT</div>
            
            <div class="sim-container">
                <!-- Left: Controls & Pipeline -->
                <div class="sim-controls-card">
                    <div class="card-title" style="font-size: 15px; margin-bottom: 4px;">
                        ⚙️ כוונון שגיאות זרם (\\(\\varepsilon = i^* - i\\))
                    </div>
                    
                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>שגיאת פאזה A (\\(\\varepsilon_a\\)):</span>
                            <span class="sim-val-badge" id="val-ea">+1.80 A</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-ea" min="-3.0" max="3.0" step="0.1" value="1.8">
                    </div>

                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>שגיאת פאזה B (\\(\\varepsilon_b\\)):</span>
                            <span class="sim-val-badge" id="val-eb">-1.20 A</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-eb" min="-3.0" max="3.0" step="0.1" value="-1.2">
                    </div>

                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>שגיאת פאזה C (\\(\\varepsilon_c\\)):</span>
                            <span class="sim-val-badge" id="val-ec">-0.60 A</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-ec" min="-3.0" max="3.0" step="0.1" value="-0.6">
                    </div>

                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>זרם סדרה אפס מדוד (\\(i_{zsc}\\)):</span>
                            <span class="sim-val-badge" id="val-izsc">0.00 A</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-izsc" min="-2.0" max="2.0" step="0.05" value="0.0">
                    </div>

                    <!-- Preset Scenarios -->
                    <div style="margin-top: 4px;">
                        <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 4px; font-weight: 600;">תרחישי בדיקה נפוצים:</div>
                        <div class="sim-btn-group" style="flex-wrap: wrap;">
                            <button class="sim-btn active" id="btn-preset-nom" onclick="setPresetErrors(1.8, -1.2, -0.6, 0.0, this)">נומינלי ABC</button>
                            <button class="sim-btn" id="btn-preset-zsc" onclick="setPresetErrors(1.5, 1.2, 0.9, 1.2, this)">חריגת ZSC</button>
                            <button class="sim-btn" id="btn-preset-asym" onclick="setPresetErrors(-2.8, 1.4, 1.4, 0.3, this)">אי-סימטריה 25%</button>
                            <button class="sim-btn" id="btn-preset-itsc" onclick="setPresetErrors(2.6, -0.5, -2.1, 0.8, this)">קצר ITSC</button>
                        </div>
                    </div>

                    <!-- Priority Decoder Output -->
                    <div style="border-top: 1px solid var(--border-color); padding-top: 8px; margin-top: 4px;">
                        <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 6px; font-weight: 600;">דירוג תעדוף השגיאות (Priority Order):</div>
                        <div class="priority-badge-row">
                            <div class="p-badge p-prime">
                                <span style="font-size: 9px; opacity: 0.8;">🥇 שגיאה ראשית</span>
                                <span id="badge-prime-phase" style="font-weight:700; font-size:13px;">פאזה A</span>
                                <span id="badge-prime-val" class="metric">+1.80 A</span>
                            </div>
                            <div class="p-badge p-sec">
                                <span style="font-size: 9px; opacity: 0.8;">🥈 שגיאה משנית</span>
                                <span id="badge-sec-phase" style="font-weight:700; font-size:13px;">פאזה B</span>
                                <span id="badge-sec-val" class="metric">-1.20 A</span>
                            </div>
                            <div class="p-badge p-minor">
                                <span style="font-size: 9px; opacity: 0.8;">🥉 שגיאה שלישית</span>
                                <span id="badge-minor-phase" style="font-weight:700; font-size:13px;">פאזה C</span>
                                <span id="badge-minor-val" class="metric">-0.60 A</span>
                            </div>
                        </div>
                    </div>

                    <!-- LUT Match & Action -->
                    <div class="lut-match-box" id="lut-decision-box">
                        <div style="font-weight: 700; color: var(--accent-cyan); margin-bottom: 3px; display:flex; justify-content:space-between;">
                            <span>חיתוך טבלת 96 המצבים:</span>
                            <span id="lut-row-num" style="color:var(--accent-gold); font-family:'Fira Code';">Case 1 (DM Priority)</span>
                        </div>
                        <div style="font-size: 12px;">
                            וקטור מיתוג נבחר: <span id="lut-vector-code" style="font-family:'Fira Code'; font-weight:700; color:#fff;">0110</span> | 
                            פעולת תיקון: <span id="lut-action-desc" style="color:var(--accent-cyan); font-weight:600;">$-i_a, +i_c$ (סימולטני)</span>
                        </div>
                        <div style="font-size: 11px; color: var(--text-secondary); margin-top: 4px; border-top: 1px dashed rgba(255,255,255,0.15); padding-top: 4px;">
                            <strong>השוואה ל-TDM:</strong> <span id="tdm-compare-note">TDM היה מתקן רק את פאזה A ומקפיא את B ו-C. OEPC מתקן 2 פאזות בו זמנית ומאפס את הריפל!</span>
                        </div>
                    </div>
                </div>

                <!-- Right: JSXGraph Space Vector Plane -->
                <div class="sim-display-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div class="card-title" style="margin: 0; font-size: 16px;">
                            🧭 מישור וקטורי המרחב $\\alpha-\\beta$ ומשושה מתחי הממיר (גרור את נקודת השגיאה $\\vec{\\varepsilon}$)
                        </div>
                        <div style="font-size: 11px; color: var(--text-muted); font-family: 'Fira Code';">
                            JSXGraph Interactive Board
                        </div>
                    </div>

                    <div class="sim-canvas-box" style="height: 380px;">
                        <div id="oepc-jxg-board" class="jxgbox"></div>
                    </div>

                    <!-- Live Telemetry Bar -->
                    <div class="telemetry-bar">
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">וקטור שגיאת זרם $|\\vec{\\varepsilon}_{\\alpha\\beta}|$</span>
                            <span class="telemetry-val" id="tel-err-mag">2.16 A</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">זווית שגיאה $\\theta_\\varepsilon$</span>
                            <span class="telemetry-val" id="tel-err-ang">-28.4°</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">מתח סדרה אפס מופעל $v_{0}$</span>
                            <span class="telemetry-val" id="tel-v0">-0.00 V</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">רווח ביצועים מול TDM</span>
                            <span class="telemetry-val" style="color:#00ff88;" id="tel-gain">+48% מהירות תיקון</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
"""

HE_SLIDE_DYNAMIC_SIM = """
        <!-- SLIDE: Dynamic PMSM Simulation Lab (Real-Time Oscilloscope) -->
        <div class="slide" id="slide-dynamic-sim">
            <div class="slide-category">מעבדת סימולציה דינמית בזמן אמת</div>
            <div class="slide-title">סימולטור מנוע PMSM: עקרון הבקרה, דיכוי ZSC ועמידות באי-סימטריה</div>
            
            <div class="sim-container">
                <!-- Left: Controls -->
                <div class="sim-controls-card">
                    <div class="card-title" style="font-size: 15px; margin-bottom: 4px;">
                        🕹️ בחירת שיטת בקרה ומאפייני מנוע
                    </div>

                    <!-- Algorithm Selector -->
                    <div class="sim-control-group">
                        <span class="sim-control-header" style="font-weight:700; color:#fff;">אלגוריתם בקרה פעיל:</span>
                        <div class="sim-btn-group" style="flex-direction: column;">
                            <button class="sim-btn active" id="btn-algo-oepc" onclick="setSimAlgo('OEPC', this)">
                                🌟 OEPC (מוצע - רב-מטרתי ודיכוי ZSC)
                            </button>
                            <button class="sim-btn" id="btn-algo-tdm" onclick="setSimAlgo('TDM', this)">
                                ⏱️ TDM קלאסי (תיקון שגיאה יחידה)
                            </button>
                            <button class="sim-btn" id="btn-algo-pwm" onclick="setSimAlgo('PWM', this)">
                                ⚠️ PWM קונבנציונלי (ללא דיכוי ZSC)
                            </button>
                        </div>
                    </div>

                    <!-- Speed Slider -->
                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>מהירות סיבוב מנוע (Speed):</span>
                            <span class="sim-val-badge" id="val-sim-speed">1500 RPM</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-sim-speed" min="300" max="3000" step="100" value="1500">
                    </div>

                    <!-- Current Ref Slider -->
                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>זרם מבוקש $I^*$ (Load Demand):</span>
                            <span class="sim-val-badge" id="val-sim-i">5.0 A</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-sim-i" min="1.0" max="10.0" step="0.5" value="5.0">
                    </div>

                    <!-- Asymmetry Slider -->
                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>אי-סימטריה בעומס (Asymmetry):</span>
                            <span class="sim-val-badge" id="val-sim-asym">25% (ניסוי מאמר)</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-sim-asym" min="0" max="30" step="5" value="25">
                    </div>

                    <!-- ZSC Suppression Gain -->
                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>משקל דיכוי ZSC ($K_{zsc}$):</span>
                            <span class="sim-val-badge" id="val-sim-kzsc">1.0</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-sim-kzsc" min="0.0" max="2.0" step="0.1" value="1.0">
                    </div>

                    <!-- Simulation Transport Buttons -->
                    <div style="border-top: 1px solid var(--border-color); padding-top: 10px; margin-top: 4px;">
                        <div class="sim-btn-group">
                            <button class="sim-btn" id="btn-sim-play" onclick="toggleSimPlay()" style="background: rgba(0,210,255,0.2);">⏸ השהה</button>
                            <button class="sim-btn" onclick="resetSimTime()">🔄 איפוס</button>
                        </div>
                    </div>
                </div>

                <!-- Right: Dual Screen Oscilloscope & Trajectory -->
                <div class="sim-display-card">
                    <div class="dual-screen-grid">
                        <!-- Screen 1: Oscilloscope Waves -->
                        <div style="display:flex; flex-direction:column; gap:6px;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <div style="font-size:13px; font-weight:700; color:var(--accent-cyan); display:flex; gap:10px; align-items:center;">
                                    <span>📈 אוסצילוסקופ זרמי פאזות וסדרה אפס (Time Domain)</span>
                                </div>
                                <div style="display:flex; gap:8px; font-size:11px; font-family:'Fira Code';">
                                    <span style="color:#00d2ff;">■ $i_a$</span>
                                    <span style="color:#9d50bb;">■ $i_b$</span>
                                    <span style="color:#f6d365;">■ $i_c$</span>
                                    <span style="color:#ff4757; font-weight:700;">■ $i_{zsc}$</span>
                                </div>
                            </div>
                            <div class="sim-canvas-box" style="height:250px;">
                                <canvas id="osc-canvas" style="width:100%; height:100%; display:block;"></canvas>
                            </div>
                        </div>

                        <!-- Screen 2: Orbital Lissajous Alpha-Beta -->
                        <div style="display:flex; flex-direction:column; gap:6px;">
                            <div style="font-size:13px; font-weight:700; color:var(--accent-cyan);">
                                🔄 מסלול זרם וקטורי $\\alpha-\\beta$
                            </div>
                            <div class="sim-canvas-box" style="height:250px;">
                                <canvas id="orbit-canvas" style="width:100%; height:100%; display:block;"></canvas>
                            </div>
                        </div>
                    </div>

                    <!-- Telemetry Performance Dashboard -->
                    <div class="telemetry-bar">
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">זרם סדרה אפס $i_{zsc}$ RMS</span>
                            <span class="telemetry-val" id="tel-sim-izsc" style="color:#00ff88;">0.04 A</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">עיוות הרמוני כולל (THD)</span>
                            <span class="telemetry-val" id="tel-sim-thd" style="color:#00d2ff;">2.3%</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">שגיאת עקיבה ממוצעת RMS</span>
                            <span class="telemetry-val" id="tel-sim-err">0.11 A</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">חיסכון בהפסדי נחושת</span>
                            <span class="telemetry-val" id="tel-sim-loss" style="color:#f6d365;">-28% מול PWM</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
"""

# 4. English Slides HTML
EN_SLIDE_OP_PRINCIPLE = """
        <!-- SLIDE: Interactive OEPC Operating Principle & Priority LUT Decoder -->
        <div class="slide" id="slide-oepc-principle">
            <div class="slide-category">Interactive Simulation • JSXGraph</div>
            <div class="slide-title">Interactive Decoder: OEPC Operating Principle & 96-State Priority LUT</div>
            
            <div class="sim-container" style="grid-template-columns: 380px 1fr;">
                <!-- Left: Controls & Pipeline -->
                <div class="sim-controls-card">
                    <div class="card-title" style="font-size: 15px; margin-bottom: 4px;">
                        ⚙️ Current Error Controls (\\(\\varepsilon = i^* - i\\))
                    </div>
                    
                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>Phase A Error (\\(\\varepsilon_a\\)):</span>
                            <span class="sim-val-badge" id="val-ea">+1.80 A</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-ea" min="-3.0" max="3.0" step="0.1" value="1.8">
                    </div>

                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>Phase B Error (\\(\\varepsilon_b\\)):</span>
                            <span class="sim-val-badge" id="val-eb">-1.20 A</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-eb" min="-3.0" max="3.0" step="0.1" value="-1.2">
                    </div>

                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>Phase C Error (\\(\\varepsilon_c\\)):</span>
                            <span class="sim-val-badge" id="val-ec">-0.60 A</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-ec" min="-3.0" max="3.0" step="0.1" value="-0.6">
                    </div>

                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>Zero-Sequence Current (\\(i_{zsc}\\)):</span>
                            <span class="sim-val-badge" id="val-izsc">0.00 A</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-izsc" min="-2.0" max="2.0" step="0.05" value="0.0">
                    </div>

                    <!-- Preset Scenarios -->
                    <div style="margin-top: 4px;">
                        <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 4px; font-weight: 600;">Benchmark Presets:</div>
                        <div class="sim-btn-group" style="flex-wrap: wrap;">
                            <button class="sim-btn active" id="btn-preset-nom" onclick="setPresetErrors(1.8, -1.2, -0.6, 0.0, this)">Nominal ABC</button>
                            <button class="sim-btn" id="btn-preset-zsc" onclick="setPresetErrors(1.5, 1.2, 0.9, 1.2, this)">ZSC Surge</button>
                            <button class="sim-btn" id="btn-preset-asym" onclick="setPresetErrors(-2.8, 1.4, 1.4, 0.3, this)">25% Asymmetry</button>
                            <button class="sim-btn" id="btn-preset-itsc" onclick="setPresetErrors(2.6, -0.5, -2.1, 0.8, this)">ITSC Fault</button>
                        </div>
                    </div>

                    <!-- Priority Decoder Output -->
                    <div style="border-top: 1px solid var(--border-color); padding-top: 8px; margin-top: 4px;">
                        <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 6px; font-weight: 600;">Error Priority Classification:</div>
                        <div class="priority-badge-row">
                            <div class="p-badge p-prime">
                                <span style="font-size: 9px; opacity: 0.8;">🥇 Prime Error</span>
                                <span id="badge-prime-phase" style="font-weight:700; font-size:13px;">Phase A</span>
                                <span id="badge-prime-val" class="metric">+1.80 A</span>
                            </div>
                            <div class="p-badge p-sec">
                                <span style="font-size: 9px; opacity: 0.8;">🥈 Secondary</span>
                                <span id="badge-sec-phase" style="font-weight:700; font-size:13px;">Phase B</span>
                                <span id="badge-sec-val" class="metric">-1.20 A</span>
                            </div>
                            <div class="p-badge p-minor">
                                <span style="font-size: 9px; opacity: 0.8;">🥉 Minor</span>
                                <span id="badge-minor-phase" style="font-weight:700; font-size:13px;">Phase C</span>
                                <span id="badge-minor-val" class="metric">-0.60 A</span>
                            </div>
                        </div>
                    </div>

                    <!-- LUT Match & Action -->
                    <div class="lut-match-box" id="lut-decision-box">
                        <div style="font-weight: 700; color: var(--accent-cyan); margin-bottom: 3px; display:flex; justify-content:space-between;">
                            <span>96-Entry LUT Match:</span>
                            <span id="lut-row-num" style="color:var(--accent-gold); font-family:'Fira Code';">Case 1 (DM Priority)</span>
                        </div>
                        <div style="font-size: 12px;">
                            Selected Vector Code: <span id="lut-vector-code" style="font-family:'Fira Code'; font-weight:700; color:#fff;">0110</span> | 
                            Action: <span id="lut-action-desc" style="color:var(--accent-cyan); font-weight:600;">$-i_a, +i_c$ (Simultaneous)</span>
                        </div>
                        <div style="font-size: 11px; color: var(--text-secondary); margin-top: 4px; border-top: 1px dashed rgba(255,255,255,0.15); padding-top: 4px;">
                            <strong>Comparison with TDM:</strong> <span id="tdm-compare-note">TDM would only correct Phase A and freeze B & C. OEPC corrects both simultaneously, eliminating tracking delay!</span>
                        </div>
                    </div>
                </div>

                <!-- Right: JSXGraph Space Vector Plane -->
                <div class="sim-display-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div class="card-title" style="margin: 0; font-size: 16px;">
                            🧭 $\\alpha-\\beta$ Space Vector Plane & Inverter Hexagon (Drag Error Point $\\vec{\\varepsilon}$)
                        </div>
                        <div style="font-size: 11px; color: var(--text-muted); font-family: 'Fira Code';">
                            JSXGraph Interactive Board
                        </div>
                    </div>

                    <div class="sim-canvas-box" style="height: 380px;">
                        <div id="oepc-jxg-board" class="jxgbox"></div>
                    </div>

                    <!-- Live Telemetry Bar -->
                    <div class="telemetry-bar">
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">Error Vector Magnitude $|\\vec{\\varepsilon}_{\\alpha\\beta}|$</span>
                            <span class="telemetry-val" id="tel-err-mag">2.16 A</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">Error Angle $\\theta_\\varepsilon$</span>
                            <span class="telemetry-val" id="tel-err-ang">-28.4°</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">Applied Zero-Seq Voltage $v_{0}$</span>
                            <span class="telemetry-val" id="tel-v0">-0.00 V</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">Performance Gain over TDM</span>
                            <span class="telemetry-val" style="color:#00ff88;" id="tel-gain">+48% Speed</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
"""

EN_SLIDE_DYNAMIC_SIM = """
        <!-- SLIDE: Dynamic PMSM Simulation Lab (Real-Time Oscilloscope) -->
        <div class="slide" id="slide-dynamic-sim">
            <div class="slide-category">Real-Time Simulation Lab</div>
            <div class="slide-title">Dynamic PMSM Drive Simulator: OEPC Principle & ZSC Suppression</div>
            
            <div class="sim-container" style="grid-template-columns: 380px 1fr;">
                <!-- Left: Controls -->
                <div class="sim-controls-card">
                    <div class="card-title" style="font-size: 15px; margin-bottom: 4px;">
                        🕹️ Control Strategy & Motor Parameters
                    </div>

                    <!-- Algorithm Selector -->
                    <div class="sim-control-group">
                        <span class="sim-control-header" style="font-weight:700; color:#fff;">Active Control Strategy:</span>
                        <div class="sim-btn-group" style="flex-direction: column;">
                            <button class="sim-btn active" id="btn-algo-oepc" onclick="setSimAlgo('OEPC', this)">
                                🌟 OEPC (Proposed - Multi-Objective & ZSC)
                            </button>
                            <button class="sim-btn" id="btn-algo-tdm" onclick="setSimAlgo('TDM', this)">
                                ⏱️ Classical TDM (Single Error per Cycle)
                            </button>
                            <button class="sim-btn" id="btn-algo-pwm" onclick="setSimAlgo('PWM', this)">
                                ⚠️ Conventional Sine-PWM (No ZSC Suppression)
                            </button>
                        </div>
                    </div>

                    <!-- Speed Slider -->
                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>Motor Speed:</span>
                            <span class="sim-val-badge" id="val-sim-speed">1500 RPM</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-sim-speed" min="300" max="3000" step="100" value="1500">
                    </div>

                    <!-- Current Ref Slider -->
                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>Load Current Demand $I^*$:</span>
                            <span class="sim-val-badge" id="val-sim-i">5.0 A</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-sim-i" min="1.0" max="10.0" step="0.5" value="5.0">
                    </div>

                    <!-- Asymmetry Slider -->
                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>Load Asymmetry (Paper Benchmark):</span>
                            <span class="sim-val-badge" id="val-sim-asym">25% (Impedance Unbalance)</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-sim-asym" min="0" max="30" step="5" value="25">
                    </div>

                    <!-- ZSC Suppression Gain -->
                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>ZSC Suppression Weight ($K_{zsc}$):</span>
                            <span class="sim-val-badge" id="val-sim-kzsc">1.0</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-sim-kzsc" min="0.0" max="2.0" step="0.1" value="1.0">
                    </div>

                    <!-- Simulation Transport Buttons -->
                    <div style="border-top: 1px solid var(--border-color); padding-top: 10px; margin-top: 4px;">
                        <div class="sim-btn-group">
                            <button class="sim-btn" id="btn-sim-play" onclick="toggleSimPlay()" style="background: rgba(0,210,255,0.2);">⏸ Pause</button>
                            <button class="sim-btn" onclick="resetSimTime()">🔄 Reset</button>
                        </div>
                    </div>
                </div>

                <!-- Right: Dual Screen Oscilloscope & Trajectory -->
                <div class="sim-display-card">
                    <div class="dual-screen-grid">
                        <!-- Screen 1: Oscilloscope Waves -->
                        <div style="display:flex; flex-direction:column; gap:6px;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <div style="font-size:13px; font-weight:700; color:var(--accent-cyan); display:flex; gap:10px; align-items:center;">
                                    <span>📈 Virtual Oscilloscope: Phase Currents & ZSC</span>
                                </div>
                                <div style="display:flex; gap:8px; font-size:11px; font-family:'Fira Code';">
                                    <span style="color:#00d2ff;">■ $i_a$</span>
                                    <span style="color:#9d50bb;">■ $i_b$</span>
                                    <span style="color:#f6d365;">■ $i_c$</span>
                                    <span style="color:#ff4757; font-weight:700;">■ $i_{zsc}$</span>
                                </div>
                            </div>
                            <div class="sim-canvas-box" style="height:250px;">
                                <canvas id="osc-canvas" style="width:100%; height:100%; display:block;"></canvas>
                            </div>
                        </div>

                        <!-- Screen 2: Orbital Lissajous Alpha-Beta -->
                        <div style="display:flex; flex-direction:column; gap:6px;">
                            <div style="font-size:13px; font-weight:700; color:var(--accent-cyan);">
                                🔄 $\\alpha-\\beta$ Orbital Current Trajectory
                            </div>
                            <div class="sim-canvas-box" style="height:250px;">
                                <canvas id="orbit-canvas" style="width:100%; height:100%; display:block;"></canvas>
                            </div>
                        </div>
                    </div>

                    <!-- Telemetry Performance Dashboard -->
                    <div class="telemetry-bar">
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">Zero-Sequence Current $i_{zsc}$ RMS</span>
                            <span class="telemetry-val" id="tel-sim-izsc" style="color:#00ff88;">0.04 A</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">Total Harmonic Distortion (THD)</span>
                            <span class="telemetry-val" id="tel-sim-thd" style="color:#00d2ff;">2.3%</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">Current Tracking Error RMS</span>
                            <span class="telemetry-val" id="tel-sim-err">0.11 A</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">Stator Loss Reduction</span>
                            <span class="telemetry-val" id="tel-sim-loss" style="color:#f6d365;">-28% vs PWM</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
"""

# 5. Injection Function
def process_html_file(filepath, is_hebrew=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Avoid duplicate injection
    if 'id="slide-oepc-principle"' in content:
        print(f"[SKIP] {filepath.name} already contains interactive slides.")
        return

    # Add JSXGraph head
    if 'jsxgraphcore.js' not in content:
        content = content.replace('</head>', JSX_HEAD + '\n</head>')

    # Add CSS
    if '.sim-container' not in content:
        content = content.replace('</style>', INTERACTIVE_CSS + '\n    </style>')

    # Insert Slide 1 (Operating Principle) before SLIDE 6
    slide_op = HE_SLIDE_OP_PRINCIPLE if is_hebrew else EN_SLIDE_OP_PRINCIPLE
    slide_dyn = HE_SLIDE_DYNAMIC_SIM if is_hebrew else EN_SLIDE_DYNAMIC_SIM

    target_s6 = "<!-- SLIDE 6: Typhoon C-HIL"
    if target_s6 in content:
        content = content.replace(target_s6, slide_op + "\n\n        " + target_s6)
    else:
        print(f"[WARN] Could not find {target_s6} in {filepath.name}")

    # Insert Slide 2 (Dynamic Simulation) before SLIDE 9
    target_s9 = "<!-- SLIDE 9: Experimental Differential Voltages"
    if target_s9 in content:
        content = content.replace(target_s9, slide_dyn + "\n\n        " + target_s9)
    else:
        print(f"[WARN] Could not find {target_s9} in {filepath.name}")

    # Add Interactive JS
    js_code = INTERACTIVE_JS
    if not is_hebrew:
        js_code = js_code.replace('פאזה A', 'Phase A').replace('פאזה B', 'Phase B').replace('פאזה C', 'Phase C')
        js_code = js_code.replace('מקרה 2/4 (עדיפות סדרה אפס - CM Priority)', 'Case 2/4 (CM Priority)')
        js_code = js_code.replace('$-i_a, +i_b, -i_c, -i_0$ (דיכוי סדרה אפס אקטיבי)', '$-i_a, +i_b, -i_c, -i_0$ (Active ZSC Suppression)')
        js_code = js_code.replace('מקרה 1/3/5 (עדיפות דיפרנציאלית - DM Priority)', 'Case 1/3/5 (DM Priority)')
        js_code = js_code.replace('תיקון סימולטני של 2 פאזות (ראשית ומשנית)', 'Simultaneous Correction of 2 Phases')
        js_code = js_code.replace('TDM מתעלם מזרם סדרה אפס ומייצר עיוות זרמים חריף! OEPC מיישם מתח $v_0$ מנוגד ומאפס את ה-ZSC!',
                                  'TDM ignores ZSC, creating severe current distortion! OEPC applies opposing $v_0$ to zero the ZSC!')
        js_code = js_code.replace(' ומשאיר את השאר ללא שינוי. OEPC מתקן את שתיהן בו-זמנית!', ' and freezes the rest. OEPC corrects both simultaneously!')
        js_code = js_code.replace(' (אי-סימטריה)', ' (Unbalance)').replace(' (מאוזן)', ' (Balanced)')
        js_code = js_code.replace('-28% מול PWM', '-28% vs PWM').replace('-12% מול PWM', '-12% vs PWM').replace('בסיס (0%)', 'Base (0%)')

    content = content.replace('</body>', js_code + '\n</body>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] Injected interactive simulations into {filepath.name}!")

if __name__ == "__main__":
    he_path = PMSM_DIR / "OEPC_SE_VSI_PMSM_Presentation_HE.html"
    en_path = PMSM_DIR / "OEPC_SE_VSI_PMSM_Presentation.html"

    process_html_file(he_path, is_hebrew=True)
    process_html_file(en_path, is_hebrew=False)
    print("Done injecting interactive components.")
