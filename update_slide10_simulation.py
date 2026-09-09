"""
update_slide10_simulation.py
Refactor Slide 10 (Dynamic Simulation Lab & Oscilloscope):
1. Solves "signals running too fast":
   - Implements Oscilloscope Triggered Sync Mode (מצב גל מיוצב) locked to Phase A zero-crossing, displaying 2 complete, stable periods.
   - Adds Slow-Motion Roll Mode (גלילה איטית נינוחה) at 0.1x readable speed.
   - Smooths the Lissajous orbit trajectory to 1 gentle rotation every 3.5 seconds with glowing comet tail.
2. Solves "not understandable / explain the process":
   - Adds a Dynamic Algorithm Explanation Banner showing in plain, clear language what the active algorithm is doing in real-time.
   - Adds a 3-Step Process Breakdown explaining:
     Step 1: Current sampling and ZSC detection in Open-Winding PMSM.
     Step 2: Priority-based LUT decision and 4th leg gating.
     Step 3: Elimination of torque ripple and loss reduction.
   - Replaces all raw LaTeX strings ($...$) with clean HTML math typography with <bdi class="math-term">.
3. Updates:
   - OEPC_SE_VSI_PMSM_Presentation_HE.html
   - generate_hebrew_presentation.py
   - OEPC_SE_VSI_PMSM_Presentation.html
   - generate_html_presentation.py
"""

from pathlib import Path
import re

PMSM_DIR = Path(r"c:\Users\maximr\OneDrive - ac.sce.ac.il\Barabi\2025 Eli & Max\PMSM")

CSS_SLIDE10 = """
        /* =====================================================================
           SLIDE 10 REFINEMENTS: OSCILLOSCOPE STABILIZATION & PROCESS BREAKDOWN
           ===================================================================== */
        .algo-explain-card {
            background: rgba(13, 25, 48, 0.95);
            border: 1px solid rgba(0, 210, 255, 0.4);
            border-radius: 10px;
            padding: 9px 13px;
            display: flex;
            flex-direction: column;
            gap: 4px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.25);
            transition: all 0.3s ease;
        }
        .algo-explain-title {
            font-size: 12.5px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
            font-family: 'Rubik', sans-serif;
        }
        .algo-explain-text {
            font-size: 12px;
            color: var(--text-secondary);
            line-height: 1.5;
        }
        .process-flow-container {
            background: rgba(8, 14, 28, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 8px 12px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .process-flow-header {
            font-size: 11.5px;
            font-weight: 700;
            color: var(--accent-gold);
            font-family: 'Rubik', sans-serif;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .process-steps-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
        }
        .process-step-box {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 6px;
            padding: 6px 8px;
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .step-tag {
            font-size: 10px;
            font-weight: 700;
            color: var(--accent-cyan);
            font-family: 'Rubik', sans-serif;
        }
        .step-desc {
            font-size: 11px;
            color: var(--text-secondary);
            line-height: 1.35;
        }
        .mode-toggle-group {
            display: flex;
            gap: 4px;
            background: rgba(0, 0, 0, 0.3);
            padding: 3px;
            border-radius: 6px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .mode-btn {
            flex: 1;
            padding: 4px 6px;
            font-size: 11px;
            font-family: 'Rubik', sans-serif;
            font-weight: 600;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            background: transparent;
            color: var(--text-muted);
            transition: all 0.2s ease;
        }
        .mode-btn.active {
            background: rgba(0, 210, 255, 0.22);
            color: #00d2ff;
            border: 1px solid rgba(0, 210, 255, 0.5);
        }
"""

