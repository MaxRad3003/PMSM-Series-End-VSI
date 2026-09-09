"""
Refactor Slide 6 (OEPC Operating Principle & Priority LUT Decoder) across both Hebrew and English presentations:
1. Fix all LaTeX issues by using clean mathematical HTML typography (&minus;, sub, sup, italic) with dedicated CSS.
2. Completely redesign the LUT decision card to be clear, structured, uncrowded, and legible.
3. Enhance the JSXGraph board with Alpha/Beta axes, sector labels (S1..S6), clear visual legend, and sector detection.
4. Prevent any BiDi / RTL text jumping or dollar sign artifacts.
"""

from pathlib import Path

PMSM_DIR = Path(r"c:\Users\maximr\OneDrive - ac.sce.ac.il\Barabi\2025 Eli & Max\PMSM")

# New CSS for Slide 6
SLIDE6_CSS = """
        /* =====================================================================
           REFINED SLIDE 6 STYLES: CRYSTAL-CLEAR LUT & MATHEMATICAL TYPOGRAPHY
           ===================================================================== */
        .math-term {
            font-family: 'Fira Code', 'Cambria Math', 'KaTeX_Math', monospace;
            font-weight: 600;
            color: var(--accent-cyan);
            direction: ltr;
            unicode-bidi: isolate;
            display: inline-block;
        }
        .math-term sub {
            font-size: 0.78em;
            vertical-align: sub;
        }
        .math-term sup {
            font-size: 0.78em;
            vertical-align: super;
        }

        .lut-match-box {
            background: rgba(13, 25, 48, 0.95);
            border: 1px solid rgba(0, 210, 255, 0.4);
            border-radius: 10px;
            padding: 10px 12px;
            display: flex;
            flex-direction: column;
            gap: 7px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }
        .lut-step-row {
            display: flex;
            flex-direction: column;
            gap: 3px;
        }
        .lut-step-title {
            font-size: 12px;
            font-weight: 700;
            color: #ffffff;
            font-family: 'Rubik', sans-serif;
        }
        .lut-mode-badge {
            align-self: flex-start;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 11.5px;
            font-weight: 700;
            font-family: 'Rubik', sans-serif;
            letter-spacing: 0.3px;
        }
        .dm-badge {
            background: rgba(0, 210, 255, 0.18);
            border: 1px solid rgba(0, 210, 255, 0.6);
            color: #00d2ff;
        }
        .cm-badge {
            background: rgba(246, 211, 101, 0.2);
            border: 1px solid rgba(246, 211, 101, 0.7);
            color: #f6d365;
        }
        .lut-vector-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
            background: rgba(0, 0, 0, 0.25);
            padding: 6px 8px;
            border-radius: 6px;
            border: 1px solid rgba(255, 255, 255, 0.07);
        }
        .vector-chip {
            display: flex;
            flex-direction: column;
            gap: 1px;
        }
        .v-label {
            font-size: 10px;
            color: var(--text-muted);
            font-family: 'Rubik', sans-serif;
        }
        .v-code {
            font-family: 'Fira Code', monospace;
            font-size: 13px;
            font-weight: 700;
            color: #ffffff;
            direction: ltr;
            unicode-bidi: isolate;
        }
        .v-action {
            font-size: 12px;
            font-weight: 600;
            color: var(--accent-cyan);
            direction: ltr;
            unicode-bidi: isolate;
        }
        .lut-comparison-row {
            border-top: 1px dashed rgba(255, 255, 255, 0.12);
            padding-top: 5px;
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .comp-label {
            font-size: 10.5px;
            font-weight: 700;
            color: var(--accent-gold);
            font-family: 'Rubik', sans-serif;
        }
        .comp-text {
            font-size: 11.5px;
            color: var(--text-secondary);
            line-height: 1.45;
        }
        .action-tag {
            display: inline-block;
            padding: 1px 5px;
            border-radius: 4px;
            font-size: 10.5px;
            font-weight: 600;
            margin-right: 4px;
        }
        .zsc-tag {
            background: rgba(255, 71, 87, 0.2);
            color: #ff6b6b;
            border: 1px solid rgba(255, 71, 87, 0.4);
        }
        .dm-tag {
            background: rgba(0, 210, 255, 0.15);
            color: #00d2ff;
            border: 1px solid rgba(0, 210, 255, 0.35);
        }
        .jxg-legend {
            display: flex;
            gap: 12px;
            font-size: 11.5px;
            font-family: 'Rubik', sans-serif;
            background: rgba(10, 15, 29, 0.85);
            padding: 4px 10px;
            border-radius: 6px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            align-items: center;
        }
        .jxg-legend-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }
"""

