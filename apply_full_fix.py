import re

def update_presentation_file(filepath, is_hebrew=True):
    print(f"\n==========================================")
    print(f"Processing: {filepath} (Hebrew={is_hebrew})")
    print(f"==========================================")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Controls Bar HTML
    scope_btn_label = "📌 גל מיוצב (נעול טריגר)" if is_hebrew else "📌 Trigger-Locked Scope"
    scope_btn_title = "ייצוב גל נעול טריגר (2 מחזורים סטציונריים) או גלילה איטית" if is_hebrew else "Trigger-locked stationary 2-cycle view or gentle slow roll"
    speed_label = "מהירות סריקה:" if is_hebrew else "Scan Speed:"

    # Check if btn-demo-scope-mode already exists
    if 'id="btn-demo-scope-mode"' not in content:
        pattern_btn_group = r'(<button[^>]+id="btn-demo-play"[^>]*>.*?</button>\s*<button[^>]+onclick="stepDemoOnce\(\)"[^>]*>.*?</button>\s*<button[^>]+onclick="resetDemo\(\)"[^>]*>.*?</button>\s*</div>)'
        match_bg = re.search(pattern_btn_group, content, re.DOTALL)
        if match_bg:
            scope_btn_html = (
                f'\n\n                    <!-- Trigger Scope Sync Mode Toggle -->\n'
                f'                    <button id="btn-demo-scope-mode" class="demo-btn" onclick="toggleDemoScopeMode()" style="background:rgba(0,255,136,0.15); border-color:#00ff88; color:#00ff88; font-size:0.78rem;" title="{scope_btn_title}">\n'
                f'                        {scope_btn_label}\n'
                f'                    </button>'
            )
            content = content[:match_bg.end()] + scope_btn_html + content[match_bg.end():]
            print("  -> Added btn-demo-scope-mode to controls bar.")
        else:
            print("  -> WARNING: Could not find demo-btn-group to inject scope button!")

    # Update speed label text
    content = re.sub(r'מהירות ריצה:', speed_label, content)
    content = re.sub(r'Run Speed:', speed_label, content)

    # 2. Update the Slide 10 JavaScript Engine
    # Find start and end of Slide 10 IIFE
    idx_iife_start = content.find('// --- 3. SLIDE 11: OEPC SWITCHING & CLOSED-LOOP ERROR CORRECTION ENGINE ---')
    if idx_iife_start == -1:
        idx_iife_start = content.find('// Slide 11: OEPC Switching & Closed-Loop Simulation')
    if idx_iife_start == -1:
        idx_iife_start = content.find('// Slide 11 (Interactive OEPC 96-LUT Switching & Closed-Loop Simulation)')
    if idx_iife_start == -1:
        idx_iife_start = content.find('let demoRunning = true;')
        idx_iife_start = content.rfind('(function()', 0, idx_iife_start)

    print(f"  -> Found Slide 10 IIFE start at index: {idx_iife_start}")

    idx_iife_end = content.find('})();', idx_iife_start)
    if idx_iife_end == -1:
        print("  -> ERROR: Could not find IIFE end (})();)!")
        return False
    idx_iife_end += 5

    # Extract the original IIFE block
    orig_iife = content[idx_iife_start:idx_iife_end]

    # Find parts to replace within the IIFE:
    # 2.1 State variables at the top of IIFE
    var_block_old_pattern = r'(\s*let demoRunning = true;.*?(?=function stepOepcPipeline))'
    match_vars = re.search(var_block_old_pattern, orig_iife, re.DOTALL)
    if not match_vars:
        print("  -> ERROR: Could not find variable declaration block!")
        return False

    var_block_new = '''
    // State & Fault Variables
    let demoRunning = true;
    let demoSpeed = 0.5; // default 0.5x scan speed
    let demoScopeMode = 'trig'; // 'trig' = stationary 2-cycle trigger lock, 'slow' = gentle rolling
    let demoScanTime = 0;
    let demoRollOffset = 0;
    let stepCounter = 0;
    let demoTime = 0;
    let demoAnimId = null;

    // PMSM Parameters for micro-step model
    let Iref = 5.0; // Amperes peak (mutable for load steps)
    const w_elec = 2 * Math.PI * 50; // 50 Hz electrical freq
    let asymPercent = 0; // 0% normal, 35% under asymmetry fault
    let leg4Fault = false;
    let activeFault = 'none';
    let loadSurge = false;
    let disturbanceTimer = 0;

    // Plant states (Physical Closed-Loop Tracking)
    let curIa = 0, curIb = 0, curIc = 0, curIzsc = 0;
    let refIa = 0, refIb = 0, refIc = 0;
    let errA = 0, errB = 0, errC = 0;
    let activeSwitches = [0, 0, 0, 1]; // [Sa, Sb, Sc, Sn]
    let activeVidx = 1;
    let activeImpact = '-C,-Z';
    let activeEpOrder = 'CBA';
    let activeAddr = 16;
    let activeRow = 1;
    let activeFmp = 0;
    let activePab = 0, activePbc = 1, activePca = 0;
    let activeSmx = 0, activeSmd = 0, activeSmn = 0;

    // Circular history buffers for continuous traces
    const HIST_LEN = 260;
    const histIa = new Float32Array(HIST_LEN);
    const histIb = new Float32Array(HIST_LEN);
    const histIc = new Float32Array(HIST_LEN);
    const histRefA = new Float32Array(HIST_LEN);
    const histRefB = new Float32Array(HIST_LEN);
    const histRefC = new Float32Array(HIST_LEN);
    const histEa = new Float32Array(HIST_LEN);
    const histEb = new Float32Array(HIST_LEN);
    const histEc = new Float32Array(HIST_LEN);
    const histIzsc = new Float32Array(HIST_LEN);
    const histSa = new Uint8Array(HIST_LEN);
    const histSb = new Uint8Array(HIST_LEN);
    const histSc = new Uint8Array(HIST_LEN);
    const histSn = new Uint8Array(HIST_LEN);
    let histPtr = 0;
'''

    # 2.2 stepOepcPipeline function
    step_old_pattern = r'(function stepOepcPipeline\(dt\)\s*\{.*?(?=function updateDemoUI))'
    match_step = re.search(step_old_pattern, orig_iife, re.DOTALL)
    if not match_step:
        print("  -> ERROR: Could not find stepOepcPipeline function!")
        return False

    step_block_new = '''function stepOepcPipeline(dt) {
        demoScanTime += dt;
        demoTime += dt;
        if (demoScopeMode === 'slow') {
            demoRollOffset += dt * 0.25; // calm gentle roll
        }

        // 2-Cycle Electrical Angle Window (40 ms @ 50 Hz = 4*PI)
        const T_window = 0.04;
        const scanFrac = (demoScanTime % T_window) / T_window;
        const scanTheta = scanFrac * 4 * Math.PI;

        // 1. References at current scan angle
        refIa = Iref * Math.cos(scanTheta);
        refIb = Iref * Math.cos(scanTheta - (2 * Math.PI / 3));
        refIc = Iref * Math.cos(scanTheta + (2 * Math.PI / 3));

        // 2. High-Frequency Switching Ripple & Physical Disturbance
        const fc = 48; // 48 * 50Hz = 2400 Hz equivalent carrier
        const swPhase = demoScanTime * 25;
        const ripA = 0.08 * Math.sin(fc * scanTheta + swPhase) + 0.02 * Math.cos(2 * fc * scanTheta);
        const ripB = 0.08 * Math.sin(fc * (scanTheta - 2 * Math.PI / 3) + swPhase) + 0.02 * Math.cos(2 * fc * (scanTheta - 2 * Math.PI / 3));
        const ripC = 0.08 * Math.sin(fc * (scanTheta + 2 * Math.PI / 3) + swPhase) + 0.02 * Math.cos(2 * fc * (scanTheta + 2 * Math.PI / 3));

        // Asymmetry component (35% on Phase A)
        const asymWave = (asymPercent / 100.0) * 0.45 * Math.cos(scanTheta);

        // Surge shock disturbance
        let distVal = 0;
        if (disturbanceTimer > 0) {
            distVal = 0.75 * Math.sin(disturbanceTimer * 35) * (disturbanceTimer / 0.08);
            disturbanceTimer -= dt;
            if (disturbanceTimer < 0) disturbanceTimer = 0;
        }

        // Error synthesis
        errA = Math.max(-1.1, Math.min(1.1, ripA + asymWave + distVal));
        errB = Math.max(-1.1, Math.min(1.1, ripB - 0.5 * asymWave - 0.5 * distVal));
        errC = Math.max(-1.1, Math.min(1.1, ripC - 0.5 * asymWave - 0.5 * distVal));

        // Actual currents
        curIa = refIa - errA;
        curIb = refIb - errB;
        curIc = refIc - errC;

        // Zero-sequence current
        if (leg4Fault) {
            curIzsc = 0.65 * (asymPercent > 0 ? (asymPercent / 35.0) : 1.0) * Math.sin(3 * scanTheta) + distVal * 0.3;
        } else if (asymPercent > 0) {
            curIzsc = 0.03 * Math.sin(3 * scanTheta); // OEPC 4th leg active cancellation clamps ZSC < 0.04A!
        } else {
            curIzsc = 0.015 * Math.sin(3 * scanTheta);
        }

        // 3. OEPC Error Priority Sorting Pipeline (from Slide 6 theory)
        const absA = Math.abs(errA);
        const absB = Math.abs(errB);
        const absC = Math.abs(errC);

        const epsA = absA;
        const epsB = absB + (absB === absA ? 1e-6 : 0);
        const epsC = absC + (absC === absA || absC === absB ? 2e-6 : 0);

        activePab = (epsA >= epsB) ? 1 : 0;
        activePbc = (epsB >= epsC) ? 1 : 0;
        activePca = (epsC >= epsA) ? 1 : 0;

        let maxVal = errA, midVal = errB, minVal = errC;

        if (epsA >= epsB && epsB >= epsC) {
            activeEpOrder = 'ABC'; maxVal = errA; midVal = errB; minVal = errC;
        } else if (epsA >= epsC && epsC >= epsB) {
            activeEpOrder = 'ACB'; maxVal = errA; midVal = errC; minVal = errB;
        } else if (epsB >= epsA && epsA >= epsC) {
            activeEpOrder = 'BAC'; maxVal = errB; midVal = errA; minVal = errC;
        } else if (epsB >= epsC && epsC >= epsA) {
            activeEpOrder = 'BCA'; maxVal = errB; midVal = errC; minVal = errA;
        } else if (epsC >= epsA && epsA >= epsB) {
            activeEpOrder = 'CAB'; maxVal = errC; midVal = errA; minVal = errB;
        } else {
            activeEpOrder = 'CBA'; maxVal = errC; midVal = errB; minVal = errA;
        }

        activeSmx = (maxVal >= 0) ? 1 : 0;
        activeSmd = (midVal >= 0) ? 1 : 0;
        activeSmn = (minVal >= 0) ? 1 : 0;

        // Fmp flag: 0 if Common-Mode priority, 1 if Differential-Mode priority
        activeFmp = (Math.abs(curIzsc) > 0.35 && !leg4Fault) ? 0 : 1;

        // 4. 7-bit Binary LUT Address Generation
        activeAddr = (activePab << 6) | (activePbc << 5) | (activePca << 4) |
                     (activeSmx << 3) | (activeSmd << 2) | (activeSmn << 1) | activeFmp;

        // 5. Optimal 96-LUT Lookup
        if (typeof OEPC_LUT_96 !== 'undefined' && OEPC_LUT_96[activeAddr]) {
            const entry = OEPC_LUT_96[activeAddr];
            activeSwitches = entry.l.slice(); // [Sa, Sb, Sc, Sn]
            if (leg4Fault) activeSwitches[3] = 0; // Inhibit 4th leg on hardware fault
            activeVidx = entry.vIdx;
            activeImpact = entry.impact;
            activeRow = entry.row;
        } else {
            activeSwitches = [activeSmx, activeSmd, activeSmn, activeFmp === 0 ? 1 : 0];
            activeVidx = 9;
            activeImpact = '+A,-C';
            activeRow = 1;
        }

        // 6. Store in Circular History for Orbit Trail
        histIa[histPtr] = curIa;
        histIb[histPtr] = curIb;
        histIc[histPtr] = curIc;
        histRefA[histPtr] = refIa;
        histRefB[histPtr] = refIb;
        histRefC[histPtr] = refIc;
        histEa[histPtr] = errA;
        histEb[histPtr] = errB;
        histEc[histPtr] = errC;
        histIzsc[histPtr] = curIzsc;
        histSa[histPtr] = activeSwitches[0];
        histSb[histPtr] = activeSwitches[1];
        histSc[histPtr] = activeSwitches[2];
        histSn[histPtr] = activeSwitches[3];
        histPtr = (histPtr + 1) % HIST_LEN;
    }
'''

    # 2.3 renderOscilloscopeCanvas and renderGateTracesCanvas
    canvases_old_pattern = r'(function renderOscilloscopeCanvas\(\)\s*\{.*?(?=function renderErrorOrbitCanvas))'
    match_canvases = re.search(canvases_old_pattern, orig_iife, re.DOTALL)
    if not match_canvases:
        print("  -> ERROR: Could not find renderOscilloscopeCanvas & renderGateTracesCanvas block!")
        return False

    scope_trig_badge = "📌 גל מיוצב (TRIG LOCKED • 2 CYCLES)" if is_hebrew else "📌 TRIG LOCKED • 2 CYCLES (Stationary)"
    scope_slow_badge = "🌊 גלילה איטית (SLOW ROLL 0.25X)" if is_hebrew else "🌊 SLOW ROLL 0.25X"
    scope_ch2_label = "CH2: 0.5 A/div (שגיאות e_x וזרם סדרה אפס i_zsc)" if is_hebrew else "CH2: 0.5 A/div (Errors e_x & Zero-Sequence Current i_zsc)"
    scope_ch1_label = "CH1: 3.0 A/div • 5.0 ms/div (2 מחזורים סטציונריים @ 50 Hz)" if is_hebrew else "CH1: 3.0 A/div • 5.0 ms/div (2 Stationary Cycles @ 50 Hz)"

    canvases_block_new = f'''function renderOscilloscopeCanvas() {{
        const canvas = document.getElementById('demo-osc-canvas');
        if (!canvas) return;
        const dpr = window.devicePixelRatio || 1;
        if (canvas.width !== canvas.clientWidth * dpr) {{
            canvas.width = canvas.clientWidth * dpr;
            canvas.height = canvas.clientHeight * dpr;
        }}
        const ctx = canvas.getContext('2d');
        const W = canvas.width;
        const H = canvas.height;

        ctx.save();
        ctx.clearRect(0, 0, W, H);

        // Dark oscilloscope background
        ctx.fillStyle = '#060a12';
        ctx.fillRect(0, 0, W, H);

        const leftMargin = 50 * dpr; // reserved space for scale markings
        const plotW = W - leftMargin;
        const midY = H * 0.52;

        // Grid lines (8 divisions horizontal => 5 ms/div across 40 ms total window)
        ctx.strokeStyle = 'rgba(0, 210, 255, 0.08)';
        ctx.lineWidth = 1 * dpr;
        for (let i = 0; i <= 8; i++) {{
            const x = leftMargin + (plotW / 8) * i;
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
        }}
        for (let j = 0; j <= 6; j++) {{
            const y = (H / 6) * j;
            ctx.beginPath(); ctx.moveTo(leftMargin, y); ctx.lineTo(W, y); ctx.stroke();
        }}

        // Section divider line
        ctx.strokeStyle = 'rgba(0, 210, 255, 0.35)';
        ctx.lineWidth = 1.2 * dpr;
        ctx.beginPath(); ctx.moveTo(0, midY); ctx.lineTo(W, midY); ctx.stroke();

        // -------------------------------------------------------------
        // TOP HALF: CURRENTS SCALE (-6.0 A to +6.0 A)
        // -------------------------------------------------------------
        const curZeroY = midY * 0.5;
        const maxCur = 6.5;
        const curScale = (midY * 0.42) / maxCur;

        ctx.strokeStyle = 'rgba(255, 255, 255, 0.22)';
        ctx.lineWidth = 1.2 * dpr;
        ctx.beginPath(); ctx.moveTo(leftMargin, curZeroY); ctx.lineTo(W, curZeroY); ctx.stroke();

        ctx.font = `bold ${{8.5 * dpr}}px monospace`;
        ctx.textAlign = 'right';
        const curTicks = [
            {{ val: 6.0, y: curZeroY - 6.0 * curScale, lbl: '+6.0A' }},
            {{ val: 3.0, y: curZeroY - 3.0 * curScale, lbl: '+3.0A' }},
            {{ val: 0.0, y: curZeroY, lbl: ' 0.0A' }},
            {{ val: -3.0, y: curZeroY + 3.0 * curScale, lbl: '-3.0A' }},
            {{ val: -6.0, y: curZeroY + 6.0 * curScale, lbl: '-6.0A' }}
        ];
        curTicks.forEach(t => {{
            ctx.fillStyle = t.val === 0 ? '#ffffff' : 'rgba(0, 210, 255, 0.75)';
            ctx.fillText(t.lbl, leftMargin - 4 * dpr, t.y + 3 * dpr);
            ctx.strokeStyle = 'rgba(0, 210, 255, 0.4)';
            ctx.beginPath(); ctx.moveTo(leftMargin - 3 * dpr, t.y); ctx.lineTo(leftMargin, t.y); ctx.stroke();
        }});

        // Top Scale Label Tag
        ctx.textAlign = 'left';
        ctx.fillStyle = 'rgba(0, 210, 255, 0.9)';
        ctx.fillText('{scope_ch1_label}', leftMargin + 8 * dpr, 14 * dpr);

        // Scope Mode Status Tag on right
        ctx.textAlign = 'right';
        if (demoScopeMode === 'trig') {{
            ctx.fillStyle = '#00ff88';
            ctx.fillText('{scope_trig_badge}', W - 10 * dpr, 14 * dpr);
        }} else {{
            ctx.fillStyle = '#00d2ff';
            ctx.fillText('{scope_slow_badge}', W - 10 * dpr, 14 * dpr);
        }}

        // -------------------------------------------------------------
        // BOTTOM HALF: ERRORS SCALE (-1.2 A to +1.2 A)
        // -------------------------------------------------------------
        const errZeroY = midY + (H - midY) * 0.5;
        const maxErr = 1.2;
        const errScale = ((H - midY) * 0.42) / maxErr;

        ctx.strokeStyle = 'rgba(255, 255, 255, 0.22)';
        ctx.lineWidth = 1.2 * dpr;
        ctx.beginPath(); ctx.moveTo(leftMargin, errZeroY); ctx.lineTo(W, errZeroY); ctx.stroke();

        ctx.textAlign = 'right';
        const errTicks = [
            {{ val: 1.0, y: errZeroY - 1.0 * errScale, lbl: '+1.0A' }},
            {{ val: 0.5, y: errZeroY - 0.5 * errScale, lbl: '+0.5A' }},
            {{ val: 0.0, y: errZeroY, lbl: ' 0.0A' }},
            {{ val: -0.5, y: errZeroY + 0.5 * errScale, lbl: '-0.5A' }},
            {{ val: -1.0, y: errZeroY + 1.0 * errScale, lbl: '-1.0A' }}
        ];
        errTicks.forEach(t => {{
            ctx.fillStyle = t.val === 0 ? '#ffffff' : 'rgba(255, 107, 129, 0.75)';
            ctx.fillText(t.lbl, leftMargin - 4 * dpr, t.y + 3 * dpr);
            ctx.strokeStyle = 'rgba(255, 107, 129, 0.4)';
            ctx.beginPath(); ctx.moveTo(leftMargin - 3 * dpr, t.y); ctx.lineTo(leftMargin, t.y); ctx.stroke();
        }});

        ctx.textAlign = 'left';
        ctx.fillStyle = 'rgba(255, 107, 129, 0.9)';
        ctx.fillText('{scope_ch2_label}', leftMargin + 8 * dpr, midY + 14 * dpr);

        // -------------------------------------------------------------
        // PLOT 2-CYCLE STATIONARY TRIGGERED WAVEFORMS (POINTS = 280)
        // -------------------------------------------------------------
        const POINTS = 280;
        const ptsIa = new Float32Array(POINTS);
        const ptsIb = new Float32Array(POINTS);
        const ptsIc = new Float32Array(POINTS);
        const ptsRefA = new Float32Array(POINTS);
        const ptsRefB = new Float32Array(POINTS);
        const ptsRefC = new Float32Array(POINTS);
        const ptsEa = new Float32Array(POINTS);
        const ptsEb = new Float32Array(POINTS);
        const ptsEc = new Float32Array(POINTS);
        const ptsIzsc = new Float32Array(POINTS);

        const rollAng = (demoScopeMode === 'slow' ? w_elec * demoRollOffset : 0);
        const pulseOffset = demoScanTime * 25;

        for (let p = 0; p < POINTS; p++) {{
            const frac = p / (POINTS - 1);
            const th = frac * 4 * Math.PI + rollAng;

            // References
            const rA = Iref * Math.cos(th);
            const rB = Iref * Math.cos(th - 2 * Math.PI / 3);
            const rC = Iref * Math.cos(th + 2 * Math.PI / 3);
            ptsRefA[p] = rA; ptsRefB[p] = rB; ptsRefC[p] = rC;

            // High frequency ripple
            const fc = 48;
            const rpA = 0.08 * Math.sin(fc * th + pulseOffset) + 0.02 * Math.cos(2 * fc * th);
            const rpB = 0.08 * Math.sin(fc * (th - 2 * Math.PI / 3) + pulseOffset) + 0.02 * Math.cos(2 * fc * (th - 2 * Math.PI / 3));
            const rpC = 0.08 * Math.sin(fc * (th + 2 * Math.PI / 3) + pulseOffset) + 0.02 * Math.cos(2 * fc * (th + 2 * Math.PI / 3));

            // Asymmetry
            const asym = (asymPercent / 100.0) * 0.45 * Math.cos(th);

            // Disturbance surge pulse
            let dist = 0;
            if (disturbanceTimer > 0) {{
                dist = 0.65 * Math.sin(disturbanceTimer * 35) * (disturbanceTimer / 0.08);
            }}

            const eA = Math.max(-1.1, Math.min(1.1, rpA + asym + dist));
            const eB = Math.max(-1.1, Math.min(1.1, rpB - 0.5 * asym - 0.5 * dist));
            const eC = Math.max(-1.1, Math.min(1.1, rpC - 0.5 * asym - 0.5 * dist));
            ptsEa[p] = eA; ptsEb[p] = eB; ptsEc[p] = eC;

            ptsIa[p] = rA - eA;
            ptsIb[p] = rB - eB;
            ptsIc[p] = rC - eC;

            if (leg4Fault) {{
                ptsIzsc[p] = 0.65 * (asymPercent > 0 ? (asymPercent / 35.0) : 1.0) * Math.sin(3 * th) + dist * 0.3;
            }} else if (asymPercent > 0) {{
                ptsIzsc[p] = 0.03 * Math.sin(3 * th);
            }} else {{
                ptsIzsc[p] = 0.015 * Math.sin(3 * th);
            }}
        }}

        function drawLine(arr, zeroY, scale, color, lineWidth, isDashed) {{
            ctx.beginPath();
            ctx.strokeStyle = color;
            ctx.lineWidth = lineWidth * dpr;
            if (isDashed) ctx.setLineDash([3 * dpr, 3 * dpr]); else ctx.setLineDash([]);
            for (let i = 0; i < POINTS; i++) {{
                const x = leftMargin + (plotW / (POINTS - 1)) * i;
                const y = zeroY - arr[i] * scale;
                if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
            }}
            ctx.stroke();
            ctx.setLineDash([]);
        }}

        // Top: References & Currents
        drawLine(ptsRefA, curZeroY, curScale, 'rgba(0, 210, 255, 0.35)', 1.4, true);
        drawLine(ptsRefB, curZeroY, curScale, 'rgba(246, 211, 101, 0.35)', 1.4, true);
        drawLine(ptsRefC, curZeroY, curScale, 'rgba(255, 107, 129, 0.35)', 1.4, true);

        drawLine(ptsIa, curZeroY, curScale, '#00d2ff', 2.0, false);
        drawLine(ptsIb, curZeroY, curScale, '#f6d365', 2.0, false);
        drawLine(ptsIc, curZeroY, curScale, '#ff6b81', 2.0, false);

        // Bottom: Errors & ZSC
        drawLine(ptsEa, errZeroY, errScale, '#00d2ff', 1.8, false);
        drawLine(ptsEb, errZeroY, errScale, '#f6d365', 1.8, false);
        drawLine(ptsEc, errZeroY, errScale, '#ff6b81', 1.8, false);
        drawLine(ptsIzsc, errZeroY, errScale, '#00ff88', 2.2, false);

        // -------------------------------------------------------------
        // DYNAMIC TRIGGER SCANNING CURSOR (מחט סריקה דינמית)
        // -------------------------------------------------------------
        const T_window = 0.04; // 40 ms
        const scanFrac = (demoScanTime % T_window) / T_window;
        const scanX = leftMargin + plotW * scanFrac;
        const scanMs = scanFrac * 40.0;

        // Glowing scan line
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.6 * dpr;
        ctx.shadowColor = '#00d2ff';
        ctx.shadowBlur = 6 * dpr;
        ctx.beginPath(); ctx.moveTo(scanX, 0); ctx.lineTo(scanX, H); ctx.stroke();
        ctx.shadowBlur = 0;

        // Scan cursor tag pill
        ctx.fillStyle = 'rgba(0, 210, 255, 0.25)';
        ctx.strokeStyle = '#00d2ff';
        ctx.lineWidth = 1 * dpr;
        const tagW = 54 * dpr, tagH = 14 * dpr;
        const tagX = Math.min(W - tagW - 2 * dpr, Math.max(leftMargin + 2 * dpr, scanX - tagW / 2));
        ctx.fillRect(tagX, midY - tagH / 2, tagW, tagH);
        ctx.strokeRect(tagX, midY - tagH / 2, tagW, tagH);

        ctx.font = `bold ${{8 * dpr}}px monospace`;
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'center';
        ctx.fillText(`${{scanMs.toFixed(1)}} ms`, tagX + tagW / 2, midY + 3.5 * dpr);

        ctx.restore();
    }}

    // Canvas 2: 4-Leg Inverter Gate Switching Traces (Saleae / Logic Analyzer style)
    function renderGateTracesCanvas() {{
        const canvas = document.getElementById('demo-gate-canvas');
        if (!canvas) return;
        const dpr = window.devicePixelRatio || 1;
        if (canvas.width !== canvas.clientWidth * dpr) {{
            canvas.width = canvas.clientWidth * dpr;
            canvas.height = canvas.clientHeight * dpr;
        }}
        const ctx = canvas.getContext('2d');
        const W = canvas.width;
        const H = canvas.height;

        ctx.save();
        ctx.clearRect(0, 0, W, H);
        ctx.direction = 'ltr';

        const labelW = 82 * dpr;   // Left channel labels & voltage scale
        const statusW = 68 * dpr;  // Right status badges
        const plotLeft = labelW;
        const plotRight = W - statusW;
        const plotW = Math.max(10, plotRight - plotLeft);
        const trackH = H / 4;

        const legs = [
            {{ legName: 'רגל A (L1)', switchName: 'S_a', color: '#00d2ff', activeVal: activeSwitches[0], hPair: 'S_ah', lPair: 'S_al', phaseOff: 0 }},
            {{ legName: 'רגל B (L2)', switchName: 'S_b', color: '#f6d365', activeVal: activeSwitches[1], hPair: 'S_bh', lPair: 'S_bl', phaseOff: -2 * Math.PI / 3 }},
            {{ legName: 'רגל C (L3)', switchName: 'S_c', color: '#ff6b81', activeVal: activeSwitches[2], hPair: 'S_ch', lPair: 'S_cl', phaseOff: 2 * Math.PI / 3 }},
            {{ legName: 'רגל N (L4)', switchName: 'S_n', color: '#00ff88', activeVal: activeSwitches[3], hPair: 'S_nh', lPair: 'S_nl', phaseOff: 0 }}
        ];

        const POINTS = 280;
        const rollAng = (demoScopeMode === 'slow' ? w_elec * demoRollOffset : 0);

        legs.forEach((leg, idx) => {{
            const topY = idx * trackH;
            const botY = topY + trackH;
            const highY = topY + trackH * 0.26;
            const lowY  = topY + trackH * 0.78;

            // Track background
            if (idx % 2 === 0) {{
                ctx.fillStyle = 'rgba(255, 255, 255, 0.02)';
                ctx.fillRect(0, topY, W, trackH);
            }}

            // Boundary divider line
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
            ctx.lineWidth = 1 * dpr;
            ctx.beginPath(); ctx.moveTo(0, botY); ctx.lineTo(W, botY); ctx.stroke();

            // Vertical partition dividers between labels, plot, and status
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
            ctx.beginPath(); ctx.moveTo(plotLeft, topY); ctx.lineTo(plotLeft, botY); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(plotRight, topY); ctx.lineTo(plotRight, botY); ctx.stroke();

            // --- 1. LEFT CHANNEL LABEL COLUMN ---
            ctx.fillStyle = leg.color;
            ctx.fillRect(3 * dpr, topY + 4 * dpr, 3 * dpr, trackH - 8 * dpr);

            ctx.font = `bold ${{8.5 * dpr}}px sans-serif`;
            ctx.fillStyle = leg.color;
            ctx.textAlign = 'left';
            ctx.fillText(leg.legName, 10 * dpr, topY + 12 * dpr);

            ctx.font = `bold ${{7.5 * dpr}}px monospace`;
            ctx.fillStyle = '#ffffff';
            ctx.fillText(leg.switchName, 10 * dpr, lowY - 3 * dpr);

            ctx.fillStyle = 'rgba(255, 255, 255, 0.40)';
            ctx.textAlign = 'right';
            ctx.fillText('Vdc', plotLeft - 5 * dpr, highY + 3 * dpr);
            ctx.fillText('0V', plotLeft - 5 * dpr, lowY + 3 * dpr);

            // --- 2. MIDDLE WAVEFORM PLOT ZONE (Stationary 2-cycle Square Wave) ---
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
            ctx.lineWidth = 1 * dpr;
            ctx.setLineDash([2 * dpr, 3 * dpr]);
            ctx.beginPath(); ctx.moveTo(plotLeft, highY); ctx.lineTo(plotRight, highY); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(plotLeft, lowY); ctx.lineTo(plotRight, lowY); ctx.stroke();
            ctx.setLineDash([]);

            // Generate stationary square wave across 2 cycles
            ctx.beginPath();
            ctx.strokeStyle = leg.color;
            ctx.lineWidth = 1.8 * dpr;
            ctx.shadowColor = leg.color;
            ctx.shadowBlur = 3 * dpr;

            let prevY = lowY;
            for (let p = 0; p < POINTS; p++) {{
                const frac = p / (POINTS - 1);
                const th = frac * 4 * Math.PI + rollAng;
                const x = plotLeft + (plotW / (POINTS - 1)) * p;

                let state = 0;
                if (idx === 3) {{
                    // Leg N
                    if (leg4Fault) {{
                        state = 0; // disabled by fault
                    }} else if (asymPercent > 0) {{
                        state = Math.sin(3 * th) > 0 ? 1 : 0;
                    }} else {{
                        state = (Math.sin(3 * th + Math.PI / 4) > 0.2) ? 1 : 0;
                    }}
                }} else {{
                    // Legs A, B, C
                    const modWave = Math.cos(th + leg.phaseOff);
                    const carrier = 0.55 * Math.sin(24 * th);
                    state = (modWave + carrier) > 0 ? 1 : 0;
                }}

                const y = (state === 1) ? highY : lowY;
                if (p === 0) {{
                    ctx.moveTo(x, y);
                }} else {{
                    if (y !== prevY) ctx.lineTo(x, prevY);
                    ctx.lineTo(x, y);
                }}
                prevY = y;
            }}
            ctx.stroke();
            ctx.shadowBlur = 0;

            // --- 3. RIGHT STATUS BADGE ZONE ---
            const badgeX = plotRight + 6 * dpr;
            const badgeW = statusW - 12 * dpr;
            const badgeH = trackH - 8 * dpr;
            const badgeY = topY + 4 * dpr;

            const isOn = leg.activeVal === 1;
            ctx.fillStyle = isOn ? 'rgba(0, 255, 136, 0.15)' : 'rgba(255, 71, 87, 0.15)';
            ctx.strokeStyle = isOn ? '#00ff88' : '#ff4757';
            ctx.lineWidth = 1 * dpr;

            ctx.beginPath();
            ctx.roundRect(badgeX, badgeY, badgeW, badgeH, 4 * dpr);
            ctx.fill();
            ctx.stroke();

            ctx.font = `bold ${{8 * dpr}}px monospace`;
            ctx.fillStyle = isOn ? '#00ff88' : '#ff6b81';
            ctx.textAlign = 'center';
            ctx.fillText(isOn ? 'ON (1)' : 'OFF (0)', badgeX + badgeW / 2, badgeY + badgeH * 0.45);

            ctx.font = `${{6.8 * dpr}}px sans-serif`;
            ctx.fillStyle = 'rgba(255, 255, 255, 0.65)';
            ctx.fillText(isOn ? `${{leg.hPair}}:ON` : `${{leg.lPair}}:ON`, badgeX + badgeW / 2, badgeY + badgeH * 0.82);
        }});

        // Synchronous Scanning Cursor over gate tracks
        const T_window = 0.04;
        const scanFrac = (demoScanTime % T_window) / T_window;
        const scanX = plotLeft + plotW * scanFrac;

        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.5 * dpr;
        ctx.shadowColor = '#00d2ff';
        ctx.shadowBlur = 5 * dpr;
        ctx.beginPath(); ctx.moveTo(scanX, 0); ctx.lineTo(scanX, H); ctx.stroke();
        ctx.shadowBlur = 0;

        ctx.restore();
    }}
'''

    # 2.4 Add toggleDemoScopeMode to Public API
    api_toggle_code = f'''
    window.toggleDemoScopeMode = function() {{
        demoScopeMode = (demoScopeMode === 'trig') ? 'slow' : 'trig';
        const btn = document.getElementById('btn-demo-scope-mode');
        const isHe = document.documentElement.lang === 'he' || document.querySelector('html[dir="rtl"]') !== null;
        if (btn) {{
            if (demoScopeMode === 'trig') {{
                btn.textContent = isHe ? '📌 גל מיוצב (נעול טריגר)' : '📌 Trigger-Locked Scope';
                btn.style.background = 'rgba(0, 255, 136, 0.15)';
                btn.style.borderColor = '#00ff88';
                btn.style.color = '#00ff88';
            }} else {{
                btn.textContent = isHe ? '🌊 גלילה איטית' : '🌊 Slow Rolling Scope';
                btn.style.background = 'rgba(0, 210, 255, 0.15)';
                btn.style.borderColor = '#00d2ff';
                btn.style.color = '#00d2ff';
            }}
        }}
    }};
'''

    # Perform the replacements in orig_iife
    # 1. Replace vars
    updated_iife = orig_iife[:match_vars.start()] + var_block_new + orig_iife[match_vars.end():]

    # Re-find step in updated_iife
    match_step = re.search(step_old_pattern, updated_iife, re.DOTALL)
    updated_iife = updated_iife[:match_step.start()] + step_block_new + updated_iife[match_step.end():]

    # Re-find canvases in updated_iife
    match_canvases = re.search(canvases_old_pattern, updated_iife, re.DOTALL)
    updated_iife = updated_iife[:match_canvases.start()] + canvases_block_new + updated_iife[match_canvases.end():]

    # Inject toggleDemoScopeMode before window.toggleDemoPlay
    idx_toggle_play = updated_iife.find('window.toggleDemoPlay')
    updated_iife = updated_iife[:idx_toggle_play] + api_toggle_code + '\n    ' + updated_iife[idx_toggle_play:]

    # Put updated_iife back into content
    content = content[:idx_iife_start] + updated_iife + content[idx_iife_end:]

    with open(filepath, 'w', encoding='utf-8') as f_out:
        f_out.write(content)

    print(f"  -> Successfully updated {filepath}!")
    return True

if __name__ == '__main__':
    update_presentation_file('generate_hebrew_presentation.py', is_hebrew=True)
    update_presentation_file('generate_html_presentation.py', is_hebrew=False)
    print("\nAll presentation generator files updated successfully!")
