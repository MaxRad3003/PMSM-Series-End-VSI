"""
Generate Master HTML Presentation & PowerPoint Presentation for OEPC SE-VSI PMSM Drive.
Includes:
- Transition from TDM to OEPC (Error Priority formulation & 96-entry LUT).
- Theoretical modeling of 4-Leg Series-End VSI & ZSC suppression.
- IEEE Transactions on Industrial Electronics (TIE) paper validation & figures.
- Typhoon C-HIL real-time validation (HIL402/HIL404).
- Physical experimental validation on GaN SE-VSI prototype with asymmetric RL load (+/-25%).
- Hardware setup built by Maxim Radkin (author contribution & publication milestone).
- New PMSM motor acquisition & custom-built inverters for next-phase dyno testing.
- Fault tolerance (ITSC) & comprehensive summary.
"""

import os
from pathlib import Path

PMSM_DIR = Path(__file__).resolve().parent
ASSETS_DIR = PMSM_DIR / "presentation_assets"

# Read images as relative or local file paths
html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Optimal Error-Priority Control (OEPC) for Series-End VSI PMSM Drives</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@400;500;600&family=Heebo:wght@400;600;700;800&display=swap" rel="stylesheet">
    <!-- MathJax for rendering LaTeX equations -->
    <script>
    window.MathJax = {
        tex: {
            inlineMath: [['$', '$'], ['\\(', '\\)']],
            displayMath: [['$$', '$$'], ['\\[', '\\]']],
            processEscapes: true
        },
        options: {
            enableMenu: false
        }
    };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        :root {
            --bg-primary: #0a0f1d;
            --bg-card: rgba(18, 26, 47, 0.85);
            --bg-card-hover: rgba(28, 40, 70, 0.95);
            --border-color: rgba(64, 120, 240, 0.25);
            --border-highlight: rgba(0, 210, 255, 0.5);
            --accent-cyan: #00d2ff;
            --accent-blue: #3a7bd5;
            --accent-purple: #9d50bb;
            --accent-green: #00f2fe;
            --accent-gold: #f6d365;
            --text-primary: #f0f4fc;
            --text-secondary: #9cb3d9;
            --text-muted: #627d98;
            --glow-cyan: 0 0 25px rgba(0, 210, 255, 0.35);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            overflow: hidden;
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(58, 123, 213, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(157, 80, 187, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 50% 50%, rgba(0, 210, 255, 0.05) 0%, transparent 60%);
        }

        /* Presentation Container */
        .presentation-wrapper {
            position: relative;
            width: 95vw;
            height: 90vh;
            max-width: 1600px;
            max-height: 900px;
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), var(--glow-cyan);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        /* Top Navigation / Status Header */
        .pres-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 28px;
            border-bottom: 1px solid var(--border-color);
            background: rgba(10, 15, 29, 0.6);
        }

        .header-title {
            font-family: 'Outfit', sans-serif;
            font-size: 15px;
            font-weight: 600;
            color: var(--accent-cyan);
            letter-spacing: 1px;
            text-transform: uppercase;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .header-badge {
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 20px;
            letter-spacing: 0.5px;
        }

        .slide-counter {
            font-family: 'Fira Code', monospace;
            font-size: 14px;
            font-weight: 600;
            color: var(--text-secondary);
        }

        /* Slides Carousel Container */
        .slides-container {
            position: relative;
            flex-grow: 1;
            width: 100%;
            height: calc(100% - 130px);
            overflow: hidden;
        }

        .slide {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            padding: 32px 48px;
            display: flex;
            flex-direction: column;
            opacity: 0;
            visibility: hidden;
            transform: translateX(50px);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            overflow-y: auto;
        }

        .slide.active {
            opacity: 1;
            visibility: visible;
            transform: translateX(0);
        }

        /* Slide Titles */
        .slide-category {
            font-family: 'Outfit', sans-serif;
            font-size: 13px;
            font-weight: 700;
            color: var(--accent-cyan);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 6px;
        }

        .slide-title {
            font-family: 'Outfit', sans-serif;
            font-size: 28px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 22px;
            line-height: 1.25;
            background: linear-gradient(90deg, #ffffff, #c7d8ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .slide-content-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 28px;
            align-items: center;
            flex-grow: 1;
        }

        .slide-content-full {
            display: flex;
            flex-direction: column;
            gap: 20px;
            flex-grow: 1;
        }

        /* Text Boxes & Cards */
        .card {
            background: rgba(23, 34, 61, 0.7);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 22px;
            transition: all 0.3s ease;
        }

        .card:hover {
            border-color: var(--border-highlight);
            box-shadow: 0 8px 25px rgba(0, 210, 255, 0.15);
        }

        .card-highlight {
            background: linear-gradient(135deg, rgba(58, 123, 213, 0.2), rgba(157, 80, 187, 0.2));
            border: 1px solid rgba(0, 210, 255, 0.4);
        }

        .card-title {
            font-family: 'Outfit', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: var(--accent-cyan);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .list-styled {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .list-styled li {
            position: relative;
            padding-left: 24px;
            font-size: 15px;
            line-height: 1.5;
            color: var(--text-primary);
        }

        .list-styled li::before {
            content: "✦";
            position: absolute;
            left: 0;
            color: var(--accent-cyan);
            font-size: 13px;
        }

        .hebrew-note {
            direction: rtl;
            font-family: 'Heebo', sans-serif;
            font-size: 14px;
            color: var(--text-secondary);
            margin-top: 10px;
            border-right: 3px solid var(--accent-cyan);
            padding-right: 12px;
            line-height: 1.5;
        }

        /* Figure and Image Containers */
        .fig-box {
            position: relative;
            background: rgba(10, 15, 29, 0.85);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }

        .fig-box img {
            max-width: 100%;
            max-height: 380px;
            object-fit: contain;
            border-radius: 8px;
            background: #ffffff;
            padding: 4px;
        }

        .fig-caption {
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 10px;
            text-align: center;
            line-height: 1.4;
        }

        /* Comparison Table */
        .table-custom {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
            margin-top: 10px;
        }

        .table-custom th {
            background: rgba(58, 123, 213, 0.3);
            color: var(--accent-cyan);
            font-weight: 700;
            padding: 10px 14px;
            text-align: left;
            border: 1px solid var(--border-color);
        }

        .table-custom td {
            padding: 10px 14px;
            border: 1px solid var(--border-color);
            color: var(--text-primary);
        }

        .table-custom tr:nth-child(even) {
            background: rgba(255, 255, 255, 0.02);
        }

        .table-custom tr.highlight-row {
            background: rgba(0, 210, 255, 0.15);
            font-weight: 600;
        }

        /* Navigation Bar Footer */
        .pres-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 28px;
            border-top: 1px solid var(--border-color);
            background: rgba(10, 15, 29, 0.8);
        }

        .nav-controls {
            display: flex;
            gap: 12px;
        }

        .btn-nav {
            background: linear-gradient(135deg, rgba(58, 123, 213, 0.8), rgba(0, 210, 255, 0.8));
            color: #ffffff;
            border: none;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: 700;
            font-family: 'Outfit', sans-serif;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .btn-nav:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 210, 255, 0.4);
        }

        .btn-nav:disabled {
            opacity: 0.4;
            cursor: not-allowed;
            transform: none;
        }

        .keyboard-hint {
            font-size: 12px;
            color: var(--text-muted);
            font-family: 'Fira Code', monospace;
        }

        /* Title Slide Custom Styling */
        .title-slide {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            height: 100%;
        }

        .title-slide h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 38px;
            font-weight: 800;
            line-height: 1.25;
            margin-bottom: 16px;
            background: linear-gradient(135deg, #00d2ff, #3a7bd5, #9d50bb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            max-width: 90%;
        }

        .title-slide h2 {
            font-family: 'Heebo', sans-serif;
            font-size: 22px;
            font-weight: 600;
            color: #d1e2ff;
            margin-bottom: 28px;
            direction: rtl;
        }

        .authors-badge-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            max-width: 900px;
            width: 100%;
            margin-top: 15px;
        }

        .author-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
        }

        .author-name {
            font-weight: 700;
            font-size: 16px;
            color: #ffffff;
        }

        .author-role {
            font-size: 12px;
            color: var(--accent-cyan);
            margin-top: 4px;
        }

        .author-inst {
            font-size: 12px;
            color: var(--text-secondary);
        }

        .tag-pill {
            display: inline-block;
            padding: 4px 10px;
            background: rgba(0, 210, 255, 0.15);
            border: 1px solid rgba(0, 210, 255, 0.3);
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            color: var(--accent-cyan);
        }
    
        /* =====================================================================
           INTERACTIVE JSXGRAPH & DYNAMIC SIMULATION STYLES
        #slide-oepc-principle, #slide-dynamic-sim { overflow: hidden !important; }
           ===================================================================== */
                .sim-container {
            display: grid;
            grid-template-columns: 460px 1fr;
            gap: 14px;
            height: calc(100% - 60px);
            margin-top: 2px;
        }
        .sim-controls-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 10px 12px;
            display: flex;
            flex-direction: column;
            gap: 5px;
            overflow-y: auto;
            max-height: 100%;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }
        .sim-controls-card::-webkit-scrollbar {
            width: 4px;
        }
        .sim-controls-card::-webkit-scrollbar-thumb {
            background: rgba(0, 210, 255, 0.4);
            border-radius: 4px;
        }
        .sliders-grid-2x2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 5px 10px;
        }
        .sim-control-group.compact {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .sim-control-group.compact .sim-control-header {
            font-size: 11.5px;
        }
        .sim-control-group.compact .sim-val-badge {
            font-size: 11px;
            padding: 1px 5px;
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
            padding: 12px 14px;
            display: flex;
            flex-direction: column;
            gap: 8px;
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

        /* =====================================================================
           REFINED SLIDE 6 STYLES: CRYSTAL-CLEAR LUT & MATHEMATICAL TYPOGRAPHY
           ===================================================================== */
        .math-term {
            font-family: 'Fira Code', 'Cambria Math', 'KaTeX_Math', monospace;
            font-weight: 600;
            color: var(--accent-cyan);
            direction: ltr !important;
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
            gap: 4px;
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
            background: rgba(0, 0, 0, 0.28);
            padding: 7px 9px;
            border-radius: 6px;
            border: 1px solid rgba(255, 255, 255, 0.08);
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
            font-size: 13.5px;
            font-weight: 700;
            color: #ffffff;
            direction: ltr !important;
            unicode-bidi: isolate;
        }
        .v-action {
            font-size: 12px;
            font-weight: 600;
            color: var(--accent-cyan);
            direction: ltr !important;
            unicode-bidi: isolate;
        }
        
        /* 96-LUT Signature Bar & Modal Styles */
        .lut-signature-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(0, 0, 0, 0.45);
            border: 1px solid rgba(0, 210, 255, 0.35);
            border-radius: 6px;
            padding: 4px 8px;
            font-size: 11px;
            font-family: 'Fira Code', monospace;
            margin-top: 2px;
        }
        .sig-label {
            color: var(--text-muted);
            font-size: 10px;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
        }
        .sig-bits {
            color: #00f2fe;
            font-weight: 700;
            direction: ltr !important;
            letter-spacing: 1px;
        }
        .sig-idx {
            color: #f6d365;
            font-weight: 700;
            font-size: 10.5px;
            direction: ltr !important;
        }
        .btn-lut-modal {
            margin-top: 5px;
            width: 100%;
            border: 1px solid rgba(0, 210, 255, 0.4);
            background: rgba(0, 210, 255, 0.12);
            color: #00d2ff;
            font-weight: 600;
            font-size: 11.5px;
            padding: 5px 8px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: 'Inter', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        .btn-lut-modal:hover {
            background: rgba(0, 210, 255, 0.25);
            border-color: #00d2ff;
            box-shadow: 0 0 12px rgba(0, 210, 255, 0.3);
            color: #ffffff;
        }

        /* Full 96-LUT Modal */
        .lut-modal-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(4, 8, 18, 0.88);
            backdrop-filter: blur(8px);
            z-index: 99999;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .lut-modal-content {
            background: rgba(13, 22, 42, 0.98);
            border: 1px solid rgba(0, 210, 255, 0.5);
            border-radius: 14px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8), 0 0 35px rgba(0, 210, 255, 0.2);
            width: 95vw;
            max-width: 1150px;
            height: 85vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            color: var(--text-primary);
        }
        .lut-modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 20px;
            background: rgba(0, 0, 0, 0.35);
            border-bottom: 1px solid var(--border-color);
        }
        .lut-modal-header h3 {
            font-family: 'Inter', sans-serif;
            font-size: 17px;
            font-weight: 700;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .lut-modal-close {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-size: 26px;
            cursor: pointer;
            line-height: 1;
            padding: 0 6px;
            transition: color 0.2s;
        }
        .lut-modal-close:hover {
            color: #ff5577;
        }
        .lut-modal-info {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 10px 20px;
            background: rgba(0, 210, 255, 0.05);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            font-size: 12.5px;
        }
        .lut-search-box {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: #ffffff;
            padding: 5px 12px;
            font-size: 12px;
            font-family: 'Inter', sans-serif;
            width: 280px;
            outline: none;
        }
        .lut-search-box:focus {
            border-color: var(--accent-cyan);
            box-shadow: 0 0 8px rgba(0, 210, 255, 0.3);
        }
        .lut-modal-body {
            flex-grow: 1;
            overflow-y: auto;
            padding: 12px 20px;
        }
        .lut-full-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            text-align: center;
        }
        .lut-full-table th {
            position: sticky;
            top: 0;
            background: #0f1a30;
            color: var(--accent-cyan);
            padding: 8px 6px;
            font-weight: 700;
            font-family: 'Inter', sans-serif;
            border-bottom: 2px solid var(--border-highlight);
            z-index: 2;
        }
        .lut-full-table td {
            padding: 5px 6px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        .lut-full-table tr:hover {
            background: rgba(0, 210, 255, 0.08);
        }
        .lut-full-table tr.active-lut-row {
            background: rgba(0, 210, 255, 0.25) !important;
            box-shadow: inset 0 0 0 1px #00d2ff;
        }
        .lut-full-table tr.active-lut-row td {
            font-weight: 700;
            color: #ffffff;
        }
        .sig-code {
            font-family: 'Fira Code', monospace;
            font-size: 11.5px;
            direction: ltr !important;
        }
        .mode-tag {
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 10.5px;
            font-weight: 700;
        }
        .vidx-pill {
            background: rgba(157, 80, 187, 0.25);
            border: 1px solid rgba(157, 80, 187, 0.6);
            color: #d1a4ff;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
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
            margin-inline-end: 4px;
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

    
        /* Fullscreen Controls & Responsive Expansion */
        .btn-fullscreen {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: rgba(0, 210, 255, 0.12);
            border: 1px solid rgba(0, 210, 255, 0.4);
            color: var(--accent-cyan);
            padding: 5px 12px;
            border-radius: 8px;
            font-size: 12.5px;
            font-family: 'Rubik', 'Heebo', sans-serif;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.25s ease;
        }
        .btn-fullscreen:hover {
            background: rgba(0, 210, 255, 0.25);
            border-color: var(--accent-cyan);
            box-shadow: 0 0 12px rgba(0, 210, 255, 0.4);
            transform: translateY(-1px);
        }
        :fullscreen .presentation-wrapper,
        :-webkit-full-screen .presentation-wrapper {
            width: 100vw !important;
            height: 100vh !important;
            max-width: 100vw !important;
            max-height: 100vh !important;
            border-radius: 0 !important;
            border: none !important;
        }

    

/* ==========================================================
   SLIDE 11: OEPC SWITCHING & CLOSED-LOOP ERROR DEMO (COMPACT)
   ========================================================== */
#slide-switching-error-demo {
    padding: 14px 28px !important;
    overflow: hidden !important;
}

#slide-switching-error-demo h2 {
    font-size: 1.35rem !important;
    margin: 0 0 2px 0 !important;
    line-height: 1.2 !important;
}

#slide-switching-error-demo h3 {
    font-size: 0.92rem !important;
    margin: 0 0 6px 0 !important;
    line-height: 1.2 !important;
}

.slide11-grid {
    display: grid;
    grid-template-columns: 1.15fr 0.9fr 1.15fr;
    gap: 10px;
    height: calc(100% - 105px);
    margin-top: 4px;
}

.slide11-card {
    background: rgba(13, 27, 42, 0.9);
    border: 1px solid rgba(0, 210, 255, 0.25);
    border-radius: 10px;
    padding: 8px 12px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}

.slide11-card-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--accent-cyan);
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 4px;
}

.demo-bar-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 2px 0;
    font-size: 0.78rem;
    font-family: monospace;
}

.demo-bar-track {
    flex: 1;
    height: 6px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 3px;
    margin: 0 8px;
    overflow: hidden;
}

.demo-bar-fill {
    height: 100%;
    width: 0%;
    border-radius: 3px;
    transition: width 0.05s ease-out;
}