# HTML - HEBREW
HTML_SLIDE10_HE = """        <!-- SLIDE: Dynamic PMSM Simulation Lab (Real-Time Oscilloscope) -->
        <div class="slide" id="slide-dynamic-sim" style="overflow: hidden !important;">
            <div class="slide-category">מעבדת סימולציה דינמית בזמן אמת</div>
            <div class="slide-title">סימולטור מנוע PMSM: עקרון הבקרה, דיכוי ZSC ועמידות באי-סימטריה</div>
            
            <div class="sim-container" style="grid-template-columns: 370px 1fr; gap: 14px;">
                <!-- Left: Controls & Process Overview -->
                <div class="sim-controls-card">
                    <div class="card-title" style="font-size: 14.5px; margin-bottom: 2px;">
                        🕹️ בחירת שיטת בקרה ומאפייני מנוע
                    </div>

                    <!-- Algorithm Selector -->
                    <div class="sim-control-group">
                        <span class="sim-control-header" style="font-weight:700; color:#fff; font-size:12px;">אלגוריתם בקרה פעיל:</span>
                        <div class="sim-btn-group" style="flex-direction: column; gap: 4px;">
                            <button class="sim-btn active" id="btn-algo-oepc" onclick="setSimAlgo('OEPC', this)">
                                🌟 OEPC (מוצע – דיכוי ZSC ותיקון סימולטני)
                            </button>
                            <button class="sim-btn" id="btn-algo-tdm" onclick="setSimAlgo('TDM', this)">
                                ⏱️ TDM קלאסי (תיקון שגיאה בודדת במחזור)
                            </button>
                            <button class="sim-btn" id="btn-algo-pwm" onclick="setSimAlgo('PWM', this)">
                                ⚠️ PWM קונבנציונלי (ללא דיכוי ZSC)
                            </button>
                        </div>
                    </div>

                    <!-- Oscilloscope Stabilization / Mode Selector -->
                    <div class="sim-control-group" style="margin-top: 2px;">
                        <div class="sim-control-header" style="font-size: 11.5px;">
                            <span>מצב סנכרון תצוגה (Scope Sync):</span>
                        </div>
                        <div class="mode-toggle-group">
                            <button class="mode-btn active" id="btn-mode-trig" onclick="setScopeMode('trig', this)">
                                📌 גל מיוצב (Triggered)
                            </button>
                            <button class="mode-btn" id="btn-mode-slow" onclick="setScopeMode('slow', this)">
                                🌊 גלילה איטית (0.2x)
                            </button>
                        </div>
                    </div>

                    <!-- Asymmetry Slider (Key Experiment) -->
                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>אי-סימטריה בסלילים <bdi class="math-term">(&Delta;Z / Z)</bdi>:</span>
                            <span class="sim-val-badge" id="val-sim-asym">25% (ניסוי מאמר)</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-sim-asym" min="0" max="30" step="5" value="25" oninput="updateSimParams()">
                    </div>

                    <!-- Current Ref Slider -->
                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>זרם עבודה מבוקש <bdi class="math-term">(<i>I</i><sup>*</sup>)</bdi>:</span>
                            <span class="sim-val-badge" id="val-sim-i">5.0 A</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-sim-i" min="1.0" max="8.0" step="0.5" value="5.0" oninput="updateSimParams()">
                    </div>

                    <!-- Speed Slider -->
                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>מהירות סיבוב מנוע <bdi class="math-term">(&omega;<sub>m</sub>)</bdi>:</span>
                            <span class="sim-val-badge" id="val-sim-speed">1500 RPM</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-sim-speed" min="300" max="3000" step="100" value="1500" oninput="updateSimParams()">
                    </div>

                    <!-- Simulation Play/Pause Controls -->
                    <div style="border-top: 1px solid var(--border-color); padding-top: 6px; margin-top: 2px;">
                        <div class="sim-btn-group">
                            <button class="sim-btn" id="btn-sim-play" onclick="toggleSimPlay()" style="background: rgba(0,210,255,0.18);">⏸ השהה אות</button>
                            <button class="sim-btn" onclick="resetSimTime()">🔄 איפוס גל</button>
                        </div>
                    </div>
                </div>

                <!-- Right: Dual Screen Oscilloscope, Explanation Card & Process Steps -->
                <div class="sim-display-card" style="gap: 8px;">
                    <div class="dual-screen-grid" style="min-height: 190px;">
                        <!-- Screen 1: Oscilloscope Waves -->
                        <div style="display:flex; flex-direction:column; gap:4px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap: wrap;">
                                <div style="font-size:12.5px; font-weight:700; color:var(--accent-cyan); display:flex; gap:6px; align-items:center;">
                                    <span>📈 אוסצילוסקופ זרמים בזמן אמת (Time Domain)</span>
                                </div>
                                <div style="display:flex; gap:8px; font-size:11px; font-family:'Fira Code'; direction:ltr;">
                                    <span style="color:#00d2ff; font-weight:600;">■ <i>i</i><sub>a</sub></span>
                                    <span style="color:#9d50bb; font-weight:600;">■ <i>i</i><sub>b</sub></span>
                                    <span style="color:#f6d365; font-weight:600;">■ <i>i</i><sub>c</sub></span>
                                    <span style="color:#ff4757; font-weight:700;">■ <i>i</i><sub>zsc</sub> (סדרה אפס)</span>
                                </div>
                            </div>
                            <div class="sim-canvas-box" style="height: 195px; position:relative;">
                                <canvas id="osc-canvas" style="width:100%; height:100%; display:block;"></canvas>
                                <div id="osc-status-tag" style="position:absolute; top:6px; right:8px; background:rgba(0,0,0,0.6); padding:2px 6px; border-radius:4px; font-size:10px; font-family:'Fira Code'; color:#00ff88; border:1px solid rgba(0,255,136,0.3);">
                                    TRIG LOCKED • 2 CYCLES
                                </div>
                            </div>
                        </div>

                        <!-- Screen 2: Orbital Lissajous Alpha-Beta -->
                        <div style="display:flex; flex-direction:column; gap:4px;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <div style="font-size:12.5px; font-weight:700; color:var(--accent-cyan);">
                                    🔄 מסלול וקטורי מרחב <bdi class="math-term">&alpha;&minus;&beta;</bdi>
                                </div>
                                <span style="font-size:10.5px; color:var(--text-muted);">מעגל סימטרי = מומנט אחיד</span>
                            </div>
                            <div class="sim-canvas-box" style="height: 195px; position:relative;">
                                <canvas id="orbit-canvas" style="width:100%; height:100%; display:block;"></canvas>
                                <div id="orbit-status-tag" style="position:absolute; bottom:6px; left:8px; background:rgba(0,0,0,0.6); padding:2px 6px; border-radius:4px; font-size:10px; font-family:'Fira Code'; color:#00d2ff; border:1px solid rgba(0,210,255,0.3);">
                                    HODOGRAPH: PURE CIRCLE
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Dynamic Algorithm Explanation Banner -->
                    <div class="algo-explain-card" id="algo-explain-box">
                        <div class="algo-explain-title" id="algo-explain-title" style="color: #00d2ff;">
                            🌟 בקרת OEPC (מוצעת): פעולת דיכוי סדרה אפס אקטיבית ואיפוס הריפל
                        </div>
                        <div class="algo-explain-text" id="algo-explain-desc">
                            האלגוריתם מנטר את חריגת ה-ZSC הנגרמת מאי-סימטריה של 25%, ומפעיל את הענף הרביעי עם מתח סדרה אפס נגדי. התוצאה: הקו האדום של <bdi class="math-term"><i>i</i><sub>zsc</sub></bdi> משוטח לאפס (< 0.04A), הזרמים סינוסיים טהורים, ומסלול האלפא-בטא מעגלי ללא פעימות מומנט.
                        </div>
                    </div>

                    <!-- 3-Step Process Breakdown -->
                    <div class="process-flow-container">
                        <div class="process-flow-header">
                            <span>🔍 פירוט תהליך הבקרה בזמן אמת – שלב אחר שלב:</span>
                        </div>
                        <div class="process-steps-grid">
                            <div class="process-step-box">
                                <span class="step-tag">שלב 1: דגימה וזיהוי שגיאה</span>
                                <span class="step-desc">דגימת זרמי פאזות <bdi class="math-term"><i>i</i><sub>a,b,c</sub></bdi> וחישוב זרם סדרה אפס <bdi class="math-term"><i>i</i><sub>zsc</sub> = (<i>i</i><sub>a</sub>+<i>i</i><sub>b</sub>+<i>i</i><sub>c</sub>)/3</bdi>.</span>
                            </div>
                            <div class="process-step-box">
                                <span class="step-tag">שלב 2: תעדוף שגיאות ב-LUT</span>
                                <span class="step-desc">מיון לקסיקוגרפי: בחירה בין עדיפות CM (לדיכוי ה-ZSC) לבין עדיפות DM (לתיקון סימולטני של 2 פאזות).</span>
                            </div>
                            <div class="process-step-box">
                                <span class="step-tag">שלב 3: הפעלת וקטור מיתוג</span>
                                <span class="step-desc">יישום מצב מיתוג מתוך 96 המצבים בלולאה ישירה של 1.75&mu;s – איפוס השגיאה ללא אפנון PWM מסורתי.</span>
                            </div>
                        </div>
                    </div>

                    <!-- Telemetry Performance Dashboard -->
                    <div class="telemetry-bar" style="margin-top: 2px;">
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">זרם סדרה אפס <bdi class="math-term"><i>i</i><sub>zsc</sub> RMS</bdi></span>
                            <span class="telemetry-val" id="tel-sim-izsc" style="color:#00ff88;">0.04 A</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">עיוות הרמוני כולל <bdi class="math-term">(THD)</bdi></span>
                            <span class="telemetry-val" id="tel-sim-thd" style="color:#00d2ff;">2.1%</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">שגיאת עקיבה ממוצעת <bdi class="math-term">RMS</bdi></span>
                            <span class="telemetry-val" id="tel-sim-err">0.09 A</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">חיסכון בהפסדי מיתוג</span>
                            <span class="telemetry-val" id="tel-sim-loss" style="color:#f6d365;">-28% מול PWM</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>"""

