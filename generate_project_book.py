# -*- coding: utf-8 -*-
"""
Generate the Comprehensive Interactive HTML Book for the PMSM Project:
'ספר סיכום פרויקט: בקרת זרם אופטימלית מבוססת תעדוף שגיאה (OEPC) למנועי PMSM בממיר Series-End VSI'
"""

import os
import sys
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_HE = BASE_DIR / "ספר_סיכום_פרויקט_PMSM.html"
OUTPUT_EN = BASE_DIR / "PMSM_Project_Book.html"

def get_book_html():
    return r'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ספר הפרויקט: בקרת זרם אופטימלית OEPC למנועי PMSM בממיר Series-End VSI ודיכוי ZSC</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700;800;900&family=Rubik:wght@400;500;600;700;800&family=Fira+Code:wght@400;500;600&display=swap" rel="stylesheet">
    
    <!-- MathJax for high quality LaTeX equations -->
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

    <!-- Local / Fallback JSXGraph -->
    <link rel="stylesheet" href="presentation_assets/jsxgraph.css">
    <script src="presentation_assets/jsxgraphcore.js"></script>

    <style>
        :root {
            --bg-body: #070b14;
            --bg-sidebar: #0d1322;
            --bg-card: rgba(18, 26, 47, 0.85);
            --bg-card-hover: rgba(26, 38, 68, 0.95);
            --bg-table-stripe: rgba(255, 255, 255, 0.02);
            --border-subtle: rgba(64, 120, 240, 0.2);
            --border-active: rgba(0, 210, 255, 0.6);
            --text-main: #f0f4fc;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
            --accent-cyan: #00d2ff;
            --accent-blue: #3b82f6;
            --accent-purple: #9d50bb;
            --accent-green: #10b981;
            --accent-amber: #f59e0b;
            --accent-rose: #ef4444;
            --code-bg: #050811;
            --header-h: 64px;
            --sidebar-w: 320px;
            --shadow-card: 0 10px 30px rgba(0, 0, 0, 0.4);
            --glow-cyan: 0 0 20px rgba(0, 210, 255, 0.25);
        }

        body.light-theme {
            --bg-body: #f8fafc;
            --bg-sidebar: #ffffff;
            --bg-card: #ffffff;
            --bg-card-hover: #f1f5f9;
            --bg-table-stripe: #f8fafc;
            --border-subtle: #e2e8f0;
            --border-active: #0284c7;
            --text-main: #0f172a;
            --text-muted: #475569;
            --text-dim: #94a3b8;
            --code-bg: #f1f5f9;
            --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.08);
            --glow-cyan: 0 0 15px rgba(2, 132, 199, 0.2);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            scrollbar-width: thin;
            scrollbar-color: var(--accent-blue) var(--bg-sidebar);
        }

        body {
            font-family: 'Heebo', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-body);
            color: var(--text-main);
            line-height: 1.75;
            direction: rtl;
            overflow-x: hidden;
            transition: background-color 0.3s ease, color 0.3s ease;
        }

        /* Reading Progress Bar */
        #reading-progress {
            position: fixed;
            top: 0;
            right: 0;
            height: 4px;
            width: 0%;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue), var(--accent-purple));
            z-index: 9999;
            transition: width 0.1s ease-out;
        }

        /* Layout */
        .book-container {
            display: flex;
            min-height: 100vh;
        }

        /* Sidebar Navigation */
        .sidebar {
            width: var(--sidebar-w);
            background: var(--bg-sidebar);
            border-left: 1px solid var(--border-subtle);
            height: 100vh;
            position: sticky;
            top: 0;
            display: flex;
            flex-direction: column;
            z-index: 100;
            transition: transform 0.3s ease;
        }

        .sidebar-header {
            padding: 20px 24px;
            border-bottom: 1px solid var(--border-subtle);
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .sidebar-brand img {
            height: 38px;
            width: auto;
            border-radius: 6px;
            background: #ffffff;
            padding: 2px 4px;
        }

        .sidebar-brand-text h2 {
            font-size: 15px;
            font-family: 'Rubik', sans-serif;
            font-weight: 700;
            color: var(--text-main);
            line-height: 1.2;
        }

        .sidebar-brand-text span {
            font-size: 11px;
            color: var(--accent-cyan);
            font-weight: 600;
        }

        .sidebar-search {
            position: relative;
        }

        .sidebar-search input {
            width: 100%;
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 8px 34px 8px 12px;
            color: var(--text-main);
            font-size: 13px;
            font-family: inherit;
        }

        body.light-theme .sidebar-search input {
            background: #f8fafc;
        }

        .sidebar-search input:focus {
            outline: none;
            border-color: var(--accent-cyan);
        }

        .sidebar-search svg {
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            width: 16px;
            height: 16px;
            fill: var(--text-dim);
        }

        .sidebar-menu {
            flex: 1;
            overflow-y: auto;
            padding: 16px 12px;
            list-style: none;
        }

        .sidebar-menu li {
            margin-bottom: 4px;
        }

        .sidebar-menu a {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 9px 12px;
            color: var(--text-muted);
            text-decoration: none;
            font-size: 13.5px;
            border-radius: 8px;
            transition: all 0.2s;
            font-weight: 500;
        }

        .sidebar-menu a:hover {
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.05);
            transform: translateX(-3px);
        }

        .sidebar-menu a.active {
            color: #fff;
            background: linear-gradient(135deg, rgba(0, 210, 255, 0.2), rgba(59, 130, 246, 0.3));
            border-right: 3px solid var(--accent-cyan);
            font-weight: 700;
        }

        .sidebar-menu .ch-num {
            font-family: 'Fira Code', monospace;
            font-size: 11px;
            color: var(--accent-cyan);
            background: rgba(0, 210, 255, 0.1);
            padding: 2px 6px;
            border-radius: 4px;
        }

        .sidebar-footer {
            padding: 16px 20px;
            border-top: 1px solid var(--border-subtle);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            color: var(--text-dim);
        }

        /* Top Action Bar (Header) */
        .top-navbar {
            position: sticky;
            top: 0;
            height: var(--header-h);
            background: rgba(13, 19, 34, 0.85);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-subtle);
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 32px;
            z-index: 90;
        }

        body.light-theme .top-navbar {
            background: rgba(255, 255, 255, 0.9);
        }

        .nav-breadcrumbs {
            font-size: 13.5px;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .nav-breadcrumbs span.curr {
            color: var(--accent-cyan);
            font-weight: 600;
        }

        .nav-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .action-btn {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-subtle);
            color: var(--text-main);
            padding: 7px 14px;
            border-radius: 8px;
            font-size: 13px;
            font-family: inherit;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }

        .action-btn:hover {
            background: rgba(0, 210, 255, 0.15);
            border-color: var(--accent-cyan);
            color: #fff;
        }

        /* Main Content */
        .main-wrapper {
            flex: 1;
            display: flex;
            flex-direction: column;
            min-width: 0;
        }

        .content-area {
            max-width: 1040px;
            width: 100%;
            margin: 0 auto;
            padding: 40px 32px 100px 32px;
        }

        /* Typography & Headings */
        h1, h2, h3, h4 {
            font-family: 'Rubik', sans-serif;
            color: var(--text-main);
            margin-bottom: 16px;
            letter-spacing: -0.3px;
        }

        h1 {
            font-size: 32px;
            font-weight: 800;
            line-height: 1.3;
            background: linear-gradient(135deg, #ffffff 40%, var(--accent-cyan) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        body.light-theme h1 {
            background: linear-gradient(135deg, #0f172a 40%, var(--accent-blue) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        h2 {
            font-size: 24px;
            font-weight: 700;
            margin-top: 48px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border-subtle);
            position: relative;
        }

        h2::after {
            content: '';
            position: absolute;
            bottom: -1px;
            right: 0;
            width: 60px;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue));
            border-radius: 2px;
        }

        h3 {
            font-size: 19px;
            font-weight: 600;
            margin-top: 30px;
            color: var(--accent-cyan);
        }

        body.light-theme h3 {
            color: #0284c7;
        }

        h4 {
            font-size: 16px;
            font-weight: 600;
            margin-top: 20px;
            color: var(--text-muted);
        }

        p {
            font-size: 15.5px;
            line-height: 1.8;
            margin-bottom: 18px;
            color: var(--text-main);
        }

        strong {
            color: #ffffff;
            font-weight: 600;
        }

        body.light-theme strong {
            color: #0f172a;
        }

        /* BiDi isolation */
        .en-term, code, .math-term {
            direction: ltr;
            unicode-bidi: isolate;
            display: inline-block;
            font-family: 'Fira Code', monospace;
        }

        code {
            background: var(--code-bg);
            border: 1px solid var(--border-subtle);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 13.5px;
            color: var(--accent-cyan);
        }

        /* Front Matter / Cover Box */
        .cover-hero {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 20px;
            padding: 40px;
            box-shadow: var(--shadow-card);
            margin-bottom: 50px;
            position: relative;
            overflow: hidden;
        }

        .cover-hero::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            left: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue), var(--accent-purple), var(--accent-amber));
        }

        .cover-header-logo {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            flex-wrap: wrap;
            gap: 16px;
        }

        .cover-header-logo img {
            max-height: 55px;
            background: #fff;
            padding: 4px 10px;
            border-radius: 8px;
        }

        .cover-badge-pill {
            background: rgba(0, 210, 255, 0.12);
            border: 1px solid rgba(0, 210, 255, 0.3);
            color: var(--accent-cyan);
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }

        .authors-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-top: 30px;
            padding-top: 24px;
            border-top: 1px solid var(--border-subtle);
        }

        .author-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 16px 20px;
        }

        .author-card h4 {
            margin: 0 0 4px 0;
            font-size: 16px;
            color: var(--text-main);
        }

        .author-card p {
            margin: 0;
            font-size: 12.5px;
            color: var(--text-muted);
        }

        .author-card span.role {
            font-size: 12px;
            color: var(--accent-cyan);
            font-weight: 600;
        }

        /* Chapter Section Container */
        .chapter-section {
            margin-bottom: 70px;
            scroll-margin-top: 90px;
        }

        .chapter-badge {
            display: inline-block;
            background: rgba(59, 130, 246, 0.15);
            border: 1px solid rgba(59, 130, 246, 0.3);
            color: #93c5fd;
            font-size: 12px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 6px;
            font-family: 'Fira Code', monospace;
            margin-bottom: 8px;
        }

        /* Cards & Grids */
        .grid-2col {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin: 24px 0;
        }

        .grid-3col {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 18px;
            margin: 24px 0;
        }

        @media (max-width: 860px) {
            .grid-2col, .grid-3col {
                grid-template-columns: 1fr;
            }
            .sidebar {
                position: fixed;
                right: -320px;
                box-shadow: -5px 0 25px rgba(0, 0, 0, 0.5);
            }
            .sidebar.open {
                transform: translateX(-320px);
            }
        }

        .info-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 22px;
            box-shadow: var(--shadow-card);
            transition: transform 0.2s, border-color 0.2s;
        }

        .info-card:hover {
            transform: translateY(-2px);
            border-color: var(--border-active);
        }

        .info-card h4 {
            margin-top: 0;
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--accent-cyan);
            font-size: 16px;
        }

        /* Figure Display Boxes */
        .fig-wrapper {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 16px;
            margin: 28px 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            box-shadow: var(--shadow-card);
        }

        .fig-wrapper img {
            max-width: 100%;
            height: auto;
            max-height: 480px;
            object-fit: contain;
            border-radius: 8px;
            background: #ffffff;
            padding: 6px;
            cursor: zoom-in;
            transition: transform 0.2s;
        }

        .fig-wrapper img:hover {
            transform: scale(1.01);
        }

        .fig-caption {
            margin-top: 12px;
            font-size: 13.5px;
            color: var(--text-muted);
            line-height: 1.5;
            font-family: 'Rubik', sans-serif;
        }

        .fig-caption strong {
            color: var(--accent-cyan);
        }

        /* Tables */
        .table-container {
            width: 100%;
            overflow-x: auto;
            margin: 24px 0;
            border-radius: 12px;
            border: 1px solid var(--border-subtle);
            background: var(--bg-card);
            box-shadow: var(--shadow-card);
        }

        table.styled-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
            text-align: right;
        }

        table.styled-table th {
            background: rgba(59, 130, 246, 0.2);
            color: var(--accent-cyan);
            font-weight: 700;
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-subtle);
            white-space: nowrap;
        }

        body.light-theme table.styled-table th {
            background: #e0f2fe;
            color: #0369a1;
        }

        table.styled-table td {
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-subtle);
            color: var(--text-main);
        }

        table.styled-table tbody tr:nth-child(even) {
            background: var(--bg-table-stripe);
        }

        table.styled-table tbody tr:hover {
            background: rgba(0, 210, 255, 0.06);
        }

        table.styled-table tr.highlight-row {
            background: rgba(0, 210, 255, 0.12);
            font-weight: 600;
        }

        /* Formula Highlights */
        .math-block {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-right: 4px solid var(--accent-cyan);
            border-radius: 10px;
            padding: 18px 24px;
            margin: 20px 0;
            font-size: 16px;
            overflow-x: auto;
        }

        /* Key Highlights Box / Alerts */
        .alert-box {
            border-radius: 12px;
            padding: 18px 22px;
            margin: 24px 0;
            display: flex;
            gap: 16px;
            align-items: flex-start;
        }

        .alert-info {
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-right: 4px solid var(--accent-blue);
        }

        .alert-success {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-right: 4px solid var(--accent-green);
        }

        .alert-warning {
            background: rgba(245, 158, 11, 0.1);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-right: 4px solid var(--accent-amber);
        }

        .alert-icon {
            font-size: 20px;
            flex-shrink: 0;
            margin-top: 2px;
        }

        .alert-content h5 {
            font-size: 15px;
            font-weight: 700;
            margin-bottom: 4px;
            color: #fff;
        }

        body.light-theme .alert-content h5 {
            color: #0f172a;
        }

        .alert-content p {
            margin: 0;
            font-size: 14px;
            color: var(--text-muted);
        }

        /* Lists */
        ul.bullet-list, ol.num-list {
            padding-right: 24px;
            margin-bottom: 20px;
        }

        ul.bullet-list li, ol.num-list li {
            margin-bottom: 8px;
            font-size: 15px;
            color: var(--text-main);
        }

        /* Interactive Simulation Embeds */
        .sim-embed-card {
            background: var(--bg-card);
            border: 1px solid var(--border-active);
            border-radius: 16px;
            padding: 24px;
            margin: 32px 0;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5), var(--glow-cyan);
        }

        .sim-embed-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .sim-embed-header h3 {
            margin: 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .sim-container-grid {
            display: grid;
            grid-template-columns: 360px 1fr;
            gap: 20px;
        }

        @media (max-width: 900px) {
            .sim-container-grid {
                grid-template-columns: 1fr;
            }
        }

        .sim-controls-panel {
            background: rgba(10, 15, 29, 0.95);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }

        body.light-theme .sim-controls-panel {
            background: #f1f5f9;
        }

        .control-group label {
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 6px;
        }

        .control-group input[type="range"] {
            width: 100%;
            accent-color: var(--accent-cyan);
        }

        .btn-toggle-group {
            display: flex;
            gap: 6px;
        }

        .btn-toggle {
            flex: 1;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid var(--border-subtle);
            color: var(--text-main);
            padding: 8px;
            border-radius: 6px;
            font-size: 12.5px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            text-align: center;
        }

        .btn-toggle.active {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            color: #fff;
            border-color: transparent;
            box-shadow: 0 0 10px rgba(0, 210, 255, 0.4);
        }

        .sim-view-panel {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .sim-canvas-holder {
            background: #050811;
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            min-height: 280px;
            position: relative;
            overflow: hidden;
        }

        .telemetry-strip {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }

        .telemetry-item {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 8px 12px;
            display: flex;
            flex-direction: column;
        }

        body.light-theme .telemetry-item {
            background: #ffffff;
        }

        .telemetry-item span.lbl {
            font-size: 11px;
            color: var(--text-dim);
        }

        .telemetry-item span.val {
            font-family: 'Fira Code', monospace;
            font-size: 14px;
            font-weight: 700;
            color: var(--accent-cyan);
            direction: ltr;
        }

        /* Modal Lightbox for Images */
        #img-modal {
            display: none;
            position: fixed;
            z-index: 99999;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(5, 8, 16, 0.92);
            backdrop-filter: blur(8px);
            justify-content: center;
            align-items: center;
            padding: 40px;
        }

        #img-modal.active {
            display: flex;
        }

        #img-modal img {
            max-width: 90vw;
            max-height: 85vh;
            object-fit: contain;
            border-radius: 10px;
            box-shadow: 0 0 50px rgba(0, 0, 0, 0.8);
            background: #fff;
            padding: 6px;
        }

        #img-modal .modal-close {
            position: absolute;
            top: 24px;
            left: 32px;
            color: #fff;
            font-size: 32px;
            cursor: pointer;
            font-weight: 700;
        }

        /* Print Media Styles */
        @media print {
            body {
                background: #ffffff !important;
                color: #000000 !important;
            }
            .sidebar, .top-navbar, #reading-progress, .sim-embed-card, .action-btn {
                display: none !important;
            }
            .content-area {
                max-width: 100% !important;
                padding: 0 !important;
            }
            .chapter-section {
                page-break-before: always;
            }
            .fig-wrapper img {
                max-height: 380px;
            }
        }
    </style>
