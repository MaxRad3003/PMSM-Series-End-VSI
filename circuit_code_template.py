def get_render_circuit_code(is_hebrew=True):
    fault_label = '⚠️ תקלת ענף 4 (מנותק)' if is_hebrew else '⚠️ Leg 4 Fault (Isolated)'
    neutral_label = 'מוליך נייטרל (ענף 4)' if is_hebrew else 'Neutral Conductor (Leg 4)'

    return f'''
    // Canvas 4: Dynamic Electronic Circuit Simulation (4-Leg SE-VSI & PMSM Topology)
    let circuitParticlePhase = 0;

    function renderCircuitCanvas() {{
        const canvas = document.getElementById('demo-circuit-canvas');
        if (!canvas) return;
        const dpr = window.devicePixelRatio || 1;
        if (canvas.width !== canvas.clientWidth * dpr) {{
            canvas.width = canvas.clientWidth * dpr;
            canvas.height = canvas.clientHeight * dpr;
        }}
        const ctx = canvas.getContext('2d');
        const W = canvas.width;
        const H = canvas.height;

        if (W < 60 || H < 60) return; // Guard against unmounted layout

        ctx.save();
        ctx.clearRect(0, 0, W, H);
        ctx.direction = 'ltr';

        // Deep blueprint background with subtle circuit grid
        ctx.fillStyle = '#060a14';
        ctx.fillRect(0, 0, W, H);

        ctx.strokeStyle = 'rgba(0, 210, 255, 0.04)';
        ctx.lineWidth = 1 * dpr;
        const gridSize = 16 * dpr;
        for (let x = 0; x <= W; x += gridSize) {{
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
        }}
        for (let y = 0; y <= H; y += gridSize) {{
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
        }}

        // Geometry layout
        const topRailY = 24 * dpr;
        const botRailY = Math.max(topRailY + 60 * dpr, H - 22 * dpr);
        const midY = (topRailY + botRailY) / 2;

        const inverterRight = W * 0.58;
        const legX = [
            W * 0.14, // Leg A
            W * 0.26, // Leg B
            W * 0.38, // Leg C
            W * 0.50  // Leg N (Neutral)
        ];

        const motorCenterX = W * 0.82;
        const motorCenterY = midY;
        const motorRadius = Math.max(18 * dpr, Math.min(W * 0.13, (botRailY - topRailY) * 0.38));

        // Advance particle phase
        if (demoRunning) {{
            circuitParticlePhase = (circuitParticlePhase + 0.08 * (demoSpeed / 0.5)) % 1.0;
        }}

        // 1. DC BUS RAILS
        // Top Rail (+Vdc)
        ctx.strokeStyle = '#f6d365';
        ctx.lineWidth = 2.4 * dpr;
        ctx.shadowColor = '#f6d365';
        ctx.shadowBlur = 4 * dpr;
        ctx.beginPath(); ctx.moveTo(12 * dpr, topRailY); ctx.lineTo(inverterRight + 8 * dpr, topRailY); ctx.stroke();

        // Bottom Rail (0V / GND)
        ctx.strokeStyle = '#00d2ff';
        ctx.beginPath(); ctx.moveTo(12 * dpr, botRailY); ctx.lineTo(inverterRight + 8 * dpr, botRailY); ctx.stroke();
        ctx.shadowBlur = 0;

        // Rail Labels
        ctx.font = `bold ${{7.5 * dpr}}px monospace`;
        ctx.fillStyle = '#f6d365';
        ctx.textAlign = 'left';
        ctx.fillText('+Vdc', 14 * dpr, topRailY - 5 * dpr);

        ctx.fillStyle = '#00d2ff';
        ctx.fillText('0V (GND)', 14 * dpr, botRailY + 14 * dpr);

        // DC Bus Filter Capacitor (C_dc)
        const capX = 28 * dpr;
        const capTopY = topRailY + 15 * dpr;
        const capBotY = botRailY - 15 * dpr;
        if (capBotY > capTopY + 10 * dpr) {{
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.45)';
            ctx.lineWidth = 1.2 * dpr;
            ctx.beginPath(); ctx.moveTo(capX, topRailY); ctx.lineTo(capX, capTopY); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(capX, botRailY); ctx.lineTo(capX, capBotY); ctx.stroke();
            // Capacitor plates
            ctx.beginPath(); ctx.moveTo(capX - 6 * dpr, capTopY); ctx.lineTo(capX + 6 * dpr, capTopY); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(capX - 6 * dpr, capBotY); ctx.lineTo(capX + 6 * dpr, capBotY); ctx.stroke();
            ctx.font = `${{6.5 * dpr}}px sans-serif`;
            ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
            ctx.fillText('C_dc', capX + 8 * dpr, midY + 3 * dpr);
        }}

        // 2. INVERTER LEGS & SWITCHES
        const legColors = ['#00d2ff', '#f6d365', '#ff6b81', '#00ff88'];
        const legNames = ['A', 'B', 'C', 'N'];
        const legCurrents = [curIa, curIb, curIc, -curIzsc]; // Inverter output currents

        legX.forEach((lx, k) => {{
            const isNeutral = (k === 3);
            const legCol = legColors[k];
            const swH = activeSwitches[k];
            const swL = (isNeutral && leg4Fault) ? 0 : (swH === 1 ? 0 : 1);

            // Vertical bus feed wires
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
            ctx.lineWidth = 1 * dpr;
            ctx.beginPath(); ctx.moveTo(lx, topRailY); ctx.lineTo(lx, topRailY + 12 * dpr); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(lx, botRailY); ctx.lineTo(lx, botRailY - 12 * dpr); ctx.stroke();

            // --- Upper Switch S_kh ---
            const swH_topY = topRailY + 12 * dpr;
            const swH_botY = midY - 12 * dpr;
            drawTransistorSwitch(ctx, lx, swH_topY, swH_botY, swH, legCol, dpr, isNeutral && leg4Fault);

            // Label S_h
            ctx.font = `bold ${{7 * dpr}}px monospace`;
            ctx.fillStyle = swH === 1 ? '#00ff88' : 'rgba(255,255,255,0.45)';
            ctx.textAlign = 'right';
            ctx.fillText(`S_${{legNames[k].toLowerCase()}}h`, lx - 7 * dpr, (swH_topY + swH_botY) / 2 + 2 * dpr);

            // --- Lower Switch S_kl ---
            const swL_topY = midY + 12 * dpr;
            const swL_botY = botRailY - 12 * dpr;
            drawTransistorSwitch(ctx, lx, swL_topY, swL_botY, swL, legCol, dpr, isNeutral && leg4Fault);

            // Label S_l
            ctx.font = `bold ${{7 * dpr}}px monospace`;
            ctx.fillStyle = swL === 1 ? '#00ff88' : 'rgba(255,255,255,0.45)';
            ctx.fillText(`S_${{legNames[k].toLowerCase()}}l`, lx - 7 * dpr, (swL_topY + swL_botY) / 2 + 2 * dpr);

            // --- Midpoint Terminal Node ---
            ctx.strokeStyle = legCol;
            ctx.lineWidth = 1.4 * dpr;
            ctx.beginPath(); ctx.moveTo(lx, swH_botY); ctx.lineTo(lx, swL_topY); ctx.stroke();

            // Terminal Dot
            ctx.fillStyle = swH === 1 ? '#f6d365' : '#00d2ff';
            ctx.beginPath(); ctx.arc(lx, midY, 3.5 * dpr, 0, 2 * Math.PI); ctx.fill();
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 1 * dpr;
            ctx.stroke();

            // Terminal Potential Tag
            ctx.font = `bold ${{7 * dpr}}px monospace`;
            ctx.fillStyle = legCol;
            ctx.textAlign = 'center';
            ctx.fillText(legNames[k], lx, midY - 6 * dpr);
        }});

        // 3. PMSM MOTOR STATOR & STAR POINT (Y-Connected with Neutral Return)
        // Stator Housing
        ctx.strokeStyle = 'rgba(0, 210, 255, 0.25)';
        ctx.lineWidth = 1.5 * dpr;
        ctx.setLineDash([4 * dpr, 3 * dpr]);
        ctx.beginPath(); ctx.arc(motorCenterX, motorCenterY, motorRadius, 0, 2 * Math.PI); ctx.stroke();
        ctx.setLineDash([]);

        ctx.font = `bold ${{7.5 * dpr}}px sans-serif`;
        ctx.fillStyle = 'rgba(0, 210, 255, 0.7)';
        ctx.textAlign = 'center';
        ctx.fillText('PMSM', motorCenterX, motorCenterY - motorRadius - 4 * dpr);

        // Neutral Star Node (N_motor)
        ctx.fillStyle = '#00ff88';
        ctx.beginPath(); ctx.arc(motorCenterX, motorCenterY, 4 * dpr, 0, 2 * Math.PI); ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1 * dpr;
        ctx.stroke();
        ctx.font = `bold ${{7 * dpr}}px monospace`;
        ctx.fillStyle = '#00ff88';
        ctx.fillText('N*', motorCenterX, motorCenterY + 12 * dpr);

        // 3 Stator Coils positions (angles: Phase A = -135 deg, Phase B = 135 deg, Phase C = 0 deg)
        const coilAngles = [-Math.PI * 0.75, Math.PI * 0.75, 0];
        const coilTerminals = coilAngles.map(ang => ({{
            x: motorCenterX + Math.cos(ang) * (motorRadius * 0.85),
            y: motorCenterY + Math.sin(ang) * (motorRadius * 0.85)
        }}));

        // --- Phase Connection Wires (Inverter Midpoint to Motor Coils) ---
        // Phase A
        drawConnectingWire(ctx, legX[0], midY, coilTerminals[0].x, coilTerminals[0].y, '#00d2ff', legCurrents[0], circuitParticlePhase, dpr);
        drawCoil(ctx, coilTerminals[0].x, coilTerminals[0].y, motorCenterX, motorCenterY, '#00d2ff', dpr, asymPercent > 0);

        // Phase B
        drawConnectingWire(ctx, legX[1], midY, coilTerminals[1].x, coilTerminals[1].y, '#f6d365', legCurrents[1], circuitParticlePhase, dpr);
        drawCoil(ctx, coilTerminals[1].x, coilTerminals[1].y, motorCenterX, motorCenterY, '#f6d365', dpr, false);

        // Phase C
        drawConnectingWire(ctx, legX[2], midY, coilTerminals[2].x, coilTerminals[2].y, '#ff6b81', legCurrents[2], circuitParticlePhase, dpr);
        drawCoil(ctx, coilTerminals[2].x, coilTerminals[2].y, motorCenterX, motorCenterY, '#ff6b81', dpr, false);

        // --- Neutral Return Wire (Motor N* to Inverter Leg N) ---
        const neutralY = midY;
        if (leg4Fault) {{
            // Faulted neutral: drawn dashed red with an open fault marker
            ctx.strokeStyle = 'rgba(255, 71, 87, 0.4)';
            ctx.lineWidth = 1.4 * dpr;
            ctx.setLineDash([4 * dpr, 4 * dpr]);
            ctx.beginPath(); ctx.moveTo(legX[3], neutralY); ctx.lineTo(motorCenterX, neutralY); ctx.stroke();
            ctx.setLineDash([]);

            // Fault Cross
            const crossX = (legX[3] + motorCenterX) / 2;
            ctx.strokeStyle = '#ff4757';
            ctx.lineWidth = 2.2 * dpr;
            ctx.beginPath();
            ctx.moveTo(crossX - 6 * dpr, neutralY - 6 * dpr); ctx.lineTo(crossX + 6 * dpr, neutralY + 6 * dpr);
            ctx.moveTo(crossX + 6 * dpr, neutralY - 6 * dpr); ctx.lineTo(crossX - 6 * dpr, neutralY + 6 * dpr);
            ctx.stroke();

            ctx.font = `bold ${{7 * dpr}}px sans-serif`;
            ctx.fillStyle = '#ff6b81';
            ctx.textAlign = 'center';
            ctx.fillText('{fault_label}', crossX, neutralY - 9 * dpr);
        }} else {{
            // Healthy neutral conductor with current flow animation
            drawConnectingWire(ctx, motorCenterX, neutralY, legX[3], neutralY, '#00ff88', curIzsc * 2, circuitParticlePhase, dpr);
            ctx.font = `${{6.8 * dpr}}px sans-serif`;
            ctx.fillStyle = 'rgba(0, 255, 136, 0.75)';
            ctx.textAlign = 'center';
            ctx.fillText('{neutral_label}', (legX[3] + motorCenterX) / 2, neutralY - 6 * dpr);
        }}

        // 4. VOLTAGE POLARITY HUD & TELEMETRY
        const vA = activeSwitches[0];
        const vB = activeSwitches[1];
        const vC = activeSwitches[2];
        const vN = leg4Fault ? 0 : activeSwitches[3];

        const van_val = (vA - vN) * 400;
        const vbn_val = (vB - vN) * 400;
        const vcn_val = (vC - vN) * 400;

        const elVan = document.getElementById('circuit-hud-van');
        const elVbn = document.getElementById('circuit-hud-vbn');
        const elVcn = document.getElementById('circuit-hud-vcn');
        const elIz = document.getElementById('circuit-hud-izsc');
        if (elVan) elVan.textContent = `v_an: ${{van_val >= 0 ? '+' : ''}}${{van_val}}V`;
        if (elVbn) elVbn.textContent = `v_bn: ${{vbn_val >= 0 ? '+' : ''}}${{vbn_val}}V`;
        if (elVcn) elVcn.textContent = `v_cn: ${{vcn_val >= 0 ? '+' : ''}}${{vcn_val}}V`;
        if (elIz) elIz.textContent = `i_zsc: ${{curIzsc >= 0 ? '+' : ''}}${{curIzsc.toFixed(2)}}A`;

        ctx.restore();
    }}

    // Helper: Draw Transistor Switch with Open/Closed Contact Arm & Antiparallel Diode
    function drawTransistorSwitch(ctx, x, yTop, yBot, state, color, dpr, isFaulted) {{
        ctx.save();
        const midY = (yTop + yBot) / 2;
        const armLen = Math.max(4 * dpr, (yBot - yTop) * 0.55);

        // Fixed terminal dots
        ctx.fillStyle = state === 1 ? '#00ff88' : 'rgba(255,255,255,0.4)';
        ctx.beginPath(); ctx.arc(x, yTop, 2 * dpr, 0, 2 * Math.PI); ctx.fill();
        ctx.beginPath(); ctx.arc(x, yBot, 2 * dpr, 0, 2 * Math.PI); ctx.fill();

        // Switch contact arm
        ctx.lineWidth = 1.8 * dpr;
        if (state === 1 && !isFaulted) {{
            // CLOSED: straight glowing conducting connection
            ctx.strokeStyle = '#00ff88';
            ctx.shadowColor = '#00ff88';
            ctx.shadowBlur = 4 * dpr;
            ctx.beginPath(); ctx.moveTo(x, yTop); ctx.lineTo(x, yBot); ctx.stroke();
            ctx.shadowBlur = 0;
        }} else {{
            // OPEN: angled switch arm with air gap
            ctx.strokeStyle = isFaulted ? 'rgba(255,71,87,0.5)' : 'rgba(255,255,255,0.35)';
            ctx.beginPath();
            ctx.moveTo(x, yTop);
            ctx.lineTo(x + armLen * 0.65, yTop + armLen * 0.85);
            ctx.stroke();
        }}

        // Mini Antiparallel Diode beside switch
        const dx = x + 8 * dpr;
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.18)';
        ctx.lineWidth = 1 * dpr;
        ctx.beginPath(); ctx.moveTo(x, yTop + 2 * dpr); ctx.lineTo(dx, yTop + 2 * dpr); ctx.lineTo(dx, yBot - 2 * dpr); ctx.lineTo(x, yBot - 2 * dpr); ctx.stroke();
        // Diode triangle
        ctx.fillStyle = 'rgba(255, 255, 255, 0.25)';
        ctx.beginPath();
        ctx.moveTo(dx - 3 * dpr, midY + 3 * dpr);
        ctx.lineTo(dx + 3 * dpr, midY + 3 * dpr);
        ctx.lineTo(dx, midY - 3 * dpr);
        ctx.closePath();
        ctx.fill();

        ctx.restore();
    }}

    // Helper: Draw Connecting Wire with Animated Moving Current Particles
    function drawConnectingWire(ctx, x1, y1, x2, y2, color, currentVal, particleT, dpr) {{
        ctx.save();
        ctx.strokeStyle = color;
        ctx.lineWidth = 1.4 * dpr;
        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();

        // Draw animated flowing current particles
        const absI = Math.abs(currentVal);
        if (absI > 0.05) {{
            const numParticles = Math.min(6, Math.max(2, Math.round(absI * 1.5)));
            const isForward = currentVal > 0;

            for (let i = 0; i < numParticles; i++) {{
                let frac = ((i / numParticles) + (isForward ? particleT : (1 - particleT))) % 1.0;
                const px = x1 + (x2 - x1) * frac;
                const py = y1 + (y2 - y1) * frac;

                // Flow particle dot
                ctx.fillStyle = '#ffffff';
                ctx.shadowColor = color;
                ctx.shadowBlur = 4 * dpr;
                ctx.beginPath(); ctx.arc(px, py, 2.2 * dpr, 0, 2 * Math.PI); ctx.fill();
                ctx.shadowBlur = 0;
            }}
        }}
        ctx.restore();
    }}

    // Helper: Draw Inductor Coil with Asymmetry Alert Badge
    function drawCoil(ctx, x1, y1, x2, y2, color, dpr, isAsym) {{
        ctx.save();
        ctx.strokeStyle = color;
        ctx.lineWidth = 2 * dpr;

        const mx = (x1 + x2) / 2;
        const my = (y1 + y2) / 2;

        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(mx, my); ctx.lineTo(x2, y2); ctx.stroke();

        if (isAsym) {{
            ctx.fillStyle = 'rgba(246, 211, 101, 0.95)';
            ctx.font = `bold ${{6.8 * dpr}}px sans-serif`;
            ctx.textAlign = 'center';
            ctx.fillText('+35% ΔL', mx, my - 5 * dpr);
        }}
        ctx.restore();
    }}

    // Tab switching between Circuit and Matrix views in Panel 2
    window.setPanel2Tab = function(tabName) {{
        const viewCirc = document.getElementById('panel2-view-circuit');
        const viewMat = document.getElementById('panel2-view-matrix');
        const btnCirc = document.getElementById('btn-tab-circuit');
        const btnMat = document.getElementById('btn-tab-matrix');

        if (tabName === 'circuit') {{
            if (viewCirc) viewCirc.style.display = 'block';
            if (viewMat) viewMat.style.display = 'none';
            if (btnCirc) {{ btnCirc.style.background = 'rgba(0,210,255,0.25)'; btnCirc.style.borderColor = '#00d2ff'; btnCirc.style.opacity = '1'; }}
            if (btnMat) {{ btnMat.style.background = 'rgba(0,210,255,0.12)'; btnMat.style.borderColor = 'var(--accent-cyan)'; btnMat.style.opacity = '0.65'; }}
            renderCircuitCanvas();
        }} else {{
            if (viewCirc) viewCirc.style.display = 'none';
            if (viewMat) viewMat.style.display = 'block';
            if (btnCirc) {{ btnCirc.style.background = 'rgba(0,210,255,0.12)'; btnCirc.style.borderColor = 'var(--accent-cyan)'; btnCirc.style.opacity = '0.65'; }}
            if (btnMat) {{ btnMat.style.background = 'rgba(0,210,255,0.25)'; btnMat.style.borderColor = '#00d2ff'; btnMat.style.opacity = '1'; }}
        }}
    }};
'''