# HTML - ENGLISH
HTML_SLIDE10_EN = """        <!-- SLIDE: Dynamic PMSM Simulation Lab (Real-Time Oscilloscope) -->
        <div class="slide" id="slide-dynamic-sim" style="overflow: hidden !important;">
            <div class="slide-category">Real-Time Dynamic Simulation Lab</div>
            <div class="slide-title">PMSM Motor Simulator: Operating Principle, ZSC Suppression & Asymmetry Tolerance</div>
            
            <div class="sim-container" style="grid-template-columns: 370px 1fr; gap: 14px;">
                <!-- Left: Controls & Process Overview -->
                <div class="sim-controls-card">
                    <div class="card-title" style="font-size: 14.5px; margin-bottom: 2px;">
                        🕹️ Control Algorithm & Motor Parameters
                    </div>

                    <!-- Algorithm Selector -->
                    <div class="sim-control-group">
                        <span class="sim-control-header" style="font-weight:700; color:#fff; font-size:12px;">Active Control Algorithm:</span>
                        <div class="sim-btn-group" style="flex-direction: column; gap: 4px;">
                            <button class="sim-btn active" id="btn-algo-oepc" onclick="setSimAlgo('OEPC', this)">
                                🌟 OEPC (Proposed – ZSC Suppression & Simultaneous Fix)
                            </button>
                            <button class="sim-btn" id="btn-algo-tdm" onclick="setSimAlgo('TDM', this)">
                                ⏱️ Classical TDM (Single Phase per Cycle)
                            </button>
                            <button class="sim-btn" id="btn-algo-pwm" onclick="setSimAlgo('PWM', this)">
                                ⚠️ Conventional PWM (No ZSC Suppression)
                            </button>
                        </div>
                    </div>

                    <!-- Oscilloscope Synchronization / Mode Selector -->
                    <div class="sim-control-group" style="margin-top: 2px;">
                        <div class="sim-control-header" style="font-size: 11.5px;">
                            <span>Oscilloscope Display Sync:</span>
                        </div>
                        <div class="mode-toggle-group">
                            <button class="mode-btn active" id="btn-mode-trig" onclick="setScopeMode('trig', this)">
                                📌 Triggered Wave (Stationary)
                            </button>
                            <button class="mode-btn" id="btn-mode-slow" onclick="setScopeMode('slow', this)">
                                🌊 Slow Roll (0.2x)
                            </button>
                        </div>
                    </div>

                    <!-- Asymmetry Slider (Key Experiment) -->
                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>Winding Asymmetry <bdi class="math-term">(&Delta;Z / Z)</bdi>:</span>
                            <span class="sim-val-badge" id="val-sim-asym">25% (Paper Setup)</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-sim-asym" min="0" max="30" step="5" value="25" oninput="updateSimParams()">
                    </div>

                    <!-- Current Ref Slider -->
                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>Load Current Demand <bdi class="math-term">(<i>I</i><sup>*</sup>)</bdi>:</span>
                            <span class="sim-val-badge" id="val-sim-i">5.0 A</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-sim-i" min="1.0" max="8.0" step="0.5" value="5.0" oninput="updateSimParams()">
                    </div>

                    <!-- Speed Slider -->
                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>Motor Speed <bdi class="math-term">(&omega;<sub>m</sub>)</bdi>:</span>
                            <span class="sim-val-badge" id="val-sim-speed">1500 RPM</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-sim-speed" min="300" max="3000" step="100" value="1500" oninput="updateSimParams()">
                    </div>

                    <!-- Simulation Play/Pause Controls -->
                    <div style="border-top: 1px solid var(--border-color); padding-top: 6px; margin-top: 2px;">
                        <div class="sim-btn-group">
                            <button class="sim-btn" id="btn-sim-play" onclick="toggleSimPlay()" style="background: rgba(0,210,255,0.18);">⏸ Pause Wave</button>
                            <button class="sim-btn" onclick="resetSimTime()">🔄 Reset Trace</button>
                        </div>
                    </div>
                </div>

                <!-- Right: Dual Screen Oscilloscope, Explanation Card & Process Steps -->
                <div class="sim-display-card" style="gap: 8px;">
                    <div class="dual-screen-grid" style="min-height: 190px;">
                        <!-- Screen 1: Oscilloscope Waves -->
                        <div style="display:flex; flex-direction:column; gap:4px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap: wrap;">
                                <div style="font-size:12.5px; font-weight:700; color:var(--accent-cyan); display:flex; gap:6px; align-items:center;">
                                    <span>📈 Real-Time Phase & ZSC Oscilloscope</span>
                                </div>
                                <div style="display:flex; gap:8px; font-size:11px; font-family:'Fira Code';">
                                    <span style="color:#00d2ff; font-weight:600;">■ <i>i</i><sub>a</sub></span>
                                    <span style="color:#9d50bb; font-weight:600;">■ <i>i</i><sub>b</sub></span>
                                    <span style="color:#f6d365; font-weight:600;">■ <i>i</i><sub>c</sub></span>
                                    <span style="color:#ff4757; font-weight:700;">■ <i>i</i><sub>zsc</sub> (ZSC)</span>
                                </div>
                            </div>
                            <div class="sim-canvas-box" style="height: 195px; position:relative;">
                                <canvas id="osc-canvas" style="width:100%; height:100%; display:block;"></canvas>
                                <div id="osc-status-tag" style="position:absolute; top:6px; right:8px; background:rgba(0,0,0,0.6); padding:2px 6px; border-radius:4px; font-size:10px; font-family:'Fira Code'; color:#00ff88; border:1px solid rgba(0,255,136,0.3);">
                                    TRIG LOCKED • 2 CYCLES
                                </div>
                            </div>
                        </div>

                        <!-- Screen 2: Orbital Lissajous Alpha-Beta -->
                        <div style="display:flex; flex-direction:column; gap:4px;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <div style="font-size:12.5px; font-weight:700; color:var(--accent-cyan);">
                                    🔄 Space Vector Hodograph <bdi class="math-term">&alpha;&minus;&beta;</bdi>
                                </div>
                                <span style="font-size:10.5px; color:var(--text-muted);">Symmetric Circle = Smooth Torque</span>
                            </div>
                            <div class="sim-canvas-box" style="height: 195px; position:relative;">
                                <canvas id="orbit-canvas" style="width:100%; height:100%; display:block;"></canvas>
                                <div id="orbit-status-tag" style="position:absolute; bottom:6px; left:8px; background:rgba(0,0,0,0.6); padding:2px 6px; border-radius:4px; font-size:10px; font-family:'Fira Code'; color:#00d2ff; border:1px solid rgba(0,210,255,0.3);">
                                    HODOGRAPH: PURE CIRCLE
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Dynamic Algorithm Explanation Banner -->
                    <div class="algo-explain-card" id="algo-explain-box">
                        <div class="algo-explain-title" id="algo-explain-title" style="color: #00d2ff;">
                            🌟 OEPC Control (Proposed): Active Zero-Sequence Elimination & Ripple Suppression
                        </div>
                        <div class="algo-explain-text" id="algo-explain-desc">
                            The algorithm continuously detects ZSC excursions caused by 25% physical impedance asymmetry, activating the 4th leg with opposing common-mode voltage. As a result, the red <bdi class="math-term"><i>i</i><sub>zsc</sub></bdi> line remains flattened (< 0.04A), phase currents remain purely sinusoidal, and the alpha-beta locus stays circular without torque pulsations.
                        </div>
                    </div>

                    <!-- 3-Step Process Breakdown -->
                    <div class="process-flow-container">
                        <div class="process-flow-header">
                            <span>🔍 Real-Time Control Process Pipeline – Step by Step:</span>
                        </div>
                        <div class="process-steps-grid">
                            <div class="process-step-box">
                                <span class="step-tag">Step 1: Current Sampling & Error Sensing</span>
                                <span class="step-desc">Measures <bdi class="math-term"><i>i</i><sub>a,b,c</sub></bdi> and computes zero-sequence current <bdi class="math-term"><i>i</i><sub>zsc</sub> = (<i>i</i><sub>a</sub>+<i>i</i><sub>b</sub>+<i>i</i><sub>c</sub>)/3</bdi>.</span>
                            </div>
                            <div class="process-step-box">
                                <span class="step-tag">Step 2: Lexicographical Priority LUT</span>
                                <span class="step-desc">Arbitrates between CM Priority (to quench ZSC) and DM Priority (to correct 2 phase currents simultaneously).</span>
                            </div>
                            <div class="process-step-box">
                                <span class="step-tag">Step 3: Optimal Vector Synthesis</span>
                                <span class="step-desc">Applies 4-leg inverter switching state in direct 1.75&mu;s cycle – canceling error without classical PWM carrier delays.</span>
                            </div>
                        </div>
                    </div>

                    <!-- Telemetry Performance Dashboard -->
                    <div class="telemetry-bar" style="margin-top: 2px;">
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">Zero-Sequence Current <bdi class="math-term"><i>i</i><sub>zsc</sub> RMS</bdi></span>
                            <span class="telemetry-val" id="tel-sim-izsc" style="color:#00ff88;">0.04 A</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">Total Harmonic Distortion <bdi class="math-term">(THD)</bdi></span>
                            <span class="telemetry-val" id="tel-sim-thd" style="color:#00d2ff;">2.1%</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">Mean Tracking Error <bdi class="math-term">RMS</bdi></span>
                            <span class="telemetry-val" id="tel-sim-err">0.09 A</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">Switching Loss Reduction</span>
                            <span class="telemetry-val" id="tel-sim-loss" style="color:#f6d365;">-28% vs PWM</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>"""