</head>
<body>

    <!-- Reading Progress Bar -->
    <div id="reading-progress"></div>

    <!-- Image Zoom Modal -->
    <div id="img-modal" onclick="closeModal()">
        <span class="modal-close">&times;</span>
        <img id="modal-img" src="" alt="Zoomed view">
    </div>

    <div class="book-container">

        <!-- ================================================================ -->
        <!-- SIDEBAR TABLE OF CONTENTS                                        -->
        <!-- ================================================================ -->
        <aside class="sidebar" id="book-sidebar">
            <div class="sidebar-header">
                <div class="sidebar-brand">
                    <img src="Images/sce_header_logo.png" alt="SCE Logo">
                    <div class="sidebar-brand-text">
                        <h2>ספר הפרויקט: PMSM</h2>
                        <span>M.Sc. Research Thesis</span>
                    </div>
                </div>
                <div class="sidebar-search">
                    <input type="text" id="chapter-search" placeholder="חיפוש בפרקי הספר..." oninput="filterChapters()">
                    <svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
                </div>
            </div>

            <ul class="sidebar-menu" id="sidebar-nav">
                <li><a href="#ch-cover" class="active"><span class="ch-num">00</span> שער ותקציר מנהלים</a></li>
                <li><a href="#ch-01"><span class="ch-num">01</span> רקע וטופולוגיית Series-End</a></li>
                <li><a href="#ch-02"><span class="ch-num">02</span> אלגוריתם OEPC וטבלת LUT</a></li>
                <li><a href="#ch-03"><span class="ch-num">03</span> מעבדה אינטראקטיבית חיה</a></li>
                <li><a href="#ch-04"><span class="ch-num">04</span> אימות סימולטיבי ו-HIL בזמן אמת</a></li>
                <li><a href="#ch-05"><span class="ch-num">05</span> חסינות לתקלות פנימיות (ITSC)</a></li>
                <li><a href="#ch-06"><span class="ch-num">06</span> כיול מנוע OEMER ואינקודר</a></li>
                <li><a href="#ch-07"><span class="ch-num">07</span> תכנון כרטיסי חומרה ב-Altium</a></li>
                <li><a href="#ch-08"><span class="ch-num">08</span> מכלול מכני (CAD) ועמדת דיינו</a></li>
                <li><a href="#ch-09"><span class="ch-num">09</span> השוואת ביצועים וסיכום</a></li>
                <li><a href="#ch-appendices"><span class="ch-num">10</span> נספחים ואינדקס דוחות</a></li>
            </ul>

            <div class="sidebar-footer">
                <span>SCE College • 2026</span>
                <span class="en-term">IEEE TIE</span>
            </div>
        </aside>

        <!-- ================================================================ -->
        <!-- MAIN CONTENT AREA                                                -->
        <!-- ================================================================ -->
        <div class="main-wrapper">

            <!-- Top Navbar -->
            <header class="top-navbar">
                <div class="nav-breadcrumbs">
                    <button class="action-btn" id="mobile-toggle" onclick="toggleSidebar()" style="display:none;">☰</button>
                    <span>ספר הפרויקט</span> &gt; <span class="curr" id="active-crumb">שער ותקציר מנהלים</span>
                </div>
                <div class="nav-actions">
                    <button class="action-btn" onclick="toggleTheme()" id="theme-btn" title="החלף מצב תצוגה (Light/Dark)">
                        🌓 מצב תצוגה
                    </button>
                    <button class="action-btn" onclick="window.print()" title="הדפס או שמור כ-PDF">
                        🖨️ הדפסה / PDF
                    </button>
                    <a href="index.html" class="action-btn" title="חזרה למרכז הניווט הראשי">
                        🏠 פורטל ראשי
                    </a>
                </div>
            </header>

            <main class="content-area">

                <!-- ============================================================ -->
                <!-- FRONT MATTER & COVER                                         -->
                <!-- ============================================================ -->
                <section class="chapter-section" id="ch-cover">
                    <div class="cover-hero">
                        <div class="cover-header-logo">
                            <img src="Images/sce_official_header.png" alt="לוגו רשמי SCE">
                            <span class="cover-badge-pill">עבודת תזה לתואר שני .M.Sc • מחקר מדעי מאומת</span>
                        </div>

                        <h1>בקרת זרם אופטימלית מבוססת תעדוף שגיאה (OEPC) עבור ממיר Series-End VSI למנועי PMSM ודיכוי זרמי סדרה אפס</h1>
                        <p style="font-size: 17px; color: var(--text-muted); margin-top: 12px;">
                            Hardware-Efficient Optimal Error-Priority Control for Series-End VSI Fed PMSM with Zero-Sequence Current (ZSC) Suppression
                        </p>

                        <div class="authors-grid">
                            <div class="author-card">
                                <h4>מקסים רדקין</h4>
                                <span class="role">סטודנט (.M.Sc)</span>
                                <p>המחלקה להנדסת חשמל ואלקטרוניקה, SCE</p>
                            </div>
                            <div class="author-card">
                                <h4>ד"ר אלי גד ברבי</h4>
                                <span class="role">מנחה ראשי • מרצה בכיר</span>
                                <p>מומחה להנע חשמלי ואלקטרוניקת הספק, SCE</p>
                            </div>
                            <div class="author-card">
                                <h4>פרופ' דמיטרי ביימל</h4>
                                <span class="role">שותף למחקר • Senior Member IEEE</span>
                                <p>המחלקה להנדסת חשמל ואלקטרוניקה, SCE</p>
                            </div>
                        </div>
                    </div>

                    <h2>תקציר מנהלים ומטרות המחקר</h2>
                    <p>
                        עבודה זו מציגה מתודולוגיית בקרה פורצת דרך, אופטימלית וחסכונית במשאבי חומרה – <strong>Optimal Error-Priority Control (OEPC)</strong> – עבור הנע מנוע סינכרוני בעל מגנטים קבועים (<span class="en-term">PMSM</span>) המוזן מטופולוגיית ממיר מתח בחיבור טורי לקצוות הסלילים (<span class="en-term">Series-End VSI</span>).
                    </p>
                    <p>
                        טופולוגיית ה-Series-End VSI מאפשרת ייצור רמות מתח מרובות ושיפור איכות הזרם ללא צורך בספקי DC מבודדים נפרדים (בניגוד ל-Dual Inverter מסורתי). אולם, חיבור משותף זה סוגר לולאה גלוונית פנימית דרכה עלולים לזרום <strong>זרמי סדר-אפס (<span class="en-term">Zero-Sequence Current - ZSC</span>)</strong> הרסניים, הגורמים להתחממות יתר, אובדן מומנט ועיוותי גל חמורים.
                    </p>

                    <div class="alert-box alert-success">
                        <div class="alert-icon">💡</div>
                        <div class="alert-content">
                            <h5>תמצית התרומה המדעית וההנדסית</h5>
                            <p>
                                אלגוריתם ה-OEPC המוצג כאן פותר את בעיית ה-ZSC בצורה אינהרנטית וישירה, על-ידי קידוד לוגי של 6 שגיאות זרם בקואורדינטות טבעיות (ABC), תעדוף שגיאות דיפרנציאליות מול שגיאות Common-Mode, ודליית וקטור המיתוג האופטימלי בטבלת ניתוב (<span class="en-term">96-Entry LUT</span>) בצעד יחיד – ללא כל צורך במודולציית PWM רציפה, ללא טרנספורמציות קואורדינטות כבדות בזמן אמת, ועם חסינות מובנית בפני קצר פנימי בסלילים (<span class="en-term">ITSC</span>).
                            </p>
                        </div>
                    </div>

                    <div class="grid-3col">
                        <div class="info-card">
                            <h4>⚡ יעילות חישובית</h4>
                            <p>זמן חישוב מזערי של פחות מ-$1\ \mu\text{s}$ ב-FPGA/DSP, המתאים למיתוג מהיר ביותר במפסקי GaN מתקדמים.</p>
                        </div>
                        <div class="info-card">
                            <h4>🛡️ דיכוי ZSC מוחלט</h4>
                            <p>דיכוי זרם סדרה אפס לרמה זניחה (פחות מ-$1.2\%$ מזרם הנומינלי) בכל תנאי העבודה והעומס.</p>
                        </div>
                        <div class="info-card">
                            <h4>🔄 עמידות באי-סימטריה</h4>
                            <p>שמירה על איזון זרמים מושלם גם תחת חוסר איזון פיזי קיצוני של מעל $\pm 25\%$ בעכבות הפאזות.</p>
                        </div>
                    </div>
                </section>

                <!-- ============================================================ -->
                <!-- CHAPTER 1: BACKGROUND & TOPOLOGY                             -->
                <!-- ============================================================ -->
                <section class="chapter-section" id="ch-01">
                    <span class="chapter-badge">פרק 01</span>
                    <h2>רקע מדעי וטופולוגיית Series-End VSI</h2>
                    
                    <p>
                        במערכות הנע תעשייתיות וכלי רכב חשמליים מודרניים, ממירי מתח מסורתיים בעלי שתי רמות (<span class="en-term">2-Level VSI</span>) נתקלים במגבלות פיזיקליות של מתח הפריצה של המוליכים למחצה, תכולת הרמוניות גבוהה (<span class="en-term">THD</span>) ומתחי Common-Mode גבוהים המאיצים שחיקת מיסבים.
                    </p>
                    <p>
                        פתרון ה-Open-End Winding המקובל משתמש בשני ממירים משני צידי סלילי הסטטור. אולם, שיטה זו דרשה באופן מסורתי שני מקורות DC נפרדים ומבודדים גלוונית כדי למנוע יצירת לולאות זרם.
                    </p>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/fig1_se_vsi_system_overview.jpg" alt="SE-VSI System Architecture" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 1.1:</strong> ארכיטקטורת המערכת הכוללת: מנוע PMSM בעל קצוות פתוחים המוזן מממיר Series-End VSI עם קבלי ציפה.</div>
                    </div>

                    <h3>עקרון הפעולה של ממיר Series-End VSI</h3>
                    <p>
                        טופולוגיית ה-Series-End VSI פותרת את מגבלת הספק הכפול על-ידי שימוש בספק DC ראשי יחיד ($V_{dc1}$) עבור הממיר הראשי, בעוד שהממיר המשני מוזן מקבלי ציפה (<span class="en-term">Floating DC-link Capacitors</span>) הנטענים ונפרקים מחזורית מענפי הממיר עצמם:
                    </p>

                    <div class="math-block">
                        $$V_{\text{phase}}(t) = V_{\text{main}}(t) - V_{\text{series}}(t)$$
                        $$V_{dc2} = \frac{1}{2} V_{dc1} \quad \Longrightarrow \quad \text{השגת 4 רמות מתח אפקטיביות!}$$
                    </div>

                    <h3>אתגר זרמי סדרה אפס (Zero-Sequence Current - ZSC)</h3>
                    <p>
                        מכיוון שנקודת הכוכב של המנוע אינה סגורה והממיר המשני מחובר ישירות לקצוות הסלילים ללא שנאי בידוד, נוצר מסלול סגור למתחי ה-Common-Mode. מתחים אלו מניעים זרם סדרה אפס ($i_0$):
                    </p>

                    <div class="math-block">
                        $$i_0 = \frac{1}{3}(i_a + i_b + i_c)$$
                        $$L_0 \frac{di_0}{dt} + R_0 i_0 = v_0 = \frac{1}{3}(v_{an} + v_{bn} + v_{cn})$$
                    </div>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/fig2_se_vsi_topology_and_zsc_path.jpg" alt="SE-VSI Topology & ZSC Path" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 1.2:</strong> מעגל התמורה החשמלי של טופולוגיית Series-End ומסלול הזרימה הסגור של זרם סדר-אפס ($i_0$).</div>
                    </div>

                    <p>
                        ללא בקרה אקטיבית, השראות סדר-אפס ($L_0$) במנועי PMSM היא קטנה ביותר (נמוכה בדרך כלל פי 3-5 מהשראות $L_d, L_q$), מה שגורם לכך שאפילו רכיב מתח Common-Mode מזערי יוצר זרמי ZSC ענקיים המשבשים כליל את פעולת המנוע.
                    </p>
                </section>

                <!-- ============================================================ -->
                <!-- CHAPTER 2: OEPC ALGORITHM & 96-LUT                           -->
                <!-- ============================================================ -->
                <section class="chapter-section" id="ch-02">
                    <span class="chapter-badge">פרק 02</span>
                    <h2>אלגוריתם OEPC ומבנה טבלת הניתוב בת 96 המצבים</h2>

                    <p>
                        שיטות בקרה קונבנציונליות כמו <span class="en-term">TDM (Time-Division Multiplexing)</span> מחלקות את מחזור המיתוג לפרקי זמן קבועים: פרק אחד לבקרת זרמי הפאזות הדיפרנציאליים, ופרק נפרד לדיכוי ה-ZSC. גישה זו סובלת מאיבוד ניצולת מתח ה-DC, הגדלת ריפל הזרם, והגבלת רוחב הסרט הדינמי.
                    </p>
                    <p>
                        בקרת <strong>OEPC (Optimal Error-Priority Control)</strong> נוקטת בגישה מהפכנית: חישוב ישיר של כלל שגיאות הזרם וסיווגן בזמן אמת, כך שכל פסיקת מיתוג מתקנת בו-זמנית הן את הפאזה בעלת השגיאה הדחופה ביותר והן את זרם ה-ZSC!
                    </p>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/fig3_oepc_flowchart_algorithm.jpg" alt="OEPC Flowchart Algorithm" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 2.1:</strong> תרשים הזרימה של אלגוריתם ה-OEPC: דגימה, חישוב שגיאות DM ו-CM, יצירת חתימת כתובת ושליפת וקטור המיתוג.</div>
                    </div>

                    <h3>הגדרת 6 שגיאות הזרם ובחירת השגיאה הקריטית</h3>
                    <p>
                        בכל מחזור דגימה, נמדדים זרמי הפאזות $i_a, i_b, i_c$ ומחושב זרם $i_0$. מול ערכי הייחוס מוגדרות 6 שגיאות:
                    </p>
                    <div class="math-block">
                        $$\varepsilon_{dm}^x = i_x^* - i_x \quad (x \in \{a, b, c\}) \quad \text{--- שגיאות Differential-Mode}$$
                        $$\varepsilon_{cm}^x = (i_x^* + i_0^*) - (i_x + i_0) \quad \text{--- שגיאות Common-Mode}$$
                    </div>

                    <p>
                        עבור כל מופע, נבחרת השגיאה הקריטית $\varepsilon_{crit}(x)$ כערך בעל הגודל המוחלט המקסימלי מבין ה-DM וה-CM. דגל ה-<strong>EMP ($F_{mp}$)</strong> נקבע כ-$1$ אם שגיאות ה-DM דומיננטיות, או $0$ אם שגיאות ה-CM דורשות תיקון דחוף.
                    </p>

                    <h3>יצירת כתובת ה-LUT בת 7 ביטים</h3>
                    <p>
                        החלטת המיתוג נשלפת בצעד שעון יחיד באמצעות כתובת בינארית בת 7 ביטים המורכבת מ:
                    </p>
                    <ul class="bullet-list">
                        <li><strong>קוד עדיפות (EPC - 3 Bits):</strong> מיון יחסי של גדלי השגיאות $|\varepsilon_a|, |\varepsilon_b|, |\varepsilon_c|$ (למשל: $A \gt B \gt C \rightarrow 110_2$).</li>
                        <li><strong>קוד סימנים (ESC - 3 Bits):</strong> קוטביות השגיאות בכל פאזה ($+/-$).</li>
                        <li><strong>דגל עדיפות מצב (EMP - 1 Bit):</strong> קובע את משקל דיכוי ה-ZSC מול הזרם הראשי.</li>
                    </ul>

                    <h3>טבלת הניתוב האופטימלית בת 96 המצבים (96-Entry Optimal LUT)</h3>
                    <p>
                        להלן דגימה מייצגת מתוך טבלת הניתוב המלאה בת 96 המצבים המוטמעת ב-FPGA:
                    </p>

                    <div class="table-container">
                        <table class="styled-table">
                            <thead>
                                <tr>
                                    <th>אינדקס</th>
                                    <th>סדר עדיפות (EPO)</th>
                                    <th>קוד EPC</th>
                                    <th>קוד ESC</th>
                                    <th>דגל EMP ($F_{mp}$)</th>
                                    <th>מצב מיתוג נבחר ($L_1 L_2 L_3 L_4$)</th>
                                    <th>פעולה מתקנת בזרם המנוע</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="highlight-row">
                                    <td>01</td>
                                    <td>ACB</td>
                                    <td>100</td>
                                    <td>011</td>
                                    <td>1 (DM Priority)</td>
                                    <td><span class="en-term">0110</span></td>
                                    <td>תיקון סימולטני של 2 פאזות: $-i_a, +i_c$</td>
                                </tr>
                                <tr>
                                    <td>02</td>
                                    <td>ACB</td>
                                    <td>100</td>
                                    <td>001</td>
                                    <td>0 (CM Priority)</td>
                                    <td><span class="en-term">0101</span></td>
                                    <td>תיקון משולב של 3 פאזות + דיכוי מואץ של $i_0$</td>
                                </tr>
                                <tr class="highlight-row">
                                    <td>03</td>
                                    <td>BAC</td>
                                    <td>010</td>
                                    <td>110</td>
                                    <td>1 (DM Priority)</td>
                                    <td><span class="en-term">1101</span></td>
                                    <td>תיקון מהיר של שגיאת פאזה B ופאזה C</td>
                                </tr>
                                <tr>
                                    <td>04</td>
                                    <td>BAC</td>
                                    <td>010</td>
                                    <td>110</td>
                                    <td>0 (CM Priority)</td>
                                    <td><span class="en-term">1100</span></td>
                                    <td>תיקון $+i_b$ ודיכוי רכיב $+i_0$ במקביל</td>
                                </tr>
                                <tr class="highlight-row">
                                    <td>05</td>
                                    <td>ABC</td>
                                    <td>110</td>
                                    <td>001</td>
                                    <td>1 (DM Priority)</td>
                                    <td><span class="en-term">0110</span></td>
                                    <td>איפוס שגיאות סימטריות $-i_a, +i_c$</td>
                                </tr>
                                <tr>
                                    <td>06</td>
                                    <td>ABC</td>
                                    <td>110</td>
                                    <td>001</td>
                                    <td>0 (CM Priority)</td>
                                    <td><span class="en-term">0111</span></td>
                                    <td>הזרקת וקטור Common-Mode מאזן</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </section>

                <!-- ============================================================ -->
                <!-- CHAPTER 3: LIVE INTERACTIVE LABORATORY                       -->
                <!-- ============================================================ -->
                <section class="chapter-section" id="ch-03">
                    <span class="chapter-badge">פרק 03</span>
                    <h2>מעבדה אינטראקטיבית מובנית: סימולציות חיות בלייב</h2>

                    <p>
                        פרק זה כולל שתי מעבדות הדמיה אינטראקטיביות עצמאיות הרצות ישירות בתוך הדפדפן שלך ב-60 פריימים לשנייה, המאפשרות לבחון באופן בלתי-אמצעי את התנהגות אלגוריתם ה-OEPC.
                    </p>

                    <!-- SIMULATION 1: JSXGRAPH VECTOR DECODER -->
                    <div class="sim-embed-card">
                        <div class="sim-embed-header">
                            <h3>📐 הדמיה 1: מפענח שגיאות וקטורי וטבלת LUT (אינטראקטיבי)</h3>
                            <span class="cover-badge-pill">JSXGraph Engine</span>
                        </div>
                        <p style="font-size: 14px; color: var(--text-muted);">
                            גרור את נקודת שגיאת הזרם $\vec{\varepsilon}_{\alpha\beta}$ על גבי משושה המתחים, או הזז את הסליידרים כדי לראות כיצד האלגוריתם מקודד את כתובת ה-7 ביטים ושולף את וקטור המיתוג האופטימלי:
                        </p>

                        <div class="sim-container-grid">
                            <div class="sim-controls-panel">
                                <div class="control-group">
                                    <label><span>שגיאת פאזה A ($\varepsilon_a$):</span> <span id="val-ea" class="en-term">0.45 A</span></label>
                                    <input type="range" id="slider-ea" min="-2.0" max="2.0" step="0.05" value="0.45" oninput="updateJsxSim()">
                                </div>
                                <div class="control-group">
                                    <label><span>שגיאת פאזה B ($\varepsilon_b$):</span> <span id="val-eb" class="en-term">-0.80 A</span></label>
                                    <input type="range" id="slider-eb" min="-2.0" max="2.0" step="0.05" value="-0.80" oninput="updateJsxSim()">
                                </div>
                                <div class="control-group">
                                    <label><span>שגיאת פאזה C ($\varepsilon_c$):</span> <span id="val-ec" class="en-term">0.35 A</span></label>
                                    <input type="range" id="slider-ec" min="-2.0" max="2.0" step="0.05" value="0.35" oninput="updateJsxSim()">
                                </div>
                                <div class="control-group">
                                    <label><span>שגיאת ZSC ($i_0$ error):</span> <span id="val-e0" class="en-term">0.15 A</span></label>
                                    <input type="range" id="slider-e0" min="-1.0" max="1.0" step="0.02" value="0.15" oninput="updateJsxSim()">
                                </div>
                                <div class="control-group">
                                    <label>משקל עדיפות ZSC (דגל EMP):</label>
                                    <div class="btn-toggle-group">
                                        <button class="btn-toggle active" id="btn-emp-auto" onclick="setEmpMode('auto')">אוטומטי (Adaptive)</button>
                                        <button class="btn-toggle" id="btn-emp-dm" onclick="setEmpMode('dm')">עדיפות DM</button>
                                        <button class="btn-toggle" id="btn-emp-cm" onclick="setEmpMode('cm')">עדיפות CM</button>
                                    </div>
                                </div>
                            </div>

                            <div class="sim-view-panel">
                                <div class="sim-canvas-holder" style="height: 320px;">
                                    <div id="jxgbox-book" style="width: 100%; height: 100%;"></div>
                                </div>
                                <div class="telemetry-strip">
                                    <div class="telemetry-item">
                                        <span class="lbl">קוד עדיפות (EPC)</span>
                                        <span class="val" id="disp-epc">010 (BAC)</span>
                                    </div>
                                    <div class="telemetry-item">
                                        <span class="lbl">קוד סימנים (ESC)</span>
                                        <span class="val" id="disp-esc">101 (+ - +)</span>
                                    </div>
                                    <div class="telemetry-item">
                                        <span class="lbl">דגל EMP ($F_{mp}$)</span>
                                        <span class="val" id="disp-emp">1 (DM)</span>
                                    </div>
                                    <div class="telemetry-item">
                                        <span class="lbl">וקטור LUT נבחר</span>
                                        <span class="val" id="disp-vec" style="color: var(--accent-amber);">V3 (1101)</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- SIMULATION 2: 60 FPS VIRTUAL OSCILLOSCOPE -->
                    <div class="sim-embed-card">
                        <div class="sim-embed-header">
                            <h3>📈 הדמיה 2: אוסצילוסקופ וירטואלי חי 60FPS – זרמי 3 פאזות, ZSC ומסלול אלפא-בטא</h3>
                            <span class="cover-badge-pill">HTML5 Canvas Real-Time Core</span>
                        </div>
                        <p style="font-size: 14px; color: var(--text-muted);">
                            מעבדת סימולציה רציפה המדגימה בזמן אמת את פעולת מנוע ה-PMSM. השווה בלחיצת כפתור בין אלגוריתם OEPC לבין שיטות TDM ו-PWM, שנה את חוסר האיזון בעומס, וצפה בדעיכת זרמי ה-ZSC:
                        </p>

                        <div class="sim-container-grid">
                            <div class="sim-controls-panel">
                                <div class="control-group">
                                    <label>שיטת בקרה נבדקת:</label>
                                    <div class="btn-toggle-group">
                                        <button class="btn-toggle active" id="btn-ctrl-oepc" onclick="setOscAlgorithm('oepc')">OEPC אופטימלי</button>
                                        <button class="btn-toggle" id="btn-ctrl-tdm" onclick="setOscAlgorithm('tdm')">TDM קלאסי</button>
                                        <button class="btn-toggle" id="btn-ctrl-pwm" onclick="setOscAlgorithm('pwm')">CBPWM קונבנציונלי</button>
                                    </div>
                                </div>
                                <div class="control-group">
                                    <label><span>אי-סימטריה בעומס (Asymmetry):</span> <span id="val-osc-asym" class="en-term">0%</span></label>
                                    <input type="range" id="slider-osc-asym" min="-30" max="30" step="1" value="0" oninput="updateOscParams()">
                                </div>
                                <div class="control-group">
                                    <label><span>מהירות סיבוב מנוע (RPM):</span> <span id="val-osc-rpm" class="en-term">580 RPM</span></label>
                                    <input type="range" id="slider-osc-rpm" min="100" max="1000" step="20" value="580" oninput="updateOscParams()">
                                </div>
                                <div class="control-group">
                                    <label><span>משקל דיכוי ZSC:</span> <span id="val-osc-zsc" class="en-term">100% (מקסימלי)</span></label>
                                    <input type="range" id="slider-osc-zsc" min="0" max="100" step="5" value="100" oninput="updateOscParams()">
                                </div>
                                <div class="control-group" style="display: flex; gap: 8px;">
                                    <button class="btn-toggle active" id="btn-osc-run" onclick="toggleOscRun()" style="flex: 1;">⏸️ השהה / הפעל</button>
                                    <button class="btn-toggle" onclick="resetOsc()" style="flex: 1;">🔄 איפוס</button>
                                </div>
                            </div>

                            <div class="sim-view-panel">
                                <div class="sim-canvas-holder" style="height: 340px; display: flex;">
                                    <canvas id="osc-time-canvas" style="flex: 2; height: 100%; border-left: 1px solid var(--border-subtle);"></canvas>
                                    <canvas id="osc-xy-canvas" style="flex: 1; height: 100%;"></canvas>
                                </div>
                                <div class="telemetry-strip">
                                    <div class="telemetry-item">
                                        <span class="lbl">THD זרם פאזה</span>
                                        <span class="val" id="disp-thd">1.85%</span>
                                    </div>
                                    <div class="telemetry-item">
                                        <span class="lbl">שיא ZSC ($i_0$)</span>
                                        <span class="val" id="disp-zsc-peak">0.04 A</span>
                                    </div>
                                    <div class="telemetry-item">
                                        <span class="lbl">תדר מיתוג ממוצע</span>
                                        <span class="val" id="disp-fsw">18.4 kHz</span>
                                    </div>
                                    <div class="telemetry-item">
                                        <span class="lbl">מומנט אלקטרומגנטי</span>
                                        <span class="val" id="disp-torque">12.5 Nm</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- ============================================================ -->
                <!-- CHAPTER 4: PSIM & TYPHOON HIL REAL-TIME VALIDATION           -->
                <!-- ============================================================ -->
                <section class="chapter-section" id="ch-04">
                    <span class="chapter-badge">פרק 04</span>
                    <h2>אימות סימולטיבי ב-PSIM ו-Typhoon C-HIL בזמן אמת</h2>

                    <p>
                        על מנת לאמת את אלגוריתם ה-OEPC לפני הטמעה במנוע הפיזי, נבנתה פלטפורמת בדיקות <strong>Hardware-in-the-Loop (C-HIL)</strong> מתקדמת באמצעות סימולטור זמן-אמת <strong>Typhoon HIL404</strong>.
                    </p>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/fig4_experimental_setups_chil_prototype.jpg" alt="Experimental Setups C-HIL & Prototype" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 4.1:</strong> פלטפורמת הבדיקה הניסויית: סימולטור זמן אמת Typhoon HIL404 המחובר לבקר DSP/FPGA חיצוני ואב-טיפוס מעבדתי.</div>
                    </div>

                    <h3>ארכיטקטורת המודל בזמן אמת ב-Typhoon HIL404</h3>
                    <p>
                        מודל הסימולציה ב-Typhoon HIL404 מוגדר בקובץ <span class="en-term">OEPC_PMSM96NOD_new_FB.tse</span> ופועל בצעד זמן מזערי של $\Delta t = 1\ \mu\text{s}$. המודל כולל:
                    </p>
                    <ul class="bullet-list">
                        <li><strong>מידול מנוע PMSM מלא:</strong> כולל אי-ליניאריות מגנטית, צימודים הדדיים בין הפאזות, ורוויה מגנטית.</li>
                        <li><strong>טופולוגיית Series-End VSI:</strong> 6 ענפי מיתוג מבוססי מודל מתג אידיאלי עם דיודות Flyback וזמני Dead-Time של $150\text{ ns}$.</li>
                        <li><strong>מערך חיישני זרם וירטואליים:</strong> הכוללים השהיות דגימה ורעש קוואנטיזציה של ממיר ADC בן 16 ביט.</li>
                    </ul>

                    <h3>תוצאות תגובה דינמית (Dynamic Response)</h3>
                    <p>
                        נבדקה תגובת המערכת בצעדי מומנט ומהירות חדים: תאוצה מ-$0$ ל-$580\text{ RPM}$, היפוך כיוון סיבוב ל-$-580\text{ RPM}$, והעמסה פתאומית של $100\%$ מומנט נומינלי.
                    </p>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/fig10_pmsm_dynamic_response_speed_torque.jpg" alt="Dynamic Response Speed & Torque" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 4.2:</strong> תגובה דינמית של מנוע ה-PMSM תחת בקרת OEPC: מהירות סיבוב (עליון), מומנט מנוע (אמצעי) וזרמי הפאזות (תחתון).</div>
                    </div>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/fig12_chil_realtime_pmsm_results.jpg" alt="C-HIL Real-Time Results" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 4.3:</strong> תוצאות מדידה גולמיות מאוסצילוסקופ ה-SCADA בזמן אמת: גלי זרם סינוסואידליים נקיים ללא עיוותי מעבר.</div>
                    </div>

                    <h3>אימות תחת חוסר איזון פיזי קיצוני ($\pm 25\%$)</h3>
                    <p>
                        אחד המבחנים הקריטיים שנערכו במעבדה היה יצירת אי-סימטריה פיזית קיצונית בעכבות המנוע על-ידי חיבור נגדים וסלילים טוריים בפאזה אחת בלבד ($\Delta R = +25\%$, $\Delta L = +25\%$).
                    </p>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/fig6_oepc_asymmetric_response.jpg" alt="OEPC Asymmetric Response" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 4.4:</strong> תגובת OEPC תחת אי-סימטריה של 25%: זרמי הפאזות נשארים מאוזנים לחלוטין תוך דיכוי של 98% מזרם ה-ZSC.</div>
                    </div>
                </section>

                <!-- ============================================================ -->
                <!-- CHAPTER 5: FAULT TOLERANCE (ITSC)                            -->
                <!-- ============================================================ -->
                <section class="chapter-section" id="ch-05">
                    <span class="chapter-badge">פרק 05</span>
                    <h2>חסינות אינהרנטית לתקלות פנימיות במנוע (ITSC)</h2>

                    <p>
                        קצר פנימי בין כריכות הסליל (<span class="en-term">Inter-Turn Short Circuit - ITSC</span>) הוא אחת התקלות ההרסניות ביותר במנועי PMSM. הזרם המושרה בכריכות המקוצרות עלול להגיע לפי 5-10 מהזרם הנומינלי, תוך יצירת חום קיצוני המוביל לשריפת בידוד המנוע ופריקת המגנטים הקבועים (<span class="en-term">Thermal Demagnetization</span>).
                    </p>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/fig13_fault_tolerance_itsc_oepc_vs_cbpwm.jpg" alt="Fault Tolerance ITSC: OEPC vs CBPWM" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 5.1:</strong> השוואת ביצועים תחת קצר פנימי (ITSC): בקרת CBPWM מסורתית חווה זינוק הרסני בזרם הלולאה (שמאל), בעוד שבקרת OEPC מדכאת את זרם התקלה תוך 2 מחזורי מיתוג (ימין).</div>
                    </div>

                    <h3>מנגנון החסינות האינהרנטי של אלגוריתם ה-OEPC</h3>
                    <p>
                        מרבית שיטות הבקרה המקובלות דורשות אלגוריתם גילוי תקלות נפרד (<span class="en-term">Fault Diagnostic Observer</span>) כדי לזהות קצר. לעומת זאת, בקרת OEPC פועלת באופן דד-ביט ישיר על שגיאות הזרם הרגעיות:
                    </p>
                    <ol class="num-list">
                        <li>ברגע התרחשות הקצר, מתח ה-Back-EMF בפאזה הפגועה מתעוות, ונוצרת שגיאת זרם גדולה ברמת המיקרו-שניות.</li>
                        <li>קוד העדיפות (EPC) מזהה מיד את הפאזה הפגועה כבעלת העדיפות העליונה ($Priority = 1$).</li>
                        <li>טבלת ה-LUT שולפת וקטור מיתוג המפעיל מתח נגדי בדיוק לכיוון השגיאה, ומאזנת מחדש את זרמי שאר הפאזות.</li>
                        <li>כתוצאה מכך, זרם התקלה המקומי מרוסן, והמנוע ממשיך לפעול בבטחה במצב שרידות (<span class="en-term">Limp-home Mode</span>).</li>
                    </ol>
                </section>

                <!-- ============================================================ -->
                <!-- CHAPTER 6: MOTOR CALIBRATION & ENCODER (OEMER QS 100S)       -->
                <!-- ============================================================ -->
                <section class="chapter-section" id="ch-06">
                    <span class="chapter-badge">פרק 06</span>
                    <h2>אפיון וכיול מנוע ה-PMSM המעבדתי ופענוח אינקודר (OEMER QS 100S)</h2>

                    <p>
                        לצורך השלב הניסויי המעבדתי המלא, נרכש מנוע סרוו תעשייתי מתקדם תוצרת <strong>OEMER (דגם QS 100S)</strong> המצויד בחיישן מיקום אבסולוטי אופטי בדיוק גבוה <strong>SICK SFM60 HIPERFACE</strong>.
                    </p>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/pmsm_motor_photo.jpeg" alt="OEMER QS100S Motor" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 6.1:</strong> מנוע ה-PMSM המעבדתי OEMER QS 100S בעמדת הבדיקה והכיול.</div>
                    </div>

                    <h3>מפרט טכני של מנוע OEMER QS 100S</h3>
                    <div class="table-container">
                        <table class="styled-table">
                            <thead>
                                <tr>
                                    <th>פרמטר</th>
                                    <th>ערך נומינלי</th>
                                    <th>יחידות</th>
                                    <th>משמעות בבקרת FOC / OEPC</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>מספר קטבים ($P$) / זוגות קטבים ($p$)</td>
                                    <td>$P = 4 \quad (p = 2)$</td>
                                    <td>-</td>
                                    <td>יחס זווית חשמלית למכנית: $\theta_e = 2 \cdot \theta_m$</td>
                                </tr>
                                <tr>
                                    <td>מהירות נומינלית ($n_n$)</td>
                                    <td>$580$</td>
                                    <td>$\text{RPM}$</td>
                                    <td>תדר חשמלי בסיסי: $f_e = 19.33\text{ Hz}$</td>
                                </tr>
                                <tr>
                                    <td>מומנט נומינלי ($T_n$)</td>
                                    <td>$12.5$</td>
                                    <td>$\text{Nm}$</td>
                                    <td>זרם פאזה נומינלי מקביל: $I_n \approx 7.2\text{ A}$</td>
                                </tr>
                                <tr>
                                    <td>התנגדות סטטור לפאזה ($R_s$)</td>
                                    <td>$1.42$</td>
                                    <td>$\Omega$</td>
                                    <td>קבוע זמן חשמלי $\tau_e = L / R$</td>
                                </tr>
                                <tr>
                                    <td>השראות ציר $d$ וציר $q$ ($L_d, L_q$)</td>
                                    <td>$L_d = 14.8\text{ mH}, L_q = 16.2\text{ mH}$</td>
                                    <td>$\text{mH}$</td>
                                    <td>בולטות מגנטית קלה ($\approx 9\%$)</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <h3>פרוטוקול כיול קטבים מלא ב-13 שלבים (13-Step Calibration Protocol)</h3>
                    <p>
                        על מנת לאפשר בקרת FOC מדויקת, נדרש לדעת בדיוק מוחלט את זווית ההיסט הזויתית ($\theta_{\text{offset}}$) שבין נקודת האפס האופטית של האינקודר לבין ציר השטף המגנטי של הרוטור ($d$-axis).
                    </p>
                    <p>
                        לשם כך פותח פרוטוקול מעבדתי קפדני בן 13 שלבים: הזרקת זרם DC מוגבל (כ-2A) ב-6 וקטורי מיתוג קבועים לאורך שני סיבובים חשמליים מלאים ($720^\circ_e$), המהווים בדיוק סיבוב מכני אחד של $360.00^\circ_m$:
                    </p>

                    <div class="math-block">
                        $$\theta_e = \left( 2 \cdot \theta_{m,\text{abs}} + \mathbf{58.98^\circ} \right) \pmod{360^\circ}$$
                        $$\mathbf{\theta_{\text{offset}} = 58.98^\circ \approx 59.0^\circ \quad (1.0295\text{ rad})}$$
                    </div>

                    <div class="alert-box alert-success">
                        <div class="alert-icon">🎯</div>
                        <div class="alert-content">
                            <h5>דיוק כיול פנומנלי של המדידות</h5>
                            <p>
                                סטיית התקן (RMS) שנמדדה על פני כל 13 השלבים היא <strong>$\pm 0.21^\circ$ בלבד</strong>, עם שגיאה מרבית של $\pm 0.34^\circ$. בסיום הסיבוב המלא (שלב 13' מול שלב 1) נרשמה התאמה מושלמת של <strong>$0.00^\circ$ שגיאה ($360.00^\circ$ סגירה)</strong>!
                            </p>
                        </div>
                    </div>

                    <h3>פתרון עכבת התקשורת במודל החומרה DFRobot DFR0845</h3>
                    <p>
                        במהלך חיבור מודול ה-RS485 המבודד מדגם DFR0845 מול כניסות ה-DIO של ה-Typhoon HIL404, התגלתה תופעה לפיה מתח ה-Logic LOW בקו ה-RXD ירד רק ל-2.5V במקום ל-0V עקב נגד Pull-Up פנימי של 10kΩ במעגל ה-Level Shifter של המודול.
                    </p>
                    <p>
                        הבעיה נפתרה באופן אלגנטי על-ידי חיבור נגד <strong>Pull-Down של $1\text{k}\Omega$</strong> בין פין `R` לבין הארקה `GND`. התנגדות זו הורידה את המתח הנמוך ל-$0.38\text{V}$ (רמת LOW תקנית לחלוטין), והתקשורת הטורית פועלת כעת ללא שגיאות ב-9600/115200 Baud.
                    </p>
                </section>

                <!-- ============================================================ -->
                <!-- CHAPTER 7: ALTIUM HARDWARE DESIGN                            -->
                <!-- ============================================================ -->
                <section class="chapter-section" id="ch-07">
                    <span class="chapter-badge">פרק 07</span>
                    <h2>תכנון ומימוש כרטיסי החומרה ב-Altium Designer</h2>

                    <p>
                        לצורך המעבר מסימולציית HIL לעבודה עם מנוע ומתח חיים במעבדה, תוכננו, פותחו ויוצרו 3 כרטיסי חומרה ייעודיים בתוכנת Altium Designer:
                    </p>

                    <div class="grid-3col">
                        <div class="info-card">
                            <h4>⚡ דרגת מפסקי GaN</h4>
                            <p><strong>פרויקט:</strong> <code>Power_Swech - GUN_ V2</code></p>
                            <p>דרגת מיתוג מהירה מבוססת טרנזיסטורי GaN HEMT בעלי התנגדות $R_{ds(on)}$ נמוכה במיוחד, דרייברים מבודדים וזמני מיתוג של פחות מ-$10\text{ ns}$.</p>
                        </div>
                        <div class="info-card">
                            <h4>🧲 חיישן זרם צף ומבודד</h4>
                            <p><strong>פרויקט:</strong> <code>Isolated_Current_Sensor _V2_1</code></p>
                            <p>מערך מדידת זרם מבודד גלוונית בריחוף גבוה, המבוסס על חיישני Hall/Shunt מהירים ומגברי בידוד אופטיים בדיוק גבוה עבור כל פאזה וזרם ה-ZSC.</p>
                        </div>
                        <div class="info-card">
                            <h4>📊 מעגל מדידת מתח גבוה</h4>
                            <p><strong>פרויקט:</strong> <code>Isolated HV Circuit - V2_1</code></p>
                            <p>כרטיס מדידת מתח דיפרנציאלי מבודד למדידת מתח קבלי הציפה ($V_{dc2}$) ומתחי ה-Phase-to-Phase עד $800\text{V}$.</p>
                        </div>
                    </div>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/hardware_setup_photo.jpg" alt="Laboratory Inverter & Altium Modules" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 7.1:</strong> מודול דרייבר מפסקי ה-GaN המהירים ומערך כרטיסי החומרה שתוכננו ב-Altium Designer ומותקנים במעבדה.</div>
                    </div>

                    <h3>עקרונות Layout ושיקולי תכנון אותות מהירים ב-Altium</h3>
                    <ul class="bullet-list">
                        <li><strong>מזעור השראות הלולאה (Parasitic Loop Inductance):</strong> בטרנזיסטורי GaN מהירים ($di/dt \gt 1000\ \text{A}/\mu\text{s}$), אפילו השראות פרזיטית של $2\text{ nH}$ בלולאת המיתוג גורמת ל-Overshoot מתח מסוכן. הלולאה תוכננה בשכבות פנימיות צמודות מעל מישור הארקה רציף.</li>
                        <li><strong>בידוד גלווני מלא (Galvanic Isolation):</strong> מרחקי Creepage ו-Clearance תוכננו לעמידה במתחי בידוד של מעל $3000\text{ V}_{\text{RMS}}$ בין צד הבקרה הנמוך (3.3V) לצד ההספק הגבוה.</li>
                        <li><strong>חיבור Kelvin Source:</strong> הפרדה מוחלטת בין מסלול הזרם הראשי של המפסק לבין מסלול אות הפיקוד של ה-Gate, למניעת מיתוגי שווא כתוצאה מנפילת מתח על השראות המקור.</li>
                    </ul>
                </section>

                <!-- ============================================================ -->
                <!-- CHAPTER 8: MECHANICAL CAD & DYNO BENCH                       -->
                <!-- ============================================================ -->
                <section class="chapter-section" id="ch-08">
                    <span class="chapter-badge">פרק 08</span>
                    <h2>המכלול המכני (SolidWorks CAD) ועמדת הדיינו</h2>

                    <p>
                        עבור עמדת הניסויים המעבדתית תוכנן מכלול מכני מלא בתוכנת SolidWorks (קובץ ראשי <span class="en-term">PMSM_Load_Stend.SLDASM</span>), המשלב את מנוע ה-OEMER QS 100S, מנוע העמסה נגדי (SEW), ומד מומנט אקסיאלי בדיוק גבוה:
                    </p>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/motor_inverter_cap1.png" alt="SolidWorks Motor Bed Assembly" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 8.1:</strong> מכלול שולחן הבדיקה המכני (SolidWorks): מנוע ה-PMSM, עריסת ההתקנה, צימוד גמיש ומד מומנט.</div>
                    </div>

                    <h3>מרכיבי עמדת הבדיקה המכנית</h3>
                    <ul class="bullet-list">
                        <li><strong>שולחן בדיקה (Machine Bed MV1004):</strong> מסד ברזל יצוק קשיח בעל חריצי T המונע רעידות ומבטיח שמירה על קו איפוס אקסיאלי מושלם בין הצירים.</li>
                        <li><strong>מד מומנט אקסיאלי מדגם T210 (100 Nm):</strong> חיישן מומנט דינמי בדיוק של $0.1\%$ המודד את המומנט והמהירות הרגעיים ומעבירם למערכת הדגימה.</li>
                        <li><strong>צימודים גמישים (Flexible Couplings BK2):</strong> מפצים על סטיות זוויתיות ואקסיאליות קלות של פחות מ-$0.05\text{ mm}$ ללא יצירת עומס צדדי על מיסבי המנוע.</li>
                    </ul>
                </section>

                <!-- ============================================================ -->
                <!-- CHAPTER 9: BENCHMARKING & CONCLUSIONS                        -->
                <!-- ============================================================ -->
                <section class="chapter-section" id="ch-09">
                    <span class="chapter-badge">פרק 09</span>
                    <h2>השוואת ביצועים כוללת (Benchmarking) ומסקנות</h2>

                    <p>
                        להלן טבלת השוואה כמותית מקיפה המרכזת את תוצאות הביצועים שנמדדו במעבדה וב-C-HIL עבור שיטת ה-OEPC המוצעת מול השיטות המקובלות בספרות המדעית:
                    </p>

                    <div class="table-container">
                        <table class="styled-table">
                            <thead>
                                <tr>
                                    <th>מדד ביצועים</th>
                                    <th>בקרת OEPC המוצעת</th>
                                    <th>שיטת TDM (חיתוך בזמן)</th>
                                    <th>CBPWM (מודולציה קלאסית)</th>
                                    <th>Dual Inverter (ספק כפול)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="highlight-row">
                                    <td><strong>תכולת הרמוניות בזרם (THD)</strong></td>
                                    <td><strong>1.85%</strong></td>
                                    <td>4.12%</td>
                                    <td>3.45%</td>
                                    <td>2.10%</td>
                                </tr>
                                <tr>
                                    <td><strong>דיכוי זרם סדרה אפס (ZSC)</strong></td>
                                    <td><strong>98.4% (זניח לחלוטין)</strong></td>
                                    <td>86.5%</td>
                                    <td>0% (דורש סלילי חניקה כבדים)</td>
                                    <td>אינו קיים (בגלל ספק מבודד)</td>
                                </tr>
                                <tr class="highlight-row">
                                    <td><strong>זמן תגובה בצעד מומנט</strong></td>
                                    <td><strong>0.45 ms</strong></td>
                                    <td>2.10 ms</td>
                                    <td>1.80 ms</td>
                                    <td>1.50 ms</td>
                                </tr>
                                <tr>
                                    <td><strong>תדר מיתוג ממוצע למפסק</strong></td>
                                    <td><strong>18.4 kHz (משתנה)</strong></td>
                                    <td>25.0 kHz (קבוע)</td>
                                    <td>20.0 kHz (קבוע)</td>
                                    <td>20.0 kHz (קבוע)</td>
                                </tr>
                                <tr class="highlight-row">
                                    <td><strong>מורכבות החומרה (עלות)</strong></td>
                                    <td><strong>נמוכה ביותר (ספק DC בודד)</strong></td>
                                    <td>נמוכה (ספק DC בודד)</td>
                                    <td>גבוהה (סלילי חניקה יקרים)</td>
                                    <td>גבוהה מאוד (שני ספקי DC מבודדים)</td>
                                </tr>
                                <tr>
                                    <td><strong>חסינות לקצר פנימי (ITSC)</strong></td>
                                    <td><strong>אינהרנטית ומיידית</strong></td>
                                    <td>מוגבלת</td>
                                    <td>ללא חסינות (התפתחות כשל)</td>
                                    <td>דורש בקר תקלה ייעודי</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <h3>תרומה אקדמית ופרסום מדעי</h3>
                    <p>
                        תוצאות המחקר סוכמו במאמר מדעי מקיף שהוגש לפרסום בכתב העת היוקרתי <strong>IEEE Transactions on Industrial Electronics (IEEE TIE, 2026)</strong> תחת הכותרת:
                    </p>
                    <div class="math-block" style="direction: ltr; text-align: left;">
                        "Hardware-Efficient Optimal Error-Priority Control for Series-End VSI With ZSC Suppression"
                    </div>
                </section>

                <!-- ============================================================ -->
                <!-- APPENDICES & DOCUMENTS HUB                                   -->
                <!-- ============================================================ -->
                <section class="chapter-section" id="ch-appendices">
                    <span class="chapter-badge">פרק 10</span>
                    <h2>נספחים ואינדקס דוחות הפרויקט</h2>

                    <p>
                        לעיון מעמיק בכל אחד מהמודולים הספציפיים, להלן גישה ישירה ל-11 הדוחות הטכניים המפורטים בפורמט HTML הזמינים בתיקיית הפרויקט:
                    </p>

                    <div class="table-container">
                        <table class="styled-table">
                            <thead>
                                <tr>
                                    <th>מסמך</th>
                                    <th>נושא הדוח הטכני</th>
                                    <th>פורמט</th>
                                    <th>קישור ישיר</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>DOC_01</td>
                                    <td>סיכום מאסטר: ציוד Typhoon HIL (404/402/DSP 180), חיישנים ומודול DFR0845</td>
                                    <td>HTML</td>
                                    <td><a href="HTML_Reports/DOC_01_PMSM_Master_Summary.html" target="_blank" style="color:var(--accent-cyan);">פתח מסמך ↗</a></td>
                                </tr>
                                <tr>
                                    <td>DOC_02</td>
                                    <td>מדריך חיווט והפעלה מקיף: אינקודר SICK, מודול DFR0845 ו-HIL404</td>
                                    <td>HTML</td>
                                    <td><a href="HTML_Reports/DOC_02_Wiring_and_Operation_Guide.html" target="_blank" style="color:var(--accent-cyan);">פתח מסמך ↗</a></td>
                                </tr>
                                <tr>
                                    <td>DOC_03</td>
                                    <td>הגדרות מפורטות למודל ה-TSE של Typhoon HIL וקוד ה-C</td>
                                    <td>HTML</td>
                                    <td><a href="HTML_Reports/DOC_03_TSE_Detailed_Settings.html" target="_blank" style="color:var(--accent-cyan);">פתח מסמך ↗</a></td>
                                </tr>
                                <tr>
                                    <td>DOC_04</td>
                                    <td>מפרט פרוטוקול HIPERFACE (RS-485 Half Duplex 9600 Baud)</td>
                                    <td>HTML</td>
                                    <td><a href="HTML_Reports/DOC_04_HIPERFACE_Protocol_Specification.html" target="_blank" style="color:var(--accent-cyan);">פתח מסמך ↗</a></td>
                                </tr>
                                <tr>
                                    <td>DOC_05</td>
                                    <td>מדריך חיווט לכרטיס MIKROE-2821 RS485 מול Typhoon HIL404</td>
                                    <td>HTML</td>
                                    <td><a href="HTML_Reports/DOC_05_MIKROE2821_RS485_Wiring_Guide.html" target="_blank" style="color:var(--accent-cyan);">פתח מסמך ↗</a></td>
                                </tr>
                                <tr>
                                    <td>DOC_06</td>
                                    <td>מדריך מלא וקונפיגורציה לאינקודר SICK SFM60 מול HIL404</td>
                                    <td>HTML</td>
                                    <td><a href="HTML_Reports/DOC_06_SICK_SFM60_HIL404_Complete_Guide.html" target="_blank" style="color:var(--accent-cyan);">פתח מסמך ↗</a></td>
                                </tr>
                                <tr>
                                    <td>DOC_07</td>
                                    <td>דוח סיכום פרויקט כולל ושלבי פעולה עתידיים</td>
                                    <td>HTML</td>
                                    <td><a href="HTML_Reports/DOC_07_PMSM_HIPERFACE_Complete_Project_Summary.html" target="_blank" style="color:var(--accent-cyan);">פתח מסמך ↗</a></td>
                                </tr>
                                <tr>
                                    <td>DOC_08</td>
                                    <td>מדריך כיול קטבים ומידע טכני על מנוע OEMER QS 100S</td>
                                    <td>HTML</td>
                                    <td><a href="HTML_Reports/DOC_08_Pole_Alignment_and_OEMER_QS100_Guide.html" target="_blank" style="color:var(--accent-cyan);">פתח מסמך ↗</a></td>
                                </tr>
                                <tr>
                                    <td>DOC_09</td>
                                    <td>פרוטוקול מדידות כיול קטבים ב-13 שלבים וניתוח שגיאות</td>
                                    <td>HTML</td>
                                    <td><a href="HTML_Reports/DOC_09_Pole_Alignment_Measurement_Protocol.html" target="_blank" style="color:var(--accent-cyan);">פתח מסמך ↗</a></td>
                                </tr>
                                <tr>
                                    <td>DOC_10</td>
                                    <td>דוח סיכום ניסוי סופי: קביעת היסט זוויתי של 58.98 מעלות</td>
                                    <td>HTML</td>
                                    <td><a href="HTML_Reports/DOC_10_Pole_Alignment_Final_Experiment_Summary.html" target="_blank" style="color:var(--accent-cyan);">פתח מסמך ↗</a></td>
                                </tr>
                                <tr>
                                    <td>DOC_11</td>
                                    <td>מדריך אינטגרציה מלא לכרטיס Digilent Pmod RS485 (5V CMOS)</td>
                                    <td>HTML</td>
                                    <td><a href="HTML_Reports/DOC_11_Digilent_Pmod_RS485_Integration_Guide.html" target="_blank" style="color:var(--accent-cyan);">פתח מסמך ↗</a></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <h3>קבצי שער רשמיים לתזה ומצגות</h3>
                    <ul class="bullet-list">
                        <li><strong>דף שער רשמי לתזה (Word OpenXML BiDi):</strong> <a href="עבודת_גמר_דף_שער_מקסים_רדקין_חדש_מתוקן.docx" style="color:var(--accent-cyan);">עבודת_גמר_דף_שער_מקסים_רדקין_חדש_מתוקן.docx</a></li>
                        <li><strong>דף שער אינטרנטי להדפסה (HTML A4):</strong> <a href="cover_page.html" target="_blank" style="color:var(--accent-cyan);">cover_page.html</a></li>
                        <li><strong>מצגת אינטראקטיבית מלאה (עברית RTL):</strong> <a href="OEPC_SE_VSI_PMSM_Presentation_HE.html" target="_blank" style="color:var(--accent-cyan);">OEPC_SE_VSI_PMSM_Presentation_HE.html</a></li>
                        <li><strong>מצגת אינטראקטיבית מלאה (אנגלית LTR):</strong> <a href="OEPC_SE_VSI_PMSM_Presentation.html" target="_blank" style="color:var(--accent-cyan);">OEPC_SE_VSI_PMSM_Presentation.html</a></li>
                    </ul>
                </section>

            </main>
        </div>
    </div>

    <!-- ==================================================================== -->
    <!-- JAVASCRIPT: NAVIGATION, SIMULATIONS & LOGIC                          -->
    <!-- ==================================================================== -->
    <script>
        // Reading Progress Bar
        window.addEventListener('scroll', () => {
            const docH = document.documentElement.scrollHeight - window.innerHeight;
            const scrolled = (window.scrollY / docH) * 100;
            document.getElementById('reading-progress').style.width = scrolled + '%';
            updateActiveSection();
        });

        // ScrollSpy for Sidebar TOC
        const sections = document.querySelectorAll('.chapter-section');
        const navLinks = document.querySelectorAll('.sidebar-menu a');
        const crumbElem = document.getElementById('active-crumb');

        function updateActiveSection() {
            let current = '';
            const scrollPos = window.scrollY + 120;
            sections.forEach(sec => {
                if (sec.offsetTop <= scrollPos) {
                    current = sec.getAttribute('id');
                }
            });

            navLinks.forEach(a => {
                a.classList.remove('active');
                if (a.getAttribute('href') === '#' + current) {
                    a.classList.add('active');
                    if (crumbElem) {
                        crumbElem.textContent = a.textContent.trim().replace(/^\d+\s*/, '');
                    }
                }
            });
        }

        // Theme Toggle (Light / Dark)
        function toggleTheme() {
            document.body.classList.toggle('light-theme');
            const isLight = document.body.classList.contains('light-theme');
            localStorage.setItem('pmsm_book_theme', isLight ? 'light' : 'dark');
        }

        if (localStorage.getItem('pmsm_book_theme') === 'light') {
            document.body.classList.add('light-theme');
        }

        // Sidebar Search
        function filterChapters() {
            const q = document.getElementById('chapter-search').value.toLowerCase();
            const items = document.querySelectorAll('.sidebar-menu li');
            items.forEach(li => {
                const txt = li.textContent.toLowerCase();
                li.style.display = txt.includes(q) ? '' : 'none';
            });
        }

        // Mobile Sidebar Toggle
        function toggleSidebar() {
            const sb = document.getElementById('book-sidebar');
            sb.classList.toggle('open');
        }

        // Modal Lightbox
        function openModal(src) {
            const modal = document.getElementById('img-modal');
            const img = document.getElementById('modal-img');
            img.src = src;
            modal.classList.add('active');
        }

        function closeModal() {
            document.getElementById('img-modal').classList.remove('active');
        }

        // ====================================================================
        // SIMULATION 1: JSXGRAPH IMPLEMENTATION
        // ====================================================================
        let jxgBoard = null;
        let pError = null;
        let empMode = 'auto';

        function initJsx() {
            if (typeof JXG === 'undefined') return;
            const container = document.getElementById('jxgbox-book');
            if (!container) return;

            jxgBoard = JXG.JSXGraph.initBoard('jxgbox-book', {
                boundingbox: [-2.2, 2.2, 2.2, -2.2],
                axis: false,
                grid: false,
                showNavigation: false,
                showCopyright: false,
                pan: { enabled: false },
                zoom: { enabled: false }
            });

            // Draw Voltage Hexagon
            const r = 1.6;
            const hexCoords = [];
            for (let i = 0; i <= 6; i++) {
                const ang = (i * 60) * (Math.PI / 180);
                hexCoords.push([r * Math.cos(ang), r * Math.sin(ang)]);
            }

            jxgBoard.create('polygon', hexCoords, {
                fillColor: 'rgba(59, 130, 246, 0.08)',
                borders: { strokeColor: 'rgba(0, 210, 255, 0.4)', strokeWidth: 2 }
            });

            // Coordinate axes
            jxgBoard.create('line', [[-2, 0], [2, 0]], { strokeColor: 'rgba(255, 255, 255, 0.15)', dash: 2 });
            jxgBoard.create('line', [[0, -2], [0, 2]], { strokeColor: 'rgba(255, 255, 255, 0.15)', dash: 2 });

            // Interactive Error Point
            pError = jxgBoard.create('point', [0.4, -0.6], {
                name: 'ε(α,β)',
                size: 6,
                color: '#00d2ff',
                strokeColor: '#ffffff',
                strokeWidth: 2
            });

            pError.on('drag', () => {
                const alpha = pError.X();
                const beta = pError.Y();
                // Clarke inverse
                const ea = alpha;
                const eb = -0.5 * alpha + (Math.sqrt(3) / 2) * beta;
                const ec = -0.5 * alpha - (Math.sqrt(3) / 2) * beta;

                document.getElementById('slider-ea').value = ea.toFixed(2);
                document.getElementById('slider-eb').value = eb.toFixed(2);
                document.getElementById('slider-ec').value = ec.toFixed(2);
                updateJsxLabels(ea, eb, ec);
            });
        }

        function setEmpMode(mode) {
            empMode = mode;
            document.querySelectorAll('#btn-emp-auto, #btn-emp-dm, #btn-emp-cm').forEach(b => b.classList.remove('active'));
            document.getElementById('btn-emp-' + mode).classList.add('active');
            updateJsxSim();
        }

        function updateJsxSim() {
            const ea = parseFloat(document.getElementById('slider-ea').value);
            const eb = parseFloat(document.getElementById('slider-eb').value);
            const ec = parseFloat(document.getElementById('slider-ec').value);
            const e0 = parseFloat(document.getElementById('slider-e0').value);

            // Clarke
            const alpha = ea - 0.5 * (eb + ec);
            const beta = (Math.sqrt(3) / 2) * (eb - ec);

            if (pError && jxgBoard) {
                pError.moveTo([alpha, beta]);
            }
            updateJsxLabels(ea, eb, ec, e0);
        }

        function updateJsxLabels(ea, eb, ec, e0 = 0.15) {
            document.getElementById('val-ea').textContent = ea.toFixed(2) + ' A';
            document.getElementById('val-eb').textContent = eb.toFixed(2) + ' A';
            document.getElementById('val-ec').textContent = ec.toFixed(2) + ' A';
            document.getElementById('val-e0').textContent = e0.toFixed(2) + ' A';

            // EPC sort
            const absA = Math.abs(ea), absB = Math.abs(eb), absC = Math.abs(ec);
            let epcStr = '000', epcDesc = 'ABC';
            if (absA >= absB && absB >= absC) { epcStr = '110'; epcDesc = 'ABC'; }
            else if (absA >= absC && absC >= absB) { epcStr = '100'; epcDesc = 'ACB'; }
            else if (absB >= absA && absA >= absC) { epcStr = '010'; epcDesc = 'BAC'; }
            else if (absB >= absC && absC >= absA) { epcStr = '011'; epcDesc = 'BCA'; }
            else if (absC >= absA && absA >= absB) { epcStr = '001'; epcDesc = 'CAB'; }
            else { epcStr = '000'; epcDesc = 'CBA'; }

            // ESC
            const sA = ea >= 0 ? '1' : '0';
            const sB = eb >= 0 ? '1' : '0';
            const sC = ec >= 0 ? '1' : '0';
            const escStr = `${sA}${sB}${sC}`;
            const escDesc = `${ea >= 0 ? '+' : '-'}${eb >= 0 ? '+' : '-'}${ec >= 0 ? '+' : '-'}`;

            // EMP
            let empVal = 1;
            if (empMode === 'auto') {
                empVal = Math.abs(e0) > 0.4 ? 0 : 1;
            } else if (empMode === 'cm') {
                empVal = 0;
            } else {
                empVal = 1;
            }

            document.getElementById('disp-epc').textContent = `${epcStr} (${epcDesc})`;
            document.getElementById('disp-esc').textContent = `${escStr} (${escDesc})`;
            document.getElementById('disp-emp').textContent = empVal === 1 ? '1 (DM Priority)' : '0 (CM Priority)';

            // Look up vector sample
            const sampleVectors = ['V1 (1001)', 'V2 (1010)', 'V3 (1101)', 'V4 (0110)', 'V5 (0101)', 'V6 (0011)'];
            const idx = (parseInt(epcStr, 2) + parseInt(escStr, 2) + empVal) % 6;
            document.getElementById('disp-vec').textContent = sampleVectors[idx];
        }

        // ====================================================================
        // SIMULATION 2: 60 FPS OSCILLOSCOPE ENGINE
        // ====================================================================
        const timeCanvas = document.getElementById('osc-time-canvas');
        const xyCanvas = document.getElementById('osc-xy-canvas');
        const tCtx = timeCanvas ? timeCanvas.getContext('2d') : null;
        const xyCtx = xyCanvas ? xyCanvas.getContext('2d') : null;

        let oscRunning = true;
        let oscAlgo = 'oepc';
        let oscAsym = 0;
        let oscRpm = 580;
        let oscZscWeight = 1.0;
        let simTime = 0;
        const timeBufferA = [], timeBufferB = [], timeBufferC = [], timeBufferZ = [];
        const maxPoints = 240;

        function setOscAlgorithm(algo) {
            oscAlgo = algo;
            document.querySelectorAll('#btn-ctrl-oepc, #btn-ctrl-tdm, #btn-ctrl-pwm').forEach(b => b.classList.remove('active'));
            document.getElementById('btn-ctrl-' + algo).classList.add('active');
            updateOscTelemetry();
        }

        function updateOscParams() {
            oscAsym = parseFloat(document.getElementById('slider-osc-asym').value) / 100;
            oscRpm = parseFloat(document.getElementById('slider-osc-rpm').value);
            oscZscWeight = parseFloat(document.getElementById('slider-osc-zsc').value) / 100;

            document.getElementById('val-osc-asym').textContent = (oscAsym * 100).toFixed(0) + '%';
            document.getElementById('val-osc-rpm').textContent = oscRpm.toFixed(0) + ' RPM';
            document.getElementById('val-osc-zsc').textContent = (oscZscWeight * 100).toFixed(0) + '%';
            updateOscTelemetry();
        }

        function toggleOscRun() {
            oscRunning = !oscRunning;
            document.getElementById('btn-osc-run').textContent = oscRunning ? '⏸️ השהה' : '▶️ הפעל';
        }

        function resetOsc() {
            timeBufferA.length = 0;
            timeBufferB.length = 0;
            timeBufferC.length = 0;
            timeBufferZ.length = 0;
            simTime = 0;
        }

        function updateOscTelemetry() {
            let thd = '1.85%', zscP = '0.04 A', fsw = '18.4 kHz', torq = '12.5 Nm';
            if (oscAlgo === 'tdm') {
                thd = (4.12 + Math.abs(oscAsym) * 3).toFixed(2) + '%';
                zscP = (0.25 * (1 - oscZscWeight * 0.8) + Math.abs(oscAsym) * 0.4).toFixed(2) + ' A';
                fsw = '25.0 kHz';
                torq = (12.2 - Math.abs(oscAsym) * 1.5).toFixed(1) + ' Nm';
            } else if (oscAlgo === 'pwm') {
                thd = (3.45 + Math.abs(oscAsym) * 4).toFixed(2) + '%';
                zscP = (0.85 * (1 - oscZscWeight * 0.5) + Math.abs(oscAsym) * 0.8).toFixed(2) + ' A';
                fsw = '20.0 kHz';
                torq = (11.8 - Math.abs(oscAsym) * 2.2).toFixed(1) + ' Nm';
            } else {
                // OEPC
                thd = (1.85 + Math.abs(oscAsym) * 0.8).toFixed(2) + '%';
                zscP = (0.04 * (1 - oscZscWeight * 0.9) + Math.abs(oscAsym) * 0.08).toFixed(2) + ' A';
                fsw = (18.4 + Math.abs(oscAsym) * 2).toFixed(1) + ' kHz';
                torq = (12.5 - Math.abs(oscAsym) * 0.3).toFixed(1) + ' Nm';
            }

            document.getElementById('disp-thd').textContent = thd;
            document.getElementById('disp-zsc-peak').textContent = zscP;
            document.getElementById('disp-fsw').textContent = fsw;
            document.getElementById('disp-torque').textContent = torq;
        }

        function oscStep() {
            if (!oscRunning || !tCtx || !xyCtx) {
                requestAnimationFrame(oscStep);
                return;
            }

            // Canvas resizing
            if (timeCanvas.width !== timeCanvas.clientWidth) {
                timeCanvas.width = timeCanvas.clientWidth;
                timeCanvas.height = timeCanvas.clientHeight;
            }
            if (xyCanvas.width !== xyCanvas.clientWidth) {
                xyCanvas.width = xyCanvas.clientWidth;
                xyCanvas.height = xyCanvas.clientHeight;
            }

            const freq = (oscRpm / 60) * 2; // p=2
            const omega = 2 * Math.PI * freq;
            const dt = 0.0004;
            simTime += dt;

            // Generate realistic currents
            let rippleAmp = oscAlgo === 'oepc' ? 0.08 : (oscAlgo === 'tdm' ? 0.22 : 0.16);
            let zscFactor = oscAlgo === 'oepc' ? (1 - oscZscWeight * 0.95) : (oscAlgo === 'tdm' ? (1 - oscZscWeight * 0.75) : 1.0);
            
            let noiseA = (Math.random() - 0.5) * rippleAmp;
            let noiseB = (Math.random() - 0.5) * rippleAmp;
            let noiseC = (Math.random() - 0.5) * rippleAmp;

            let ampA = 1.0 * (1 + oscAsym);
            let ampB = 1.0;
            let ampC = 1.0 * (1 - oscAsym * 0.5);

            let ia = ampA * Math.sin(omega * simTime) + noiseA;
            let ib = ampB * Math.sin(omega * simTime - (2 * Math.PI / 3)) + noiseB;
            let ic = ampC * Math.sin(omega * simTime + (2 * Math.PI / 3)) + noiseC;

            let zsc = ((ia + ib + ic) / 3) * zscFactor + (Math.random() - 0.5) * 0.02;

            timeBufferA.push(ia);
            timeBufferB.push(ib);
            timeBufferC.push(ic);
            timeBufferZ.push(zsc);

            if (timeBufferA.length > maxPoints) {
                timeBufferA.shift();
                timeBufferB.shift();
                timeBufferC.shift();
                timeBufferZ.shift();
            }

            // Draw Time Domain
            const w = timeCanvas.width, h = timeCanvas.height;
            tCtx.fillStyle = '#050811';
            tCtx.fillRect(0, 0, w, h);

            // Grid lines
            tCtx.strokeStyle = 'rgba(255, 255, 255, 0.06)';
            tCtx.lineWidth = 1;
            for (let y = 0; y < h; y += h / 6) {
                tCtx.beginPath(); tCtx.moveTo(0, y); tCtx.lineTo(w, y); tCtx.stroke();
            }
            for (let x = 0; x < w; x += w / 8) {
                tCtx.beginPath(); tCtx.moveTo(x, 0); tCtx.lineTo(x, h); tCtx.stroke();
            }

            // Centerline
            tCtx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
            tCtx.beginPath(); tCtx.moveTo(0, h / 2); tCtx.lineTo(w, h / 2); tCtx.stroke();

            // Trace function
            const drawTrace = (buf, color, lw = 1.5) => {
                tCtx.strokeStyle = color;
                tCtx.lineWidth = lw;
                tCtx.beginPath();
                const stepX = w / (maxPoints - 1);
                for (let i = 0; i < buf.length; i++) {
                    const py = (h / 2) - buf[i] * (h / 3.4);
                    if (i === 0) tCtx.moveTo(0, py);
                    else tCtx.lineTo(i * stepX, py);
                }
                tCtx.stroke();
            };

            drawTrace(timeBufferA, '#ef4444'); // Phase A: Red
            drawTrace(timeBufferB, '#10b981'); // Phase B: Green
            drawTrace(timeBufferC, '#3b82f6'); // Phase C: Blue
            drawTrace(timeBufferZ, '#f59e0b', 2.2); // ZSC: Amber

            // Legend
            tCtx.font = '11px Fira Code';
            tCtx.fillStyle = '#ef4444'; tCtx.fillText('— Ia', 10, 20);
            tCtx.fillStyle = '#10b981'; tCtx.fillText('— Ib', 55, 20);
            tCtx.fillStyle = '#3b82f6'; tCtx.fillText('— Ic', 100, 20);
            tCtx.fillStyle = '#f59e0b'; tCtx.fillText('— i0 (ZSC)', 145, 20);

            // Draw XY Lissajous (Alpha-Beta Orbit)
            const xw = xyCanvas.width, xh = xyCanvas.height;
            xyCtx.fillStyle = '#060a15';
            xyCtx.fillRect(0, 0, xw, xh);

            xyCtx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
            xyCtx.beginPath();
            xyCtx.arc(xw / 2, xh / 2, Math.min(xw, xh) * 0.38, 0, 2 * Math.PI);
            xyCtx.stroke();

            // Coordinate cross
            xyCtx.beginPath(); xyCtx.moveTo(xw / 2, 0); xyCtx.lineTo(xw / 2, xh); xyCtx.stroke();
            xyCtx.beginPath(); xyCtx.moveTo(0, xh / 2); xyCtx.lineTo(xw, xh / 2); xyCtx.stroke();

            xyCtx.strokeStyle = '#00d2ff';
            xyCtx.lineWidth = 2;
            xyCtx.beginPath();
            for (let i = 0; i < timeBufferA.length; i++) {
                const a = timeBufferA[i];
                const b = timeBufferB[i];
                const c = timeBufferC[i];
                const alpha = a - 0.5 * (b + c);
                const beta = (Math.sqrt(3) / 2) * (b - c);
                const px = (xw / 2) + alpha * (xw * 0.28);
                const py = (xh / 2) - beta * (xh * 0.28);
                if (i === 0) xyCtx.moveTo(px, py);
                else xyCtx.lineTo(px, py);
            }
            xyCtx.stroke();

            xyCtx.font = '11px Rubik';
            xyCtx.fillStyle = '#00d2ff';
            xyCtx.fillText('מסלול α-β Orbit', 10, 20);

            requestAnimationFrame(oscStep);
        }

        // Initialize on load
        window.addEventListener('load', () => {
            initJsx();
            updateJsxSim();
            updateOscParams();
            requestAnimationFrame(oscStep);
        });
    </script>
</body>
</html>
'''

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    print("Generating comprehensive HTML books...")
    content = get_book_html()
    
    with open(OUTPUT_HE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Generated Hebrew book ({len(content)} bytes)")
    
    with open(OUTPUT_EN, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Generated English-named link: PMSM_Project_Book.html")

if __name__ == "__main__":
    main()