.fill-a { background: linear-gradient(90deg, #0072ff, #00d2ff); }
.fill-b { background: linear-gradient(90deg, #f39c12, #f6d365); }
.fill-c { background: linear-gradient(90deg, #e74c3c, #ff6b81); }
.fill-zsc { background: linear-gradient(90deg, #00b894, #00ff88); }

.demo-order-tag {
    display: inline-block;
    background: rgba(0, 210, 255, 0.15);
    border: 1px solid var(--accent-cyan);
    color: var(--accent-cyan);
    padding: 1px 8px;
    border-radius: 5px;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 1px;
}

.demo-ranks-container {
    display: flex;
    gap: 5px;
    margin: 4px 0;
}

.demo-rank-tag {
    flex: 1;
    text-align: center;
    padding: 3px 2px;
    border-radius: 5px;
    font-size: 0.75rem;
    font-weight: 700;
}

.rank-mx { background: rgba(255, 107, 129, 0.15); border: 1px solid #ff6b81; color: #ff6b81; }
.rank-md { background: rgba(246, 211, 101, 0.15); border: 1px solid #f6d365; color: #f6d365; }
.rank-mn { background: rgba(0, 255, 136, 0.15); border: 1px solid #00ff88; color: #00ff88; }

.demo-bin-box {
    background: #060a12;
    border: 1px solid rgba(0, 210, 255, 0.35);
    border-radius: 6px;
    padding: 4px 8px;
    font-family: monospace;
    font-size: 1.05rem;
    font-weight: 700;
    text-align: center;
    margin: 4px 0;
    letter-spacing: 2px;
}

.bit-p { color: var(--accent-cyan); }
.bit-sep { color: rgba(255,255,255,0.25); margin: 0 3px; }
.bit-s { color: #f6d365; }
.bit-f { color: #00ff88; }

.demo-idx-tag {
    text-align: center;
    color: #ffffff;
    font-size: 0.82rem;
    font-weight: 600;
    margin-bottom: 3px;
}

.demo-pill {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 0.74rem;
    font-weight: 700;
    text-align: center;
}

.pill-zsc { background: rgba(0, 255, 136, 0.15); border: 1px solid #00ff88; color: #00ff88; }
.pill-dm { background: rgba(0, 210, 255, 0.15); border: 1px solid #00d2ff; color: #00d2ff; }

.demo-vec-hero {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(0, 210, 255, 0.08);
    border: 1px solid rgba(0, 210, 255, 0.25);
    border-radius: 6px;
    padding: 4px 8px;
    margin: 3px 0;
}

.demo-vec-label { font-size: 0.82rem; color: #cbd5e0; }
.demo-vec-val { font-size: 1.15rem; font-weight: 800; color: #00d2ff; font-family: monospace; }

.demo-tuple-hero {
    font-size: 0.78rem;
    font-family: monospace;
    background: #070e1a;
    padding: 3px 6px;
    border-radius: 5px;
    margin: 2px 0;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.demo-impact-hero {
    font-size: 0.76rem;
    background: #070e1a;
    padding: 3px 6px;
    border-radius: 5px;
    margin: 2px 0;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.transistor-matrix-card {
    background: rgba(6, 11, 20, 0.95);
    border: 1px solid rgba(0, 210, 255, 0.35);
    border-radius: 6px;
    padding: 4px 6px;
    margin: 4px 0;
}

.matrix-title {
    font-size: 0.74rem;
    color: var(--accent-cyan);
    font-weight: 700;
    margin-bottom: 3px;
    display: flex;
    align-items: center;
    gap: 4px;
}

.matrix-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 4px;
}

.matrix-leg {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 5px;
    padding: 2px 4px;
    text-align: center;
}

.leg-neutral {
    border-color: rgba(0, 255, 136, 0.35);
    background: rgba(0, 255, 136, 0.04);
}

.leg-header {
    font-size: 0.7rem;
    font-weight: 700;
    color: #cbd5e0;
    margin-bottom: 2px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    padding-bottom: 1px;
}

.transistor-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 1px 0;
    font-size: 0.68rem;
    font-family: monospace;
}

.t-badge {
    padding: 1px 4px;
    border-radius: 3px;
    font-weight: 700;
    font-size: 0.64rem;
}

.badge-on {
    background: rgba(0, 255, 136, 0.22);
    color: #00ff88;
    border: 1px solid #00ff88;
    box-shadow: 0 0 4px rgba(0, 255, 136, 0.3);
}

.badge-off {
    background: rgba(255, 71, 87, 0.15);
    color: #ff6b81;
    border: 1px solid rgba(255, 71, 87, 0.3);
}

.matrix-footnote {
    font-size: 0.65rem;
    color: var(--text-muted);
    margin-top: 3px;
    line-height: 1.2;
}

.demo-norm-box {
    margin-top: auto;
    background: rgba(0, 0, 0, 0.35);
    padding: 4px 6px;
    border-radius: 5px;
    font-size: 0.78rem;
    text-align: center;
    border: 1px dashed rgba(0, 210, 255, 0.25);
}

.demo-controls-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(8, 15, 26, 0.95);
    border: 1px solid rgba(0, 210, 255, 0.3);
    border-radius: 8px;
    padding: 5px 12px;
    margin-top: 6px;
    gap: 10px;
}

.demo-btn-group {
    display: flex;
    gap: 6px;
    align-items: center;
}

.demo-btn {
    background: rgba(0, 210, 255, 0.12);
    border: 1px solid var(--accent-cyan);
    color: #ffffff;
    padding: 4px 10px;
    border-radius: 5px;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 4px;
}

.demo-btn:hover {
    background: rgba(0, 210, 255, 0.25);
    box-shadow: 0 0 8px rgba(0, 210, 255, 0.4);
}


.fault-btn {
    font-size: 0.74rem !important;
    padding: 3px 7px !important;
    border-radius: 5px !important;
    transition: all 0.2s ease !important;
}
.fault-btn.active-fault {
    background: rgba(0, 210, 255, 0.25) !important;
    border-color: #00d2ff !important;
    color: #ffffff !important;
    box-shadow: 0 0 10px rgba(0, 210, 255, 0.45) !important;
    font-weight: 700 !important;
}

.demo-btn-surge {
    border-color: #ff6b81;
    color: #ff8598;
    background: rgba(255, 107, 129, 0.12);
}

.demo-surge-banner {
    position: absolute;
    top: 8px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(255, 71, 87, 0.95);
    color: #ffffff;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(255, 71, 87, 0.5);
    font-size: 0.8rem;
    pointer-events: none;
    transition: opacity 0.3s;
    z-index: 100;
}
</style>

    <!-- JSXGraph Mathematical & Dynamic Visualizer -->
    <link rel="stylesheet" type="text/css" href="presentation_assets/jsxgraph.css" />
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/jsxgraph/distrib/jsxgraph.css" />
    <script type="text/javascript" src="presentation_assets/jsxgraphcore.js"></script>
    <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/jsxgraph/distrib/jsxgraphcore.js"></script>

</head>
<body>

<div class="presentation-wrapper">
    <!-- Header -->
    <div class="pres-header">
        <div class="header-title">
            <span>⚡ Shamoon College of Engineering (SCE)</span>
            <span class="header-badge">IEEE TIE Research</span>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
            <button class="btn-fullscreen" id="fullscreen-btn" onclick="toggleFullscreen()" title="Fullscreen (F)">
                <span id="fullscreen-icon">⛶</span>
                <span id="fullscreen-text">Fullscreen</span>
            </button>
            <div class="slide-counter">
            Slide <span id="current-slide">1</span> / <span id="total-slides">16</span>
        </div>
    </div>
    </div>

    <!-- Slides -->
    <div class="slides-container" id="slides-container">

        <!-- SLIDE 1: Title Slide -->
        <div class="slide active">
            <div class="title-slide">
                <span class="tag-pill" style="margin-bottom: 15px;">Advanced Motor Drive Research & Hardware Validation</span>
                <h1>Hardware-Efficient Optimal Error-Priority Control for Series-End VSI With ZSC Suppression</h1>
                <h2>בקרת זרם אופטימלית מבוססת תעדוף שגיאה (OEPC) לממיר Series-End VSI עבור מנועי PMSM ודיכוי זרמי סדרה אפס</h2>
                
                <div class="authors-badge-grid">
                    <div class="author-card">
                        <div class="author-name">Dr. Eli Gad Barbie</div>
                        <div class="author-role">Project Supervisor & Senior Lecturer</div>
                        <div class="author-inst">Shamoon College of Engineering</div>
                    </div>
                    <div class="author-card">
                        <div class="author-name">Maxim Radkin</div>
                        <div class="author-role">M.Sc. Candidate</div>
                        <div class="author-inst">Shamoon College of Engineering</div>
                    </div>
                    <div class="author-card">
                        <div class="author-name">Prof. Dmitry Baimel</div>
                        <div class="author-role">Senior Member, IEEE</div>
                        <div class="author-inst">Shamoon College of Engineering</div>
                    </div>
                </div>

                <div style="margin-top: 25px; font-size: 13px; color: var(--text-muted); font-family: 'Fira Code', monospace;">
                    Published in: IEEE Transactions on Industrial Electronics (IEEE TIE, 2026)
                </div>
            </div>
        </div>

        <!-- SLIDE 2: Evolution from TDM to OEPC -->
        <div class="slide">
            <div class="slide-category">Methodology Evolution</div>
            <div class="slide-title">Evolution: From Single-Error TDM to Multi-Objective OEPC</div>
            <div class="slide-content-grid">
                <div class="card">
                    <div class="card-title">⏳ Classical TDM Approach (Time Division Multiplexing)</div>
                    <ul class="list-styled">
                        <li><strong>Single Error Focus:</strong> TDM corrects only the single most critical error at each switching instant.</li>
                        <li><strong>Fixed Round-Robin Logic:</strong> Cycles through phases sequentially, discarding potential secondary corrections.</li>
                        <li><strong>Preservation Policy:</strong> Applies zero voltage to non-prime phases to avoid error deterioration.</li>
                    </ul>
                    <div class="hebrew-note">
                        בשיטת TDM הקלאסית מתקנים שגיאה קריטית אחת בלבד בכל פסיעת בקרה, תוך שמירה על שאר הפאזות ללא שינוי.
                    </div>
                </div>

                <div class="card card-highlight">
                    <div class="card-title">🚀 Proposed OEPC Strategy (Optimal Error-Priority Control)</div>
                    <ul class="list-styled">
                        <li><strong>Multi-Objective Optimality:</strong> OEPC actively attempts to correct <em>as many phase errors and ZSC components simultaneously</em> as physically possible.</li>
                        <li><strong>Deterministic 96-Entry LUT:</strong> Maps a 7-bit error signature (EPC + ESC + EMP) directly to the optimal switching state in &lt;1.75 µs.</li>
                        <li><strong>Zero Dynamic Compromise:</strong> Secondary errors are corrected whenever they do not conflict with the prime error.</li>
                    </ul>
                    <div class="hebrew-note">
                        בשיטת OEPC מנתחים את כל 6 שגיאות הזרם ומתקנים מקסימום שגיאות בו-זמנית לפי סדר עדיפויות דטרמיניסטי ב-LUT.
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 3: SE-VSI Topology & ZSC Challenge -->
        <div class="slide">
            <div class="slide-category">System Topology & Modeling</div>
            <div class="slide-title">Series-End VSI Architecture & Zero-Sequence Current (ZSC)</div>
            <div class="slide-content-grid">
                <div>
                    <div class="card" style="margin-bottom: 18px;">
                        <div class="card-title">4-Leg Series-End VSI Advantages</div>
                        <ul class="list-styled">
                            <li><strong>Optimal DC Utilization:</strong> Delivers $M_a = 1.0$ (identical to dual-inverter setups) with only 4 legs (8 switches vs 12).</li>
                            <li><strong>Open-Winding PMSM:</strong> Enhances power density and dynamic torque response.</li>
                            <li><strong>Dedicated Hardware Realization (Altium PCB Design):</strong>
                                Topology advantages were physically realized and validated through custom in-house hardware:
                                <div style="margin-top: 6px; padding: 6px 10px; background: rgba(0, 210, 255, 0.08); border: 1px solid rgba(0, 210, 255, 0.3); border-radius: 8px; font-size: 13px; line-height: 1.5;">
                                    <div>⚡ <strong>High-Speed GaN Power Switches:</strong> <code>Power_Swech - GUN_ V2</code> (Ultra-low switching loss GaN FET stage for high-frequency modulation).</div>
                                    <div style="margin-top: 3px;">🎯 <strong>Floating Isolated Current Sensors:</strong> <code>Isolated_Current_Sensor _V2_1</code> (High-bandwidth isolated sensing for fast phase current & ZSC feedback).</div>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <div class="card">
                        <div class="card-title">The ZSC Mitigation Dilemma</div>
                        <ul class="list-styled">
                            <li><strong>Common-Mode Loop:</strong> Floating neutral absence creates a closed ZSC path via inverter legs 1 and 4 ($v_1 - v_4$).</li>
                            <li><strong>Phase Coupling:</strong> Leg 4 switching impacts all 3 phase currents simultaneously through zero-sequence circulation.</li>
                        </ul>
                    </div>
                </div>

                <div class="fig-box">
                    <img src="presentation_assets/fig2_se_vsi_topology_and_zsc_path.jpg" alt="SE-VSI Topology & ZSC Path">
                    <div class="fig-caption">Fig. 2: Three-phase Series-End VSI with Open-Winding load and equivalent zero-sequence loop.</div>
                </div>
            </div>
        </div>

        <!-- SLIDE 4: Error Formulation & Priority Encoding -->
        <div class="slide">
            <div class="slide-category">Control Algorithm</div>
            <div class="slide-title">Error-Priority Processing & 7-Bit LUT Signature</div>
            <div class="slide-content-grid">
                <div class="card">
                    <div class="card-title">Deterministic Logic Flow in ABC Coordinates</div>
                    <ul class="list-styled">
                        <li><strong>6 Current Errors:</strong> 3 Differential-Mode (DM: $\varepsilon_{dm}^x = i_x^* - i_x$) and 3 Common-Mode (CM: $\varepsilon_{cm}^x = i_x^* + i_0^* - i_x - i_0$).</li>
                        <li><strong>Critical Error Selection:</strong> Pairwise comparison selects the dominant error $\varepsilon_{crit}(x)$ per phase.</li>
                        <li><strong>Error Mode Predominance (EMP / $F_{mp}$):</strong> Flag indicates whether CM ($F_{mp}=0$) or DM ($F_{mp}=1$) demands dominate.</li>
                        <li><strong>Error Priority Code (EPC):</strong> 3-bit binary sorting of $|\varepsilon_{crit}(a)|, |\varepsilon_{crit}(b)|, |\varepsilon_{crit}(c)|$.</li>
                        <li><strong>Error Signs Code (ESC):</strong> 3-bit polarity representation (+/-).</li>
                    </ul>
                    <div class="hebrew-note">
                        חישוב לוגי ישיר בקואורדינטות ABC המפיק כתובת בת 7 ביטים לטבלת LUT קומפקטית ללא אינטגרטורים וללא התמרות צירים.
                    </div>
                </div>

                <div class="fig-box">
                    <img src="presentation_assets/fig3_oepc_flowchart_algorithm.jpg" alt="OEPC Flowchart Algorithm">
                    <div class="fig-caption">Fig. 3: Procedural flowchart of the OEPC current control framework.</div>
                </div>
            </div>
        </div>

        <!-- SLIDE 5: 96-Entry LUT Switching Selection -->
        <div class="slide">
            <div class="slide-category">Switching State Selection</div>
            <div class="slide-title">96-Entry Optimal Look-Up Table (LUT) Design</div>
            <div class="slide-content-full">
                <table class="table-custom">
                    <thead>
                        <tr>
                            <th>Case #</th>
                            <th>Priority Order (EPO)</th>
                            <th>EPC (Pab, Pbc, Pca)</th>
                            <th>ESC (Smx, Smd, Smn)</th>
                            <th>EMP (Fmp)</th>
                            <th>Selected State (L1 L2 L3 L4)</th>
                            <th>Corrective Physical Impact</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="highlight-row">
                            <td>Case 1</td>
                            <td>ACB</td>
                            <td>100</td>
                            <td>011</td>
                            <td>1 (DM Priority)</td>
                            <td><strong>0110</strong></td>
                            <td>$-i_a, +i_c$ (Simultaneous correction of 2 phases)</td>
                        </tr>
                        <tr>
                            <td>Case 2</td>
                            <td>ACB</td>
                            <td>100</td>
                            <td>001</td>
                            <td>0 (CM Priority)</td>
                            <td><strong>0101</strong></td>
                            <td>$-i_a, +i_b, -i_c, -i_0$ (Full 3-Phase + ZSC Regulation)</td>
                        </tr>
                        <tr class="highlight-row">
                            <td>Case 3</td>
                            <td>BAC</td>
                            <td>010</td>
                            <td>110</td>
                            <td>1 (DM Priority)</td>
                            <td><strong>1101</strong></td>
                            <td>$+i_b, -i_c$</td>
                        </tr>
                        <tr>
                            <td>Case 4</td>
                            <td>BAC</td>
                            <td>010</td>
                            <td>110</td>
                            <td>0 (CM Priority)</td>
                            <td><strong>1100</strong></td>
                            <td>$+i_b, +i_0$</td>
                        </tr>
                        <tr class="highlight-row">
                            <td>Case 5</td>
                            <td>ABC</td>
                            <td>110</td>
                            <td>001</td>
                            <td>1 (DM Priority)</td>
                            <td><strong>0110</strong></td>
                            <td>$-i_a, +i_c$</td>
                        </tr>
                        <tr>
                            <td>Case 6</td>
                            <td>ABC</td>
                            <td>110</td>
                            <td>001</td>
                            <td>0 (CM Priority)</td>
                            <td><strong>0111</strong></td>
                            <td>$-i_a, -i_0$</td>
                        </tr>
                    </tbody>
                </table>

                <div class="card" style="margin-top: 10px;">
                    <div class="card-title">⚡ Key Principles of the 96-Node Table</div>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; font-size: 13px;">
                        <div><strong>1. Lexicographic Priority:</strong> Prime error is always strictly corrected first.</div>
                        <div><strong>2. Maximum Correction:</strong> Secondary errors are addressed whenever feasible without conflict.</div>
                        <div><strong>3. Non-Interference:</strong> Infeasible secondary errors are safely bypassed via zero-voltage self-circulation.</div>
                    </div>
                </div>
            </div>
        </div>

        
        <!-- SLIDE: Interactive OEPC Operating Principle & Priority LUT Decoder -->
        <!-- SLIDE: Interactive OEPC Operating Principle & Priority LUT Decoder -->
        <!-- SLIDE: Interactive OEPC Operating Principle & Priority LUT Decoder -->
        <div class="slide" id="slide-oepc-principle" style="overflow: hidden !important;">
            <div class="slide-category">Interactive Simulation • JSXGraph</div>
            <div class="slide-title">Interactive Decoder: OEPC Operating Principle & 96-State Priority LUT</div>
            
            <div class="sim-container" style="grid-template-columns: 380px 1fr;">
                                <!-- Left: Controls & Pipeline -->
                <div class="sim-controls-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div class="card-title" style="font-size: 13.5px; margin-bottom: 0;">
                            ⚙️ Current Error Controls: <bdi class="math-term">&epsilon; = <i>i</i><sup>*</sup> &minus; <i>i</i></bdi>
                        </div>
                    </div>
                    
                    <!-- 2x2 Sliders Grid (Ultra-compact, saves 105px) -->
                    <div class="sliders-grid-2x2">
                        <div class="sim-control-group compact">
                            <div class="sim-control-header">
                                <span>Phase A: <bdi class="math-term">&epsilon;<sub>a</sub></bdi></span>
                                <span class="sim-val-badge" id="val-ea">+1.80 A</span>
                            </div>
                            <input type="range" class="sim-slider" id="slider-ea" min="-3.0" max="3.0" step="0.1" value="1.8" oninput="updateErrorPrinciple()">
                        </div>

                        <div class="sim-control-group compact">
                            <div class="sim-control-header">
                                <span>Phase B: <bdi class="math-term">&epsilon;<sub>b</sub></bdi></span>
                                <span class="sim-val-badge" id="val-eb">-1.20 A</span>
                            </div>
                            <input type="range" class="sim-slider" id="slider-eb" min="-3.0" max="3.0" step="0.1" value="-1.2" oninput="updateErrorPrinciple()">
                        </div>

                        <div class="sim-control-group compact">
                            <div class="sim-control-header">
                                <span>Phase C: <bdi class="math-term">&epsilon;<sub>c</sub></bdi></span>
                                <span class="sim-val-badge" id="val-ec">-0.60 A</span>
                            </div>
                            <input type="range" class="sim-slider" id="slider-ec" min="-3.0" max="3.0" step="0.1" value="-0.6" oninput="updateErrorPrinciple()">
                        </div>

                        <div class="sim-control-group compact">
                            <div class="sim-control-header">
                                <span>Zero-Seq: <bdi class="math-term"><i>i</i><sub>zsc</sub></bdi></span>
                                <span class="sim-val-badge" id="val-izsc">0.00 A</span>
                            </div>
                            <input type="range" class="sim-slider" id="slider-izsc" min="-2.0" max="2.0" step="0.05" value="0.0" oninput="updateErrorPrinciple()">
                        </div>
                    </div>

                    <!-- Preset Scenarios -->
                    <div style="margin-top: 1px;">
                        <div style="font-size: 10.5px; color: var(--text-muted); margin-bottom: 2px; font-weight: 600;">Preset Scenarios:</div>
                        <div class="sim-btn-group" style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 4px;">
                            <button class="sim-btn active" style="padding: 4px 2px; font-size: 11px;" id="btn-preset-nom" onclick="setPresetErrors(1.8, -1.2, -0.6, 0.0, this)">Nominal ABC</button>
                            <button class="sim-btn" style="padding: 4px 2px; font-size: 11px;" id="btn-preset-zsc" onclick="setPresetErrors(1.5, 1.2, 0.9, 1.2, this)">ZSC Spike</button>
                            <button class="sim-btn" style="padding: 4px 2px; font-size: 11px;" id="btn-preset-asym" onclick="setPresetErrors(-2.8, 1.4, 1.4, 0.3, this)">Asymmetry</button>
                            <button class="sim-btn" style="padding: 4px 2px; font-size: 11px;" id="btn-preset-itsc" onclick="setPresetErrors(2.6, -0.5, -2.1, 0.8, this)">ITSC Short</button>
                        </div>
                    </div>

                    <!-- Priority Decoder Output -->
                    <div style="border-top: 1px solid var(--border-color); padding-top: 3px; margin-top: 1px;">
                        <div style="font-size: 10.5px; color: var(--text-muted); margin-bottom: 2px; font-weight: 600;">Error Priority Hierarchy:</div>
                        <div class="priority-badge-row" style="gap: 5px;">
                            <div class="p-badge p-prime" style="padding: 3px 6px;">
                                <span style="font-size: 8.5px; opacity: 0.85;">🥇 Primary</span>
                                <span id="badge-prime-phase" style="font-weight:700; font-size:11.5px;">Phase A</span>
                                <span id="badge-prime-val" class="metric" style="font-size:11px;">+1.80 A</span>
                            </div>
                            <div class="p-badge p-sec" style="padding: 3px 6px;">
                                <span style="font-size: 8.5px; opacity: 0.85;">🥈 Secondary</span>
                                <span id="badge-sec-phase" style="font-weight:700; font-size:11.5px;">Phase B</span>
                                <span id="badge-sec-val" class="metric" style="font-size:11px;">-1.20 A</span>
                            </div>
                            <div class="p-badge p-minor" style="padding: 3px 6px;">
                                <span style="font-size: 8.5px; opacity: 0.85;">🥉 Minor</span>
                                <span id="badge-minor-phase" style="font-weight:700; font-size:11.5px;">Phase C</span>
                                <span id="badge-minor-val" class="metric" style="font-size:11px;">-0.60 A</span>
                            </div>
                        </div>
                    </div>

                    <!-- Redesigned Crystal-Clear LUT Match & Action Box (Full 96-LUT Integrated) -->
                    <div class="lut-match-box" id="lut-decision-box" style="padding: 7px 9px; gap: 4px;">
                        <div class="lut-step-row">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span class="lut-step-title" style="font-size: 11px;">📋 96-State Priority LUT Decision:</span>
                                <span id="lut-row-num" class="lut-mode-badge dm-badge" style="font-size: 10px; padding: 2px 6px;">⚡ Differential-Mode Priority</span>
                            </div>
                        </div>
                        
                        <!-- Real-time 7-Bit Address Signature -->
                        <div class="lut-signature-bar">
                            <span class="sig-label">7-Bit Signature [EPO|ESC|EMP]:</span>
                            <span class="sig-bits" id="lut-7bits">1 1 0 &nbsp;|&nbsp; 1 0 0 &nbsp;|&nbsp; 1</span>
                            <span class="sig-idx" id="lut-idx-badge">Idx=105 • Row #88</span>
                        </div>

                        <div class="lut-vector-grid" style="padding: 4px 7px; gap: 4px;">
                            <div class="vector-chip">
                                <span class="v-label" style="font-size: 8.5px;">Selected Vector (L1 L2 L3 L4):</span>
                                <span id="lut-vector-code" class="v-code" style="font-size: 12px;">[1 0 1 1] (Vector 11)</span>
                            </div>
                            <div class="vector-chip">
                                <span class="v-label" style="font-size: 8.5px;">Physical Current Action:</span>
                                <span id="lut-action-desc" class="v-action" style="font-size: 11px;">+<i>i</i><sub>a</sub>, &minus;<i>i</i><sub>b</sub></span>
                            </div>
                        </div>

                        <div class="lut-comparison-row" style="padding-top: 3px;">
                            <div class="comp-label" style="font-size: 9px;">⚖️ OEPC Superiority over Conventional TDM:</div>
                            <div id="tdm-compare-note" class="comp-text" style="font-size: 10px; line-height: 1.3;">
                                Conventional TDM corrects only 1 phase per cycle and freezes the others. <strong>OEPC</strong> selects an optimal switching state executing <strong>simultaneous 2-phase correction</strong>, eliminating delays and ripple!
                            </div>
                        </div>

                        <button class="btn-lut-modal" id="btn-open-lut-modal" onclick="openLutModal()">
                            📊 Open Full 96-State LUT with Real-Time Row Tracker
                        </button>
                    </div>
                </div>

                <!-- Right: JSXGraph Space Vector Plane -->
                <div class="sim-display-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px;">
                        <div class="card-title" style="margin: 0; font-size: 15px;">
                            🧭 Space Vector Plane <bdi class="math-term">&alpha;&minus;&beta;</bdi> & Hexagon • <span style="color: var(--accent-cyan); font-weight: 500;">Dragging Error <bdi class="math-term"><b>&epsilon;</b></bdi> updates in real time</span>
                        </div>
                        <!-- Clear Visual Legend -->
                        <div class="jxg-legend">
                            <div class="jxg-legend-item">
                                <span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:#ff4757; box-shadow:0 0 6px #ff4757;"></span>
                                <span style="color:#ff6b6b; font-weight:600;">Current Error <bdi class="math-term"><b>&epsilon;</b></bdi></span>
                            </div>
                            <div class="jxg-legend-item">
                                <span style="display:inline-block; width:14px; height:3px; background:#00d2ff; box-shadow:0 0 6px #00d2ff;"></span>
                                <span style="color:#00d2ff; font-weight:600;">OEPC Voltage</span>
                            </div>
                            <div class="jxg-legend-item">
                                <span style="display:inline-block; width:14px; height:2px; border-top:2px dashed #f6d365;"></span>
                                <span style="color:#f6d365; font-weight:600;">TDM Voltage</span>
                            </div>
                        </div>
                    </div>

                    <div class="sim-canvas-box" style="height: 330px;">
                        <div id="oepc-jxg-board" class="jxgbox"></div>
                    </div>

                    <!-- Live Telemetry Bar with clean HTML Math typography -->
                    <div class="telemetry-bar">
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">Error Magnitude <bdi class="math-term">|<b>&epsilon;</b><sub>&alpha;&beta;</sub>|</bdi></span>
                            <span class="telemetry-val" id="tel-err-mag">2.16 A</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">Error Angle <bdi class="math-term">&theta;<sub>&epsilon;</sub></bdi></span>
                            <span class="telemetry-val" id="tel-err-ang">-28.4°</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">Applied Zero-Sequence <bdi class="math-term"><i>v</i><sub>0</sub></bdi></span>
                            <span class="telemetry-val" id="tel-v0">-0.0 V</span>
                        </div>
                        <div class="telemetry-chip">
                            <span class="telemetry-lbl">Tracking Speed Gain vs TDM</span>
                            <span class="telemetry-val" style="color:#00ff88;" id="tel-gain">+48% Faster</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 6: Typhoon C-HIL Experimental Platform -->
        <div class="slide">
            <div class="slide-category">Validation & Real-Time HIL</div>
            <div class="slide-title">Typhoon Controller-Hardware-In-the-Loop (C-HIL) Setup</div>
            <div class="slide-content-grid">
                <div>
                    <div class="card" style="margin-bottom: 18px;">
                        <div class="card-title">C-HIL Real-Time Emulation Architecture</div>
                        <ul class="list-styled">
                            <li><strong>Typhoon HIL402/HIL404:</strong> Real-time hardware emulation of the Series-End PMSM and power electronics at 1 MHz sample rate.</li>
                            <li><strong>Physical DSP Controller:</strong> Texas Instruments TMS320F28335 / TMS320F28379D executing the compiled OEPC algorithm in real time.</li>
                            <li><strong>Ultra-Low Latency:</strong> Current loop execution time &lt; 1.75 µs on standard 150 MHz core.</li>
                        </ul>
                    </div>
                    <div class="card card-highlight">
                        <div class="card-title">🏆 Lead Hardware Setup by Maxim Radkin</div>
                        <p style="font-size: 14px; line-height: 1.5;">
                            Maxim Radkin designed, built, and calibrated the complete experimental hardware setup, interfacing the physical DSP controller, GaN power converters, and Typhoon HIL interfaces, directly enabling the experimental milestones of this research.
                        </p>
                    </div>
                </div>

                <div class="fig-box">
                    <img src="presentation_assets/fig4_experimental_setups_chil_prototype.jpg" alt="C-HIL and Hardware Prototype Setup">
                    <div class="fig-caption">Fig. 4: (a) Typhoon C-HIL real-time validation platform; (b) Custom GaN-based Series-End VSI laboratory prototype.</div>
                </div>
            </div>
        </div>

        <!-- SLIDE 7: C-HIL Real-Time PMSM Dynamic Results -->
        <div class="slide">
            <div class="slide-category">C-HIL Experimental Results</div>
            <div class="slide-title">Real-Time Motor Drive Dynamic Response under C-HIL</div>
            <div class="slide-content-grid">
                <div class="fig-box">
                    <img src="presentation_assets/fig12_chil_realtime_pmsm_results.jpg" alt="C-HIL Real-Time PMSM Results">
                    <div class="fig-caption">Fig. 12: Real-time C-HIL experimental results: (a) Speed and torque response under sequential dynamic steps; (b) 3-phase currents and suppressed ZSC.</div>
                </div>

                <div>
                    <div class="card" style="margin-bottom: 18px;">
                        <div class="card-title">Dynamic Performance Verification</div>
                        <ul class="list-styled">
                            <li><strong>Speed Transitions:</strong> Smooth acceleration from 0 to 1500 RPM with rapid settling time (&lt;50 ms).</li>
                            <li><strong>Load Torque Steps:</strong> Abrupt step from 5 Nm to 45 Nm rejected with minimal speed dip.</li>
                            <li><strong>Torque Ripple:</strong> Maintained within $\pm 0.5\text{ Nm}$ under full load conditions.</li>
                        </ul>
                    </div>
                    <div class="card">
                        <div class="card-title">Complete ZSC Suppression in Real Time</div>
                        <ul class="list-styled">
                            <li><strong>$i_0$ Clamping:</strong> Peak-to-peak ZSC ripple held below 0.42 A during heavy transients.</li>
                            <li><strong>Waveform Fidelity:</strong> Clean sinusoidal phase currents without distortion across all 4 quadrants.</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 8: Physical Laboratory Prototype & Asymmetric Load Test -->
        
        <!-- SLIDE: Dynamic PMSM Simulation Lab (Real-Time Oscilloscope) -->
        <!-- SLIDE: Dynamic PMSM Simulation Lab (Real-Time Oscilloscope) -->
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
        </div>

        <!-- SLIDE 11: LIVE SWITCHING & ERROR CORRECTION DEMO -->
        <!-- SLIDE 10: LIVE SWITCHING & ERROR CORRECTION DEMO -->
        <div class="slide" id="slide-switching-error-demo">
            <div id="demo-surge-banner" class="demo-surge-banner" style="opacity:0;">
                ⚠️ Sudden Error Surge Injected! OEPC immediately identifies max phase and applies corrective vector!
            </div>

            <h2>⚡ Real-Time Switching Dynamics & Closed-Loop Error Correction (OEPC Pipeline)</h2>
            <h3 style="color:var(--text-muted); font-size:0.92rem; margin-bottom:4px;">
                Current Sampling &larr; Error Priority Sorting &larr; 96-LUT Optimal Lookup &larr; 4-Leg Gate Switching (<span class="math-term"><i>S</i><sub>a</sub>, <i>S</i><sub>b</sub>, <i>S</i><sub>c</sub>, <i>S</i><sub>n</sub></span>)
            </h3>

            <div class="slide11-grid">
                <!-- PANEL 1: OSCILLOSCOPE & ERROR MONITOR -->
                <div class="slide11-card">
                    <div class="slide11-card-title">
                        <span>🌊</span> Current Sampling & Instantaneous Errors (<span class="math-term"><i>i</i><sub>x</sub></span> ו-<span class="math-term"><i>e</i><sub>x</sub></span>)
                    </div>
                    <canvas id="demo-osc-canvas" style="width:100%; height:190px; background:#060a12; border-radius:6px; display:block;"></canvas>

                    <div style="margin-top:4px;">
                        <div class="demo-bar-row">
                            <span style="color:#00d2ff; font-weight:700;">Phase A:</span>
                            <div class="demo-bar-track"><div id="demo-bar-ea" class="demo-bar-fill fill-a"></div></div>
                            <span id="demo-val-ea" style="color:#00d2ff;">+0.00 A</span>
                        </div>
                        <div class="demo-bar-row">
                            <span style="color:#f6d365; font-weight:700;">Phase B:</span>
                            <div class="demo-bar-track"><div id="demo-bar-eb" class="demo-bar-fill fill-b"></div></div>
                            <span id="demo-val-eb" style="color:#f6d365;">+0.00 A</span>
                        </div>
                        <div class="demo-bar-row">
                            <span style="color:#ff6b81; font-weight:700;">Phase C:</span>
                            <div class="demo-bar-track"><div id="demo-bar-ec" class="demo-bar-fill fill-c"></div></div>
                            <span id="demo-val-ec" style="color:#ff6b81;">+0.00 A</span>
                        </div>
                        <div class="demo-bar-row">
                            <span style="color:#00ff88; font-weight:700;">Zero-Sequence (i₀):</span>
                            <div class="demo-bar-track"><div id="demo-bar-izsc" class="demo-bar-fill fill-zsc"></div></div>
                            <span id="demo-val-izsc" style="color:#00ff88;">+0.00 A</span>
                        </div>
                    </div>
                </div>

                <!-- PANEL 2: OEPC 96-LUT DECISION CORE & LIVE ELECTRONIC CIRCUIT SIMULATION -->
                <div class="slide11-card">
                    <div class="slide11-card-title" style="justify-content:space-between; margin-bottom:4px;">
                        <span><span>🔌</span> Series-End VSI & Open-End Windings (Fig. 2)</span>
                        <div style="display:flex; gap:4px;">
                            <button id="btn-tab-circuit" class="demo-btn active-tab" onclick="setPanel2Tab('circuit')" style="padding:2px 7px; font-size:0.72rem; background:rgba(0,210,255,0.25); border-color:#00d2ff; color:#fff;">Live Circuit</button>
                            <button id="btn-tab-matrix" class="demo-btn" onclick="setPanel2Tab('matrix')" style="padding:2px 7px; font-size:0.72rem; opacity:0.65;">Matrix</button>
                        </div>
                    </div>

                    <!-- Compact Decision Core HUD -->
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2px;">
                        <div style="display:flex; align-items:center; gap:5px;">
                            <span style="font-size:0.75rem; color:var(--text-muted);">Priority:</span>
                            <div id="demo-badge-order" class="demo-order-tag" style="font-size:0.85rem; padding:0 6px;">CBA</div>
                        </div>
                        <div style="display:flex; align-items:center; gap:5px;">
                            <span style="font-size:0.75rem; color:var(--text-muted);">Vector:</span>
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
                        <div style="font-size:0.68rem; color:var(--text-muted); text-align:center; margin-top:2px; font-weight:500;">Series Windings between Inverter Legs L1-L4 (Open-End, No Star/Delta)</div>
                        <div style="display:flex; justify-content:space-between; font-size:0.70rem; font-family:monospace; background:rgba(0,0,0,0.45); padding:2px 8px; border-radius:5px; border:1px solid rgba(255,255,255,0.08); margin-top:3px;">
                            <span id="circuit-hud-van" style="color:#00d2ff;">v_an: +Vdc</span>
                            <span id="circuit-hud-vbn" style="color:#f6d365;">v_bn: 0V</span>
                            <span id="circuit-hud-vcn" style="color:#ff6b81;">v_cn: -Vdc</span>
                            <span id="circuit-hud-izsc" style="color:#00ff88;">i_zsc: 0.01A</span>
                        </div>
                    </div>

                    <!-- VIEW 2: 8-TRANSISTOR MATRIX (Tab Selectable) -->
                    <div id="panel2-view-matrix" style="display:none;">
                        <div class="transistor-matrix-card">
                        <div class="matrix-title">
                            🔌 8-Transistor Leg States (Fig. 2):
                        </div>
                        <div class="matrix-grid">
                            <div class="matrix-leg" id="leg-box-a">
                                <div class="leg-header" style="color:#00d2ff;">Leg A</div>
                                <div class="transistor-row">
                                    <span style="color:#00d2ff;">S<sub>ah</sub>:</span>
                                    <span class="t-badge badge-on" id="badge-sah">ON (1)</span>
                                </div>
                                <div class="transistor-row">
                                    <span style="color:#a0aec0;">S<sub>al</sub>:</span>
                                    <span class="t-badge badge-off" id="badge-sal">OFF (0)</span>
                                </div>
                            </div>
                            <div class="matrix-leg" id="leg-box-b">
                                <div class="leg-header" style="color:#f6d365;">Leg B</div>
                                <div class="transistor-row">
                                    <span style="color:#f6d365;">S<sub>bh</sub>:</span>
                                    <span class="t-badge badge-off" id="badge-sbh">OFF (0)</span>
                                </div>
                                <div class="transistor-row">
                                    <span style="color:#a0aec0;">S<sub>bl</sub>:</span>
                                    <span class="t-badge badge-on" id="badge-sbl">ON (1)</span>
                                </div>
                            </div>
                            <div class="matrix-leg" id="leg-box-c">
                                <div class="leg-header" style="color:#ff6b81;">Leg C</div>
                                <div class="transistor-row">
                                    <span style="color:#ff6b81;">S<sub>ch</sub>:</span>
                                    <span class="t-badge badge-off" id="badge-sch">OFF (0)</span>
                                </div>
                                <div class="transistor-row">
                                    <span style="color:#a0aec0;">S<sub>cl</sub>:</span>
                                    <span class="t-badge badge-on" id="badge-scl">ON (1)</span>
                                </div>
                            </div>
                            <div class="matrix-leg leg-neutral" id="leg-box-n">
                                <div class="leg-header" style="color:#00ff88;">Leg N</div>
                                <div class="transistor-row">
                                    <span style="color:#00ff88;">S<sub>nh</sub>:</span>
                                    <span class="t-badge badge-on" id="badge-snh">ON (1)</span>
                                </div>
                                <div class="transistor-row">
                                    <span style="color:#a0aec0;">S<sub>nl</sub>:</span>
                                    <span class="t-badge badge-off" id="badge-snl">OFF (0)</span>
                                </div>
                            </div>
                        </div>
                        <div class="matrix-footnote">
                            * כל רגל: זוג מתגים משלימים (S<sub>h</sub> ו-S<sub>l</sub>) עם Dead-Time למניעת קצר Shoot-Through.
                        </div>
                    </div>
                    </div>

                    <div class="demo-impact-hero" style="margin-top:2px; font-size:0.75rem; padding:2px 4px;">
                        Physical Impact: <span id="demo-active-impact" class="demo-val-readout" style="color:#f6d365; font-weight:700;">-i_c, -i_0</span>
                        • Norm: <span id="demo-tel-norm" class="demo-val-readout" style="color:#00d2ff; font-weight:700;">0.10 A</span>
                    </div>
                </div>

                <!-- PANEL 3: GATE SWITCHING TRACES & ERROR CONVERGENCE -->
                <div class="slide11-card">
                    <div class="slide11-card-title">
                        <span>⚡</span> 4-Leg Gate Switching Traces (Fig. 2: Switch Pairs <span class="math-term"><i>S</i><sub>h</sub>, <i>S</i><sub>l</sub></span>)
                    </div>
                    <canvas id="demo-gate-canvas" style="width:100%; height:110px; background:#060a12; border-radius:6px; display:block; margin-bottom:6px;"></canvas>

                    <div class="slide11-card-title" style="margin-top:1px; font-size:0.85rem;">
                        <span>🎯</span> Error Convergence in <span class="math-term">&alpha;-&beta;</span> (Corrective Pull to Origin)
                    </div>
                    <canvas id="demo-error-orbit-canvas" style="width:100%; height:260px; background:#060a12; border-radius:6px; display:block;"></canvas>
                </div>
            </div>

                        <!-- CONTROLS BAR WITH MULTI-FAULT SUITE & SPEED CONTROL -->
            <div class="demo-controls-bar">
                <!-- Fault Injection Suite -->
                <div style="display:flex; align-items:center; gap:5px; flex-wrap:wrap;">
                    <span style="font-size:0.78rem; font-weight:700; color:var(--accent-gold); display:flex; align-items:center; gap:3px;">
                        <span>⚡</span> Fault Scenarios:
                    </span>
                    <button id="btn-fault-none" class="demo-btn fault-btn active-fault" onclick="setDemoFault('none')">🟢 Healthy</button>
                    <button id="btn-fault-surge" class="demo-btn fault-btn" onclick="setDemoFault('surge')">⚡ Error Surge</button>
                    <button id="btn-fault-asym" class="demo-btn fault-btn" onclick="setDemoFault('asym')">🔌 35% Asymmetry</button>
                    <button id="btn-fault-leg4" class="demo-btn fault-btn" onclick="setDemoFault('leg4')">⚠️ Leg 4 Fault</button>
                    <button id="btn-fault-load" class="demo-btn fault-btn" onclick="setDemoFault('load')">📈 Load Step 125%</button>
                </div>

                <!-- Playback & True Speed Slider -->
                <div style="display:flex; align-items:center; gap:10px;">
                    <div class="demo-btn-group">
                        <button id="btn-demo-play" class="demo-btn" onclick="toggleDemoPlay()">⏸ Pause</button>
                        <button class="demo-btn" onclick="stepDemoOnce()">⏯ Step</button>
                        <button class="demo-btn" onclick="resetDemo()" style="border-color:rgba(255,255,255,0.3);">🔄 Reset</button>
                    </div>

                    <!-- Trigger Scope Sync Mode Toggle -->
                    <button id="btn-demo-scope-mode" class="demo-btn" onclick="toggleDemoScopeMode()" style="background:rgba(0,255,136,0.15); border-color:#00ff88; color:#00ff88; font-size:0.78rem;" title="Trigger-locked stationary 2-cycle view or gentle slow roll">
                        📌 Trigger-Locked Scope
                    </button>

                    <div style="display:flex; align-items:center; gap:8px; background:rgba(0,0,0,0.45); padding:3px 10px; border-radius:6px; border:1px solid rgba(0,210,255,0.25);">
                        <span style="font-size:0.78rem; color:#cbd5e0; white-space:nowrap;">Speed:</span>
                        <input id="demo-speed-slider" type="range" min="0.1" max="1.5" step="0.1" value="0.5" oninput="updateDemoSpeed(this.value)" style="width:85px; cursor:pointer;">
                        <span id="demo-speed-val" style="color:#00d2ff; font-family:monospace; font-weight:700; font-size:0.8rem; min-width:35px;">0.5x</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 9: Experimental Differential Voltages -->
        <div class="slide">
            <div class="slide-category">Physical Hardware Validation</div>
            <div class="slide-title">Measured Differential Voltages & Adaptive Modulation</div>
            <div class="slide-content-grid">
                <div class="fig-box">
                    <img src="presentation_assets/fig8_experimental_differential_voltages.jpg" alt="Experimental Differential Voltages">
                    <div class="fig-caption">Fig. 8: Measured differential phase voltages ($v_a, v_c$) across SE-VSI legs 1–2 and 3–4.</div>
                </div>

                <div>
                    <div class="card" style="margin-bottom: 18px;">
                        <div class="card-title">Adaptive Duty-Cycle Distribution</div>
                        <ul class="list-styled">
                            <li><strong>Dynamic Duty-Cycle Synthesis:</strong> Demonstrates distinct switching patterns required across legs to counter asymmetric impedance.</li>
                            <li><strong>Full Bus Voltage Utilization:</strong> Achieves full DC voltage exploitation ($M_a = 1.0$) without entering overmodulation clipping.</li>
                        </ul>
                    </div>
                    <div class="card">
                        <div class="card-title">Variable Frequency Switching Benefits</div>
                        <ul class="list-styled">
                            <li><strong>Loss Reduction:</strong> Up to <strong>30% reduction in switching losses</strong> compared to conventional fixed-frequency CBPWM.</li>
                            <li><strong>EMI Spread Spectrum:</strong> Natural dispersion of switching frequency harmonics suppresses EMI peaks.</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 10: Comparison with CBPWM & 3D-SVM -->
        <div class="slide">
            <div class="slide-category">Benchmarking & Performance</div>
            <div class="slide-title">Comparative Analysis: OEPC vs. Conventional Schemes</div>
            <div class="slide-content-full">
                <table class="table-custom">
                    <thead>
                        <tr>
                            <th>Control Strategy</th>
                            <th>Platform & Clock</th>
                            <th>Execution Time</th>
                            <th>Relative Computational Burden</th>
                            <th>Switching Losses</th>
                            <th>Asymmetry Robustness</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="highlight-row">
                            <td><strong>Proposed OEPC</strong></td>
                            <td>TMS320F28335 (150 MHz)</td>
                            <td><strong>1.75 µs (0.85 µs on F28379D)</strong></td>
                            <td><strong>100% (Baseline - Lowest)</strong></td>
                            <td><strong>Lowest (~30% reduction)</strong></td>
                            <td><strong>Excellent (&plusmn;25% Verified)</strong></td>
                        </tr>
                        <tr>
                            <td>3-D Space Vector Modulation (3D-SVM)</td>
                            <td>dSPACE DS1202 (2.0 GHz)</td>
                            <td>0.43 µs (@ 2.0 GHz)</td>
                            <td>330% (3.3x heavier per cycle)</td>
                            <td>High (Fixed Frequency)</td>
                            <td>Moderate (Requires Tuning)</td>
                        </tr>
                        <tr>
                            <td>Carrier-Based PWM (CBPWM)</td>
                            <td>dSPACE DS1202 (2.0 GHz)</td>
                            <td>2.10 µs (@ 2.0 GHz)</td>
                            <td>1600% (16x heavier)</td>
                            <td>High (Continuous Switching)</td>
                            <td>Poor (Harmonic Spikes)</td>
                        </tr>
                        <tr>
                            <td>Virtual-Vector SVM ($V^3$-SVM)</td>
                            <td>dSPACE DS1202 (2.0 GHz)</td>
                            <td>2.50 µs (@ 2.0 GHz)</td>
                            <td>1900% (19x heavier)</td>
                            <td>Moderate</td>
                            <td>Moderate</td>
                        </tr>
                        <tr>
                            <td>Multi-Vector MPC (MV-MPCC)</td>
                            <td>dSPACE DS1202 (2.0 GHz)</td>
                            <td>&gt;20.0 µs (@ 2.0 GHz)</td>
                            <td>&gt;15000% (150x heavier)</td>
                            <td>Moderate</td>
                            <td>Highly Parameter-Sensitive</td>
                        </tr>
                    </tbody>
                </table>

                <div class="fig-box" style="margin-top: 15px;">
                    <img src="presentation_assets/fig11_steady_state_comparison_oepc_cbpwm.jpg" alt="Steady-State Comparison OEPC vs CBPWM" style="max-height: 200px;">
                    <div class="fig-caption">Fig. 11: Steady-state comparison: (a) Proposed OEPC ($THD = 1.84\%$, $ZSC = 0.42\text{ A}$); (b) CBPWM ($THD = 3.12\%$, $ZSC = 1.57\text{ A}$).</div>
                </div>
            </div>
        </div>

        <!-- SLIDE 11: Fault Tolerance - ITSC Short Circuits -->
        <div class="slide">
            <div class="slide-category">Machine Fault Tolerance</div>
            <div class="slide-title">Intrinsic Fault Robustness under Inter-Turn Short Circuits (ITSC)</div>
            <div class="slide-content-grid">
                <div class="fig-box">
                    <img src="presentation_assets/fig13_fault_tolerance_itsc_oepc_vs_cbpwm.jpg" alt="Fault Tolerance ITSC OEPC vs CBPWM">
                    <div class="fig-caption">Fig. 13: Dynamic response under 10% ITSC stator fault: (a) OEPC prevents runaway; (b) CBPWM causes catastrophic current divergence.</div>
                </div>

                <div>
                    <div class="card" style="margin-bottom: 18px;">
                        <div class="card-title">Passive Tolerance without Extra Sensors</div>
                        <ul class="list-styled">
                            <li><strong>Stator Fault Simulation:</strong> 10% inter-turn short-circuit (ITSC) initiated during steady-state operation.</li>
                            <li><strong>CBPWM Failure:</strong> Carrier-based PWM cannot constrain the fault current, leading to severe current runaway and destruction.</li>
                            <li><strong>OEPC Inherent Clamping:</strong> OEPC's instantaneous priority logic naturally clamps the fault currents, maintaining stable operation and preventing runaway!</li>
                        </ul>
                    </div>
                    <div class="card card-highlight">
                        <div class="card-title">🛡️ Thermal & Mechanical Protection</div>
                        <p style="font-size: 14px; line-height: 1.5;">
                            Provides critical limp-home capability for mission-critical electric vehicle (EV) and aerospace drivetrains without requiring complex fault-detection observers.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 12: Authorship & Research Milestone -->
        <div class="slide">
            <div class="slide-category">Research Contributions & Publication</div>
            <div class="slide-title">IEEE TIE Publication & Experimental Foundation</div>
            <div class="slide-content-grid">
                <div class="card card-highlight">
                    <div class="card-title">🌟 Acceptance in IEEE Transactions on Industrial Electronics</div>
                    <ul class="list-styled">
                        <li><strong>Decisive Factor:</strong> The comprehensive physical experimental verification and C-HIL validation were the cornerstone of acceptance in IEEE TIE (Top Tier Q1 Power Electronics Journal).</li>
                        <li><strong>Authorship Context:</strong> While Maxim Radkin was not formally listed on the initial submission due to IEEE initial-round author freeze policies, his work on experimental hardware interfacing, C-HIL integration, and laboratory testing served as the foundation for the published results.</li>
                    </ul>
                    <div class="hebrew-note" style="margin-top: 15px;">
                        המאמר היוקרתי ב-IEEE Transactions on Industrial Electronics התקבל תודות לתוצאות הניסוייות המעשיות ולסטאפ ה-HIL והחומרה שנבנה ונבדק ע"י מקסים רדקין.
                    </div>
                </div>

                <div class="card">
                    <div class="card-title">🔬 Laboratory Validation & Experimental Tasks</div>
                    <ul class="list-styled">
                        <li><strong>C-HIL Setup & Wiring:</strong> Interfacing the Texas Instruments TMS320 DSP with the Typhoon HIL emulator.</li>
                        <li><strong>GaN Inverter Assembly:</strong> Design, testing, and debugging of the 4-Leg Series-End VSI power stage.</li>
                        <li><strong>Physical Load Asymmetry Bench:</strong> Implementation and calibration of the $\pm 25\%$ variable inductor test rig.</li>
                        <li><strong>Data Acquisition:</strong> High-bandwidth 4-channel oscilloscope current/voltage capture and FFT harmonic analysis.</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- SLIDE 13: Next Phase - New PMSM Motor & Inverter Hardware -->
        <div class="slide">
            <div class="slide-category">Ongoing Research & Next Steps</div>
            <div class="slide-title">Hardware Progression: Newly Acquired PMSM & Custom Inverters</div>
            <div class="slide-content-grid">
                <div>
                    <div class="card" style="margin-bottom: 18px;">
                        <div class="card-title">Newly Purchased Industrial PMSM Motor</div>
                        <ul class="list-styled">
                            <li><strong>SEW / OEMER Industrial PMSM:</strong> High-performance open-winding servomotor with integrated SICK SFM60 Hiperface high-resolution optical encoder.</li>
                            <li><strong>Mechanical Load Bench:</strong> Custom-designed machine bed (MV1004) with inline torque sensor (Sensata / HBM T210) and dyno coupling.</li>
                        </ul>
                    </div>
                    <div class="card card-highlight">
                        <div class="card-title">Custom-Built Power Converters</div>
                        <ul class="list-styled">
                            <li><strong>In-House Built Inverters:</strong> Complete fabrication of dedicated 4-leg Series-End power stages for full-scale dyno testing.</li>
                            <li><strong>Experimental Continuity:</strong> Conducting comprehensive physical drive testing with the new motor, sensor integration, and field-weakening validation.</li>
                        </ul>
                    </div>
                </div>

                <div class="fig-box">
                    <img src="presentation_assets/pmsm_motor_photo.jpeg" alt="Purchased PMSM Motor" style="max-height: 360px;">
                    <div class="fig-caption">Newly acquired open-winding PMSM servomotor prepared for next-stage laboratory dyno testing.</div>
                </div>
            </div>
        </div>

        <!-- SLIDE 14: Mechanical Integration & CAD Assembly -->
        <div class="slide">
            <div class="slide-category">Mechanical & Structural Setup</div>
            <div class="slide-title">SolidWorks CAD Mechanical Assembly & Sensor Integration</div>
            <div class="slide-content-grid">
                <div class="fig-box">
                    <img src="presentation_assets/hardware_setup_photo.jpg" alt="Mechanical Test Stand Photo">
                    <div class="fig-caption">Laboratory mechanical test stand with machine bed, torque sensor, and PMSM motor mount.</div>
                </div>

                <div>
                    <div class="card" style="margin-bottom: 18px;">
                        <div class="card-title">Mechanical Engineering Work Completed</div>
                        <ul class="list-styled">
                            <li><strong>SolidWorks 3D Modeling:</strong> Full CAD design of the motor test bench (<code>PMSM_Load_Stend.SLDASM</code>) and machine bed adapters.</li>
                            <li><strong>T210 Torque Sensor Mount:</strong> Precision alignment flange for dynamic shaft torque and efficiency measurements.</li>
                            <li><strong>SICK SFM60 Hiperface RS485 Interface:</strong> High-speed serial protocol decoding on DSP for rotor flux angle estimation.</li>
                        </ul>
                    </div>
                    <div class="card">
                        <div class="card-title">🔬 Complete Experimental Ecosystem</div>
                        <p style="font-size: 14px; line-height: 1.5;">
                            Combines electromagnetic modeling, fast C-HIL real-time simulation, GaN power electronics, precision mechanics, and digital serial encoder communications.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 15: Comprehensive Summary -->
        <div class="slide">
            <div class="slide-category">Summary & Conclusions</div>
            <div class="slide-title">Summary of Key Achievements & Technological Impact</div>
            <div class="slide-content-grid">
                <div class="card card-highlight">
                    <div class="card-title">💎 Technical Breakthroughs</div>
                    <ul class="list-styled">
                        <li><strong>Sub-Microsecond Execution:</strong> Ultra-fast logic-based LUT ($&lt;1.75\text{ µs}$) on low-cost single-core DSPs.</li>
                        <li><strong>Complete ZSC Suppression:</strong> Eliminates zero-sequence circulating current without bulky passive filters or isolation transformers.</li>
                        <li><strong>Full DC-Bus Utilization:</strong> Delivers $M_a = 1.0$ equivalent to 6-leg dual-inverters with 33% fewer switches.</li>
                        <li><strong>Superior Efficiency:</strong> ~30% reduction in switching losses via adaptive switching frequency.</li>
                        <li><strong>Inherent Fault Tolerance:</strong> Resilient against $\pm 25\%$ load unbalance and internal stator ITSC short circuits.</li>
                    </ul>
                </div>

                <div class="card">
                    <div class="card-title">📊 Validation & Next Horizons</div>
                    <ul class="list-styled">
                        <li><strong>Fully Verified:</strong> Validated across digital simulations, Typhoon HIL real-time emulation, and physical GaN laboratory prototypes.</li>
                        <li><strong>IEEE TIE Publication:</strong> Top-tier academic recognition grounded in solid experimental data.</li>
                        <li><strong>Active Continuation:</strong> Hardware progression with new industrial PMSM, custom-built inverters, and high-precision dyno testing.</li>
                    </ul>
                    <div class="hebrew-note" style="margin-top: 15px;">
                        המחקר ביסס את שיטת ה-OEPC כחלופה מעשית, יעילה ופורצת דרך עבור מערכות הנעה תעשייתיות ורכבים חשמליים.
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 16: Q&A Slide -->
        <div class="slide">
            <div class="title-slide">
                <span class="tag-pill" style="margin-bottom: 20px;">Open for Discussion</span>
                <h1 style="font-size: 48px;">Thank You!</h1>
                <h2 style="font-size: 26px; margin-bottom: 30px;">תודה רבה על ההקשבה - שאלות ותשובות</h2>
                
                <div class="card" style="max-width: 600px; padding: 25px;">
                    <div style="font-size: 16px; font-weight: 600; color: var(--accent-cyan); margin-bottom: 8px;">
                        Department of Electrical & Electronic Engineering
                    </div>
                    <div style="font-size: 15px; color: #ffffff; margin-bottom: 12px;">
                        Shamoon College of Engineering (SCE)
                    </div>
                    <div style="font-family: 'Fira Code', monospace; font-size: 14px; color: var(--text-secondary);">
                        Maxim Radkin | Dr. Eli Gad Barbie | Prof. Dmitry Baimel
                    </div>
                </div>
            </div>
        </div>

    </div>

    <!-- Navigation Footer -->
    <div class="pres-footer">
        <div class="keyboard-hint">
            ⌨️ Use <kbd>←</kbd> <kbd>→</kbd> keys or buttons to navigate | Fullscreen <kbd>F</kbd></div>
        <div class="nav-controls">
            <button class="btn-nav" id="footer-fullscreen-btn" onclick="toggleFullscreen()" title="Fullscreen (F)" style="background: rgba(0, 210, 255, 0.12); border-color: rgba(0, 210, 255, 0.35); color: var(--accent-cyan);">
                ⛶ Fullscreen
            </button>
            <button class="btn-nav" id="prev-btn" onclick="prevSlide()" disabled>
                ◀ Previous
            </button>
            <button class="btn-nav" id="next-btn" onclick="nextSlide()">
                Next ▶
            </button>
        </div>
    </div>
</div>

<script>
    let currentSlideIdx = 0;
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    const currentSlideEl = document.getElementById('current-slide');
    const totalSlidesEl = document.getElementById('total-slides');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');

    totalSlidesEl.textContent = totalSlides;

    function updateSlide(newIdx) {
        if (newIdx < 0 || newIdx >= totalSlides) return;
        
        slides[currentSlideIdx].classList.remove('active');
        currentSlideIdx = newIdx;
        slides[currentSlideIdx].classList.add('active');

        currentSlideEl.textContent = currentSlideIdx + 1;
        prevBtn.disabled = (currentSlideIdx === 0);
        nextBtn.disabled = (currentSlideIdx === totalSlides - 1);

        if (window.MathJax && window.MathJax.typesetPromise) {
            window.MathJax.typesetPromise([slides[currentSlideIdx]]).catch(function (err) {});
        }
    }

    function nextSlide() {
        if (currentSlideIdx < totalSlides - 1) {
            updateSlide(currentSlideIdx + 1);
        }
    }

    function prevSlide() {
        if (currentSlideIdx > 0) {
            updateSlide(currentSlideIdx - 1);
        }
    }

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'f' || e.key === 'F') {
            toggleFullscreen();
            return;
        }

        if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
            nextSlide();
        } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
            prevSlide();
        } else if (e.key === 'Home') {
            updateSlide(0);
        } else if (e.key === 'End') {
            updateSlide(totalSlides - 1);
        }
    });


    // Fullscreen Navigation & Toggle
    function toggleFullscreen() {
        if (!document.fullscreenElement && !document.webkitFullscreenElement) {
            if (document.documentElement.requestFullscreen) {
                document.documentElement.requestFullscreen().catch(() => {});
            } else if (document.documentElement.webkitRequestFullscreen) {
                document.documentElement.webkitRequestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen().catch(() => {});
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            }
        }
    }

    function updateFullscreenUI() {
        const isFull = !!(document.fullscreenElement || document.webkitFullscreenElement);
        const isHe = document.documentElement.lang === 'he' || document.querySelector('html[dir="rtl"]') !== null;
        
        const headerBtn = document.getElementById('fullscreen-btn');
        const footerBtn = document.getElementById('footer-fullscreen-btn');
        const iconEl = document.getElementById('fullscreen-icon');
        const textEl = document.getElementById('fullscreen-text');

        if (iconEl) iconEl.textContent = isFull ? '🗗' : '⛶';
        if (textEl) textEl.textContent = isFull ? (isHe ? 'צא ממסך מלא' : 'Exit Fullscreen') : (isHe ? 'מסך מלא' : 'Fullscreen');
        if (footerBtn) {
            footerBtn.innerHTML = (isFull ? '🗗 ' : '⛶ ') + (isFull ? (isHe ? 'צא ממסך מלא' : 'Exit Fullscreen') : (isHe ? 'מסך מלא' : 'Fullscreen'));
        }
    }

    document.addEventListener('fullscreenchange', updateFullscreenUI);
    document.addEventListener('webkitfullscreenchange', updateFullscreenUI);

</script>


<script>
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

// Hook into presentation slide change to initialize JSXGraph board cleanly
const origUpdateSlide = updateSlide;
updateSlide = function(newIdx) {
    origUpdateSlide(newIdx);
    setTimeout(() => {
        if (slides[currentSlideIdx] && slides[currentSlideIdx].id === 'slide-oepc-principle') {
            initJSXGraphBoard();
        }
    }, 150);
};

// Also trigger on load if first
window.addEventListener('load', () => {
    setTimeout(initJSXGraphBoard, 300);
});

// =====================================================================
// --- 2. DYNAMIC PMSM & OSCILLOSCOPE SIMULATOR (SLIDE 10) ---
// =====================================================================

let simRunning = true;
let simAlgo = 'OEPC'; // 'OEPC', 'TDM', 'PWM'
let simScopeMode = 'trig'; // 'trig' = stationary triggered, 'slow' = gentle rolling
let simAnimId = null;

let simAsym = 25; // % asymmetry (0 to 30)
let simIref = 5.0; // A
let simSpeed = 1500; // RPM
let simTime = 0;

// Algorithm selection
function setSimAlgo(algo, btn) {
    simAlgo = algo;
    document.querySelectorAll('#slide-dynamic-sim .sim-btn-group .sim-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');

    // Update explanation card
    const titleEl = document.getElementById('algo-explain-title');
    const descEl = document.getElementById('algo-explain-desc');
    const oscTagEl = document.getElementById('osc-status-tag');
    const orbTagEl = document.getElementById('orbit-status-tag');

    const telIzsc = document.getElementById('tel-sim-izsc');
    const telThd = document.getElementById('tel-sim-thd');
    const telErr = document.getElementById('tel-sim-err');
    const telLoss = document.getElementById('tel-sim-loss');

    const isHe = document.documentElement.lang === 'he' || document.querySelector('html[dir="rtl"]') !== null;

    if (algo === 'OEPC') {
        if (titleEl) {
            titleEl.textContent = isHe ? '🌟 בקרת OEPC (מוצעת): דיכוי ZSC אקטיבי ואיפוס הריפל' : '🌟 Proposed OEPC: Active ZSC Suppression & Zero Differential Ripple';
            titleEl.style.color = '#00d2ff';
        }
        if (descEl) {
            descEl.innerHTML = isHe 
                ? 'האלגוריתם מנטר את חריגת ה-ZSC הנגרמת מאי-סימטריה של ' + simAsym + '%, ומפעיל את הענף הרביעי עם מתח נגדי מהיר. התוצאה: זרם סדרה אפס משוטח לאפס (<span class="math-term"><i>i</i><sub>zsc</sub> &lt; 0.04 A</span>), הזרמים סינוסיים טהורים, ומסלול ה-&alpha;-&beta; מעגלי לחלוטין ללא פעימות מומנט.'
                : 'The algorithm monitors zero-sequence current anomalies caused by ' + simAsym + '% winding asymmetry and drives the 4th inverter leg with counter-voltage. Result: ZSC is clamped below 0.04 A, currents are pure sinusoids, and the &alpha;-&beta; hodograph is a perfect circle with zero torque ripple.';
        }
        if (oscTagEl) {
            oscTagEl.textContent = simScopeMode === 'trig' ? 'TRIG LOCKED • 2 CYCLES' : 'SLOW ROLL 0.2X • CLEAN';
            oscTagEl.style.color = '#00ff88';
        }
        if (orbTagEl) {
            orbTagEl.textContent = 'HODOGRAPH: PURE CIRCLE';
            orbTagEl.style.color = '#00d2ff';
        }
        if (telIzsc) { telIzsc.textContent = '0.04 A'; telIzsc.style.color = '#00ff88'; }
        if (telThd) { telThd.textContent = '2.1%'; telThd.style.color = '#00d2ff'; }
        if (telErr) { telErr.textContent = '0.09 A'; telErr.style.color = '#ffffff'; }
        if (telLoss) { telLoss.textContent = '-28% vs PWM'; telLoss.style.color = '#f6d365'; }
    } else if (algo === 'TDM') {
        if (titleEl) {
            titleEl.textContent = isHe ? '⏱️ שיטת TDM קלאסית: שגיאות פאזה וזרם סדרה אפס משמעותיים' : '⏱️ Conventional TDM: High ZSC Circulation & Phase Delay';
            titleEl.style.color = '#f6d365';
        }
        if (descEl) {
            descEl.innerHTML = isHe 
                ? 'שיטת ה-TDM מתקנת פאזה בודדת בלבד בכל מחזור בקרה ומקפיאה את שאר הפאזות. אי-הסימטריה מייצרת זרם סדרה אפס מסוכן (<span class="math-term"><i>i</i><sub>zsc</sub> &approx; ' + (0.55 * (simAsym/25)).toFixed(2) + ' A</span>), עיוותי צורה בגלי הזרם ומסלול &alpha;-&beta; אליפטי מפותל.'
                : 'Conventional TDM corrects only 1 phase per cycle and freezes the others. Asymmetry generates severe zero-sequence current ripple (~' + (0.55 * (simAsym/25)).toFixed(2) + ' A), noticeable waveform distortion, and an eccentric elliptic orbit.';
        }
        if (oscTagEl) {
            oscTagEl.textContent = 'HIGH ZSC RIPPLE (0.65A)';
            oscTagEl.style.color = '#f6d365';
        }
        if (orbTagEl) {
            orbTagEl.textContent = 'HODOGRAPH: PULSATING ELLIPSE';
            orbTagEl.style.color = '#f6d365';
        }
        if (telIzsc) { telIzsc.textContent = (0.55 * (simAsym/25)).toFixed(2) + ' A'; telIzsc.style.color = '#f6d365'; }
        if (telThd) { telThd.textContent = '8.4%'; telThd.style.color = '#f6d365'; }
        if (telErr) { telErr.textContent = '0.42 A'; telErr.style.color = '#ffffff'; }
        if (telLoss) { telLoss.textContent = '-15% vs PWM'; telLoss.style.color = '#f6d365'; }
    } else if (algo === 'PWM') {
        if (titleEl) {
            titleEl.textContent = isHe ? '⚠️ אפנון PWM קונבנציונלי: עיוות הרמוני חמור והפסדי הספק' : '⚠️ Conventional PWM: Severe Distortion & High Switching Losses';
            titleEl.style.color = '#ff4757';
        }
        if (descEl) {
            descEl.innerHTML = isHe 
                ? 'בהיעדר בקרת ענף רביעי ייעודית, אי-הסימטריה של ' + simAsym + '% מפתחת לולאת זרם סדרה אפס עצומה (<span class="math-term"><i>i</i><sub>zsc</sub> &approx; ' + (1.15 * (simAsym/25)).toFixed(2) + ' A</span>). הדבר גורם לחימום מסוכן של סלילי המנוע, פעימות מומנט קשות ועיוות כולל.'
                : 'Without dedicated 4th leg zero-sequence control, ' + simAsym + '% winding asymmetry causes massive zero-sequence circulating current (~' + (1.15 * (simAsym/25)).toFixed(2) + ' A), causing severe thermal stress and torque pulsations.';
        }
        if (oscTagEl) {
            oscTagEl.textContent = 'DANGEROUS ZSC LOOP (1.25A)';
            oscTagEl.style.color = '#ff4757';
        }
        if (orbTagEl) {
            orbTagEl.textContent = 'HODOGRAPH: SEVERELY DISTORTED';
            orbTagEl.style.color = '#ff4757';
        }
        if (telIzsc) { telIzsc.textContent = (1.15 * (simAsym/25)).toFixed(2) + ' A'; telIzsc.style.color = '#ff4757'; }
        if (telThd) { telThd.textContent = '12.8%'; telThd.style.color = '#ff4757'; }
        if (telErr) { telErr.textContent = '0.85 A'; telErr.style.color = '#ffffff'; }
        if (telLoss) { telLoss.textContent = 'Reference (0%)'; telLoss.style.color = '#a0aec0'; }
    }
}

function setScopeMode(mode, btn) {
    simScopeMode = mode;
    document.querySelectorAll('.mode-toggle-group .mode-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');

    const oscTagEl = document.getElementById('osc-status-tag');
    if (oscTagEl) {
        if (simAlgo === 'OEPC') {
            oscTagEl.textContent = mode === 'trig' ? 'TRIG LOCKED • 2 CYCLES' : 'SLOW ROLL 0.2X • CLEAN';
        }
    }
}

function updateSimParams() {
    const sAsym = document.getElementById('slider-sim-asym');
    const sI = document.getElementById('slider-sim-i');
    const sSpeed = document.getElementById('slider-sim-speed');

    if (sAsym) {
        simAsym = parseFloat(sAsym.value);
        document.getElementById('val-sim-asym').textContent = simAsym + '% ' + (simAsym === 25 ? '(ניסוי מאמר)' : '');
    }
    if (sI) {
        simIref = parseFloat(sI.value);
        document.getElementById('val-sim-i').textContent = simIref.toFixed(1) + ' A';
    }
    if (sSpeed) {
        simSpeed = parseFloat(sSpeed.value);
        document.getElementById('val-sim-speed').textContent = simSpeed + ' RPM';
    }

    // Refresh algorithm badge text
    setSimAlgo(simAlgo, null);
}

function toggleSimPlay() {
    simRunning = !simRunning;
    const btn = document.getElementById('btn-sim-play');
    const isHe = document.documentElement.lang === 'he' || document.querySelector('html[dir="rtl"]') !== null;
    if (btn) {
        btn.textContent = simRunning 
            ? (isHe ? '⏸ השהה אות' : '⏸ Pause Signal')
            : (isHe ? '▶ המשך אות' : '▶ Resume Signal');
        btn.style.background = simRunning ? 'rgba(0,210,255,0.18)' : 'rgba(0,255,136,0.25)';
    }
    if (simRunning) {
        if (!simAnimId) {
            simAnimId = requestAnimationFrame(renderSimulationLoop);
        }
    } else if (simAnimId) {
        cancelAnimationFrame(simAnimId);
        simAnimId = null;
    }
}

function resetSimTime() {
    simTime = 0;
}

// Main Render Loop for Oscilloscope and Lissajous Orbit
function renderSimulationLoop() {
    const oscCanvas = document.getElementById('osc-canvas');
    const orbitCanvas = document.getElementById('orbit-canvas');

    if (!oscCanvas || !orbitCanvas) return;

    // Check if slide 10 is active
    const slide10 = document.getElementById('slide-dynamic-sim');
    const isActive = slide10 && slide10.classList.contains('active');

    if (!isActive) {
        // Paused while not on slide 10 to save CPU
        simAnimId = null;
        return;
    }

    const dpr = window.devicePixelRatio || 1;

    // Size canvas to CSS container
    if (oscCanvas.width !== oscCanvas.clientWidth * dpr) {
        oscCanvas.width = oscCanvas.clientWidth * dpr;
        oscCanvas.height = oscCanvas.clientHeight * dpr;
    }
    if (orbitCanvas.width !== orbitCanvas.clientWidth * dpr) {
        orbitCanvas.width = orbitCanvas.clientWidth * dpr;
        orbitCanvas.height = orbitCanvas.clientHeight * dpr;
    }

    const oCtx = oscCanvas.getContext('2d');
    const orbCtx = orbitCanvas.getContext('2d');

    const oW = oscCanvas.width;
    const oH = oscCanvas.height;
    const orbW = orbitCanvas.width;
    const orbH = orbitCanvas.height;

    // Time advancement
    if (simRunning) {
        if (simScopeMode === 'slow') {
            simTime += 0.0003 * (simSpeed / 1500);
        } else {
            // In stationary triggered mode, advance micro-time for subtle ripple pulsation
            simTime += 0.0001;
        }
    }

    // -------------------------------------------------------------
    // 1. DRAW OSCILLOSCOPE (Time Domain Waves)
    // -------------------------------------------------------------
    oCtx.save();
    oCtx.clearRect(0, 0, oW, oH);

    // Dark oscilloscope background
    oCtx.fillStyle = '#060b18';
    oCtx.fillRect(0, 0, oW, oH);

    // Grid lines (8 divisions horizontal, 6 vertical)
    oCtx.strokeStyle = 'rgba(0, 210, 255, 0.08)';
    oCtx.lineWidth = 1 * dpr;
    for (let x = 0; x <= oW; x += oW / 8) {
        oCtx.beginPath();
        oCtx.moveTo(x, 0);
        oCtx.lineTo(x, oH);
        oCtx.stroke();
    }
    for (let y = 0; y <= oH; y += oH / 6) {
        oCtx.beginPath();
        oCtx.moveTo(0, y);
        oCtx.lineTo(oW, y);
        oCtx.stroke();
    }

    // Center Zero Line
    oCtx.strokeStyle = 'rgba(255, 255, 255, 0.18)';
    oCtx.lineWidth = 1.5 * dpr;
    oCtx.beginPath();
    oCtx.moveTo(0, oH / 2);
    oCtx.lineTo(oW, oH / 2);
    oCtx.stroke();

    // Fundamental angular frequency (2 cycles across screen width)
    const points = 300;
    const ampY = (oH / 2) * 0.72; // scale for amplitude
    const asymFrac = simAsym / 100;

    // Arrays for waveforms
    const iaArr = [], ibArr = [], icArr = [], izscArr = [];

    for (let i = 0; i < points; i++) {
        const frac = i / points;
        // theta spans exactly 2 cycles (4 * PI)
        let theta = frac * 4 * Math.PI;
        if (simScopeMode === 'slow') {
            theta += simTime * 200;
        }

        // Base signals
        let ia = Math.sin(theta);
        let ib = Math.sin(theta - (2 * Math.PI / 3));
        let ic = Math.sin(theta + (2 * Math.PI / 3));
        let izsc = 0;

        if (simAlgo === 'OEPC') {
            // OEPC active suppression: pure sinusoids with tiny ripple (<0.04A)
            const microNoise = 0.02 * Math.sin(theta * 18 + simTime * 50);
            ia += microNoise;
            ib += microNoise * 0.8;
            ic -= microNoise * 1.8;
            izsc = 0.03 * asymFrac * Math.sin(3 * theta);
        } else if (simAlgo === 'TDM') {
            // TDM: uncompensated asymmetry generates heavy 3rd harmonic ZSC
            const tdmZsc = 0.45 * asymFrac * Math.sin(3 * theta + 0.3);
            izsc = tdmZsc;
            ia = (1 + 0.12 * asymFrac) * Math.sin(theta) + 0.1 * Math.sin(theta * 5);
            ib = (1 - 0.28 * asymFrac) * Math.sin(theta - (2 * Math.PI / 3)) + tdmZsc * 0.7;
            ic = (1 + 0.16 * asymFrac) * Math.sin(theta + (2 * Math.PI / 3)) - tdmZsc * 0.7;
        } else if (simAlgo === 'PWM') {
            // PWM: dangerous circulating ZSC loop & carrier ripple
            const pwmZsc = 0.85 * asymFrac * Math.sin(theta - 0.5) + 0.15 * Math.sin(theta * 9);
            izsc = pwmZsc;
            ia = (1 + 0.25 * asymFrac) * Math.sin(theta) + 0.15 * Math.sin(theta * 12);
            ib = (1 - 0.35 * asymFrac) * Math.sin(theta - (2 * Math.PI / 3)) + pwmZsc * 0.9;
            ic = (1 + 0.10 * asymFrac) * Math.sin(theta + (2 * Math.PI / 3)) - pwmZsc * 0.9;
        }

        iaArr.push(ia);
        ibArr.push(ib);
        icArr.push(ic);
        izscArr.push(izsc);
    }

    // Helper to draw a single wave trace
    function drawTrace(arr, color, lineWidth, glowColor) {
        oCtx.strokeStyle = color;
        oCtx.lineWidth = lineWidth * dpr;
        oCtx.shadowColor = glowColor || color;
        oCtx.shadowBlur = 8 * dpr;
        oCtx.beginPath();
        for (let i = 0; i < points; i++) {
            const x = (i / points) * oW;
            const y = (oH / 2) - (arr[i] * ampY);
            if (i === 0) oCtx.moveTo(x, y);
            else oCtx.lineTo(x, y);
        }
        oCtx.stroke();
        oCtx.shadowBlur = 0;
    }

    // Draw Traces: Phase A (Cyan), Phase B (Purple), Phase C (Gold), ZSC (Red Thick)
    drawTrace(iaArr, '#00d2ff', 2.0, 'rgba(0, 210, 255, 0.4)');
    drawTrace(ibArr, '#9d50bb', 2.0, 'rgba(157, 80, 187, 0.4)');
    drawTrace(icArr, '#f6d365', 2.0, 'rgba(246, 211, 101, 0.4)');
    drawTrace(izscArr, '#ff4757', 3.0, 'rgba(255, 71, 87, 0.8)');

    oCtx.restore();

    // -------------------------------------------------------------
    // 2. DRAW ORBITAL LISSAJOUS HODOGRAPH (Alpha-Beta Plane)
    // -------------------------------------------------------------
    orbCtx.save();
    orbCtx.clearRect(0, 0, orbW, orbH);

    // Dark background
    orbCtx.fillStyle = '#060b18';
    orbCtx.fillRect(0, 0, orbW, orbH);

    const cX = orbW / 2;
    const cY = orbH / 2;
    const maxR = Math.min(cX, cY) * 0.78;

    // Concentric Circular Radar Grid
    orbCtx.strokeStyle = 'rgba(0, 210, 255, 0.08)';
    orbCtx.lineWidth = 1 * dpr;
    for (let r = 0.25; r <= 1.0; r += 0.25) {
        orbCtx.beginPath();
        orbCtx.arc(cX, cY, maxR * r, 0, 2 * Math.PI);
        orbCtx.stroke();
    }

    // Axes Alpha & Beta
    orbCtx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
    orbCtx.beginPath();
    orbCtx.moveTo(cX - maxR * 1.1, cY);
    orbCtx.lineTo(cX + maxR * 1.1, cY);
    orbCtx.moveTo(cX, cY - maxR * 1.1);
    orbCtx.lineTo(cX, cY + maxR * 1.1);
    orbCtx.stroke();

    // Axis Labels
    orbCtx.fillStyle = '#00d2ff';
    orbCtx.font = `${10 * dpr}px Rubik, sans-serif`;
    orbCtx.textAlign = 'right';
    orbCtx.fillText('α', cX + maxR * 1.15, cY - 4 * dpr);
    orbCtx.fillStyle = '#9d50bb';
    orbCtx.textAlign = 'center';
    orbCtx.fillText('β', cX + 10 * dpr, cY - maxR * 1.05);

    // Generate Alpha-Beta Trajectory
    const orbSteps = 240;
    orbCtx.beginPath();
    let curTipX = cX, curTipY = cY;

    // Instantaneous angle rotating smoothly (3.5s period)
    const tRot = (Date.now() / 3500) * 2 * Math.PI;

    for (let step = 0; step <= orbSteps; step++) {
        const phi = (step / orbSteps) * 2 * Math.PI;
        let rAlpha = Math.cos(phi);
        let rBeta = Math.sin(phi);

        if (simAlgo === 'OEPC') {
            // Pure circular hodograph
            rAlpha *= maxR;
            rBeta *= maxR;
        } else if (simAlgo === 'TDM') {
            // Eccentric, pulsating ellipse due to uncompensated ZSC
            const ripple = 0.15 * asymFrac * Math.sin(3 * phi);
            rAlpha = (1.18 * (1 + 0.1 * asymFrac) * Math.cos(phi) + ripple) * (maxR * 0.85);
            rBeta = (0.82 * (1 - 0.2 * asymFrac) * Math.sin(phi) - ripple) * (maxR * 0.85);
        } else if (simAlgo === 'PWM') {
            // Severely squashed and skewed ellipse with noise
            rAlpha = (1.30 * Math.cos(phi) + 0.1 * Math.sin(5 * phi)) * (maxR * 0.75);
            rBeta = (0.65 * Math.sin(phi) + 0.08 * Math.cos(5 * phi)) * (maxR * 0.75);
        }

        const px = cX + rAlpha;
        const py = cY - rBeta; // Canvas inverted Y

        if (step === 0) orbCtx.moveTo(px, py);
        else orbCtx.lineTo(px, py);

        // Find current instantaneous rotating tip
        if (Math.abs(phi - (tRot % (2 * Math.PI))) < (2 * Math.PI / orbSteps)) {
            curTipX = px;
            curTipY = py;
        }
    }

    // Trajectory style
    const orbColor = simAlgo === 'OEPC' ? '#00d2ff' : (simAlgo === 'TDM' ? '#f6d365' : '#ff4757');
    orbCtx.strokeStyle = orbColor;
    orbCtx.lineWidth = 2.5 * dpr;
    orbCtx.shadowColor = orbColor;
    orbCtx.shadowBlur = 10 * dpr;
    orbCtx.stroke();
    orbCtx.shadowBlur = 0;

    // Vector Arrow from Center to Tip
    orbCtx.strokeStyle = 'rgba(255, 255, 255, 0.4)';
    orbCtx.lineWidth = 1.5 * dpr;
    orbCtx.beginPath();
    orbCtx.moveTo(cX, cY);
    orbCtx.lineTo(curTipX, curTipY);
    orbCtx.stroke();

    // Rotating Glowing Tip Dot
    orbCtx.fillStyle = '#ffffff';
    orbCtx.shadowColor = orbColor;
    orbCtx.shadowBlur = 14 * dpr;
    orbCtx.beginPath();
    orbCtx.arc(curTipX, curTipY, 5 * dpr, 0, 2 * Math.PI);
    orbCtx.fill();
    orbCtx.shadowBlur = 0;

    orbCtx.restore();

    // Schedule next frame
    if (simRunning) {
        simAnimId = requestAnimationFrame(renderSimulationLoop);
    }
}

// Hook into presentation slide change to trigger/pause simulation
const prevSlideHook = updateSlide;
updateSlide = function(newIdx) {
    prevSlideHook(newIdx);
    setTimeout(() => {
        const slide10 = document.getElementById('slide-dynamic-sim');
        if (slide10 && slide10.classList.contains('active')) {
            if (!simAnimId && simRunning) {
                renderSimulationLoop();
            }
        }
    }, 150);
};

// Start immediately on load
window.addEventListener('load', () => {
    setTimeout(() => {
        setSimAlgo('OEPC', null);
        renderSimulationLoop();
    }, 400);
});



// =====================================================================
// =====================================================================
// =====================================================================
// --- 3. SLIDE 11: OEPC SWITCHING & CLOSED-LOOP ERROR CORRECTION ENGINE ---
// =====================================================================

(function() {
    // State & Fault Variables
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
function stepOepcPipeline(dt) {
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
function updateDemoUI() {
        const isHe = document.documentElement.lang === 'he' || document.querySelector('html[dir="rtl"]') !== null;

        // Update Error Values
        const elEa = document.getElementById('demo-val-ea');
        const elEb = document.getElementById('demo-val-eb');
        const elEc = document.getElementById('demo-val-ec');
        const elIzsc = document.getElementById('demo-val-izsc');
        if (elEa) elEa.textContent = (errA >= 0 ? '+' : '') + errA.toFixed(2) + ' A';
        if (elEb) elEb.textContent = (errB >= 0 ? '+' : '') + errB.toFixed(2) + ' A';
        if (elEc) elEc.textContent = (errC >= 0 ? '+' : '') + errC.toFixed(2) + ' A';
        if (elIzsc) elIzsc.textContent = (curIzsc >= 0 ? '+' : '') + curIzsc.toFixed(2) + ' A';

        // Update Sorting Badges
        const elOrder = document.getElementById('demo-badge-order');
        if (elOrder) elOrder.textContent = activeEpOrder;

        const elSmx = document.getElementById('demo-badge-smx');
        const elSmd = document.getElementById('demo-badge-smd');
        const elSmn = document.getElementById('demo-badge-smn');
        if (elSmx) elSmx.textContent = `S_mx: ${activeEpOrder[0]} (${activeSmx ? '+' : '-'})`;
        if (elSmd) elSmd.textContent = `S_md: ${activeEpOrder[1]} (${activeSmd ? '+' : '-'})`;
        if (elSmn) elSmn.textContent = `S_mn: ${activeEpOrder[2]} (${activeSmn ? '+' : '-'})`;

        // Update 7-Bit Address Display
        const elBin = document.getElementById('demo-7bit-bin');
        if (elBin) {
            elBin.innerHTML = `<span class="bit-p">${activePab}${activePbc}${activePca}</span>` +
                              `<span class="bit-sep">|</span>` +
                              `<span class="bit-s">${activeSmx}${activeSmd}${activeSmn}</span>` +
                              `<span class="bit-sep">|</span>` +
                              `<span class="bit-f">${activeFmp}</span>`;
        }
        const elIdx = document.getElementById('demo-lut-idx');
        if (elIdx) {
            elIdx.textContent = `Idx = ${activeAddr} (שורה #${activeRow})`;
        }

        // Update Selected Vector & Action
        const elVec = document.getElementById('demo-active-vec');
        if (elVec) elVec.textContent = `V_${activeVidx}`;

        const elSwitchTuple = document.getElementById('demo-switch-tuple');
        if (elSwitchTuple) {
            elSwitchTuple.textContent = `[${activeSwitches.join(', ')}]`;
        }

        const elImpact = document.getElementById('demo-active-impact');
        if (elImpact) {
            const formatted = activeImpact
                .replace(/\+A/g, '+i_a ').replace(/-A/g, '-i_a ')
                .replace(/\+B/g, '+i_b ').replace(/-B/g, '-i_b ')
                .replace(/\+C/g, '+i_c ').replace(/-C/g, '-i_c ')
                .replace(/\+Z/g, '+i_0 ').replace(/-Z/g, '-i_0 ');
            elImpact.innerHTML = `<span style="direction:ltr; unicode-bidi:isolate; display:inline-block; font-family:monospace; font-weight:700;">${formatted}</span>`;
        }

        const elFmpBadge = document.getElementById('demo-fmp-badge');
        if (elFmpBadge) {
            if (activeFmp === 0) {
                elFmpBadge.textContent = isHe ? 'התערבות סדרה אפס (Fmp=0)' : 'ZSC Critical (Fmp=0)';
                elFmpBadge.className = 'demo-pill pill-zsc';
            } else {
                elFmpBadge.textContent = isHe ? 'תיקון הפרשי (Fmp=1)' : 'Differential (Fmp=1)';
                elFmpBadge.className = 'demo-pill pill-dm';
            }
        }

        // Update 8-Transistor States (Sh & Sl per Leg according to Figure 2)
        const updateTBadge = (id, isOn) => {
            const el = document.getElementById(id);
            if (el) {
                el.textContent = isOn ? 'ON (1)' : 'OFF (0)';
                el.className = 't-badge ' + (isOn ? 'badge-on' : 'badge-off');
            }
        };
        const sa = activeSwitches[0];
        const sb = activeSwitches[1];
        const sc = activeSwitches[2];
        const sn = activeSwitches[3];

        updateTBadge('badge-sah', sa === 1);
        updateTBadge('badge-sal', sa === 0);
        updateTBadge('badge-sbh', sb === 1);
        updateTBadge('badge-sbl', sb === 0);
        updateTBadge('badge-sch', sc === 1);
        updateTBadge('badge-scl', sc === 0);
        updateTBadge('badge-snh', sn === 1);
        updateTBadge('badge-snl', sn === 0);

        // Telemetry error norms
        const normE = Math.sqrt(errA*errA + errB*errB + errC*errC);
        const elNorm = document.getElementById('demo-tel-norm');
        if (elNorm) elNorm.textContent = normE.toFixed(2) + ' A';

        // Animate dynamic error progress bars (calibrated to 1.0A full scale)
        const barA = document.getElementById('demo-bar-ea');
        const barB = document.getElementById('demo-bar-eb');
        const barC = document.getElementById('demo-bar-ec');
        const barZ = document.getElementById('demo-bar-izsc');
        if (barA) barA.style.width = Math.min(100, Math.abs(errA) * 100) + '%';
        if (barB) barB.style.width = Math.min(100, Math.abs(errB) * 100) + '%';
        if (barC) barC.style.width = Math.min(100, Math.abs(errC) * 100) + '%';
        if (barZ) barZ.style.width = Math.min(100, Math.abs(curIzsc) * 150) + '%';
    }

    // Canvas 1: Dual Oscilloscope with FULL SCIENTIFIC SCALES (קני מידה מדויקים)
    function renderOscilloscopeCanvas() {
        const canvas = document.getElementById('demo-osc-canvas');
        if (!canvas) return;
        const dpr = window.devicePixelRatio || 1;
        if (canvas.width !== canvas.clientWidth * dpr) {
            canvas.width = canvas.clientWidth * dpr;
            canvas.height = canvas.clientHeight * dpr;
        }
        const ctx = canvas.getContext('2d');
        const W = canvas.width;
        const H = canvas.height;

        ctx.save();
        ctx.clearRect(0, 0, W, H);
        ctx.direction = 'ltr';

        // Dark oscilloscope background
        ctx.fillStyle = '#060a12';
        ctx.fillRect(0, 0, W, H);

        const leftMargin = 50 * dpr; // reserved space for scale markings
        const plotW = W - leftMargin;
        const midY = H * 0.52;

        // Grid lines (8 divisions horizontal => 5 ms/div across 40 ms total window)
        ctx.strokeStyle = 'rgba(0, 210, 255, 0.08)';
        ctx.lineWidth = 1 * dpr;
        for (let i = 0; i <= 8; i++) {
            const x = leftMargin + (plotW / 8) * i;
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
        }
        for (let j = 0; j <= 6; j++) {
            const y = (H / 6) * j;
            ctx.beginPath(); ctx.moveTo(leftMargin, y); ctx.lineTo(W, y); ctx.stroke();
        }

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

        ctx.font = `bold ${8.5 * dpr}px monospace`;
        ctx.textAlign = 'right';
        const curTicks = [
            { val: 6.0, y: curZeroY - 6.0 * curScale, lbl: '+6.0A' },
            { val: 3.0, y: curZeroY - 3.0 * curScale, lbl: '+3.0A' },
            { val: 0.0, y: curZeroY, lbl: ' 0.0A' },
            { val: -3.0, y: curZeroY + 3.0 * curScale, lbl: '-3.0A' },
            { val: -6.0, y: curZeroY + 6.0 * curScale, lbl: '-6.0A' }
        ];
        curTicks.forEach(t => {
            ctx.fillStyle = t.val === 0 ? '#ffffff' : 'rgba(0, 210, 255, 0.75)';
            ctx.fillText(t.lbl, leftMargin - 6 * dpr, t.y + 3 * dpr);
            ctx.strokeStyle = 'rgba(0, 210, 255, 0.4)';
            ctx.beginPath(); ctx.moveTo(leftMargin, t.y); ctx.lineTo(leftMargin + 4 * dpr, t.y); ctx.stroke();
        });

        // Top Scale Label Tag
        ctx.textAlign = 'left';
        ctx.fillStyle = 'rgba(0, 210, 255, 0.9)';
        ctx.fillText('CH1: 3.0 A/div • 5.0 ms/div (i_a, i_b, i_c)', leftMargin + 8 * dpr, 14 * dpr);

        // Scope Mode Status Tag on right
        ctx.textAlign = 'right';
        if (demoScopeMode === 'trig') {
            ctx.fillStyle = '#00ff88';
            ctx.fillText('📌 TRIG LOCKED • 2 CYCLES', W - 10 * dpr, 14 * dpr);
        } else {
            ctx.fillStyle = '#00d2ff';
            ctx.fillText('🌊 SLOW ROLL 0.25X', W - 10 * dpr, 14 * dpr);
        }

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
            { val: 1.0, y: errZeroY - 1.0 * errScale, lbl: '+1.0A' },
            { val: 0.5, y: errZeroY - 0.5 * errScale, lbl: '+0.5A' },
            { val: 0.0, y: errZeroY, lbl: ' 0.0A' },
            { val: -0.5, y: errZeroY + 0.5 * errScale, lbl: '-0.5A' },
            { val: -1.0, y: errZeroY + 1.0 * errScale, lbl: '-1.0A' }
        ];
        errTicks.forEach(t => {
            ctx.fillStyle = t.val === 0 ? '#ffffff' : 'rgba(255, 107, 129, 0.75)';
            ctx.fillText(t.lbl, leftMargin - 6 * dpr, t.y + 3 * dpr);
            ctx.strokeStyle = 'rgba(255, 107, 129, 0.4)';
            ctx.beginPath(); ctx.moveTo(leftMargin, t.y); ctx.lineTo(leftMargin + 4 * dpr, t.y); ctx.stroke();
        });

        ctx.textAlign = 'left';
        ctx.fillStyle = 'rgba(255, 107, 129, 0.9)';
        ctx.fillText('CH2: 0.5 A/div (Errors e_x & Zero-Sequence Current i_zsc)', leftMargin + 8 * dpr, midY + 14 * dpr);

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

        for (let p = 0; p < POINTS; p++) {
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
            if (disturbanceTimer > 0) {
                dist = 0.65 * Math.sin(disturbanceTimer * 35) * (disturbanceTimer / 0.08);
            }

            const eA = Math.max(-1.1, Math.min(1.1, rpA + asym + dist));
            const eB = Math.max(-1.1, Math.min(1.1, rpB - 0.5 * asym - 0.5 * dist));
            const eC = Math.max(-1.1, Math.min(1.1, rpC - 0.5 * asym - 0.5 * dist));
            ptsEa[p] = eA; ptsEb[p] = eB; ptsEc[p] = eC;

            ptsIa[p] = rA - eA;
            ptsIb[p] = rB - eB;
            ptsIc[p] = rC - eC;

            if (leg4Fault) {
                ptsIzsc[p] = 0.65 * (asymPercent > 0 ? (asymPercent / 35.0) : 1.0) * Math.sin(3 * th) + dist * 0.3;
            } else if (asymPercent > 0) {
                ptsIzsc[p] = 0.03 * Math.sin(3 * th);
            } else {
                ptsIzsc[p] = 0.015 * Math.sin(3 * th);
            }
        }

        function drawLine(arr, zeroY, scale, color, lineWidth, isDashed) {
            ctx.beginPath();
            ctx.strokeStyle = color;
            ctx.lineWidth = lineWidth * dpr;
            if (isDashed) ctx.setLineDash([3 * dpr, 3 * dpr]); else ctx.setLineDash([]);
            for (let i = 0; i < POINTS; i++) {
                const x = leftMargin + (plotW / (POINTS - 1)) * i;
                const y = zeroY - arr[i] * scale;
                if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
            }
            ctx.stroke();
            ctx.setLineDash([]);
        }

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

        ctx.font = `bold ${8 * dpr}px monospace`;
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'center';
        ctx.fillText(`${scanMs.toFixed(1)} ms`, tagX + tagW / 2, midY + 3.5 * dpr);

        ctx.restore();
    }

    // Canvas 2: 4-Leg Inverter Gate Switching Traces (Saleae / Logic Analyzer style)
    function renderGateTracesCanvas() {
        const canvas = document.getElementById('demo-gate-canvas');
        if (!canvas) return;
        const dpr = window.devicePixelRatio || 1;
        if (canvas.width !== canvas.clientWidth * dpr) {
            canvas.width = canvas.clientWidth * dpr;
            canvas.height = canvas.clientHeight * dpr;
        }
        const ctx = canvas.getContext('2d');
        const W = canvas.width;
        const H = canvas.height;

        ctx.save();
        ctx.clearRect(0, 0, W, H);
        ctx.direction = 'ltr';
        ctx.direction = 'ltr';

        const labelW = 82 * dpr;   // Left channel labels & voltage scale
        const statusW = 68 * dpr;  // Right status badges
        const plotLeft = labelW;
        const plotRight = W - statusW;
        const plotW = Math.max(10, plotRight - plotLeft);
        const trackH = H / 4;

        const legs = [
            { legName: 'רגל A (L1)', switchName: 'S_a', color: '#00d2ff', activeVal: activeSwitches[0], hPair: 'S_ah', lPair: 'S_al', phaseOff: 0 },
            { legName: 'רגל B (L2)', switchName: 'S_b', color: '#f6d365', activeVal: activeSwitches[1], hPair: 'S_bh', lPair: 'S_bl', phaseOff: -2 * Math.PI / 3 },
            { legName: 'רגל C (L3)', switchName: 'S_c', color: '#ff6b81', activeVal: activeSwitches[2], hPair: 'S_ch', lPair: 'S_cl', phaseOff: 2 * Math.PI / 3 },
            { legName: 'רגל N (L4)', switchName: 'S_n', color: '#00ff88', activeVal: activeSwitches[3], hPair: 'S_nh', lPair: 'S_nl', phaseOff: 0 }
        ];

        const POINTS = 280;
        const rollAng = (demoScopeMode === 'slow' ? w_elec * demoRollOffset : 0);

        legs.forEach((leg, idx) => {
            const topY = idx * trackH;
            const botY = topY + trackH;
            const highY = topY + trackH * 0.26;
            const lowY  = topY + trackH * 0.78;

            // Track background
            if (idx % 2 === 0) {
                ctx.fillStyle = 'rgba(255, 255, 255, 0.02)';
                ctx.fillRect(0, topY, W, trackH);
            }

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

            ctx.font = `bold ${8.5 * dpr}px sans-serif`;
            ctx.fillStyle = leg.color;
            ctx.textAlign = 'left';
            ctx.fillText(leg.legName, 10 * dpr, topY + 12 * dpr);

            ctx.font = `bold ${7.5 * dpr}px monospace`;
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
            for (let p = 0; p < POINTS; p++) {
                const frac = p / (POINTS - 1);
                const th = frac * 4 * Math.PI + rollAng;
                const x = plotLeft + (plotW / (POINTS - 1)) * p;

                let state = 0;
                if (idx === 3) {
                    // Leg N
                    if (leg4Fault) {
                        state = 0; // disabled by fault
                    } else if (asymPercent > 0) {
                        state = Math.sin(3 * th) > 0 ? 1 : 0;
                    } else {
                        state = (Math.sin(3 * th + Math.PI / 4) > 0.2) ? 1 : 0;
                    }
                } else {
                    // Legs A, B, C
                    const modWave = Math.cos(th + leg.phaseOff);
                    const carrier = 0.55 * Math.sin(24 * th);
                    state = (modWave + carrier) > 0 ? 1 : 0;
                }

                const y = (state === 1) ? highY : lowY;
                if (p === 0) {
                    ctx.moveTo(x, y);
                } else {
                    if (y !== prevY) ctx.lineTo(x, prevY);
                    ctx.lineTo(x, y);
                }
                prevY = y;
            }
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

            ctx.font = `bold ${8 * dpr}px monospace`;
            ctx.fillStyle = isOn ? '#00ff88' : '#ff6b81';
            ctx.textAlign = 'center';
            ctx.fillText(isOn ? 'ON (1)' : 'OFF (0)', badgeX + badgeW / 2, badgeY + badgeH * 0.45);

            ctx.font = `${6.8 * dpr}px sans-serif`;
            ctx.fillStyle = 'rgba(255, 255, 255, 0.65)';
            ctx.fillText(isOn ? `${leg.hPair}:ON` : `${leg.lPair}:ON`, badgeX + badgeW / 2, badgeY + badgeH * 0.82);
        });

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
    }

    // Canvas 4: Dynamic Electronic Circuit Simulation (Fig. 2: Series-End VSI with Series Windings)
    let circuitParticlePhase = 0;

    function renderCircuitCanvas() {
        const canvas = document.getElementById('demo-circuit-canvas');
        if (!canvas) return;
        const dpr = window.devicePixelRatio || 1;
        if (canvas.width !== canvas.clientWidth * dpr) {
            canvas.width = canvas.clientWidth * dpr;
            canvas.height = canvas.clientHeight * dpr;
        }
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
        for (let x = 0; x <= W; x += gridSize) {
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
        }
        for (let y = 0; y <= H; y += gridSize) {
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
        }

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
        if (demoRunning) {
            circuitParticlePhase = (circuitParticlePhase + 0.08 * (demoSpeed / 0.5)) % 1.0;
        }

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
        ctx.font = `bold ${7.5 * dpr}px monospace`;
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

        ctx.font = `${6.5 * dpr}px sans-serif`;
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

        for (let k = 0; k < 4; k++) {
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
            ctx.font = `${6.5 * dpr}px monospace`;
            ctx.fillStyle = highState ? '#00ff88' : 'rgba(255,255,255,0.4)';
            ctx.textAlign = 'right';
            ctx.fillText(`S_H${k+1}`, lx - 6 * dpr, (swTopStart + swTopEnd) / 2 + 2 * dpr);

            ctx.fillStyle = lowState ? '#00ff88' : 'rgba(255,255,255,0.4)';
            ctx.fillText(`S_L${k+1}`, lx - 6 * dpr, (swBotStart + swBotEnd) / 2 + 2 * dpr);

            // Midpoint Node Dot (vk)
            ctx.fillStyle = isFaultedLeg ? '#ff4757' : (activeSwitches[k] ? '#f6d365' : '#00d2ff');
            ctx.shadowColor = ctx.fillStyle;
            ctx.shadowBlur = 5 * dpr;
            ctx.beginPath(); ctx.arc(lx, midY, 3.2 * dpr, 0, 2 * Math.PI); ctx.fill();
            ctx.shadowBlur = 0;

            // Midpoint Voltage Label (v1, v2, v3, v4)
            ctx.font = `bold ${7.5 * dpr}px monospace`;
            ctx.fillStyle = '#f368e0';
            ctx.textAlign = 'center';
            ctx.fillText(`v_${k+1}`, lx, midY - 6 * dpr);

            // Leg Label under bottom rail (L1, L2, L3, L4)
            ctx.font = `bold ${8.5 * dpr}px sans-serif`;
            ctx.fillStyle = isFaultedLeg ? '#ff6b81' : legColors[k];
            ctx.fillText(legNames[k], lx, botRailY + 15 * dpr);

            // Draw current flowing from active switch into midpoint
            if (!isFaultedLeg) {
                if (highState) {
                    drawSwitchCurrentParticles(ctx, lx, swTopStart, lx, midY, legColors[k], circuitParticlePhase, dpr);
                } else {
                    drawSwitchCurrentParticles(ctx, lx, midY, lx, swBotEnd, legColors[k], circuitParticlePhase, dpr);
                }
            }
        }

        // If Leg 4 is faulted: draw fault cross
        if (isLeg4Fault) {
            const lx4 = legX[3];
            ctx.strokeStyle = '#ff4757';
            ctx.lineWidth = 2.2 * dpr;
            ctx.beginPath();
            ctx.moveTo(lx4 - 8 * dpr, midY - 8 * dpr); ctx.lineTo(lx4 + 8 * dpr, midY + 8 * dpr);
            ctx.moveTo(lx4 + 8 * dpr, midY - 8 * dpr); ctx.lineTo(lx4 - 8 * dpr, midY + 8 * dpr);
            ctx.stroke();

            ctx.font = `bold ${6.8 * dpr}px sans-serif`;
            ctx.fillStyle = '#ff6b81';
            ctx.textAlign = 'center';
            ctx.fillText('⚠️ Leg L4 Fault (Isolated)', lx4, midY + 16 * dpr);
        }

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
        if (elVan) elVan.textContent = `v_a: ${va_val >= 0 ? '+' : ''}${va_val}V`;
        if (elVbn) elVbn.textContent = `v_b: ${vb_val >= 0 ? '+' : ''}${vb_val}V`;
        if (elVcn) elVcn.textContent = `v_c: ${vc_val >= 0 ? '+' : ''}${vc_val}V`;
        if (elIz) elIz.textContent = `i_0: ${zsc_calc >= 0 ? '+' : ''}${zsc_calc.toFixed(2)}A`;

        ctx.restore();
    }

    // Helper: Draw Transistor Switch with Open/Closed Contact Arm & Antiparallel Diode
    function drawTransistorSwitch(ctx, x, yTop, yBot, state, color, dpr, isFaulted) {
        ctx.save();
        const midY = (yTop + yBot) / 2;
        const armLen = (yBot - yTop) * 0.55;

        // Fixed terminal dots
        ctx.fillStyle = state === 1 ? '#00ff88' : 'rgba(255,255,255,0.4)';
        ctx.beginPath(); ctx.arc(x, yTop, 2 * dpr, 0, 2 * Math.PI); ctx.fill();
        ctx.beginPath(); ctx.arc(x, yBot, 2 * dpr, 0, 2 * Math.PI); ctx.fill();

        // Switch contact arm
        ctx.lineWidth = 1.8 * dpr;
        if (state === 1 && !isFaulted) {
            // CLOSED: straight glowing conducting connection
            ctx.strokeStyle = '#00ff88';
            ctx.shadowColor = '#00ff88';
            ctx.shadowBlur = 4 * dpr;
            ctx.beginPath(); ctx.moveTo(x, yTop); ctx.lineTo(x, yBot); ctx.stroke();
            ctx.shadowBlur = 0;
        } else {
            // OPEN: angled switch arm with air gap
            ctx.strokeStyle = isFaulted ? 'rgba(255,71,87,0.5)' : 'rgba(255,255,255,0.35)';
            ctx.beginPath();
            ctx.moveTo(x, yTop);
            ctx.lineTo(x + armLen * 0.65, yTop + armLen * 0.85);
            ctx.stroke();
        }

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
    }

    // Helper: Draw Series Motor Winding (Za, Zb, Zc) between consecutive legs
    function drawSeriesWinding(ctx, x1, x2, y, zName, vName, color, currentVal, particleT, dpr, isAsym) {
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
        for (let l = 1; l <= loops; l++) {
            const lx = leftConnEnd + l * step;
            ctx.arc(lx, y, 3 * dpr, 0, Math.PI, true);
        }
        ctx.stroke();

        // 3. Winding Label (Za, Zb, Zc)
        ctx.font = `bold ${7.2 * dpr}px sans-serif`;
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'center';
        ctx.fillText(zName, midX, y + boxH / 2 + 10 * dpr);

        // 4. Voltage Polarity Label: "+ va -"
        ctx.font = `bold ${7.2 * dpr}px monospace`;
        ctx.fillStyle = '#f6d365';
        ctx.textAlign = 'center';
        ctx.fillText(`+  ${vName}  -`, midX, y - boxH / 2 - 4 * dpr);

        // 5. Directional reference arrow (i ->)
        ctx.font = `${6.5 * dpr}px sans-serif`;
        ctx.fillStyle = 'rgba(255,255,255,0.6)';
        ctx.fillText(`i_${zName.slice(-1)} →`, midX, y - boxH / 2 - 12 * dpr);

        // Asymmetry badge
        if (isAsym) {
            ctx.fillStyle = 'rgba(246, 211, 101, 0.95)';
            ctx.font = `bold ${6.5 * dpr}px sans-serif`;
            ctx.fillText('+35% ΔL', midX, y + boxH / 2 + 19 * dpr);
        }

        // 6. Flowing Animated Current Particles along winding
        const absI = Math.abs(currentVal);
        if (absI > 0.05) {
            const isForward = currentVal > 0;
            const numParticles = Math.min(5, Math.max(2, Math.round(absI * 1.5)));

            for (let i = 0; i < numParticles; i++) {
                let frac = ((i / numParticles) + (isForward ? particleT : (1 - particleT))) % 1.0;
                const px = x1 + segLen * frac;

                // Particle dot
                ctx.fillStyle = '#ffffff';
                ctx.shadowColor = color;
                ctx.shadowBlur = 4 * dpr;
                ctx.beginPath(); ctx.arc(px, y, 2.2 * dpr, 0, 2 * Math.PI); ctx.fill();
                ctx.shadowBlur = 0;
            }
        }

        ctx.restore();
    }

    // Helper: Draw flowing current particles through switch to midpoint
    function drawSwitchCurrentParticles(ctx, x1, y1, x2, y2, color, particleT, dpr) {
        ctx.save();
        const py = y1 + (y2 - y1) * ((particleT) % 1.0);
        ctx.fillStyle = '#ffffff';
        ctx.shadowColor = color;
        ctx.shadowBlur = 3 * dpr;
        ctx.beginPath(); ctx.arc(x1, py, 1.8 * dpr, 0, 2 * Math.PI); ctx.fill();
        ctx.restore();
    }

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

    function renderErrorOrbitCanvas() {
        const canvas = document.getElementById('demo-error-orbit-canvas');
        if (!canvas) return;
        const dpr = window.devicePixelRatio || 1;
        if (canvas.width !== canvas.clientWidth * dpr) {
            canvas.width = canvas.clientWidth * dpr;
            canvas.height = canvas.clientHeight * dpr;
        }
        const ctx = canvas.getContext('2d');
        const W = canvas.width;
        const H = canvas.height;

        ctx.save();
        ctx.clearRect(0, 0, W, H);
        ctx.direction = 'ltr';
        ctx.direction = 'ltr';

        // Deep radar navy background
        ctx.fillStyle = '#060a12';
        ctx.fillRect(0, 0, W, H);

        const centerX = W * 0.50;
        const centerY = H * 0.53;
        const radius = Math.min(W * 0.42, H * 0.43);

        // Zoom factor: 0.35 Amperes full-scale radius (magnifies small errors for instant visibility)
        const maxAmp = 0.35;
        const scale = radius / maxAmp;

        // 1. Concentric Radial Grid (0.1A, 0.2A Deadband, 0.35A Boundary)
        const rings = [
            { rAmp: 0.10, lbl: '0.1A', color: 'rgba(255, 255, 255, 0.10)', isDashed: true, fill: null },
            { rAmp: 0.20, lbl: 'Deadband Threshold ±0.2A', color: 'rgba(0, 255, 136, 0.55)', isDashed: true, fill: 'rgba(0, 255, 136, 0.05)' },
            { rAmp: 0.35, lbl: '0.35A Max', color: 'rgba(0, 210, 255, 0.35)', isDashed: false, fill: null }
        ];

        rings.forEach(ring => {
            const rPx = ring.rAmp * scale;
            if (ring.fill) {
                ctx.fillStyle = ring.fill;
                ctx.beginPath(); ctx.arc(centerX, centerY, rPx, 0, 2 * Math.PI); ctx.fill();
            }
            ctx.strokeStyle = ring.color;
            ctx.lineWidth = ring.rAmp === 0.20 ? 1.5 * dpr : 1 * dpr;
            if (ring.isDashed) ctx.setLineDash([4 * dpr, 4 * dpr]); else ctx.setLineDash([]);
            ctx.beginPath(); ctx.arc(centerX, centerY, rPx, 0, 2 * Math.PI); ctx.stroke();
            ctx.setLineDash([]);

            // Ring Label on 45-degree diagonal to avoid axis collision
            const diagAngle = -Math.PI / 4;
            const lx = centerX + rPx * Math.cos(diagAngle);
            const ly = centerY + rPx * Math.sin(diagAngle);
            ctx.font = `bold ${8.5 * dpr}px monospace`;
            ctx.fillStyle = ring.rAmp === 0.20 ? '#00ff88' : 'rgba(255, 255, 255, 0.45)';
            ctx.textAlign = 'left';
            ctx.fillText(ring.lbl, lx + 3 * dpr, ly - 3 * dpr);
        });

        // 2. Main Orthogonal Axes (Alpha - Beta)
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.25)';
        ctx.lineWidth = 1.4 * dpr;
        ctx.beginPath(); ctx.moveTo(centerX - radius - 8 * dpr, centerY); ctx.lineTo(centerX + radius + 8 * dpr, centerY); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(centerX, centerY - radius - 8 * dpr); ctx.lineTo(centerX, centerY + radius + 8 * dpr); ctx.stroke();

        // Ticks & Numerical Scale on Axes (+0.2A, -0.2A)
        ctx.font = `bold ${9 * dpr}px monospace`;
        ctx.fillStyle = '#cbd5e0';
        ctx.textAlign = 'center';
        ctx.fillText('+0.2A', centerX + 0.20 * scale, centerY + 13 * dpr);
        ctx.fillText('-0.2A', centerX - 0.20 * scale, centerY + 13 * dpr);
        ctx.textAlign = 'right';
        ctx.fillText('+0.2A', centerX - 6 * dpr, centerY - 0.20 * scale + 3 * dpr);
        ctx.fillText('-0.2A', centerX - 6 * dpr, centerY + 0.20 * scale + 3 * dpr);

        // Prominent Axis Headers
        ctx.font = `bold ${11 * dpr}px sans-serif`;
        ctx.fillStyle = '#00d2ff';
        ctx.textAlign = 'right';
        ctx.fillText('e_α [A] →', W - 10 * dpr, centerY - 8 * dpr);

        ctx.fillStyle = '#f6d365';
        ctx.textAlign = 'left';
        ctx.fillText('↑ e_β [A]', centerX + 8 * dpr, 20 * dpr);

        // 3. Dynamic Convergence History Trail (Glowing Cyan Orbit)
        const trailLen = Math.min(55, HIST_LEN);
        ctx.lineWidth = 2.4 * dpr;
        for (let i = trailLen - 1; i > 0; i--) {
            const hIdx1 = (histPtr - 1 - i + HIST_LEN) % HIST_LEN;
            const hIdx2 = (histPtr - i + HIST_LEN) % HIST_LEN;
            const ea1 = histEa[hIdx1], eb1 = histEb[hIdx1], ec1 = histEc[hIdx1];
            const ea2 = histEa[hIdx2], eb2 = histEb[hIdx2], ec2 = histEc[hIdx2];
            const p1x = centerX + ea1 * scale;
            const p1y = centerY - ((eb1 - ec1) / 1.732) * scale;
            const p2x = centerX + ea2 * scale;
            const p2y = centerY - ((eb2 - ec2) / 1.732) * scale;

            const alpha = (1 - i / trailLen);
            ctx.strokeStyle = `rgba(0, 210, 255, ${alpha * 0.75})`;
            ctx.beginPath(); ctx.moveTo(p1x, p1y); ctx.lineTo(p2x, p2y); ctx.stroke();
        }

        // 4. Current Error Coordinates & Norm
        const curEalpha = errA;
        const curEbeta = (errB - errC) / 1.732;
        const curPtX = centerX + curEalpha * scale;
        const curPtY = centerY - curEbeta * scale;
        const normE = Math.sqrt(curEalpha * curEalpha + curEbeta * curEbeta);

        // 5. Corrective Voltage Vector Arrow (V_opt Pulling to Origin)
        const pullAngle = Math.atan2(centerY - curPtY, centerX - curPtX);
        const distToCenter = Math.hypot(curPtX - centerX, curPtY - centerY);
        const arrowLen = Math.max(30 * dpr, Math.min(distToCenter * 0.90, 65 * dpr));
        const arrowEndX = curPtX + Math.cos(pullAngle) * arrowLen;
        const arrowEndY = curPtY + Math.sin(pullAngle) * arrowLen;

        // Arrow Shaft with Intense Glow
        ctx.shadowColor = '#f6d365';
        ctx.shadowBlur = 10 * dpr;
        ctx.strokeStyle = '#f6d365';
        ctx.lineWidth = 3.8 * dpr;
        ctx.beginPath(); ctx.moveTo(curPtX, curPtY); ctx.lineTo(arrowEndX, arrowEndY); ctx.stroke();
        ctx.shadowBlur = 0;

        // Large Sharp Arrowhead
        const headLen = 11 * dpr;
        ctx.fillStyle = '#f6d365';
        ctx.beginPath();
        ctx.moveTo(arrowEndX, arrowEndY);
        ctx.lineTo(arrowEndX - headLen * Math.cos(pullAngle - Math.PI / 6), arrowEndY - headLen * Math.sin(pullAngle - Math.PI / 6));
        ctx.lineTo(arrowEndX - headLen * Math.cos(pullAngle + Math.PI / 6), arrowEndY - headLen * Math.sin(pullAngle + Math.PI / 6));
        ctx.closePath();
        ctx.fill();

        // Arrow Badge Plaque: "⚡ וקטור מתקן V_k"
        const midX = (curPtX + arrowEndX) / 2;
        const midY = (curPtY + arrowEndY) / 2;
        const isHe = document.documentElement.lang === 'he' || document.querySelector('html[dir="rtl"]') !== null;
        const labelText = isHe ? `⚡ וקטור מתקן V_${activeVidx}` : `⚡ Corrective V_${activeVidx}`;

        ctx.font = `bold ${9 * dpr}px sans-serif`;
        const tw = ctx.measureText(labelText).width;
        ctx.fillStyle = 'rgba(10, 18, 32, 0.92)';
        ctx.fillRect(midX - tw / 2 - 6 * dpr, midY - 18 * dpr, tw + 12 * dpr, 16 * dpr);
        ctx.strokeStyle = '#f6d365';
        ctx.lineWidth = 1.2 * dpr;
        ctx.strokeRect(midX - tw / 2 - 6 * dpr, midY - 18 * dpr, tw + 12 * dpr, 16 * dpr);

        ctx.fillStyle = '#f6d365';
        ctx.textAlign = 'center';
        ctx.fillText(labelText, midX, midY - 6 * dpr);

        // 6. Current Error Point: Glowing Beacon
        // Outer pulsing ring
        ctx.fillStyle = 'rgba(0, 210, 255, 0.30)';
        ctx.beginPath(); ctx.arc(curPtX, curPtY, 10 * dpr, 0, 2 * Math.PI); ctx.fill();

        // Inner solid core
        ctx.shadowColor = '#00d2ff';
        ctx.shadowBlur = 14 * dpr;
        ctx.fillStyle = '#ffffff';
        ctx.beginPath(); ctx.arc(curPtX, curPtY, 5 * dpr, 0, 2 * Math.PI); ctx.fill();
        ctx.shadowBlur = 0;

        // Center Origin Target (0,0)
        ctx.fillStyle = '#00ff88';
        ctx.beginPath(); ctx.arc(centerX, centerY, 3.5 * dpr, 0, 2 * Math.PI); ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1 * dpr;
        ctx.beginPath(); ctx.arc(centerX, centerY, 6 * dpr, 0, 2 * Math.PI); ctx.stroke();

        // 7. Top HUD Overlays
        ctx.font = `bold ${9 * dpr}px monospace`;
        ctx.textAlign = 'left';
        ctx.fillStyle = '#00d2ff';
        ctx.fillText(`|e_αβ| Error: ${normE.toFixed(2)} A`, 10 * dpr, 16 * dpr);

        const inDeadband = normE <= 0.20;
        ctx.textAlign = 'right';
        ctx.fillStyle = inDeadband ? '#00ff88' : '#ff6b81';
        const statusText = inDeadband
            ? 'Status: Deadband OK (±0.2A)'
            : '⚠️ Error Exceeded (OEPC Active)';
        ctx.fillText(statusText, W - 10 * dpr, 16 * dpr);

        ctx.restore();
    }

    // Main Animation Loop
    function demoLoop() {
        const slide11 = document.getElementById('slide-switching-error-demo');
        const isActive = slide11 && slide11.classList.contains('active');

        if (!isActive) {
            demoAnimId = null;
            return;
        }

        if (demoRunning) {
            stepOepcPipeline(0.00006 * demoSpeed);
            updateDemoUI();
            renderOscilloscopeCanvas();
            renderGateTracesCanvas();
            renderCircuitCanvas();
            renderErrorOrbitCanvas();
            demoAnimId = requestAnimationFrame(demoLoop);
        } else {
            demoAnimId = null;
        }
    }

    // Public API for Buttons & Controls
    
    window.toggleDemoScopeMode = function() {
        demoScopeMode = (demoScopeMode === 'trig') ? 'slow' : 'trig';
        const btn = document.getElementById('btn-demo-scope-mode');
        const isHe = document.documentElement.lang === 'he' || document.querySelector('html[dir="rtl"]') !== null;
        if (btn) {
            if (demoScopeMode === 'trig') {
                btn.textContent = isHe ? '📌 גל מיוצב (נעול טריגר)' : '📌 Trigger-Locked Scope';
                btn.style.background = 'rgba(0, 255, 136, 0.15)';
                btn.style.borderColor = '#00ff88';
                btn.style.color = '#00ff88';
            } else {
                btn.textContent = isHe ? '🌊 גלילה איטית' : '🌊 Slow Rolling Scope';
                btn.style.background = 'rgba(0, 210, 255, 0.15)';
                btn.style.borderColor = '#00d2ff';
                btn.style.color = '#00d2ff';
            }
        }
    };

    window.toggleDemoPlay = function() {
        demoRunning = !demoRunning;
        const btn = document.getElementById('btn-demo-play');
        const isHe = document.documentElement.lang === 'he' || document.querySelector('html[dir="rtl"]') !== null;
        if (btn) {
            btn.textContent = demoRunning
                ? (isHe ? '⏸ השהה' : '⏸ Pause')
                : (isHe ? '▶ הפעל' : '▶ Play');
            btn.style.background = demoRunning ? 'rgba(0,210,255,0.18)' : 'rgba(0,255,136,0.25)';
        }
        if (demoRunning && !demoAnimId) {
            demoAnimId = requestAnimationFrame(demoLoop);
        }
    };

    window.stepDemoOnce = function() {
        demoRunning = false;
        const btn = document.getElementById('btn-demo-play');
        const isHe = document.documentElement.lang === 'he' || document.querySelector('html[dir="rtl"]') !== null;
        if (btn) btn.textContent = isHe ? '▶ הפעל' : '▶ Play';

        // Advance by exactly 1 control period (20 microseconds scaled)
        stepOepcPipeline(0.00008);
        updateDemoUI();
        renderOscilloscopeCanvas();
        renderGateTracesCanvas();
        renderCircuitCanvas();
        renderErrorOrbitCanvas();
    };


    // Public API for Fault Injection
    window.setDemoFault = function(faultType) {
        activeFault = faultType;
        asymPercent = 0;
        leg4Fault = false;
        loadSurge = false;

        const faultIds = ['none', 'surge', 'asym', 'leg4', 'load'];
        faultIds.forEach(fid => {
            const btn = document.getElementById('btn-fault-' + fid);
            if (btn) {
                if (fid === faultType) btn.classList.add('active-fault');
                else btn.classList.remove('active-fault');
            }
        });

        const banner = document.getElementById('demo-surge-banner');
        const isHe = document.documentElement.lang === 'he' || document.querySelector('html[dir="rtl"]') !== null;

        if (faultType === 'none') {
            Iref = 5.0;
            if (banner) {
                banner.textContent = isHe
                    ? '✅ פעולה תקינה: בקרת OEPC שומרת על זרמי סדרה אפס ודיפרנציאליים בתוך התחום (<0.04A)!'
                    : '✅ Healthy Symmetrical Operation: OEPC maintains ZSC < 0.04A!';
                banner.style.background = 'rgba(0, 255, 136, 0.90)';
                banner.style.color = '#060a12';
                banner.style.opacity = '1';
                setTimeout(() => { if (activeFault === 'none') banner.style.opacity = '0'; }, 2200);
            }
        } else if (faultType === 'surge') {
            disturbanceTimer = 0.08;
            errA += 0.45; errC -= 0.45;
            if (banner) {
                banner.textContent = isHe
                    ? '⚡ קפיצת מדרגת שגיאה! ה-OEPC מאתר את שגיאת המקסימום ומפעיל וקטור מתקן מיידי!'
                    : '⚡ Error Surge Shock! OEPC prioritizes max-error phase and applies direct corrective vector!';
                banner.style.background = 'rgba(255, 71, 87, 0.95)';
                banner.style.color = '#ffffff';
                banner.style.opacity = '1';
                setTimeout(() => { banner.style.opacity = '0'; }, 2500);
            }
        } else if (faultType === 'asym') {
            asymPercent = 35;
            if (banner) {
                banner.textContent = isHe
                    ? '🔌 אי-סימטריה של 35% בסליל פאזה A! ה-OEPC מעביר עדיפות ל-Fmp=0 ומדכא זרמי ZSC!'
                    : '🔌 35% Winding Asymmetry on Phase A! OEPC engages Fmp=0 and eliminates ZSC circulation!';
                banner.style.background = 'rgba(246, 211, 101, 0.95)';
                banner.style.color = '#060a12';
                banner.style.opacity = '1';
            }
        } else if (faultType === 'leg4') {
            leg4Fault = true;
            if (banner) {
                banner.textContent = isHe
                    ? '⚠️ תקלת ענף 4 (השבתת ענף נייטרלי)! זרם סדרה-אפס חורג – הבקרה נלחמת לייצוב הפאזות!'
                    : '⚠️ Leg 4 Fault (Neutral Inhibit)! Severe ZSC surge - OEPC forces differential corrections!';
                banner.style.background = 'rgba(255, 107, 129, 0.95)';
                banner.style.color = '#ffffff';
                banner.style.opacity = '1';
            }
        } else if (faultType === 'load') {
            Iref = 6.2;
            errA += 0.35; errB += 0.35;
            if (banner) {
                banner.textContent = isHe
                    ? '📈 קפיצת עומס של 125%! הזרם המבוקש מזנק – ה-OEPC מגיב ב-1.75μs ומתכנס במהירות!'
                    : '📈 125% Load Step Surge! Reference jumps - OEPC converges smoothly within 1.75μs!';
                banner.style.background = 'rgba(0, 210, 255, 0.95)';
                banner.style.color = '#060a12';
                banner.style.opacity = '1';
                setTimeout(() => { banner.style.opacity = '0'; }, 2500);
            }
        }
    };

    window.updateDemoSpeed = function(val) {
        demoSpeed = parseFloat(val);
        stepCounter = 0;
        const lbl = document.getElementById('demo-speed-val');
        if (lbl) {
            lbl.textContent = demoSpeed.toFixed(1) + 'x';
        }
    };


    window.resetDemo = function() {
        demoTime = 0;
        errA = 0; errB = 0; errC = 0;
        curIa = Iref; curIb = -Iref*0.5; curIc = -Iref*0.5; curIzsc = 0;
        stepOepcPipeline(0.001);
        updateDemoUI();
        renderOscilloscopeCanvas();
        renderGateTracesCanvas();
        renderCircuitCanvas();
        renderErrorOrbitCanvas();
    };

    // Slide change lifecycle hook
    const prevSlide11Hook = window.updateSlide;
    window.updateSlide = function(newIdx) {
        if (typeof prevSlide11Hook === 'function') prevSlide11Hook(newIdx);
        setTimeout(() => {
            const slide11 = document.getElementById('slide-switching-error-demo');
            if (slide11 && slide11.classList.contains('active')) {
                if (!demoAnimId && demoRunning) {
                    demoAnimId = requestAnimationFrame(demoLoop);
                }
            }
        }, 150);
    };

    // On window load trigger initial frames
    window.addEventListener('load', () => {
        setTimeout(() => {
            stepOepcPipeline(0.001);
            updateDemoUI();
            renderOscilloscopeCanvas();
            renderGateTracesCanvas();
            renderCircuitCanvas();
            renderErrorOrbitCanvas();
        }, 500);
    });

})();

</script>


<!-- FULL 96-LUT INTERACTIVE MODAL VIEWER -->
<div id="lut-modal" class="lut-modal-overlay" style="display:none;" onclick="if(event.target===this)closeLutModal()">
    <div class="lut-modal-content">
        <div class="lut-modal-header">
            <h3>📖 Complete 96-Entry Optimal Lookup Table (OEPC 96-LUT) • IEEE TIE</h3>
            <button class="lut-modal-close" onclick="closeLutModal()">&times;</button>
        </div>
        <div class="lut-modal-info">
            <span>Current 7-Bit Address: <strong id="modal-active-addr" style="color:var(--accent-cyan)">105 (0b1101001)</strong></span>
            <span>Excel Row: <strong id="modal-active-row" style="color:var(--accent-gold)">#88 (ABC)</strong></span>
            <span>Selected Vector: <strong id="modal-active-vec" style="color:#00ff88">[1 0 1 1] (Vector 11)</strong></span>
            <input type="text" id="lut-search-input" placeholder="Search by permutation (ABC), impact (+A), or vector..." oninput="filterLutTable(this.value)" class="lut-search-box">
        </div>
        <div class="lut-modal-body">
            <table class="lut-full-table" id="lut-table-element">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Address (Idx)</th>
                        <th>Order (EPO)</th>
                        <th>Pab Pbc Pca</th>
                        <th>Smx Smd Smn</th>
                        <th>Fmp</th>
                        <th>L1 L2 L3 L4</th>
                        <th>Vector</th>
                        <th>Physical Impact</th>
                    </tr>
                </thead>
                <tbody id="lut-table-tbody">
                    <!-- Populated dynamically by JS -->
                </tbody>
            </table>
        </div>
    </div>
</div>

</body>
</html>

"""

with open(PMSM_DIR / "OEPC_SE_VSI_PMSM_Presentation.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Generated OEPC_SE_VSI_PMSM_Presentation.html successfully!")