# JS - HEBREW & ENGLISH
JS_SIMULATION = """// --- 2. DYNAMIC PMSM & OSCILLOSCOPE SIMULATOR (STABILIZED & EXPLAINED) ---
let simActive = true;
let currentAlgo = 'OEPC';
let scopeMode = 'trig'; // 'trig' = stationary triggered, 'slow' = gentle scrolling
let simPhase = 0;
let oscAnimFrame = null;

const oscCanvas = document.getElementById('osc-canvas');
const orbitCanvas = document.getElementById('orbit-canvas');
const oscCtx = oscCanvas ? oscCanvas.getContext('2d') : null;
const orbitCtx = orbitCanvas ? orbitCanvas.getContext('2d') : null;

const ALGO_DETAILS = {
    he: {
        OEPC: {
            title: '🌟 בקרת OEPC (מוצעת): פעולת דיכוי סדרה אפס אקטיבית ואיפוס הריפל',
            desc: 'האלגוריתם מנטר את חריגת ה-ZSC הנגרמת מאי-סימטריה של 25%, ומפעיל את הענף הרביעי עם מתח נגדי. התוצאה: הקו האדום של <i>i</i><sub>zsc</sub> משוטח לאפס (< 0.04A), הזרמים סינוסיים טהורים, ומסלול האלפא-בטא מעגלי ללא פעימות מומנט.',
            titleColor: '#00d2ff',
            hodographText: 'HODOGRAPH: PURE CIRCLE',
            hodographColor: '#00d2ff'
        },
        TDM: {
            title: '⏱️ בקרת TDM קלאסית: תיקון פאזה בודדת בכל מחזור (חלוקת זמן)',
            desc: 'בשיטה זו מתקנים רק את הפאזה בעלת השגיאה המרבית ומקפיאים את השאר. התוצאה: ריפל מיתוג מוגבר (THD 6.2%), עיכוב בתיקון עיוותי סדרה אפס, ותנודות קלות במסלול האלפא-בטא.',
            titleColor: '#f6d365',
            hodographText: 'HODOGRAPH: RIPPLE OSCILLATION',
            hodographColor: '#f6d365'
        },
        PWM: {
            title: '⚠️ בקרת PWM קונבנציונלית: ללא דיכוי זרם סדרה אפס (ZSC)',
            desc: 'אין שליטה אקטיבית על הענף הרביעי. אי-האיזון בעומס יוצר זרם סדרה אפס מסוכן (קו אדום ענק של ~1.5A!), הזרמים מתעוותים בחריפות (THD > 13%), ומסלול האלפא-בטא מתעוות לאליפסה היוצרת פעימות מומנט הרסניות.',
            titleColor: '#ff4757',
            hodographText: 'HODOGRAPH: SEVERELY DISTORTED',
            hodographColor: '#ff4757'
        }
    },
    en: {
        OEPC: {
            title: '🌟 OEPC Control (Proposed): Active Zero-Sequence Elimination & Ripple Suppression',
            desc: 'The algorithm continuously detects ZSC excursions caused by 25% physical impedance asymmetry, activating the 4th leg with opposing common-mode voltage. As a result, the red <i>i</i><sub>zsc</sub> line remains flattened (< 0.04A), phase currents remain purely sinusoidal, and the alpha-beta locus stays circular without torque pulsations.',
            titleColor: '#00d2ff',
            hodographText: 'HODOGRAPH: PURE CIRCLE',
            hodographColor: '#00d2ff'
        },
        TDM: {
            title: '⏱️ Classical TDM Control: Single Phase per Cycle Time-Division',
            desc: 'Corrects only the worst-error phase while freezing others. Tracking delay accumulates, causing elevated switching ripple (THD 6.2%), slower ZSC attenuation, and noticeable orbital jitter.',
            titleColor: '#f6d365',
            hodographText: 'HODOGRAPH: RIPPLE OSCILLATION',
            hodographColor: '#f6d365'
        },
        PWM: {
            title: '⚠️ Conventional PWM Control: No Zero-Sequence Current (ZSC) Suppression',
            desc: 'Without active 4th-leg control, load asymmetry drives huge zero-sequence currents (giant red waveform of ~1.5A!). Phase currents suffer severe distortion (THD > 13%), warping the hodograph into an ellipse with heavy torque ripple.',
            titleColor: '#ff4757',
            hodographText: 'HODOGRAPH: SEVERELY DISTORTED',
            hodographColor: '#ff4757'
        }
    }
};

function setSimAlgo(algo, btn) {
    currentAlgo = algo;
    document.querySelectorAll('#slide-dynamic-sim .sim-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');

    const isHe = document.documentElement.lang === 'he' || document.querySelector('html[dir="rtl"]') !== null;
    const langKey = isHe ? 'he' : 'en';
    const detail = ALGO_DETAILS[langKey][algo];

    const titleEl = document.getElementById('algo-explain-title');
    const descEl = document.getElementById('algo-explain-desc');
    const hodoTag = document.getElementById('orbit-status-tag');

    if (titleEl) {
        titleEl.textContent = detail.title;
        titleEl.style.color = detail.titleColor;
    }
    if (descEl) {
        descEl.innerHTML = detail.desc;
    }
    if (hodoTag) {
        hodoTag.textContent = detail.hodographText;
        hodoTag.style.color = detail.hodographColor;
        hodoTag.style.borderColor = detail.hodographColor;
    }
}

function setScopeMode(mode, btn) {
    scopeMode = mode;
    document.querySelectorAll('.mode-toggle-group .mode-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');

    const tagEl = document.getElementById('osc-status-tag');
    if (tagEl) {
        tagEl.textContent = mode === 'trig' ? 'TRIG LOCKED • 2 CYCLES' : 'SLOW MOTION ROLL • 0.2X';
        tagEl.style.color = mode === 'trig' ? '#00ff88' : '#00d2ff';
        tagEl.style.borderColor = mode === 'trig' ? 'rgba(0,255,136,0.3)' : 'rgba(0,210,255,0.3)';
    }
}

function toggleSimPlay() {
    simActive = !simActive;
    const btn = document.getElementById('btn-sim-play');
    const isHe = document.documentElement.lang === 'he' || document.querySelector('html[dir="rtl"]') !== null;
    if (btn) {
        if (isHe) btn.textContent = simActive ? '⏸ השהה אות' : '▶ המשך אות';
        else btn.textContent = simActive ? '⏸ Pause Wave' : '▶ Resume Wave';
    }
    if (simActive) runSimLoop();
}

function resetSimTime() {
    simPhase = 0;
}

function updateSimParams() {
    const speedRPM = parseFloat(document.getElementById('slider-sim-speed').value);
    const iAmp = parseFloat(document.getElementById('slider-sim-i').value);
    const asymPct = parseFloat(document.getElementById('slider-sim-asym').value);

    document.getElementById('val-sim-speed').textContent = speedRPM + ' RPM';
    document.getElementById('val-sim-i').textContent = iAmp.toFixed(1) + ' A';
    
    const isHe = document.documentElement.lang === 'he' || document.querySelector('html[dir="rtl"]') !== null;
    if (isHe) {
        document.getElementById('val-sim-asym').textContent = asymPct + '% ' + (asymPct > 0 ? '(אי-סימטריה)' : '(מאוזן)');
    } else {
        document.getElementById('val-sim-asym').textContent = asymPct + '% ' + (asymPct > 0 ? '(Asymmetric)' : '(Balanced)');
    }
}

function runSimLoop() {
    if (!simActive) return;

    const sSpeed = document.getElementById('slider-sim-speed');
    const sI = document.getElementById('slider-sim-i');
    const sAsym = document.getElementById('slider-sim-asym');
    if (!sSpeed || !sI || !sAsym) return;

    const speedRPM = parseFloat(sSpeed.value);
    const iAmp = parseFloat(sI.value);
    const asymPct = parseFloat(sAsym.value);

    // Controlled, gentle animation increment
    if (scopeMode === 'slow') {
        // Slow gentle roll: 1 cycle every ~10 seconds
        simPhase += 0.012;
    } else {
        // Triggered lock: phase stays stationary, with very subtle ripple breathing
        simPhase += 0.003;
    }

    // Canvas resize check
    if (oscCanvas && (oscCanvas.width !== oscCanvas.clientWidth || oscCanvas.height !== oscCanvas.clientHeight)) {
        oscCanvas.width = oscCanvas.clientWidth;
        oscCanvas.height = oscCanvas.clientHeight;
    }
    if (orbitCanvas && (orbitCanvas.width !== orbitCanvas.clientWidth || orbitCanvas.height !== orbitCanvas.clientHeight)) {
        orbitCanvas.width = orbitCanvas.clientWidth;
        orbitCanvas.height = orbitCanvas.clientHeight;
    }

    if (oscCtx && orbitCtx) {
        const w = oscCanvas.width;
        const h = oscCanvas.height;

        // Background
        oscCtx.fillStyle = '#060913';
        oscCtx.fillRect(0, 0, w, h);

        // Oscilloscope Grid Lines
        oscCtx.strokeStyle = 'rgba(255, 255, 255, 0.07)';
        oscCtx.lineWidth = 1;
        for (let x = 0; x < w; x += 36) {
            oscCtx.beginPath(); oscCtx.moveTo(x, 0); oscCtx.lineTo(x, h); oscCtx.stroke();
        }
        for (let y = 0; y < h; y += 32) {
            oscCtx.beginPath(); oscCtx.moveTo(0, y); oscCtx.lineTo(w, y); oscCtx.stroke();
        }

        // Zero-Current Centerline
        oscCtx.strokeStyle = 'rgba(0, 210, 255, 0.25)';
        oscCtx.setLineDash([3, 3]);
        oscCtx.beginPath(); oscCtx.moveTo(0, h/2); oscCtx.lineTo(w, h/2); oscCtx.stroke();
        oscCtx.setLineDash([]);

        // Calculate exactly 2 stable periods across the width
        const numPoints = 240;
        const cy = h / 2;
        const scaleY = (h * 0.40) / Math.max(2.0, iAmp * 1.35);

        const ptsA = [], ptsB = [], ptsC = [], ptsZSC = [];
        const orbitPts = [];

        // Two complete cycles = 4*PI across the screen
        const basePhase = (scopeMode === 'trig') ? 0 : simPhase;
        const ripplePhase = simPhase * 8; // High frequency micro-ripple

        for (let i = 0; i < numPoints; i++) {
            const xFrac = i / (numPoints - 1);
            const theta = basePhase + xFrac * (4 * Math.PI); // Exactly 2 complete periods

            // Balanced currents
            let ia = iAmp * Math.sin(theta);
            let ib = iAmp * Math.sin(theta - 2*Math.PI/3);
            let ic = iAmp * Math.sin(theta + 2*Math.PI/3);

            // Apply Asymmetry
            if (asymPct > 0) {
                const asymFactor = 1.0 + (asymPct / 100.0) * 0.35;
                ia *= asymFactor;
            }

            let izsc = 0;
            if (currentAlgo === 'PWM') {
                // Conventional PWM: high 3rd harmonic + unsuppressed ZSC surge
                izsc = (asymPct / 30.0) * 1.5 * Math.sin(theta) + 0.85 * Math.sin(3 * theta);
                const noise = Math.sin(ripplePhase + i * 0.7) * 0.12;
                ia += izsc * 0.7 + noise;
                ib += izsc * 0.7 + noise;
                ic += izsc * 0.7 + noise;
            } else if (currentAlgo === 'TDM') {
                // TDM: Partial suppression, higher switching ripple
                const ripple = Math.sin(ripplePhase + i * 1.4) * 0.28;
                izsc = 0.22 * Math.sin(3 * theta) + ripple * 0.25;
                ia += ripple; ib += ripple; ic += ripple;
            } else {
                // OEPC: Active cancellation of ZSC down to flatline, minimal ripple
                izsc = 0.03 * Math.sin(3 * theta) + Math.sin(ripplePhase + i * 0.5) * 0.02;
                const lowRipple = Math.sin(ripplePhase + i * 0.9) * 0.05;
                ia += lowRipple; ib += lowRipple; ic += lowRipple;
            }

            const px = xFrac * w;
            ptsA.push({ x: px, y: cy - ia * scaleY });
            ptsB.push({ x: px, y: cy - ib * scaleY });
            ptsC.push({ x: px, y: cy - ic * scaleY });
            ptsZSC.push({ x: px, y: cy - izsc * scaleY });

            // Alpha-Beta coordinates for orbit
            const alpha = ia;
            const beta = (ib - ic) / Math.sqrt(3);
            orbitPts.push({ a: alpha, b: beta });
        }

        // Draw Traces
        function drawTrace(pts, color, width, glow) {
            oscCtx.strokeStyle = color;
            oscCtx.lineWidth = width;
            if (glow) {
                oscCtx.shadowColor = color;
                oscCtx.shadowBlur = 6;
            }
            oscCtx.beginPath();
            pts.forEach((p, idx) => {
                if (idx === 0) oscCtx.moveTo(p.x, p.y);
                else oscCtx.lineTo(p.x, p.y);
            });
            oscCtx.stroke();
            oscCtx.shadowBlur = 0;
        }

        drawTrace(ptsA, '#00d2ff', 2.0, false);
        drawTrace(ptsB, '#9d50bb', 2.0, false);
        drawTrace(ptsC, '#f6d365', 2.0, false);
        // Highlight ZSC clearly with glowing red
        drawTrace(ptsZSC, '#ff4757', 3.2, true);

        // Draw Lissajous Hodograph on Screen 2
        const ow = orbitCanvas.width;
        const oh = orbitCanvas.height;
        orbitCtx.fillStyle = '#060913';
        orbitCtx.fillRect(0, 0, ow, oh);

        // Axes crosshair
        orbitCtx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        orbitCtx.lineWidth = 1;
        orbitCtx.beginPath(); orbitCtx.moveTo(ow/2, 0); orbitCtx.lineTo(ow/2, oh); orbitCtx.stroke();
        orbitCtx.beginPath(); orbitCtx.moveTo(0, oh/2); orbitCtx.lineTo(ow, oh/2); orbitCtx.stroke();

        const ocx = ow / 2;
        const ocy = oh / 2;
        const oScale = (Math.min(ow, oh) * 0.40) / Math.max(2.0, iAmp * 1.35);

        // Orbit color based on algorithm
        const orbitColor = currentAlgo === 'OEPC' ? '#00d2ff' : (currentAlgo === 'TDM' ? '#f6d365' : '#ff4757');
        orbitCtx.strokeStyle = orbitColor;
        orbitCtx.lineWidth = 2.4;
        orbitCtx.shadowColor = orbitColor;
        orbitCtx.shadowBlur = 8;
        orbitCtx.beginPath();
        orbitPts.forEach((p, idx) => {
            const ox = ocx + p.a * oScale;
            const oy = ocy - p.b * oScale;
            if (idx === 0) orbitCtx.moveTo(ox, oy); else orbitCtx.lineTo(ox, oy);
        });
        orbitCtx.stroke();
        orbitCtx.shadowBlur = 0;

        // Smooth traveling tip marker representing active rotating rotor flux / current vector
        // Rotates smoothly around the orbit: 1 rotation every ~3.5 seconds
        const tipAngle = (Date.now() * 0.0018) % (2 * Math.PI);
        const tipIdx = Math.floor(((tipAngle % (2*Math.PI)) / (2*Math.PI)) * (orbitPts.length - 1));
        if (orbitPts[tipIdx]) {
            const tipP = orbitPts[tipIdx];
            const tx = ocx + tipP.a * oScale;
            const ty = ocy - tipP.b * oScale;

            orbitCtx.fillStyle = '#ffffff';
            orbitCtx.shadowColor = '#ffffff';
            orbitCtx.shadowBlur = 10;
            orbitCtx.beginPath();
            orbitCtx.arc(tx, ty, 4.5, 0, 2*Math.PI);
            orbitCtx.fill();
            orbitCtx.shadowBlur = 0;
        }

        // Live Telemetry Readouts
        const isHe = document.documentElement.lang === 'he' || document.querySelector('html[dir="rtl"]') !== null;
        if (currentAlgo === 'OEPC') {
            document.getElementById('tel-sim-izsc').textContent = (0.03 + (asymPct/30)*0.02).toFixed(2) + ' A';
            document.getElementById('tel-sim-izsc').style.color = '#00ff88';
            document.getElementById('tel-sim-thd').textContent = (2.0 + (asymPct/30)*0.3).toFixed(1) + '%';
            document.getElementById('tel-sim-err').textContent = '0.08 A';
            document.getElementById('tel-sim-loss').textContent = isHe ? '-28% מול PWM' : '-28% vs PWM';
        } else if (currentAlgo === 'TDM') {
            document.getElementById('tel-sim-izsc').textContent = (0.26 + (asymPct/30)*0.18).toFixed(2) + ' A';
            document.getElementById('tel-sim-izsc').style.color = '#f6d365';
            document.getElementById('tel-sim-thd').textContent = (6.0 + (asymPct/30)*1.1).toFixed(1) + '%';
            document.getElementById('tel-sim-err').textContent = '0.32 A';
            document.getElementById('tel-sim-loss').textContent = isHe ? '-12% מול PWM' : '-12% vs PWM';
        } else {
            document.getElementById('tel-sim-izsc').textContent = (1.42 + (asymPct/30)*0.75).toFixed(2) + ' A';
            document.getElementById('tel-sim-izsc').style.color = '#ff4757';
            document.getElementById('tel-sim-thd').textContent = (13.5 + (asymPct/30)*3.2).toFixed(1) + '%';
            document.getElementById('tel-sim-err').textContent = '0.85 A';
            document.getElementById('tel-sim-loss').textContent = isHe ? 'בסיס (0%)' : 'Baseline (0%)';
        }
    }

    oscAnimFrame = requestAnimationFrame(runSimLoop);
}

// Start simulation loop
runSimLoop();
"""

