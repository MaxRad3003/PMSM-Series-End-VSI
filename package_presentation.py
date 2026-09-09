"""
package_presentation.py
Pack the entire OEPC Presentation project into a clean, standalone, 100% offline-ready distribution package for the project advisor:
1. Creates directory 'OEPC_PMSM_Presentation_Package' (and Hebrew alias 'ערכת_מצגת_למנחה_OEPC_PMSM').
2. Ensures all assets, images, JSXGraph, and offline MathJax are included.
3. Generates 1-click Windows batch launchers for Hebrew & English.
4. Generates an elegant 'START_HERE_Advisor_Portal.html' (and Hebrew 'התחל_כאן_פורטל_למנחה.html').
5. Generates 'README_Advisor_Guide.txt' and 'README_מדריך_למנחה_הפרויקט.txt'.
6. Builds a rock-solid ZIP archive: 'OEPC_PMSM_Presentation_For_Advisor.zip'.
"""

import os
import shutil
import zipfile
from pathlib import Path

PMSM_DIR = Path(__file__).resolve().parent
PACKAGE_NAME = "OEPC_PMSM_Presentation_Package"
DIST_DIR = PMSM_DIR / PACKAGE_NAME
HE_DIST_DIR = PMSM_DIR / "ערכת_מצגת_למנחה_OEPC_PMSM"
ZIP_FILE = PMSM_DIR / "OEPC_PMSM_Presentation_For_Advisor.zip"