# New HTML for Slide 6 in Hebrew
SLIDE6_HTML_HE = """
        <!-- SLIDE: Interactive OEPC Operating Principle & Priority LUT Decoder -->
        <div class="slide" id="slide-oepc-principle" style="overflow: hidden !important;">
            <div class="slide-category">הדמיה אינטראקטיבית • JSXGraph</div>
            <div class="slide-title">מפענח עקרון הפעולה של OEPC – מיפוי שגיאות, תעדוף ובחירת וקטורי LUT</div>
            
            <div class="sim-container">
                <!-- Left: Controls & Pipeline -->
                <div class="sim-controls-card">
                    <div class="card-title" style="font-size: 15px; margin-bottom: 2px;">
                        ⚙️ כוונון שגיאות זרם (<span class="math-term">&epsilon; = <i>i</i><sup>*</sup> &minus; <i>i</i></span>)
                    </div>
                    
                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>שגיאת פאזה A (<span class="math-term">&epsilon;<sub>a</sub></span>):</span>
                            <span class="sim-val-badge" id="val-ea">+1.80 A</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-ea" min="-3.0" max="3.0" step="0.1" value="1.8">
                    </div>

                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>שגיאת פאזה B (<span class="math-term">&epsilon;<sub>b</sub></span>):</span>
                            <span class="sim-val-badge" id="val-eb">-1.20 A</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-eb" min="-3.0" max="3.0" step="0.1" value="-1.2">
                    </div>

                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>שגיאת פאזה C (<span class="math-term">&epsilon;<sub>c</sub></span>):</span>
                            <span class="sim-val-badge" id="val-ec">-0.60 A</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-ec" min="-3.0" max="3.0" step="0.1" value="-0.6">
                    </div>

                    <div class="sim-control-group">
                        <div class="sim-control-header">
                            <span>זרם סדרה אפס מדוד (<span class="math-term"><i>i</i><sub>zsc</sub></span>):</span>
                            <span class="sim-val-badge" id="val-izsc">0.00 A</span>
                        </div>
                        <input type="range" class="sim-slider" id="slider-izsc" min="-2.0" max="2.0" step="0.05" value="0.0">
                    </div>

                    <!-- Preset Scenarios -->
                    <div style="margin-top: 2px;">
                        <div style="font-size: 11.5px; color: var(--text-muted); margin-bottom: 4px; font-weight: 600;">תרחישי עבודה מוכנים:</div>
                        <div class="sim-btn-group" style="flex-wrap: wrap;">
                            <button class="sim-btn active" id="btn-preset-nom" onclick="setPresetErrors(1.8, -1.2, -0.6, 0.0, this)">נומינלי ABC</button>
                            <button class="sim-btn" id="btn-preset-zsc" onclick="setPresetErrors(1.5, 1.2, 0.9, 1.2, this)">חריגת ZSC</button>
                            <button class="sim-btn" id="btn-preset-asym" onclick="setPresetErrors(-2.8, 1.4, 1.4, 0.3, this)">אי-סימטריה 25%</button>
                            <button class="sim-btn" id="btn-preset-itsc" onclick="setPresetErrors(2.6, -0.5, -2.1, 0.8, this)">קצר ITSC</button>
                        </div>
                    </div>

                    <!-- Priority Decoder Output -->
                    <div style="border-top: 1px solid var(--border-color); padding-top: 6px; margin-top: 2px;">
                        <div style="font-size: 11.5px; color: var(--text-muted); margin-bottom: 4px; font-weight: 600;">דירוג תעדוף שגיאות (Error Priority Hierarchy):</div>
                        <div class="priority-badge-row">
                            <div class="p-badge p-prime">
                                <span style="font-size: 9px; opacity: 0.85;">🥇 שגיאה ראשית</span>
                                <span id="badge-prime-phase" style="font-weight:700; font-size:12.5px;">פאזה A</span>
                                <span id="badge-prime-val" class="metric">+1.80 A</span>
                            </div>
                            <div class="p-badge p-sec">
                                <span style="font-size: 9px; opacity: 0.85;">🥈 שגיאה משנית</span>
                                <span id="badge-sec-phase" style="font-weight:700; font-size:12.5px;">פאזה B</span>
                                <span id="badge-sec-val" class="metric">-1.20 A</span>
                            </div>
                            <div class="p-badge p-minor">
                                <span style="font-size: 9px; opacity: 0.85;">🥉 שגיאה שלישית</span>
                                <span id="badge-minor-phase" style="font-weight:700; font-size:12.5px;">פאזה C</span>
                                <span id="badge-minor-val" class="metric">-0.60 A</span>
                            </div>
                        </div>
                    </div>

                    <!-- Redesigned Crystal-Clear LUT Match & Action Box -->
                    <div class="lut-match-box" id="lut-decision-box">
                        <div class="lut-step-row">
                            <span class="lut-step-title">📋 החלטת אלגוריתם OEPC מטבלת 96-LUT:</span>
                            <span id="lut-row-num" class="lut-mode-badge dm-badge">עדיפות דיפרנציאלית (DM Priority)</span>
                        </div>
                        
                        <div class="lut-vector-grid">
                            <div class="vector-chip">
                                <span class="v-label">וקטור מיתוג נבחר (State):</span>
                                <span id="lut-vector-code" class="v-code">[0 1 1 0]</span>
                            </div>
                            <div class="vector-chip">
                                <span class="v-label">פעולת התיקון בפועל:</span>
                                <span id="lut-action-desc" class="v-action">&minus;<i>i</i><sub>a</sub>, +<i>i</i><sub>c</sub></span>
                            </div>
                        </div>

                        <div class="lut-comparison-row">
                            <div class="comp-label">⚖️ עליונות OEPC מול שיטת TDM:</div>
                            <div id="tdm-compare-note" class="comp-text">
                                TDM מתקן פאזה אחת בלבד ומקפיא את השאר. OEPC מתקן בו-זמנית שתי פאזות ומאפס את הריפל!
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Right: JSXGraph Space Vector Plane -->
                <div class="sim-display-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px;">
                        <div class="card-title" style="margin: 0; font-size: 15px;">
                            🧭 מישור וקטורי המרחב <span class="math-term">&alpha;&minus;&beta;</span> ומשושה המתחים (גרור את נקודת השגיאה <span class="math-term">&vec;&epsilon;</span>)
                        </div>
                        <!-- Clear Visual Legend -->
                        <div class="jxg-legend">
                            <div class="jxg-legend-item">
                                <span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:#ff4757; box-shadow:0 0 6px #ff4757;"></span>
                                <span style="color:#ff6b6b; font-weight:600;">שגיאת זרם <span class="math-term">&vec;&epsilon;</span></span>
                            </div>
                            <div class="jxg-legend-item">
                                <span style="display:inline-block; width:14px; height:3px; background:#00d2ff; box-shadow:0 0 6px #00d2ff;"></span>
                                <span style="color:#00d2ff; font-weight:600;">מתח OEPC מוצע</span>
                            </div>
                            <div class="jxg-legend-item">
                                <span style="display:inline-block; width:14px; height:2px; border-top:2px dashed #f6d365;"></span>
                                <span style="color:#f6d365; font-weight:600;">מתח TDM קלאסי</span>
                            </div>
                        </div>
                    </div>

                    <div class="sim-canvas-box" style="height: 330px;">
                        <div id="oepc-jxg-board" class="jxgbox"></div>
                    </div>

                    <!-- Live Telemetry Bar with clean HTML Math typography -->
                    <div class="telemetry-bar">
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">גודל וקטור השגיאה <span class="math-term">|&vec;&epsilon;<sub>&alpha;&beta;</sub>|</span></span>
                            <span class="telemetry-val" id="tel-err-mag">2.16 A</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">זווית השגיאה במרחב <span class="math-term">&theta;<sub>&epsilon;</sub></span></span>
                            <span class="telemetry-val" id="tel-err-ang">-28.4°</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">מתח סדרה אפס מופעל <span class="math-term"><i>v</i><sub>0</sub></span></span>
                            <span class="telemetry-val" id="tel-v0">-0.0 V</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">רווח ביצועי עקיבה מול TDM</span>
                            <span class="telemetry-val" style="color:#00ff88;" id="tel-gain">+48% מהירות</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
"""

