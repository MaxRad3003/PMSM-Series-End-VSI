import re

def refine_canvas_labels(filepath, is_hebrew=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Refine oscilloscope canvas text and tick spacing
    # 1. Ensure ctx.direction = 'ltr' right after getContext in renderOscilloscopeCanvas
    old_get_ctx = "const ctx = canvas.getContext('2d');\n        const W = canvas.width;\n        const H = canvas.height;\n\n        ctx.save();\n        ctx.clearRect(0, 0, W, H);"
    new_get_ctx = "const ctx = canvas.getContext('2d');\n        const W = canvas.width;\n        const H = canvas.height;\n\n        ctx.save();\n        ctx.clearRect(0, 0, W, H);\n        ctx.direction = 'ltr';"
    content = content.replace(old_get_ctx, new_get_ctx)

    # 2. Refine ticks so they don't look like a minus sign next to numbers:
    # Use inward ticks: ctx.moveTo(leftMargin, t.y); ctx.lineTo(leftMargin + 4 * dpr, t.y);
    old_tick_draw = "ctx.fillText(t.lbl, leftMargin - 4 * dpr, t.y + 3 * dpr);\n            ctx.strokeStyle = 'rgba(0, 210, 255, 0.4)';\n            ctx.beginPath(); ctx.moveTo(leftMargin - 3 * dpr, t.y); ctx.lineTo(leftMargin, t.y); ctx.stroke();"
    new_tick_draw = "ctx.fillText(t.lbl, leftMargin - 6 * dpr, t.y + 3 * dpr);\n            ctx.strokeStyle = 'rgba(0, 210, 255, 0.4)';\n            ctx.beginPath(); ctx.moveTo(leftMargin, t.y); ctx.lineTo(leftMargin + 4 * dpr, t.y); ctx.stroke();"
    content = content.replace(old_tick_draw, new_tick_draw)

    old_err_tick_draw = "ctx.fillText(t.lbl, leftMargin - 4 * dpr, t.y + 3 * dpr);\n            ctx.strokeStyle = 'rgba(255, 107, 129, 0.4)';\n            ctx.beginPath(); ctx.moveTo(leftMargin - 3 * dpr, t.y); ctx.lineTo(leftMargin, t.y); ctx.stroke();"
    new_err_tick_draw = "ctx.fillText(t.lbl, leftMargin - 6 * dpr, t.y + 3 * dpr);\n            ctx.strokeStyle = 'rgba(255, 107, 129, 0.4)';\n            ctx.beginPath(); ctx.moveTo(leftMargin, t.y); ctx.lineTo(leftMargin + 4 * dpr, t.y); ctx.stroke();"
    content = content.replace(old_err_tick_draw, new_err_tick_draw)

    # 3. Clean header text to prevent overlap
    if is_hebrew:
        old_headers = (
            "ctx.textAlign = 'left';\n"
            "        ctx.fillStyle = 'rgba(0, 210, 255, 0.9)';\n"
            "        ctx.fillText('CH1: 3.0 A/div • 5.0 ms/div (2 מחזורים סטציונריים @ 50 Hz)', leftMargin + 8 * dpr, 14 * dpr);\n\n"
            "        // Scope Mode Status Tag on right\n"
            "        ctx.textAlign = 'right';\n"
            "        if (demoScopeMode === 'trig') {\n"
            "            ctx.fillStyle = '#00ff88';\n"
            "            ctx.fillText('📌 גל מיוצב (TRIG LOCKED • 2 CYCLES)', W - 10 * dpr, 14 * dpr);\n"
            "        } else {\n"
            "            ctx.fillStyle = '#00d2ff';\n"
            "            ctx.fillText('🌊 גלילה איטית (SLOW ROLL 0.25X)', W - 10 * dpr, 14 * dpr);\n"
            "        }"
        )
        new_headers = (
            "ctx.textAlign = 'left';\n"
            "        ctx.fillStyle = 'rgba(0, 210, 255, 0.9)';\n"
            "        ctx.fillText('CH1: 3.0 A/div • 5.0 ms/div (i_a, i_b, i_c)', leftMargin + 8 * dpr, 14 * dpr);\n\n"
            "        // Scope Mode Status Tag on right\n"
            "        ctx.textAlign = 'right';\n"
            "        if (demoScopeMode === 'trig') {\n"
            "            ctx.fillStyle = '#00ff88';\n"
            "            ctx.fillText('📌 גל מיוצב • 2 מחזורים (TRIG LOCKED)', W - 10 * dpr, 14 * dpr);\n"
            "        } else {\n"
            "            ctx.fillStyle = '#00d2ff';\n"
            "            ctx.fillText('🌊 גלילה איטית (SLOW ROLL 0.25X)', W - 10 * dpr, 14 * dpr);\n"
            "        }"
        )
        content = content.replace(old_headers, new_headers)
    else:
        old_headers_en = (
            "ctx.textAlign = 'left';\n"
            "        ctx.fillStyle = 'rgba(0, 210, 255, 0.9)';\n"
            "        ctx.fillText('CH1: 3.0 A/div • 5.0 ms/div (2 Stationary Cycles @ 50 Hz)', leftMargin + 8 * dpr, 14 * dpr);\n\n"
            "        // Scope Mode Status Tag on right\n"
            "        ctx.textAlign = 'right';\n"
            "        if (demoScopeMode === 'trig') {\n"
            "            ctx.fillStyle = '#00ff88';\n"
            "            ctx.fillText('📌 TRIG LOCKED • 2 CYCLES (Stationary)', W - 10 * dpr, 14 * dpr);\n"
            "        } else {\n"
            "            ctx.fillStyle = '#00d2ff';\n"
            "            ctx.fillText('🌊 SLOW ROLL 0.25X', W - 10 * dpr, 14 * dpr);\n"
            "        }"
        )
        new_headers_en = (
            "ctx.textAlign = 'left';\n"
            "        ctx.fillStyle = 'rgba(0, 210, 255, 0.9)';\n"
            "        ctx.fillText('CH1: 3.0 A/div • 5.0 ms/div (i_a, i_b, i_c)', leftMargin + 8 * dpr, 14 * dpr);\n\n"
            "        // Scope Mode Status Tag on right\n"
            "        ctx.textAlign = 'right';\n"
            "        if (demoScopeMode === 'trig') {\n"
            "            ctx.fillStyle = '#00ff88';\n"
            "            ctx.fillText('📌 TRIG LOCKED • 2 CYCLES', W - 10 * dpr, 14 * dpr);\n"
            "        } else {\n"
            "            ctx.fillStyle = '#00d2ff';\n"
            "            ctx.fillText('🌊 SLOW ROLL 0.25X', W - 10 * dpr, 14 * dpr);\n"
            "        }"
        )
        content = content.replace(old_headers_en, new_headers_en)

    with open(filepath, 'w', encoding='utf-8') as f_out:
        f_out.write(content)
    print(f"Refined labels in: {filepath}")

refine_canvas_labels('generate_hebrew_presentation.py', is_hebrew=True)
refine_canvas_labels('generate_html_presentation.py', is_hebrew=False)
