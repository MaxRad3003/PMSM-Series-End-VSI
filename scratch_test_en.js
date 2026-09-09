
/* =====================================================================
   INTERACTIVE SIMULATION ENGINES (JSXGraph + Oscilloscope + Trajectory)
   ===================================================================== */

// --- 1. OEPC OPERATING PRINCIPLE & JSXGRAPH BOARD (ENHANCED) ---
let jxgBoard = null;
let errPoint = null;
let errVectorArrow = null;
let optVoltArrow = null;
let tdmVoltArrow = null;

function setPresetErrors(ea, eb, ec, izsc, btn) {
    const sEa = document.getElementById('slider-ea');
    const sEb = document.getElementById('slider-eb');
    const sEc = document.getElementById('slider-ec');
    const sIzsc = document.getElementById('slider-izsc');
    if (sEa) sEa.value = ea;
    if (sEb) sEb.value = eb;
    if (sEc) sEc.value = ec;
    if (sIzsc) sIzsc.value = izsc;

    document.querySelectorAll('#slide-oepc-principle .sim-btn-group .sim-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');

    updateErrorPrinciple();
}

function initJSXGraphBoard() {
    const boardEl = document.getElementById('oepc-jxg-board');
    if (!boardEl || !window.JXG) return;

    if (jxgBoard) {
        try {
            jxgBoard.update();
        } catch (e) {}
        return;
    }

    try {
        jxgBoard = JXG.JSXGraph.initBoard('oepc-jxg-board', {
            boundingbox: [-3.8, 3.8, 3.8, -3.8],
            axis: false,
            grid: { strokeColor: 'rgba(255,255,255,0.05)', gridX: 0.5, gridY: 0.5 },
            showCopyright: false,
            showNavigation: false,
            keepaspectratio: true
        });

        // Alpha Axis (Horizontal)
        jxgBoard.create('line', [[-3.4, 0], [3.4, 0]], {
            straightFirst: false,
            straightLast: false,
            strokeColor: 'rgba(0, 210, 255, 0.35)',
            strokeWidth: 1.5,
            highlight: false
        });
        jxgBoard.create('text', [3.3, 0.25, 'α-Axis'], {
            color: '#00d2ff',
            fontSize: 11,
            fontFamily: 'Inter, sans-serif',
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
        jxgBoard.create('text', [0.15, 3.3, 'β-Axis'], {
            color: '#9d50bb',
            fontSize: 11,
            fontFamily: 'Inter, sans-serif',
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
        const sectorNames = ['Sector 1', 'Sector 2', 'Sector 3', 'Sector 4', 'Sector 5', 'Sector 6'];

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

            // Sector Label
            const secAngle = hexAngles[i] + Math.PI/6;
            const secR = hexRadius * 0.55;
            jxgBoard.create('text', [secR * Math.cos(secAngle), secR * Math.sin(secAngle), sectorNames[i]], {
                color: 'rgba(255,255,255,0.22)',
                fontSize: 9.5,
                fontFamily: 'Inter, sans-serif',
                anchorX: 'middle',
                anchorY: 'middle',
                highlight: false
            });
        }

        // Draggable Error Point P (Alpha-Beta)
        errPoint = jxgBoard.create('point', [1.8, -0.6], {
            name: 'Error ε',
            size: 8,
            color: '#ff4757',
            strokeColor: '#ffffff',
            strokeWidth: 2.5,
            withLabel: true,
            label: { color: '#ff6b6b', fontSize: 12, fontFamily: 'Inter, sans-serif', fontWeight: 700, offset: [10, 10] }
        });

        // Error Vector Arrow (Red)
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

            const sEa = document.getElementById('slider-ea');
            const sEb = document.getElementById('slider-eb');
            const sEc = document.getElementById('slider-ec');
            if (sEa) sEa.value = Math.max(-3, Math.min(3, ea)).toFixed(1);
            if (sEb) sEb.value = Math.max(-3, Math.min(3, eb)).toFixed(1);
            if (sEc) sEc.value = Math.max(-3, Math.min(3, ec)).toFixed(1);

            document.querySelectorAll('#slide-oepc-principle .sim-btn-group .sim-btn').forEach(b => b.classList.remove('active'));
            updateErrorPrinciple();
        });

        updateErrorPrinciple();
    } catch (e) {
        console.warn('JSXGraph init error:', e);
    }
}

const OEPC_LUT_96 = {
    16: { row: 1, ep: 'CBA', l: [0, 0, 0, 1], vIdx: 1, impact: '-C,-Z', fmp: 0 },
    17: { row: 2, ep: 'CBA', l: [0, 0, 0, 1], vIdx: 1, impact: '-C,-Z', fmp: 1 },
    18: { row: 3, ep: 'CBA', l: [0, 0, 0, 1], vIdx: 1, impact: '-C,-Z', fmp: 0 },
    19: { row: 4, ep: 'CBA', l: [1, 0, 0, 1], vIdx: 9, impact: '+A,-C', fmp: 1 },
    20: { row: 5, ep: 'CBA', l: [0, 0, 0, 1], vIdx: 1, impact: '-C,-Z', fmp: 0 },
    21: { row: 6, ep: 'CBA', l: [1, 1, 0, 1], vIdx: 13, impact: '+B,-C', fmp: 1 },
    22: { row: 7, ep: 'CBA', l: [0, 0, 0, 1], vIdx: 1, impact: '-C,-Z', fmp: 0 },
    23: { row: 8, ep: 'CBA', l: [1, 1, 0, 1], vIdx: 13, impact: '+B,-C', fmp: 1 },
    24: { row: 9, ep: 'CBA', l: [1, 1, 1, 0], vIdx: 14, impact: '+C,+Z', fmp: 0 },
    25: { row: 10, ep: 'CBA', l: [0, 0, 1, 0], vIdx: 2, impact: '-B,+C', fmp: 1 },
    26: { row: 11, ep: 'CBA', l: [1, 1, 1, 0], vIdx: 14, impact: '+C,+Z', fmp: 0 },
    27: { row: 12, ep: 'CBA', l: [0, 0, 1, 0], vIdx: 2, impact: '-B,+C', fmp: 1 },
    28: { row: 13, ep: 'CBA', l: [1, 1, 1, 0], vIdx: 14, impact: '+C,+Z', fmp: 0 },
    29: { row: 14, ep: 'CBA', l: [0, 1, 1, 0], vIdx: 6, impact: '-A,+C', fmp: 1 },
    30: { row: 15, ep: 'CBA', l: [1, 1, 1, 0], vIdx: 14, impact: '+C,+Z', fmp: 0 },
    31: { row: 16, ep: 'CBA', l: [1, 1, 1, 0], vIdx: 14, impact: '+C,+Z', fmp: 1 },
    32: { row: 17, ep: 'BAC', l: [0, 0, 1, 1], vIdx: 3, impact: '-B,-Z', fmp: 0 },
    33: { row: 18, ep: 'BAC', l: [0, 0, 1, 1], vIdx: 3, impact: '-B,-Z', fmp: 1 },
    34: { row: 19, ep: 'BAC', l: [0, 0, 1, 1], vIdx: 3, impact: '-B,-Z', fmp: 0 },
    35: { row: 20, ep: 'BAC', l: [0, 0, 1, 0], vIdx: 2, impact: '-B,+C', fmp: 1 },
    36: { row: 21, ep: 'BAC', l: [0, 0, 1, 1], vIdx: 3, impact: '-B,-Z', fmp: 0 },
    37: { row: 22, ep: 'BAC', l: [1, 0, 1, 1], vIdx: 11, impact: '+A,-B', fmp: 1 },
    38: { row: 23, ep: 'BAC', l: [0, 0, 1, 1], vIdx: 3, impact: '-B,-Z', fmp: 0 },
    39: { row: 24, ep: 'BAC', l: [1, 0, 1, 1], vIdx: 11, impact: '+A,-B', fmp: 1 },
    40: { row: 25, ep: 'BAC', l: [1, 1, 0, 0], vIdx: 12, impact: '+B,+Z', fmp: 0 },
    41: { row: 26, ep: 'BAC', l: [0, 1, 0, 0], vIdx: 4, impact: '-A,+B', fmp: 1 },
    42: { row: 27, ep: 'BAC', l: [1, 1, 0, 0], vIdx: 12, impact: '+B,+Z', fmp: 0 },
    43: { row: 28, ep: 'BAC', l: [0, 1, 0, 0], vIdx: 4, impact: '-A,+B', fmp: 1 },
    44: { row: 29, ep: 'BAC', l: [1, 1, 0, 0], vIdx: 12, impact: '+B,+Z', fmp: 0 },
    45: { row: 30, ep: 'BAC', l: [1, 1, 0, 1], vIdx: 13, impact: '+B,-C', fmp: 1 },
    46: { row: 31, ep: 'BAC', l: [1, 1, 0, 0], vIdx: 12, impact: '+B,+Z', fmp: 0 },
    47: { row: 32, ep: 'BAC', l: [1, 1, 0, 0], vIdx: 12, impact: '+B,+Z', fmp: 1 },
    48: { row: 33, ep: 'BCA', l: [0, 0, 1, 1], vIdx: 3, impact: '-B,-Z', fmp: 0 },
    49: { row: 34, ep: 'BCA', l: [0, 0, 1, 1], vIdx: 3, impact: '-B,-Z', fmp: 1 },
    50: { row: 35, ep: 'BCA', l: [0, 0, 1, 1], vIdx: 3, impact: '-B,-Z', fmp: 0 },
    51: { row: 36, ep: 'BCA', l: [1, 0, 1, 1], vIdx: 11, impact: '+A,-B', fmp: 1 },
    52: { row: 37, ep: 'BCA', l: [0, 0, 1, 1], vIdx: 3, impact: '-B,-Z', fmp: 0 },
    53: { row: 38, ep: 'BCA', l: [0, 0, 1, 0], vIdx: 2, impact: '-B,+C', fmp: 1 },
    54: { row: 39, ep: 'BCA', l: [0, 0, 1, 1], vIdx: 3, impact: '-B,-Z', fmp: 0 },
    55: { row: 40, ep: 'BCA', l: [0, 0, 1, 0], vIdx: 2, impact: '-B,+C', fmp: 1 },
    56: { row: 41, ep: 'BCA', l: [1, 1, 0, 0], vIdx: 12, impact: '+B,+Z', fmp: 0 },
    57: { row: 42, ep: 'BCA', l: [1, 1, 0, 1], vIdx: 13, impact: '+B,-C', fmp: 1 },
    58: { row: 43, ep: 'BCA', l: [1, 1, 0, 0], vIdx: 12, impact: '+B,+Z', fmp: 0 },
    59: { row: 44, ep: 'BCA', l: [1, 1, 0, 1], vIdx: 13, impact: '+B,-C', fmp: 1 },
    60: { row: 45, ep: 'BCA', l: [1, 1, 0, 0], vIdx: 12, impact: '+B,+Z', fmp: 0 },
    61: { row: 46, ep: 'BCA', l: [0, 1, 0, 0], vIdx: 4, impact: '-A,+B', fmp: 1 },
    62: { row: 47, ep: 'BCA', l: [1, 1, 0, 0], vIdx: 12, impact: '+B,+Z', fmp: 0 },
    63: { row: 48, ep: 'BCA', l: [1, 1, 0, 0], vIdx: 12, impact: '+B,+Z', fmp: 1 },
    64: { row: 49, ep: 'ACB', l: [0, 1, 1, 1], vIdx: 7, impact: '-A,-Z', fmp: 0 },
    65: { row: 50, ep: 'ACB', l: [0, 1, 1, 1], vIdx: 7, impact: '-A,-Z', fmp: 1 },
    66: { row: 51, ep: 'ACB', l: [0, 1, 0, 1], vIdx: 5, impact: '-A,+B,-C,-Z', fmp: 0 },
    67: { row: 52, ep: 'ACB', l: [0, 1, 0, 1], vIdx: 5, impact: '-A,+B,-C,-Z', fmp: 1 },
    68: { row: 53, ep: 'ACB', l: [0, 1, 1, 1], vIdx: 7, impact: '-A,-Z', fmp: 0 },
    69: { row: 54, ep: 'ACB', l: [0, 1, 1, 0], vIdx: 6, impact: '-A,+C', fmp: 1 },
    70: { row: 55, ep: 'ACB', l: [0, 1, 1, 1], vIdx: 7, impact: '-A,-Z', fmp: 0 },
    71: { row: 56, ep: 'ACB', l: [0, 1, 1, 0], vIdx: 6, impact: '-A,+C', fmp: 1 },
    72: { row: 57, ep: 'ACB', l: [1, 0, 0, 0], vIdx: 8, impact: '+A,+Z', fmp: 0 },
    73: { row: 58, ep: 'ACB', l: [1, 0, 0, 1], vIdx: 9, impact: '+A,-C', fmp: 1 },
    74: { row: 59, ep: 'ACB', l: [1, 0, 0, 0], vIdx: 8, impact: '+A,+Z', fmp: 0 },
    75: { row: 60, ep: 'ACB', l: [1, 0, 0, 1], vIdx: 9, impact: '+A,-C', fmp: 1 },
    76: { row: 61, ep: 'ACB', l: [1, 0, 1, 0], vIdx: 10, impact: '+A,-B,+C,+Z', fmp: 0 },
    77: { row: 62, ep: 'ACB', l: [1, 0, 1, 0], vIdx: 10, impact: '+A,-B,+C,+Z', fmp: 1 },
    78: { row: 63, ep: 'ACB', l: [1, 0, 0, 0], vIdx: 8, impact: '+A,+Z', fmp: 0 },
    79: { row: 64, ep: 'ACB', l: [1, 0, 0, 0], vIdx: 8, impact: '+A,+Z', fmp: 1 },
    80: { row: 65, ep: 'CAB', l: [0, 0, 0, 1], vIdx: 1, impact: '-C,-Z', fmp: 0 },
    81: { row: 66, ep: 'CAB', l: [0, 0, 0, 1], vIdx: 1, impact: '-C,-Z', fmp: 1 },
    82: { row: 67, ep: 'CAB', l: [0, 1, 0, 1], vIdx: 5, impact: '-A,+B,-C,-Z', fmp: 0 },
    83: { row: 68, ep: 'CAB', l: [0, 1, 0, 1], vIdx: 5, impact: '-A,+B,-C,-Z', fmp: 1 },
    84: { row: 69, ep: 'CAB', l: [0, 0, 0, 1], vIdx: 1, impact: '-C,-Z', fmp: 0 },
    85: { row: 70, ep: 'CAB', l: [1, 0, 0, 1], vIdx: 9, impact: '+A,-C', fmp: 1 },
    86: { row: 71, ep: 'CAB', l: [0, 0, 0, 1], vIdx: 1, impact: '-C,-Z', fmp: 0 },
    87: { row: 72, ep: 'CAB', l: [1, 0, 0, 1], vIdx: 9, impact: '+A,-C', fmp: 1 },
    88: { row: 73, ep: 'CAB', l: [1, 1, 1, 0], vIdx: 14, impact: '+C,+Z', fmp: 0 },
    89: { row: 74, ep: 'CAB', l: [0, 1, 1, 0], vIdx: 6, impact: '-A,+C', fmp: 1 },
    90: { row: 75, ep: 'CAB', l: [1, 1, 1, 0], vIdx: 14, impact: '+C,+Z', fmp: 0 },
    91: { row: 76, ep: 'CAB', l: [0, 1, 1, 0], vIdx: 6, impact: '-A,+C', fmp: 1 },
    92: { row: 77, ep: 'CAB', l: [1, 0, 1, 0], vIdx: 10, impact: '+A,-B,+C,+Z', fmp: 0 },
    93: { row: 78, ep: 'CAB', l: [1, 0, 1, 0], vIdx: 10, impact: '+A,-B,+C,+Z', fmp: 1 },
    94: { row: 79, ep: 'CAB', l: [1, 1, 1, 0], vIdx: 14, impact: '+C,+Z', fmp: 0 },
    95: { row: 80, ep: 'CAB', l: [1, 1, 1, 0], vIdx: 14, impact: '+C,+Z', fmp: 1 },
    96: { row: 81, ep: 'ABC', l: [0, 1, 1, 1], vIdx: 7, impact: '-A,-Z', fmp: 0 },
    97: { row: 82, ep: 'ABC', l: [0, 1, 1, 1], vIdx: 7, impact: '-A,-Z', fmp: 1 },
    98: { row: 83, ep: 'ABC', l: [0, 1, 1, 1], vIdx: 7, impact: '-A,-Z', fmp: 0 },
    99: { row: 84, ep: 'ABC', l: [0, 1, 1, 0], vIdx: 6, impact: '-A,+C', fmp: 1 },
    100: { row: 85, ep: 'ABC', l: [0, 1, 1, 1], vIdx: 7, impact: '-A,-Z', fmp: 0 },
    101: { row: 86, ep: 'ABC', l: [0, 1, 0, 0], vIdx: 4, impact: '-A,+B', fmp: 1 },
    102: { row: 87, ep: 'ABC', l: [0, 1, 1, 1], vIdx: 7, impact: '-A,-Z', fmp: 0 },
    103: { row: 88, ep: 'ABC', l: [0, 1, 0, 0], vIdx: 4, impact: '-A,+B', fmp: 1 },
    104: { row: 89, ep: 'ABC', l: [1, 0, 0, 0], vIdx: 8, impact: '+A,+Z', fmp: 0 },
    105: { row: 90, ep: 'ABC', l: [1, 0, 1, 1], vIdx: 11, impact: '+A,-B', fmp: 1 },
    106: { row: 91, ep: 'ABC', l: [1, 0, 0, 0], vIdx: 8, impact: '+A,+Z', fmp: 0 },
    107: { row: 92, ep: 'ABC', l: [1, 0, 1, 1], vIdx: 11, impact: '+A,-B', fmp: 1 },
    108: { row: 93, ep: 'ABC', l: [1, 0, 0, 0], vIdx: 8, impact: '+A,+Z', fmp: 0 },
    109: { row: 94, ep: 'ABC', l: [1, 0, 0, 1], vIdx: 9, impact: '+A,-C', fmp: 1 },
    110: { row: 95, ep: 'ABC', l: [1, 0, 0, 0], vIdx: 8, impact: '+A,+Z', fmp: 0 },
    111: { row: 96, ep: 'ABC', l: [1, 0, 0, 0], vIdx: 8, impact: '+A,+Z', fmp: 1 },
};

// Helper to format physical impact into mathematical HTML
function formatPhysicalImpact(impact) {
    if (!impact || impact === 'None') return '<span style="color:var(--text-muted)">No Action</span>';
    
    const isZsc = impact.includes('Z');
    const badgeClass = isZsc ? 'zsc-tag' : 'dm-tag';
    const tagTitle = isZsc ? 'ZSC Suppression' : '2-Phase Correction';

    let formatted = impact
        .replace(/\+A/g, '+<i>i</i><sub>a</sub>')
        .replace(/-A/g, '&minus;<i>i</i><sub>a</sub>')
        .replace(/\+B/g, '+<i>i</i><sub>b</sub>')
        .replace(/-B/g, '&minus;<i>i</i><sub>b</sub>')
        .replace(/\+C/g, '+<i>i</i><sub>c</sub>')
        .replace(/-C/g, '&minus;<i>i</i><sub>c</sub>')
        .replace(/\+Z/g, '+<i>i</i><sub>0</sub>')
        .replace(/-Z/g, '&minus;<i>i</i><sub>0</sub>');

    return `<span class="action-tag ${badgeClass}">${tagTitle}</span> <span class="math-term">${formatted}</span>`;
}

// Populate 96-LUT Modal Table dynamically
function populateLutModalTable() {
    const tbody = document.getElementById('lut-table-tbody');
    if (!tbody || tbody.children.length > 0) return;
    let html = '';
    for (let idx = 16; idx <= 111; idx++) {
        const r = OEPC_LUT_96[idx];
        if (!r) continue;
        const pBits = `${(idx>>6)&1} ${(idx>>5)&1} ${(idx>>4)&1}`;
        const sBits = `${(idx>>3)&1} ${(idx>>2)&1} ${(idx>>1)&1}`;
        const fmp = idx & 1;
        const fmpTag = fmp === 1 ? '<span class="mode-tag dm-tag">DM (1)</span>' : '<span class="mode-tag cm-tag">CM (0)</span>';
        const binStr = idx.toString(2).padStart(7, '0');
        html += `<tr id="lut-row-${idx}" data-idx="${idx}" data-row="${r.row}" data-ep="${r.ep}" data-impact="${r.impact}">
            <td>#${r.row}</td>
            <td><code class="sig-code">${idx} (0b${binStr})</code></td>
            <td><strong style="color:var(--accent-cyan)">${r.ep}</strong></td>
            <td><code class="sig-code">${pBits}</code></td>
            <td><code class="sig-code">${sBits}</code></td>
            <td>${fmpTag}</td>
            <td><code class="sig-code" style="color:#ffffff; font-weight:700;">[${r.l.join(' ')}]</code></td>
            <td><span class="vidx-pill">Vector ${r.vIdx}</span></td>
            <td><strong style="color:var(--accent-gold)">${r.impact}</strong></td>
        </tr>`;
    }
    tbody.innerHTML = html;
}

window.lastLutAddr = 105;

function openLutModal() {
    const m = document.getElementById('lut-modal');
    if (m) {
        m.style.display = 'flex';
        populateLutModalTable();
        highlightLutRow(window.lastLutAddr);
    }
}

function closeLutModal() {
    const m = document.getElementById('lut-modal');
    if (m) m.style.display = 'none';
}

function filterLutTable(query) {
    query = (query || '').trim().toUpperCase();
    const rows = document.querySelectorAll('#lut-table-tbody tr');
    rows.forEach(r => {
        if (!query) {
            r.style.display = '';
        } else {
            const ep = r.getAttribute('data-ep') || '';
            const imp = (r.getAttribute('data-impact') || '').toUpperCase();
            const idx = r.getAttribute('data-idx') || '';
            const row = r.getAttribute('data-row') || '';
            const text = r.textContent.toUpperCase();
            if (ep.includes(query) || imp.includes(query) || idx === query || row === query || text.includes(query)) {
                r.style.display = '';
            } else {
                r.style.display = 'none';
            }
        }
    });
}

function highlightLutRow(activeIdx) {
    window.lastLutAddr = activeIdx;
    const m = document.getElementById('lut-modal');
    if (!m || m.style.display === 'none') return;
    populateLutModalTable();
    document.querySelectorAll('#lut-table-tbody tr.active-lut-row').forEach(tr => tr.classList.remove('active-lut-row'));
    const target = document.getElementById('lut-row-' + activeIdx);
    if (target) {
        target.classList.add('active-lut-row');
        target.scrollIntoView({ behavior: 'smooth', block: 'center' });
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

    // Clark Transformation: alpha-beta error coordinates
    const e_alpha = ea;
    const e_beta = (eb - ec) / Math.sqrt(3);

    if (errPoint && !errPoint.isDraggable) {
        errPoint.moveTo([e_alpha, e_beta]);
    }

    const mag = Math.sqrt(e_alpha*e_alpha + e_beta*e_beta);
    let ang = Math.atan2(e_beta, e_alpha) * (180 / Math.PI);
    document.getElementById('tel-err-mag').textContent = mag.toFixed(2) + ' A';
    document.getElementById('tel-err-ang').textContent = ang.toFixed(1) + '°';

    // 1. Calculate Priority Bits Pab, Pbc, Pca
    const absA = Math.abs(ea);
    const absB = Math.abs(eb);
    const absC = Math.abs(ec);
    
    const epsA = absA;
    const epsB = absB + (absB === absA ? 1e-6 : 0);
    const epsC = absC + (absC === absA || absC === absB ? 2e-6 : 0);
    
    const pab = (epsA >= epsB) ? 1 : 0;
    const pbc = (epsB >= epsC) ? 1 : 0;
    const pca = (epsC >= epsA) ? 1 : 0;

    let epOrder = '';
    let maxVal = ea, midVal = eb, minVal = ec;
    let primePhase = 'Phase A', secPhase = 'Phase B', minorPhase = 'Phase C';
    let primeCode = 'a', secCode = 'b', minorCode = 'c';

    if (epsA >= epsB && epsB >= epsC) { 
        epOrder = 'ABC'; maxVal = ea; midVal = eb; minVal = ec;
        primePhase = 'Phase A'; secPhase = 'Phase B'; minorPhase = 'Phase C';
        primeCode = 'a'; secCode = 'b'; minorCode = 'c';
    } else if (epsA >= epsC && epsC >= epsB) { 
        epOrder = 'ACB'; maxVal = ea; midVal = ec; minVal = eb;
        primePhase = 'Phase A'; secPhase = 'Phase C'; minorPhase = 'Phase B';
        primeCode = 'a'; secCode = 'c'; minorCode = 'b';
    } else if (epsB >= epsA && epsA >= epsC) { 
        epOrder = 'BAC'; maxVal = eb; midVal = ea; minVal = ec;
        primePhase = 'Phase B'; secPhase = 'Phase A'; minorPhase = 'Phase C';
        primeCode = 'b'; secCode = 'a'; minorCode = 'c';
    } else if (epsB >= epsC && epsC >= epsA) { 
        epOrder = 'BCA'; maxVal = eb; midVal = ec; minVal = ea;
        primePhase = 'Phase B'; secPhase = 'Phase C'; minorPhase = 'Phase A';
        primeCode = 'b'; secCode = 'c'; minorCode = 'a';
    } else if (epsC >= epsA && epsA >= epsB) { 
        epOrder = 'CAB'; maxVal = ec; midVal = ea; minVal = eb;
        primePhase = 'Phase C'; secPhase = 'Phase A'; minorPhase = 'Phase B';
        primeCode = 'c'; secCode = 'a'; minorCode = 'b';
    } else { 
        epOrder = 'CBA'; maxVal = ec; midVal = eb; minVal = ea;
        primePhase = 'Phase C'; secPhase = 'Phase B'; minorPhase = 'Phase A';
        primeCode = 'c'; secCode = 'b'; minorCode = 'a';
    }

    document.getElementById('badge-prime-phase').textContent = primePhase;
    document.getElementById('badge-prime-val').textContent = (maxVal >= 0 ? '+' : '') + maxVal.toFixed(2) + ' A';
    document.getElementById('badge-sec-phase').textContent = secPhase;
    document.getElementById('badge-sec-val').textContent = (midVal >= 0 ? '+' : '') + midVal.toFixed(2) + ' A';
    document.getElementById('badge-minor-phase').textContent = minorPhase;
    document.getElementById('badge-minor-val').textContent = (minVal >= 0 ? '+' : '') + minVal.toFixed(2) + ' A';

    // 2. Calculate Sign Bits Smx, Smd, Smn
    const smx = (maxVal >= 0) ? 1 : 0;
    const smd = (midVal >= 0) ? 1 : 0;
    const snm = (minVal >= 0) ? 1 : 0;

    // 3. Calculate Error Mode Priority Flag Fmp
    const isZscCritical = Math.abs(izsc) > 0.35;
    const fmp = isZscCritical ? 0 : 1;

    // 4. Compute 7-bit binary address matching exact OEPC_LUT96.xlsx
    const addr = (pab << 6) | (pbc << 5) | (pca << 4) | (smx << 3) | (smd << 2) | (snm << 1) | fmp;
    window.lastLutAddr = addr;

    // 5. Direct Lookup in OEPC_LUT_96
    const lutMatch = OEPC_LUT_96[addr] || { row: 1, ep: epOrder, l: [0,0,0,1], vIdx: 1, impact: '-C,-Z', fmp: fmp };

    // Update 7-bit Signature Display
    const sig7El = document.getElementById('lut-7bits');
    if (sig7El) {
        sig7El.innerHTML = `${pab}&nbsp;${pbc}&nbsp;${pca} &nbsp;|&nbsp; ${smx}&nbsp;${smd}&nbsp;${snm} &nbsp;|&nbsp; ${fmp}`;
    }
    const idxBadgeEl = document.getElementById('lut-idx-badge');
    if (idxBadgeEl) {
        idxBadgeEl.textContent = `Idx=${addr} • Row #${lutMatch.row} (${lutMatch.ep})`;
    }

    // Update Mode Badge
    const badgeEl = document.getElementById('lut-row-num');
    if (badgeEl) {
        if (fmp === 0) {
            badgeEl.textContent = `⚠️ Zero-Sequence Priority (CM Priority, Fmp=0) • Row #${lutMatch.row}`;
            badgeEl.className = 'lut-mode-badge cm-badge';
        } else {
            badgeEl.textContent = `⚡ Differential-Mode Priority (DM Priority, Fmp=1) • Row #${lutMatch.row}`;
            badgeEl.className = 'lut-mode-badge dm-badge';
        }
    }

    // Update Vector Code & Impact
    const vCodeEl = document.getElementById('lut-vector-code');
    if (vCodeEl) {
        vCodeEl.textContent = `[${lutMatch.l.join(' ')}] (Vector ${lutMatch.vIdx})`;
    }
    const vActEl = document.getElementById('lut-action-desc');
    if (vActEl) {
        vActEl.innerHTML = formatPhysicalImpact(lutMatch.impact);
    }

    // Physical V0 voltage
    const v0 = (lutMatch.l[3] === 1) ? -18.5 : +18.5;
    const v0El = document.getElementById('tel-v0');
    if (v0El) {
        v0El.textContent = isZscCritical ? ((v0 >= 0 ? '+' : '') + v0.toFixed(1) + ' V') : '0.0 V';
    }

    // Dynamic TDM Comparison Note
    const compEl = document.getElementById('tdm-compare-note');
    if (compEl) {
        if (fmp === 0) {
            compEl.innerHTML = `Zero-sequence current anomaly (${(izsc>=0?'+':'')+izsc.toFixed(2)} A) mandates immediate suppression. Conventional TDM ignores ZSC, creating severe distortion. <strong>OEPC</strong> accesses <strong>Row #${lutMatch.row} in 96-LUT</strong>, driving Vector ${lutMatch.vIdx} to quench zero-sequence current without phase lag!`;
        } else {
            compEl.innerHTML = `Differential errors dominate. Conventional TDM corrects only 1 phase per cycle and freezes the others. <strong>OEPC</strong> accesses Row #${lutMatch.row} in 96-LUT to execute <strong>${lutMatch.impact}</strong> simultaneously in under 1.75 µs!`;
        }
    }

    // Update modal active row labels
    const mAddr = document.getElementById('modal-active-addr');
    if (mAddr) mAddr.textContent = `${addr} (0b${addr.toString(2).padStart(7, '0')})`;
    const mRow = document.getElementById('modal-active-row');
    if (mRow) mRow.textContent = `#${lutMatch.row} (${lutMatch.ep})`;
    const mVec = document.getElementById('modal-active-vec');
    if (mVec) mVec.textContent = `[${lutMatch.l.join(' ')}] (Vector ${lutMatch.vIdx} • ${lutMatch.impact})`;

    // Highlight row in modal table if open
    highlightLutRow(addr);

    // Plot vectors on JSXGraph
    if (mag > 0.1) {
        const vMag = 2.4;
        const optVx = - (e_alpha / mag) * vMag;
        const optVy = - (e_beta / mag) * vMag;

        // TDM vector projects only on prime axis
        const tdmMag = 1.6;
        let tdmVx = 0, tdmVy = 0;
        if (primeCode === 'a') {
            tdmVx = -Math.sign(maxVal) * tdmMag;
            tdmVy = 0;
        } else if (primeCode === 'b') {
            tdmVx = -Math.sign(maxVal) * tdmMag * Math.cos(2*Math.PI/3);
            tdmVy = -Math.sign(maxVal) * tdmMag * Math.sin(2*Math.PI/3);
        } else {
            tdmVx = -Math.sign(maxVal) * tdmMag * Math.cos(4*Math.PI/3);
            tdmVy = -Math.sign(maxVal) * tdmMag * Math.sin(4*Math.PI/3);
        }

        if (optVoltArrow && optVoltArrow.point2) optVoltArrow.point2.moveTo([optVx, optVy]);
        if (tdmVoltArrow && tdmVoltArrow.point2) tdmVoltArrow.point2.moveTo([tdmVx, tdmVy]);
    }
}

if (slides[currentSlideIdx] && slides[currentSlideIdx].id === 'slide-oepc-principle') {
            initJSXGraphBoard();
        }
    }, 150);
};

// Also trigger on load if first
window.addEventListener('load', () => {
    setTimeout(initJSXGraphBoard, 300);
});