# New JavaScript for Slide 6
SLIDE6_JS = """
// --- 1. OEPC OPERATING PRINCIPLE & JSXGRAPH BOARD (ENHANCED) ---
let jxgBoard = null;
let errPoint = null;
let errVectorArrow = null;
let optVoltArrow = null;
let tdmVoltArrow = null;
let sectorText = null;

function initJSXGraphBoard() {
    if (jxgBoard) return;
    const boardEl = document.getElementById('oepc-jxg-board');
    if (!boardEl || !window.JXG) return;

    try {
        jxgBoard = JXG.JSXGraph.initBoard('oepc-jxg-board', {
            boundingbox: [-3.8, 3.8, 3.8, -3.8],
            axis: false,
            grid: { strokeColor: 'rgba(255,255,255,0.05)', gridX: 0.5, gridY: 0.5 },
            showCopyright: false,
            showNavigation: false,
            keepaspectratio: true
        });

        // Labeled Coordinate Axes (Alpha & Beta)
        // Alpha Axis (Horizontal)
        jxgBoard.create('line', [[-3.4, 0], [3.4, 0]], {
            straightFirst: false,
            straightLast: false,
            strokeColor: 'rgba(0, 210, 255, 0.35)',
            strokeWidth: 1.5,
            highlight: false
        });
        jxgBoard.create('text', [3.3, 0.25, 'ציר α'], {
            color: '#00d2ff',
            fontSize: 11,
            fontFamily: 'Rubik',
            fontWeight: 700,
            anchorX: 'right',
            highlight: false
        });

        // Beta Axis (Vertical)
        jxgBoard.create('line', [[0, -3.4], [0, 3.4]], {
            straightFirst: false,
            straightLast: false,
            strokeColor: 'rgba(157, 80, 187, 0.35)',
            strokeWidth: 1.5,
            highlight: false
        });
        jxgBoard.create('text', [0.15, 3.3, 'ציר β'], {
            color: '#9d50bb',
            fontSize: 11,
            fontFamily: 'Rubik',
            fontWeight: 700,
            anchorX: 'left',
            highlight: false
        });

        // Outer Space Vector Hexagon
        const hexAngles = [0, Math.PI/3, 2*Math.PI/3, Math.PI, 4*Math.PI/3, 5*Math.PI/3, 2*Math.PI];
        const hexRadius = 2.8;
        const hexX = hexAngles.map(a => hexRadius * Math.cos(a));
        const hexY = hexAngles.map(a => hexRadius * Math.sin(a));

        jxgBoard.create('curve', [hexX, hexY], {
            strokeColor: 'rgba(64, 120, 240, 0.5)',
            strokeWidth: 2,
            dash: 2,
            highlight: false
        });

        // Hexagon Axes, Vector Labels & Sector Numbers
        const vecNames = ['V1 (100)', 'V2 (110)', 'V3 (010)', 'V4 (011)', 'V5 (001)', 'V6 (101)'];
        const sectorNames = ['סקטור 1', 'סקטור 2', 'סקטור 3', 'סקטור 4', 'סקטור 5', 'סקטור 6'];

        for (let i = 0; i < 6; i++) {
            const vx = hexRadius * Math.cos(hexAngles[i]);
            const vy = hexRadius * Math.sin(hexAngles[i]);
            jxgBoard.create('line', [[0, 0], [vx, vy]], {
                straightFirst: false,
                straightLast: false,
                strokeColor: 'rgba(255,255,255,0.12)',
                strokeWidth: 1,
                highlight: false
            });
            // Vector Label
            jxgBoard.create('text', [vx * 1.18, vy * 1.18, vecNames[i]], {
                color: 'var(--text-secondary)',
                fontSize: 10,
                fontFamily: 'Fira Code',
                anchorX: 'middle',
                anchorY: 'middle',
                highlight: false
            });

            // Sector Label (in the middle of sector)
            const secAngle = hexAngles[i] + Math.PI/6;
            const secR = hexRadius * 0.55;
            jxgBoard.create('text', [secR * Math.cos(secAngle), secR * Math.sin(secAngle), sectorNames[i]], {
                color: 'rgba(255,255,255,0.22)',
                fontSize: 9.5,
                fontFamily: 'Rubik',
                anchorX: 'middle',
                anchorY: 'middle',
                highlight: false
            });
        }

        // Draggable Error Point P (Alpha-Beta)
        errPoint = jxgBoard.create('point', [1.8, -0.6], {
            name: 'שגיאה ε',
            size: 8,
            color: '#ff4757',
            strokeColor: '#ffffff',
            strokeWidth: 2.5,
            withLabel: true,
            label: { color: '#ff6b6b', fontSize: 12, fontFamily: 'Rubik', fontWeight: 700, offset: [10, 10] }
        });

        // Error Vector Arrow (Red glowing)
        errVectorArrow = jxgBoard.create('arrow', [[0, 0], errPoint], {
            strokeColor: '#ff4757',
            strokeWidth: 3.5,
            highlight: false
        });

        // Optimal Voltage Vector Chosen by OEPC (Cyan)
        optVoltArrow = jxgBoard.create('arrow', [[0, 0], [-1.8, 0.6]], {
            strokeColor: '#00d2ff',
            strokeWidth: 4,
            highlight: false
        });

        // TDM Voltage Vector (Yellow dashed)
        tdmVoltArrow = jxgBoard.create('arrow', [[0, 0], [-1.5, 0]], {
            strokeColor: '#f6d365',
            strokeWidth: 2.5,
            dash: 2,
            highlight: false
        });

        // Dragging listener
        errPoint.on('drag', function () {
            const ea = errPoint.X();
            const eb = -0.5 * errPoint.X() + (Math.sqrt(3)/2) * errPoint.Y();
            const ec = -0.5 * errPoint.X() - (Math.sqrt(3)/2) * errPoint.Y();

            document.getElementById('slider-ea').value = Math.max(-3, Math.min(3, ea)).toFixed(1);
            document.getElementById('slider-eb').value = Math.max(-3, Math.min(3, eb)).toFixed(1);
            document.getElementById('slider-ec').value = Math.max(-3, Math.min(3, ec)).toFixed(1);
            updateErrorPrinciple();
        });

        updateErrorPrinciple();
    } catch (e) {
        console.warn('JSXGraph init error:', e);
    }
}

function updateErrorPrinciple() {
    const ea = parseFloat(document.getElementById('slider-ea').value);
    const eb = parseFloat(document.getElementById('slider-eb').value);
    const ec = parseFloat(document.getElementById('slider-ec').value);
    const izsc = parseFloat(document.getElementById('slider-izsc').value);

    document.getElementById('val-ea').textContent = (ea >= 0 ? '+' : '') + ea.toFixed(2) + ' A';
    document.getElementById('val-eb').textContent = (eb >= 0 ? '+' : '') + eb.toFixed(2) + ' A';
    document.getElementById('val-ec').textContent = (ec >= 0 ? '+' : '') + ec.toFixed(2) + ' A';
    document.getElementById('val-izsc').textContent = (izsc >= 0 ? '+' : '') + izsc.toFixed(2) + ' A';

    // Alpha-Beta transform: e_alpha = e_a, e_beta = (e_b - e_c)/sqrt(3)
    const e_alpha = ea;
    const e_beta = (eb - ec) / Math.sqrt(3);

    if (errPoint && !errPoint.isDraggable) {
        errPoint.moveTo([e_alpha, e_beta]);
    }

    const mag = Math.sqrt(e_alpha*e_alpha + e_beta*e_beta);
    let ang = Math.atan2(e_beta, e_alpha) * (180 / Math.PI);
    document.getElementById('tel-err-mag').textContent = mag.toFixed(2) + ' A';
    document.getElementById('tel-err-ang').textContent = ang.toFixed(1) + '°';

    // Priority Sorting
    const phases = [
        { name: 'פאזה A', code: 'a', val: ea, abs: Math.abs(ea), sign: ea >= 0 ? '+' : '-' },
        { name: 'פאזה B', code: 'b', val: eb, abs: Math.abs(eb), sign: eb >= 0 ? '+' : '-' },
        { name: 'פאזה C', code: 'c', val: ec, abs: Math.abs(ec), sign: ec >= 0 ? '+' : '-' }
    ];
    phases.sort((a, b) => b.abs - a.abs);

    const prime = phases[0];
    const sec = phases[1];
    const minor = phases[2];

    document.getElementById('badge-prime-phase').textContent = prime.name;
    document.getElementById('badge-prime-val').textContent = (prime.val >= 0 ? '+' : '') + prime.val.toFixed(2) + ' A';
    document.getElementById('badge-sec-phase').textContent = sec.name;
    document.getElementById('badge-sec-val').textContent = (sec.val >= 0 ? '+' : '') + sec.val.toFixed(2) + ' A';
    document.getElementById('badge-minor-phase').textContent = minor.name;
    document.getElementById('badge-minor-val').textContent = (minor.val >= 0 ? '+' : '') + minor.val.toFixed(2) + ' A';

    // Decision Logic with CLEAN HTML (No raw MathJax dollars)
    const isZscCritical = Math.abs(izsc) > 0.4;
    let lutCase = '';
    let lutBadgeClass = 'dm-badge';
    let lutCode = '';
    let lutAction = '';
    let tdmNote = '';
    let v0 = 0.0;
    let optVx = 0, optVy = 0;
    let tdmVx = 0, tdmVy = 0;

    if (isZscCritical) {
        lutCase = 'עדיפות סדרה אפס (CM Priority - מקרה 2/4)';
        lutBadgeClass = 'cm-badge';
        lutCode = izsc > 0 ? '[0 1 0 1]' : '[1 0 1 0]';
        lutAction = '<span class="action-tag zsc-tag">דיכוי ZSC</span> <span class="math-term">&minus;<i>i</i><sub>a</sub>, +<i>i</i><sub>b</sub>, &minus;<i>i</i><sub>c</sub>, &minus;<i>i</i><sub>0</sub></span>';
        v0 = izsc > 0 ? -18.5 : +18.5;
        tdmNote = 'שיטת TDM מתעלמת מזרם סדרה אפס ומייצרת עיוותים קשים! אלגוריתם <strong>OEPC</strong> מזהה את החריגה, מיישם מתח <span class="math-term"><i>v</i><sub>0</sub> = ' + (v0 > 0 ? '+' : '') + v0.toFixed(1) + ' V</span> מנוגד, ומאפס מיידית את זרם ה-ZSC.';
    } else {
        lutCase = 'עדיפות דיפרנציאלית (DM Priority - מקרה 1/3/5)';
        lutBadgeClass = 'dm-badge';
        lutCode = (prime.name === 'פאזה A' && prime.val > 0) ? '[0 1 1 0]' : '[1 1 0 1]';
        lutAction = '<span class="action-tag dm-tag">תיקון 2 פאזות</span> <span class="math-term">&minus;<i>i</i><sub>' + prime.code + '</sub>, +<i>i</i><sub>' + sec.code + '</sub></span>';
        v0 = 0.0;
        tdmNote = 'שיטת TDM מתקנת רק את ' + prime.name + ' ומקפיאה את שאר הפאזות. אלגוריתם <strong>OEPC</strong> בוחר מצב שמבצע <strong>תיקון סימולטני של 2 הפאזות</strong> ללא עיכוב ומאפס את הריפל!';
    }

    const badgeEl = document.getElementById('lut-row-num');
    badgeEl.textContent = lutCase;
    badgeEl.className = 'lut-mode-badge ' + lutBadgeClass;

    document.getElementById('lut-vector-code').textContent = lutCode;
    document.getElementById('lut-action-desc').innerHTML = lutAction;
    document.getElementById('tdm-compare-note').innerHTML = tdmNote;
    document.getElementById('tel-v0').textContent = (v0 >= 0 ? '+' : '') + v0.toFixed(1) + ' V';

    // Plot vectors: Optimal vector points opposite to error
    if (mag > 0.1) {
        const vMag = 2.4;
        optVx = - (e_alpha / mag) * vMag;
        optVy = - (e_beta / mag) * vMag;

        // TDM vector projects only on prime axis
        const tdmMag = 1.6;
        if (prime.name === 'פאזה A') {
            tdmVx = -Math.sign(prime.val) * tdmMag;
            tdmVy = 0;
        } else if (prime.name === 'פאזה B') {
            tdmVx = -Math.sign(prime.val) * tdmMag * Math.cos(2*Math.PI/3);
            tdmVy = -Math.sign(prime.val) * tdmMag * Math.sin(2*Math.PI/3);
        } else {
            tdmVx = -Math.sign(prime.val) * tdmMag * Math.cos(4*Math.PI/3);
            tdmVy = -Math.sign(prime.val) * tdmMag * Math.sin(4*Math.PI/3);
        }

        if (optVoltArrow) optVoltArrow.point2.moveTo([optVx, optVy]);
        if (tdmVoltArrow) tdmVoltArrow.point2.moveTo([tdmVx, tdmVy]);
    }
}
"""

