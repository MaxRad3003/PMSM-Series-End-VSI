def get_render_circuit_code(is_hebrew=True):
    fault_label = '⚠️ תקלת ענף L4 (מנותק)' if is_hebrew else '⚠️ Leg L4 Fault (Isolated)'
    series_note = 'סלילי מנוע טוריים בין רגלי הממיר (איור 2)' if is_hebrew else 'Series Motor Windings Between Legs (Fig. 2)'
    cap_label = 'C'
    vdc_label = 'Vdc'
    
    return f'''
    // Canvas 4: Dynamic Electronic Circuit Simulation (Fig. 2: Series-End VSI with Series Windings)
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

        // Geometry layout - Fig. 2 exact topology
        const topRailY = 24 * dpr;
        const botRailY = Math.max(topRailY + 65 * dpr, H - 24 * dpr);
        const midY = (topRailY + botRailY) / 2;

        // Left DC source with split caps
        const xDc = 22 * dpr;
        const xRailStart = xDc;
        
        // 4 Legs: L1, L2, L3, L4
        const legX = [
            xDc + (W - xDc) * 0.18, // Leg 1 (v1)
            xDc + (W - xDc) * 0.44, // Leg 2 (v2)
            xDc + (W - xDc) * 0.70, // Leg 3 (v3)
            xDc + (W - xDc) * 0.93  // Leg 4 (v4)
        ];
        const xRailEnd = legX[3] + 10 * dpr;

        // Advance particle phase
        if (demoRunning) {{
            circuitParticlePhase = (circuitParticlePhase + 0.08 * (demoSpeed / 0.5)) % 1.0;
        }}

        // 1. DC BUS RAILS (+Vdc and 0V / GND)
        // Top Rail (+Vdc)
        ctx.strokeStyle = '#f6d365';
        ctx.lineWidth = 2.4 * dpr;
        ctx.shadowColor = '#f6d365';
        ctx.shadowBlur = 4 * dpr;
        ctx.beginPath(); ctx.moveTo(xRailStart, topRailY); ctx.lineTo(xRailEnd, topRailY); ctx.stroke();

        // Bottom Rail (0V / GND)
        ctx.strokeStyle = '#00d2ff';
        ctx.beginPath(); ctx.moveTo(xRailStart, botRailY); ctx.lineTo(xRailEnd, botRailY); ctx.stroke();
        ctx.shadowBlur = 0;

        // Rail Labels
        ctx.font = `bold ${{7.5 * dpr}}px monospace`;
        ctx.fillStyle = '#f6d365';
        ctx.textAlign = 'left';
        ctx.fillText('+Vdc', xDc + 2 * dpr, topRailY - 5 * dpr);

        ctx.fillStyle = '#00d2ff';
        ctx.fillText('0V', xDc + 2 * dpr, botRailY + 14 * dpr);

        // DC Source & Split Capacitors C/2 on left (Fig. 2)
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)';
        ctx.lineWidth = 1.2 * dpr;
        ctx.beginPath(); ctx.moveTo(xDc, topRailY); ctx.lineTo(xDc, midY - 6 * dpr); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(xDc, botRailY); ctx.lineTo(xDc, midY + 6 * dpr); ctx.stroke();
        
        // Ground tap at midY
        ctx.beginPath(); ctx.moveTo(xDc, midY); ctx.lineTo(xDc - 10 * dpr, midY); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(xDc - 10 * dpr, midY - 4 * dpr); ctx.lineTo(xDc - 10 * dpr, midY + 4 * dpr); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(xDc - 13 * dpr, midY - 2.5 * dpr); ctx.lineTo(xDc - 13 * dpr, midY + 2.5 * dpr); ctx.stroke();

        // Split cap plates
        const capPlateW = 5 * dpr;
        // Top C
        ctx.beginPath(); ctx.moveTo(xDc - capPlateW, topRailY + 12 * dpr); ctx.lineTo(xDc + capPlateW, topRailY + 12 * dpr); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(xDc - capPlateW, topRailY + 16 * dpr); ctx.lineTo(xDc + capPlateW, topRailY + 16 * dpr); ctx.stroke();
        // Bot C
        ctx.beginPath(); ctx.moveTo(xDc - capPlateW, botRailY - 16 * dpr); ctx.lineTo(xDc + capPlateW, botRailY - 16 * dpr); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(xDc - capPlateW, botRailY - 12 * dpr); ctx.lineTo(xDc + capPlateW, botRailY - 12 * dpr); ctx.stroke();

        ctx.font = `${{6.5 * dpr}}px sans-serif`;
        ctx.fillStyle = 'rgba(255, 255, 255, 0.45)';
        ctx.textAlign = 'right';
        ctx.fillText('C', xDc - 6 * dpr, topRailY + 16 * dpr);
        ctx.fillText('C', xDc - 6 * dpr, botRailY - 12 * dpr);

        // 2. FOUR INVERTER LEGS: L1, L2, L3, L4 (Switches & Diodes)
        const legColors = ['#00d2ff', '#ff9f43', '#ff6b81', '#00ff88'];
        const legNames = ['L1', 'L2', 'L3', 'L4'];
        const isLeg4Fault = (typeof leg4Fault !== 'undefined' && leg4Fault) || (typeof activeFault !== 'undefined' && activeFault === 'leg4');
        const isAsymActive = (typeof asymPercent !== 'undefined' && asymPercent > 0) || (typeof activeFault !== 'undefined' && activeFault === 'asym');

        const switchGap = 13 * dpr;
        const swTopStart = topRailY;
        const swTopEnd = midY - switchGap;
        const swBotStart = midY + switchGap;
        const swBotEnd = botRailY;

        for (let k = 0; k < 4; k++) {{
            const lx = legX[k];
            const isFaultedLeg = (k === 3 && isLeg4Fault);
            const highState = isFaultedLeg ? 0 : activeSwitches[k];
            const lowState = isFaultedLeg ? 0 : (1 - activeSwitches[k]);

            // Vertical wire from rail to top switch
            ctx.strokeStyle = 'rgba(255,255,255,0.25)';
            ctx.lineWidth = 1.2 * dpr;
            ctx.beginPath(); ctx.moveTo(lx, topRailY); ctx.lineTo(lx, swTopStart); ctx.stroke();
            // From top switch to midpoint
            ctx.beginPath(); ctx.moveTo(lx, swTopEnd); ctx.lineTo(lx, midY); ctx.stroke();
            // From midpoint to bottom switch
            ctx.beginPath(); ctx.moveTo(lx, midY); ctx.lineTo(lx, swBotStart); ctx.stroke();
            // From bottom switch to bottom rail
            ctx.beginPath(); ctx.moveTo(lx, swBotEnd); ctx.lineTo(lx, botRailY); ctx.stroke();

            // Draw Switches
            drawTransistorSwitch(ctx, lx, swTopStart + 2 * dpr, swTopEnd - 2 * dpr, highState, legColors[k], dpr, isFaultedLeg);
            drawTransistorSwitch(ctx, lx, swBotStart + 2 * dpr, swBotEnd - 2 * dpr, lowState, legColors[k], dpr, isFaultedLeg);

            // Switch Labels: S_Hk, S_Lk
            ctx.font = `${{6.5 * dpr}}px monospace`;
            ctx.fillStyle = highState ? '#00ff88' : 'rgba(255,255,255,0.4)';
            ctx.textAlign = 'right';
            ctx.fillText(`S_H${{k+1}}`, lx - 6 * dpr, (swTopStart + swTopEnd) / 2 + 2 * dpr);

            ctx.fillStyle = lowState ? '#00ff88' : 'rgba(255,255,255,0.4)';
            ctx.fillText(`S_L${{k+1}}`, lx - 6 * dpr, (swBotStart + swBotEnd) / 2 + 2 * dpr);

            // Midpoint Node Dot (vk)
            ctx.fillStyle = isFaultedLeg ? '#ff4757' : (activeSwitches[k] ? '#f6d365' : '#00d2ff');
            ctx.shadowColor = ctx.fillStyle;
            ctx.shadowBlur = 5 * dpr;
            ctx.beginPath(); ctx.arc(lx, midY, 3.2 * dpr, 0, 2 * Math.PI); ctx.fill();
            ctx.shadowBlur = 0;

            // Midpoint Voltage Label (v1, v2, v3, v4)
            ctx.font = `bold ${{7.5 * dpr}}px monospace`;
            ctx.fillStyle = '#f368e0';
            ctx.textAlign = 'center';
            ctx.fillText(`v_${{k+1}}`, lx, midY - 6 * dpr);

            // Leg Label under bottom rail (L1, L2, L3, L4)
            ctx.font = `bold ${{8.5 * dpr}}px sans-serif`;
            ctx.fillStyle = isFaultedLeg ? '#ff6b81' : legColors[k];
            ctx.fillText(legNames[k], lx, botRailY + 15 * dpr);

            // Draw current flowing from active switch into midpoint
            if (!isFaultedLeg) {{
                if (highState) {{
                    drawSwitchCurrentParticles(ctx, lx, swTopStart, lx, midY, legColors[k], circuitParticlePhase, dpr);
                }} else {{
                    drawSwitchCurrentParticles(ctx, lx, midY, lx, swBotEnd, legColors[k], circuitParticlePhase, dpr);
                }}
            }}
        }}

        // If Leg 4 is faulted: draw fault cross
        if (isLeg4Fault) {{
            const lx4 = legX[3];
            ctx.strokeStyle = '#ff4757';
            ctx.lineWidth = 2.2 * dpr;
            ctx.beginPath();
            ctx.moveTo(lx4 - 8 * dpr, midY - 8 * dpr); ctx.lineTo(lx4 + 8 * dpr, midY + 8 * dpr);
            ctx.moveTo(lx4 + 8 * dpr, midY - 8 * dpr); ctx.lineTo(lx4 - 8 * dpr, midY + 8 * dpr);
            ctx.stroke();

            ctx.font = `bold ${{6.8 * dpr}}px sans-serif`;
            ctx.fillStyle = '#ff6b81';
            ctx.textAlign = 'center';
            ctx.fillText('{fault_label}', lx4, midY + 16 * dpr);
        }}

        // 3. SERIES MOTOR WINDINGS (Between Consecutive Midpoints - Fig. 2):
        // Winding A (Za): Connected between v1 (legX[0]) and v2 (legX[1])
        drawSeriesWinding(ctx, legX[0], legX[1], midY, 'Z_a', 'v_a', legColors[0], curIa, circuitParticlePhase, dpr, false);

        // Winding B (Zb): Connected between v2 (legX[1]) and v3 (legX[2])
        drawSeriesWinding(ctx, legX[1], legX[2], midY, 'Z_b', 'v_b', legColors[1], curIb, circuitParticlePhase, dpr, isAsymActive);

        // Winding C (Zc): Connected between v3 (legX[2]) and v4 (legX[3])
        drawSeriesWinding(ctx, legX[2], legX[3], midY, 'Z_c', 'v_c', legColors[2], curIc, circuitParticlePhase, dpr, false);

        // 4. VOLTAGE POLARITY HUD & TELEMETRY (Fig. 2 equations)
        const v1 = activeSwitches[0];
        const v2 = activeSwitches[1];
        const v3 = activeSwitches[2];
        const v4 = isLeg4Fault ? 0 : activeSwitches[3];

        const va_val = (v1 - v2) * 400;
        const vb_val = (v2 - v3) * 400;
        const vc_val = (v3 - v4) * 400;
        const zsc_calc = (curIa + curIb + curIc) / 3;

        const elVan = document.getElementById('circuit-hud-van');
        const elVbn = document.getElementById('circuit-hud-vbn');
        const elVcn = document.getElementById('circuit-hud-vcn');
        const elIz = document.getElementById('circuit-hud-izsc');
        if (elVan) elVan.textContent = `v_a: ${{va_val >= 0 ? '+' : ''}}${{va_val}}V`;
        if (elVbn) elVbn.textContent = `v_b: ${{vb_val >= 0 ? '+' : ''}}${{vb_val}}V`;
        if (elVcn) elVcn.textContent = `v_c: ${{vc_val >= 0 ? '+' : ''}}${{vc_val}}V`;
        if (elIz) elIz.textContent = `i_0: ${{zsc_calc >= 0 ? '+' : ''}}${{zsc_calc.toFixed(2)}}A`;

        ctx.restore();
    }}

    // Helper: Draw Transistor Switch with Open/Closed Contact Arm & Antiparallel Diode
    function drawTransistorSwitch(ctx, x, yTop, yBot, state, color, dpr, isFaulted) {{
        ctx.save();
        const midY = (yTop + yBot) / 2;
        const armLen = (yBot - yTop) * 0.55;

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

        // Antiparallel Diode beside switch
        const dx = x + 7 * dpr;
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
        ctx.lineWidth = 1 * dpr;
        ctx.beginPath(); ctx.moveTo(x, yTop + 2 * dpr); ctx.lineTo(dx, yTop + 2 * dpr); ctx.lineTo(dx, yBot - 2 * dpr); ctx.lineTo(x, yBot - 2 * dpr); ctx.stroke();
        // Diode triangle (pointing upward for antiparallel)
        ctx.fillStyle = 'rgba(255, 255, 255, 0.28)';
        ctx.beginPath();
        ctx.moveTo(dx - 3 * dpr, midY + 3 * dpr);
        ctx.lineTo(dx + 3 * dpr, midY + 3 * dpr);
        ctx.lineTo(dx, midY - 3 * dpr);
        ctx.closePath();
        ctx.fill();

        ctx.restore();
    }}

    // Helper: Draw Series Motor Winding (Za, Zb, Zc) between consecutive legs
    function drawSeriesWinding(ctx, x1, x2, y, zName, vName, color, currentVal, particleT, dpr, isAsym) {{
        ctx.save();
        const segLen = x2 - x1;
        const boxW = Math.min(28 * dpr, segLen * 0.38);
        const boxH = 13 * dpr;
        const midX = (x1 + x2) / 2;

        const leftConnEnd = midX - boxW / 2;
        const rightConnStart = midX + boxW / 2;

        // 1. Connecting horizontal conductors
        ctx.strokeStyle = color;
        ctx.lineWidth = 1.6 * dpr;
        ctx.beginPath(); ctx.moveTo(x1, y); ctx.lineTo(leftConnEnd, y); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(rightConnStart, y); ctx.lineTo(x2, y); ctx.stroke();

        // 2. Winding impedance box / coil (Fig. 2 rectangular box with coil loops)
        ctx.fillStyle = isAsym ? 'rgba(246, 211, 101, 0.18)' : 'rgba(0, 210, 255, 0.12)';
        ctx.strokeStyle = isAsym ? '#f6d365' : color;
        ctx.lineWidth = 1.4 * dpr;
        ctx.fillRect(leftConnEnd, y - boxH / 2, boxW, boxH);
        ctx.strokeRect(leftConnEnd, y - boxH / 2, boxW, boxH);

        // Internal inductor coils inside box
        ctx.beginPath();
        const loops = 3;
        const step = boxW / (loops + 1);
        for (let l = 1; l <= loops; l++) {{
            const lx = leftConnEnd + l * step;
            ctx.arc(lx, y, 3 * dpr, 0, Math.PI, true);
        }}
        ctx.stroke();

        // 3. Winding Label (Za, Zb, Zc)
        ctx.font = `bold ${{7.2 * dpr}}px sans-serif`;
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'center';
        ctx.fillText(zName, midX, y + boxH / 2 + 10 * dpr);

        // 4. Voltage Polarity Label: "+ va -"
        ctx.font = `bold ${{7.2 * dpr}}px monospace`;
        ctx.fillStyle = '#f6d365';
        ctx.textAlign = 'center';
        ctx.fillText(`+  ${{vName}}  -`, midX, y - boxH / 2 - 4 * dpr);

        // 5. Directional reference arrow (i ->)
        ctx.font = `${{6.5 * dpr}}px sans-serif`;
        ctx.fillStyle = 'rgba(255,255,255,0.6)';
        ctx.fillText(`i_${{zName.slice(-1)}} →`, midX, y - boxH / 2 - 12 * dpr);

        // Asymmetry badge
        if (isAsym) {{
            ctx.fillStyle = 'rgba(246, 211, 101, 0.95)';
            ctx.font = `bold ${{6.5 * dpr}}px sans-serif`;
            ctx.fillText('+35% ΔL', midX, y + boxH / 2 + 19 * dpr);
        }}

        // 6. Flowing Animated Current Particles along winding
        const absI = Math.abs(currentVal);
        if (absI > 0.05) {{
            const isForward = currentVal > 0;
            const numParticles = Math.min(5, Math.max(2, Math.round(absI * 1.5)));

            for (let i = 0; i < numParticles; i++) {{
                let frac = ((i / numParticles) + (isForward ? particleT : (1 - particleT))) % 1.0;
                const px = x1 + segLen * frac;

                // Particle dot
                ctx.fillStyle = '#ffffff';
                ctx.shadowColor = color;
                ctx.shadowBlur = 4 * dpr;
                ctx.beginPath(); ctx.arc(px, y, 2.2 * dpr, 0, 2 * Math.PI); ctx.fill();
                ctx.shadowBlur = 0;
            }}
        }}

        ctx.restore();
    }}

    // Helper: Draw flowing current particles through switch to midpoint
    function drawSwitchCurrentParticles(ctx, x1, y1, x2, y2, color, particleT, dpr) {{
        ctx.save();
        const py = y1 + (y2 - y1) * ((particleT) % 1.0);
        ctx.fillStyle = '#ffffff';
        ctx.shadowColor = color;
        ctx.shadowBlur = 3 * dpr;
        ctx.beginPath(); ctx.arc(x1, py, 1.8 * dpr, 0, 2 * Math.PI); ctx.fill();
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