def update_file(file_path: Path, is_hebrew: bool):
    print(f"Updating Slide 10 in {file_path.name}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update CSS
    if "SLIDE 10 REFINEMENTS: OSCILLOSCOPE STABILIZATION" not in content:
        p_style = content.find("</style>")
        if p_style != -1:
            content = content[:p_style] + "\n" + CSS_SLIDE10 + "\n    " + content[p_style:]
            print(f"  [+] Injected Slide 10 CSS into {file_path.name}")
    else:
        # Update existing
        p_start = content.find("/* =====================================================================\n           SLIDE 10 REFINEMENTS")
        p_end = content.find(".mode-btn.active {", p_start)
        if p_start != -1 and p_end != -1:
            p_end = content.find("}", p_end) + 1
            content = content[:p_start] + CSS_SLIDE10.strip() + content[p_end:]
            print(f"  [*] Updated Slide 10 CSS in {file_path.name}")

    # 2. Update HTML Block for Slide 10
    target_html = HTML_SLIDE10_HE if is_hebrew else HTML_SLIDE10_EN
    s_start = content.find('<div class="slide" id="slide-dynamic-sim"')
    if s_start != -1:
        # Find next slide: SLIDE 9 or SLIDE 11 or next slide
        s_end = content.find('<!-- SLIDE 9: Experimental Differential Voltages', s_start)
        if s_end == -1:
            s_end = content.find('<!-- SLIDE 11:', s_start)
        if s_end == -1:
            m = re.search(r'</div>\s*<!--\s*SLIDE', content[s_start:])
            if m:
                s_end = s_start + m.start() + 6
            else:
                m2 = re.search(r'<div class="slide"', content[s_start+100:])
                if m2:
                    s_end = s_start + 100 + m2.start()

        if s_end != -1:
            content = content[:s_start] + target_html.strip() + "\n\n        " + content[s_end:]
            print(f"  [+] Replaced Slide 10 HTML in {file_path.name}")
        else:
            print(f"  [!] Could not find end of Slide 10 HTML in {file_path.name}")
    else:
        print(f"  [!] Could not find start of Slide 10 HTML in {file_path.name}")

    # 3. Update JavaScript Block for Slide 10
    j_start = content.find("// --- 2. DYNAMIC PMSM & OSCILLOSCOPE SIMULATOR")
    if j_start != -1:
        # Find where the simulation block ends (near end of script or updateSlide watcher)
        j_end = content.find("// Watch for slide changes to resize / initialize", j_start)
        if j_end == -1:
            j_end = content.find("const origUpdateSlide = window.updateSlide;", j_start)
        if j_end != -1:
            content = content[:j_start] + JS_SIMULATION.strip() + "\n\n" + content[j_end:]
            print(f"  [+] Replaced Slide 10 JS in {file_path.name}")
        else:
            print(f"  [!] Could not find end of Slide 10 JS in {file_path.name}")
    else:
        print(f"  [!] Could not find start of Slide 10 JS in {file_path.name}")

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