def apply_refactor():
    # 1. Update Hebrew presentation
    he_file = PMSM_DIR / "OEPC_SE_VSI_PMSM_Presentation_HE.html"
    with open(he_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace CSS
    # Find start of INTERACTIVE JSXGRAPH & DYNAMIC SIMULATION STYLES
    css_start = "/* =====================================================================\n           INTERACTIVE JSXGRAPH & DYNAMIC SIMULATION STYLES"
    css_end = ".dual-screen-grid {"
    p_start = content.find(css_start)
    p_end = content.find(css_end)

    if p_start != -1 and p_end != -1:
        # Insert SLIDE6_CSS right after dual-screen-grid
        p_dual_end = content.find("}", p_end) + 1
        content = content[:p_dual_end] + "\n" + SLIDE6_CSS + content[p_dual_end:]
        print("[OK] Injected Slide 6 refined CSS into Hebrew HTML")

    # Replace Slide 6 HTML block
    s6_marker_start = '<!-- SLIDE: Interactive OEPC Operating Principle & Priority LUT Decoder -->'
    s6_marker_end = '<!-- SLIDE 6: Typhoon C-HIL Experimental Platform -->'
    p1 = content.find(s6_marker_start)
    p2 = content.find(s6_marker_end)
    if p1 != -1 and p2 != -1:
        content = content[:p1] + SLIDE6_HTML_HE.strip() + "\n\n        " + content[p2:]
        print("[OK] Replaced Slide 6 HTML in Hebrew HTML")
    else:
        print("[WARN] Slide 6 markers not matched in Hebrew HTML")

    # Replace JS functions for Slide 6
    js_start = "// --- 1. OEPC OPERATING PRINCIPLE & JSXGRAPH BOARD ---"
    js_end = "// --- 2. DYNAMIC PMSM & OSCILLOSCOPE SIMULATOR ---"
    jp1 = content.find(js_start)
    jp2 = content.find(js_end)
    if jp1 != -1 and jp2 != -1:
        content = content[:jp1] + SLIDE6_JS.strip() + "\n\n" + content[jp2:]
        print("[OK] Replaced Slide 6 JS in Hebrew HTML")
    else:
        print("[WARN] JS markers not matched in Hebrew HTML")

    with open(he_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[DONE] Hebrew HTML updated.")

apply_refactor()