PORTAL_HTML = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ערכת מצגת למנחה הפרויקט – בקרת OEPC לממיר Series-End VSI</title>
    <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700;800&family=Fira+Code:wght@500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #070b14;
            --bg-card: rgba(13, 22, 41, 0.95);
            --border-color: rgba(0, 210, 255, 0.25);
            --accent-cyan: #00d2ff;
            --accent-gold: #f6d365;
            --accent-green: #00ff88;
            --text-primary: #ffffff;
            --text-secondary: #a0aec0;
            --text-muted: #718096;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg-base);
            color: var(--text-primary);
            font-family: 'Rubik', sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 30px 20px;
            background-image: 
                radial-gradient(circle at 90% 15%, rgba(58, 123, 213, 0.18) 0%, transparent 45%),
                radial-gradient(circle at 10% 85%, rgba(157, 80, 187, 0.18) 0%, transparent 45%),
                radial-gradient(circle at 50% 50%, rgba(0, 210, 255, 0.06) 0%, transparent 60%);
        }
        .portal-wrapper {
            width: 100%;
            max-width: 1100px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 35px 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7), 0 0 30px rgba(0, 210, 255, 0.2);
            display: flex;
            flex-direction: column;
            gap: 25px;
        }
        .header-section {
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 20px;
        }
        .badge-tag {
            display: inline-block;
            padding: 4px 12px;
            background: rgba(0, 210, 255, 0.15);
            border: 1px solid rgba(0, 210, 255, 0.4);
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            color: var(--accent-cyan);
            margin-bottom: 12px;
        }
        h1 {
            font-size: 26px;
            font-weight: 800;
            line-height: 1.35;
            color: #ffffff;
            margin-bottom: 8px;
        }
        .subtitle {
            font-size: 15px;
            color: var(--text-secondary);
            line-height: 1.5;
        }
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
        }
        .portal-card {
            background: rgba(8, 14, 28, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 22px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 16px;
            transition: transform 0.25s, border-color 0.25s, box-shadow 0.25s;
        }
        .portal-card:hover {
            transform: translateY(-3px);
            border-color: var(--accent-cyan);
            box-shadow: 0 10px 30px rgba(0, 210, 255, 0.18);
        }
        .card-top {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .card-icon-title {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .card-icon {
            font-size: 24px;
        }
        .card-title {
            font-size: 17px;
            font-weight: 700;
            color: #ffffff;
        }
        .card-desc {
            font-size: 13.5px;
            color: var(--text-secondary);
            line-height: 1.55;
        }
        .feature-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 6px;
            font-size: 12.5px;
            color: var(--text-muted);
            margin-top: 5px;
        }
        .feature-list li {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .feature-list li::before {
            content: "✓";
            color: var(--accent-green);
            font-weight: bold;
        }
        .action-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: 12px 18px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 700;
            font-family: 'Rubik', sans-serif;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.2s;
            border: 1px solid transparent;
        }
        .btn-primary {
            background: linear-gradient(135deg, #00d2ff, #3a7bd5);
            color: #ffffff;
            box-shadow: 0 4px 18px rgba(0, 210, 255, 0.35);
        }
        .btn-primary:hover {
            box-shadow: 0 6px 24px rgba(0, 210, 255, 0.55);
            transform: scale(1.02);
        }
        .btn-secondary {
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(255, 255, 255, 0.15);
            color: #ffffff;
        }
        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.12);
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
        }
        .instructions-panel {
            background: rgba(10, 16, 32, 0.95);
            border: 1px dashed rgba(246, 211, 101, 0.35);
            border-radius: 12px;
            padding: 18px 22px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .inst-title {
            font-size: 14px;
            font-weight: 700;
            color: var(--accent-gold);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .inst-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 14px;
            font-size: 13px;
            color: var(--text-secondary);
            line-height: 1.5;
        }
        .inst-item strong {
            color: #ffffff;
        }
        .footer-credits {
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            padding-top: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            font-size: 12.5px;
            color: var(--text-muted);
        }
        .authors-tag {
            color: var(--accent-cyan);
            font-weight: 600;
        }
        kbd {
            background: rgba(255, 255, 255, 0.12);
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            font-family: 'Fira Code', monospace;
            font-size: 11.5px;
            color: #fff;
        }
    </style>
</head>
<body>

<div class="portal-wrapper">
    <!-- Header -->
    <div class="header-section">
        <span class="badge-tag">⚡ המכללה האקדמית להנדסה ע"ש סמי שמעון (SCE) • פרויקט מחקר IEEE TIE</span>
        <h1>ערכת בדיקה למנחה הפרויקט – בקרת OEPC לממיר Series-End VSI</h1>
        <div class="subtitle">
            בקרה אופטימלית מבוססת תעדוף שגיאה (OEPC) למנועי PMSM ודיכוי זרמי סדרה אפס (ZSC) | אימות C-HIL מעבדתי ומדידות פיזיקליות.
        </div>
    </div>

    <!-- Cards Grid -->
    <div class="cards-grid">
        <!-- Card 1: Interactive Hebrew Presentation -->
        <div class="portal-card" style="border-color: rgba(0, 210, 255, 0.4);">
            <div class="card-top">
                <div class="card-icon-title">
                    <span class="card-icon">&#x1F4CA;</span>
                    <div class="card-title" style="color: var(--accent-cyan);">מצגת אינטראקטיבית בעברית (מומלץ)</div>
                </div>
                <div class="card-desc">
                    המצגת הראשית והמלאה. כוללת סימולציות חיות, מפענח 96-LUT אינטראקטיבי, אוסצילוסקופ זרמים בזמן אמת, וכפתור מסך מלא.
                </div>
                <ul class="feature-list" dir="ltr" style="text-align: left;">
                    <li>שקף 6: מפענח טבלת 96 המצבים ומישור &alpha;&minus;&beta; ב-JSXGraph</li>
                    <li>שקף 10: סימולטור PMSM מיוצב (Triggered) והשוואת OEPC מול TDM ו-PWM</li>
                    <li>100% עצמאי ועובד ללא חיבור לאינטרנט (Offline-Ready)</li>
                </ul>
            </div>
            <a href="OEPC_SE_VSI_PMSM_Presentation_HE.html" class="action-btn btn-primary" target="_blank">
                ▶ פתח מצגת אינטראקטיבית (עברית)
            </a>
        </div>

        <!-- Card 2: Interactive English Presentation -->
        <div class="portal-card" dir="ltr" style="text-align: left;">
            <div class="card-top">
                <div class="card-icon-title">
                    <span class="card-icon">&#x1F310;</span>
                    <div class="card-title">English Interactive Presentation</div>
                </div>
                <div class="card-desc">
                    גרסה מלאה באנגלית התואמת לנוסח מאמר המחקר בכתב העת IEEE Transactions on Industrial Electronics.
                </div>
                <ul class="feature-list">
                    <li>Full IEEE Transactions on Industrial Electronics terminology</li>
                    <li>Interactive 96-state LUT decoder and real-time simulator</li>
                    <li>Keyboard navigation and Fullscreen mode with <kbd>F</kbd> key</li>
                </ul>
            </div>
            <a href="OEPC_SE_VSI_PMSM_Presentation.html" class="action-btn btn-secondary" target="_blank">
                ▶ Open English Presentation
            </a>
        </div>

        <!-- Card 3: PowerPoint Presentations (PPTX) -->
        <div class="portal-card">
            <div class="card-top">
                <div class="card-icon-title">
                    <span class="card-icon">📊</span>
                    <div class="card-title">קובצי PowerPoint (PPTX)</div>
                </div>
                <div class="card-desc">
                    גרסאות PowerPoint סטנדרטיות להקרנה בכיתה, להרצאות או לעריכה נוספת ב-Microsoft Office / Google Slides.
                </div>
                <ul class="feature-list">
                    <li>כולל את כל 18 השקפים, האיורים המעבדתיים ותרשימי הזרימה</li>
                    <li>טקסטים ומבנה שקופיות מעוצבים ומוכנים להרצאה</li>
                </ul>
            </div>
            <div style="display: flex; gap: 8px;">
                <a href="OEPC_Series_End_PMSM_Presentation_HE.pptx" class="action-btn btn-secondary" style="flex:1; font-size:12.5px;">
                    📥 מצגת עברית (PPTX)
                </a>
                <a href="OEPC_Series_End_PMSM_Presentation.pptx" class="action-btn btn-secondary" style="flex:1; font-size:12.5px;">
                    📥 English PPTX
                </a>
            </div>
        </div>
    </div>

    <!-- Supervisor Guidance Panel -->
    <div class="instructions-panel">
        <div class="inst-title">
            <span>💡 דגשים והנחיות ניווט לבדיקת המנחה:</span>
        </div>
        <div class="inst-grid">
            <div class="inst-item">
                <strong>⌨️ ניווט נוח במצגת:</strong><br>
                ניתן לעבור בין שקפים באמצעות מקשי החצים <kbd>→</kbd> <kbd>←</kbd> במקלדת, או בעזרת כפתורי הניווט.
            </div>
            <div class="inst-item">
                <strong>⛶ מסך מלא (Fullscreen):</strong><br>
                לחץ על כפתור <kbd>⛶ מסך מלא</kbd> בראש או בתחתית השקף, או הקש על המקש <kbd>F</kbd> להרחבה מלאה.
            </div>
            <div class="inst-item">
                <strong>⚙️ הדמיית שקף 6 (מפענח LUT):</strong><br>
                כוונן את 4 סליידרי שגיאות הפאזה וה-ZSC, או בחר בתרחיש מוכן לבדיקת תעדוף סדרה אפס (CM) מול דיפרנציאלי (DM).
            </div>
            <div class="inst-item">
                <strong>📈 הדמיית שקף 10 (סימולטור PMSM):</strong><br>
                השווה בלחיצה אחת בין OEPC (דיכוי מלא), TDM (ריפל גבוה) ו-PWM (עיוות קשה). השתמש במצב <em>גל מיוצב</em> לצפייה נינוחה.
            </div>
        </div>
    </div>

    <!-- Footer Credits -->
    <div class="footer-credits">
        <div>
            סטודנט ומבצע החומרה: <span class="authors-tag">מקסים רדקין</span> | מנחה הפרויקט: <span class="authors-tag">ד"ר אלי גד ברבי</span> | שותף מחקרי: <span class="authors-tag">פרופ' דמיטרי ביימל</span>
        </div>
        <div>
            SCE Department of Electrical & Electronics Engineering • 2026
        </div>
    </div>
</div>

</body>
</html>
"""

BAT_HE = """@echo off
chcp 65001 > nul
echo ========================================================
echo  הפעלת מצגת אינטראקטיבית - בקרת OEPC לממיר Series-End
echo ========================================================
echo.
echo פותח את המצגת האינטראקטיבית בעברית בדפדפן ברירת המחדל...
start "" "OEPC_SE_VSI_PMSM_Presentation_HE.html"
exit
"""

BAT_EN = """@echo off
chcp 65001 > nul
echo ========================================================
echo  Launching OEPC Series-End VSI Presentation (English)
echo ========================================================
echo.
echo Opening interactive presentation in default browser...
start "" "OEPC_SE_VSI_PMSM_Presentation.html"
exit
"""

BAT_PORTAL = """@echo off
chcp 65001 > nul
echo ========================================================
echo  ערכת בדיקה למנחה הפרויקט - פורטל ראשי
echo ========================================================
echo.
start "" "START_HERE_Advisor_Portal.html"
exit
"""

README_TEXT = """================================================================================
ערכת מצגת למנחה הפרויקט - בקרת OEPC לממיר Series-End VSI ומנועי PMSM
המכללה האקדמית להנדסה ע"ש סמי שמעון (SCE)
מחקר מאמר IEEE Transactions on Industrial Electronics
================================================================================

שלום רב למנחה הפרויקט,

ערכה זו מרכזת את כלל תוצרי המצגת האינטראקטיבית וקובצי ה-PowerPoint לבדיקתך.

--------------------------------------------------------------------------------
1. קבצים עיקריים בערכה:
--------------------------------------------------------------------------------
- START_HERE_Advisor_Portal.html / התחל_כאן_פורטל_למנחה.html
  פורטל ראשי מעוצב המאפשר פתיחה בלחיצה אחת של כל גרסאות המצגת (עברית, אנגלית, PPTX)
  והסבר על קיצורי המקשים וההדמיות.

- Open_Presentation_HE.bat / הפעלת_מצגת_אינטראקטיבית_עברית.bat
  קובץ הפעלה מהיר ב-Windows (לחיצה כפולה) לפתיחת המצגת האינטראקטיבית בעברית בדפדפן.

- Open_Presentation_EN.bat
  קובץ הפעלה מהיר לפתיחת המצגת האינטראקטיבית באנגלית.

- OEPC_SE_VSI_PMSM_Presentation_HE.html
  המצגת האינטראקטיבית הראשית בעברית (18 שקפים) הכוללת את כל הסימולציות.

- OEPC_SE_VSI_PMSM_Presentation.html
  מצגת אינטראקטיבית מקבילה באנגלית.

- OEPC_Series_End_PMSM_Presentation_HE.pptx
  קובץ PowerPoint בעברית (18 שקפים) להקרנה או עריכה ב-Microsoft Office.

- OEPC_Series_End_PMSM_Presentation.pptx
  קובץ PowerPoint באנגלית (18 שקפים).

- presentation_assets/
  תיקיית המדיה הכוללת את כל האיורים הניסויים, תמונות הסטאפ המעבדתי (מנוע ה-PMSM
  החדש שנרכש, עמדת ה-C-HIL בטייפון, ממיר ה-GaN), וכן ספריות מתמטיות להפעלה מלאה Offline.

--------------------------------------------------------------------------------
2. דגשים בהדמיות האינטראקטיביות לבדיקתך:
--------------------------------------------------------------------------------
* שקף 6 - מפענח עקרון הפעולה של OEPC וטבלת 96-LUT:
  - כולל לוח אינטראקטיבי של משושה המתחים ומישור אלפא-בטא (JSXGraph).
  - ניתן לשנות את שגיאות הזרם וה-ZSC בארבעה סליידרים או לבחור תרחיש מוכן
    (נומינלי, חריגת ZSC, אי-סימטריה של 25%, קצר ITSC).
  - המפענח מציג בזמן אמת את החלטת האלגוריתם, מצב המיתוג הנבחר [L1 L2 L3 L4],
    וההסבר המדויק לעליונות OEPC על פני שיטת TDM.

* שקף 10 - סימולטור דינמי של מנוע ה-PMSM ואוסצילוסקופ בזמן אמת:
  - השוואה חיה בין שלוש שיטות: OEPC (מוצע), TDM קלאסי, ו-PWM קונבנציונלי.
  - מסלול וקטור המרחב אלפא-בטא (Lissajous Hodograph) מציג בבירור את ההבדל
    בין מעגל מושלם ב-OEPC לבין אליפסה מעוותת ופעימות מומנט ב-PWM.
  - נוסף מתג "גל מיוצב (Triggered)" המייצב את האותות לתצוגה חדה ונינוחה.

* כפתור מסך מלא (Fullscreen):
  - ניתן להקליק על כפתור "מסך מלא" בכותרת העליונה או בסרגל הניווט, או להקיש F במקלדת.

--------------------------------------------------------------------------------
3. קרדיטים ופרטי הפרויקט:
--------------------------------------------------------------------------------
- סטודנט ומבצע אימות החומרה: מקסים רדקין (M.Sc candidate)
- מנחה הפרויקט: ד"ר אלי גד ברבי
- שותף מחקרי: פרופ' דמיטרי ביימל
- מוסד: המכללה האקדמית להנדסה ע"ש סמי שמעון (SCE)

בברכה,
מקסים רדקין
"""

def build_package():
    print(f"Building package at: {DIST_DIR} ...")
    
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Copy Assets
    assets_src = PMSM_DIR / "presentation_assets"
    assets_dst = DIST_DIR / "presentation_assets"
    if assets_src.exists():
        shutil.copytree(assets_src, assets_dst, dirs_exist_ok=True)
        print("  [+] Copied presentation_assets")

    # 2. Copy HTML presentations with local MathJax
    html_files = [
        "OEPC_SE_VSI_PMSM_Presentation_HE.html",
        "OEPC_SE_VSI_PMSM_Presentation.html"
    ]
    for hf in html_files:
        src = PMSM_DIR / hf
        dst = DIST_DIR / hf
        if src.exists():
            with open(src, 'r', encoding='utf-8') as f:
                c = f.read()
            if 'presentation_assets/tex-mml-chtml.js' not in c:
                c = c.replace(
                    '<script id="MathJax-script"',
                    '<script src="presentation_assets/tex-mml-chtml.js"></script>\n    <script id="MathJax-script"'
                )
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f"  [+] Prepared & copied {hf}")

    # 3. Copy PPTX files
    pptx_files = [
        "OEPC_Series_End_PMSM_Presentation_HE.pptx",
        "OEPC_Series_End_PMSM_Presentation.pptx"
    ]
    for pf in pptx_files:
        src = PMSM_DIR / pf
        dst = DIST_DIR / pf
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  [+] Copied {pf}")

    # 4. Create Portal HTML
    with open(DIST_DIR / "START_HERE_Advisor_Portal.html", 'w', encoding='utf-8') as f:
        f.write(PORTAL_HTML)
    with open(DIST_DIR / "התחל_כאן_פורטל_למנחה.html", 'w', encoding='utf-8') as f:
        f.write(PORTAL_HTML)
    print("  [+] Created Portal HTML files")

    # 5. Create Batch Launchers
    with open(DIST_DIR / "Open_Presentation_HE.bat", 'w', encoding='utf-8') as f:
        f.write(BAT_HE)
    with open(DIST_DIR / "הפעלת_מצגת_אינטראקטיבית_עברית.bat", 'w', encoding='utf-8') as f:
        f.write(BAT_HE)
    with open(DIST_DIR / "Open_Presentation_EN.bat", 'w', encoding='utf-8') as f:
        f.write(BAT_EN)
    with open(DIST_DIR / "Open_Advisor_Portal.bat", 'w', encoding='utf-8') as f:
        f.write(BAT_PORTAL)
    print("  [+] Created 1-click batch launcher scripts")

    # 6. Create README
    with open(DIST_DIR / "README_Advisor_Guide.txt", 'w', encoding='utf-8') as f:
        f.write(README_TEXT)
    with open(DIST_DIR / "README_מדריך_למנחה_הפרויקט.txt", 'w', encoding='utf-8') as f:
        f.write(README_TEXT)
    print("  [+] Created README files")

    # Mirror to Hebrew directory
    shutil.copytree(DIST_DIR, HE_DIST_DIR, dirs_exist_ok=True)
    print("  [+] Mirrored to Hebrew folder name")

    # 7. Create ZIP Archive with clean ASCII root
    print(f"Creating ZIP archive at {ZIP_FILE.name} ...")
    if ZIP_FILE.exists():
        ZIP_FILE.unlink()

    with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(DIST_DIR):
            for file in files:
                file_path = Path(root) / file
                # Write inside archive with root PACKAGE_NAME
                rel_path = file_path.relative_to(DIST_DIR)
                arcname = str(Path(PACKAGE_NAME) / rel_path).replace("\\", "/")
                zf.write(file_path, arcname)

    print(f"  [DONE] Created ZIP package: {ZIP_FILE.name} ({ZIP_FILE.stat().st_size // 1024} KB)")

if __name__ == "__main__":
    build_package()
