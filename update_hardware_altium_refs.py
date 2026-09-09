"""
Add Altium hardware design references to Slide 3 and Slide 15 across all presentations:
- Power_Swech - GUN_ V2
- Isolated_Current_Sensor _V2_1
"""

from pathlib import Path

PMSM_DIR = Path(r"c:\Users\maximr\OneDrive - ac.sce.ac.il\Barabi\2025 Eli & Max\PMSM")

# 1. Update OEPC_SE_VSI_PMSM_Presentation_HE.html
he_file = PMSM_DIR / "OEPC_SE_VSI_PMSM_Presentation_HE.html"
with open(he_file, 'r', encoding='utf-8') as f:
    he_html = f.read()

target_he = """                        <div class="card-title">יתרונות ממיר Series-End בעל 4 ענפים</div>
                        <ul class="list-styled">
                            <li><strong>ניצולת DC מקסימלית:</strong> משיג $M_a = 1.0$ (זהה לממירי Dual-Inverter) תוך שימוש ב-4 ענפים בלבד (8 מתגים במקום 12).</li>
                            <li><strong>מנוע PMSM בסלילים פתוחים (Open-Winding):</strong> מעלה משמעותית את צפיפות ההספק והתגובה הדינמית.</li>
                        </ul>"""

replacement_he = """                        <div class="card-title">יתרונות ממיר Series-End בעל 4 ענפים</div>
                        <ul class="list-styled">
                            <li><strong>ניצולת DC מקסימלית:</strong> משיג $M_a = 1.0$ (זהה לממירי Dual-Inverter) תוך שימוש ב-4 ענפים בלבד (8 מתגים במקום 12).</li>
                            <li><strong>מנוע PMSM בסלילים פתוחים (Open-Winding):</strong> מעלה משמעותית את צפיפות ההספק והתגובה הדינמית.</li>
                            <li><strong>מימוש חומרתי ייעודי (Altium PCB Design):</strong>
                                יתרונות הממיר מומשו פיזית במלואם באמצעות חומרה ייעודית שתוכננה ונבנתה במעבדה:
                                <div style="margin-top: 6px; padding: 6px 10px; background: rgba(0, 210, 255, 0.08); border: 1px solid rgba(0, 210, 255, 0.3); border-radius: 8px; font-size: 13px; line-height: 1.5;">
                                    <div>⚡ <strong>כרטיסי מפסקי כוח GaN מהירים:</strong> <code>Power_Swech - GUN_ V2</code> (מתגי GaN בעלי הפסדי מיתוג נמוכים לתדר גבוה).</div>
                                    <div style="margin-top: 3px;">🎯 <strong>כרטיסי מדי זרם מבודדים בריחוף:</strong> <code>Isolated_Current_Sensor _V2_1</code> (דגימה מהירה ומדויקת של זרמי הפאזות וזרם ה-ZSC).</div>
                                </div>
                            </li>
                        </ul>"""

if target_he in he_html:
    he_html = he_html.replace(target_he, replacement_he)
    with open(he_file, 'w', encoding='utf-8') as f:
        f.write(he_html)
    print("[OK] Updated OEPC_SE_VSI_PMSM_Presentation_HE.html")
else:
    print("[WARN] Target not found in Hebrew HTML")


# 2. Update OEPC_SE_VSI_PMSM_Presentation.html
en_file = PMSM_DIR / "OEPC_SE_VSI_PMSM_Presentation.html"
with open(en_file, 'r', encoding='utf-8') as f:
    en_html = f.read()

target_en = """                        <div class="card-title">4-Leg Series-End VSI Advantages</div>
                        <ul class="list-styled">
                            <li><strong>Optimal DC-Bus Utilization:</strong> Delivers $M_a = 1.0$ (identical to dual-inverter setups) using only 4 legs (8 switches vs 12).</li>
                            <li><strong>Open-Winding PMSM:</strong> Significantly enhances power density, dynamic torque response, and fault capability.</li>
                        </ul>"""

replacement_en = """                        <div class="card-title">4-Leg Series-End VSI Advantages</div>
                        <ul class="list-styled">
                            <li><strong>Optimal DC-Bus Utilization:</strong> Delivers $M_a = 1.0$ (identical to dual-inverter setups) using only 4 legs (8 switches vs 12).</li>
                            <li><strong>Open-Winding PMSM:</strong> Significantly enhances power density, dynamic torque response, and fault capability.</li>
                            <li><strong>Dedicated Hardware Realization (Altium PCB Design):</strong>
                                Converter advantages were physically realized and validated via custom in-house hardware:
                                <div style="margin-top: 6px; padding: 6px 10px; background: rgba(0, 210, 255, 0.08); border: 1px solid rgba(0, 210, 255, 0.3); border-radius: 8px; font-size: 13px; line-height: 1.5;">
                                    <div>⚡ <strong>High-Speed GaN Power Switch Modules:</strong> <code>Power_Swech - GUN_ V2</code> (Ultra-low switching loss GaN FET stage).</div>
                                    <div style="margin-top: 3px;">🎯 <strong>Floating Isolated Current Sensors:</strong> <code>Isolated_Current_Sensor _V2_1</code> (High-bandwidth sensing for phase currents & ZSC suppression).</div>
                                </div>
                            </li>
                        </ul>"""

if target_en in en_html:
    en_html = en_html.replace(target_en, replacement_en)
    with open(en_file, 'w', encoding='utf-8') as f:
        f.write(en_html)
    print("[OK] Updated OEPC_SE_VSI_PMSM_Presentation.html")
else:
    print("[WARN] Target not found in English HTML")


# 3. Update generate_pptx_presentation.py
pptx_py_file = PMSM_DIR / "generate_pptx_presentation.py"
with open(pptx_py_file, 'r', encoding='utf-8') as f:
    pptx_py = f.read()

target_pptx_items = """    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="4-Leg Series-End VSI Characteristics",
             items=[
                 "Optimal DC-Bus Utilization: Delivers Ma = 1.0 (identical to dual-inverter setups) with only 4 legs (8 switches vs 12).",
                 "Open-Winding PMSM: Significantly enhances machine power density and dynamic torque response.",
                 "ZSC Mitigation Challenge: Absence of floating neutral creates closed ZSC path via outer legs 1 and 4.",
                 "Inter-Phase Coupling: Leg 4 switching impacts all 3 phase currents simultaneously."
             ])"""

repl_pptx_items = """    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="4-Leg Series-End VSI Characteristics",
             items=[
                 "Optimal DC-Bus Utilization: Delivers Ma = 1.0 (identical to dual-inverter setups) with only 4 legs (8 switches vs 12).",
                 "Open-Winding PMSM: Significantly enhances machine power density and dynamic torque response.",
                 "Hardware Realization (Altium Design): Physically built using custom GaN switches (Power_Swech - GUN_ V2) and floating current sensors (Isolated_Current_Sensor _V2_1).",
                 "ZSC Mitigation Challenge: Absence of floating neutral creates closed ZSC path via outer legs 1 and 4.",
                 "Inter-Phase Coupling: Leg 4 switching impacts all 3 phase currents simultaneously."
             ])"""

if target_pptx_items in pptx_py:
    pptx_py = pptx_py.replace(target_pptx_items, repl_pptx_items)
    with open(pptx_py_file, 'w', encoding='utf-8') as f:
        f.write(pptx_py)
    print("[OK] Updated generate_pptx_presentation.py")
else:
    print("[WARN] Target not found in generate_pptx_presentation.py")


# 4. Update generate_hebrew_presentation.py
he_py_file = PMSM_DIR / "generate_hebrew_presentation.py"
with open(he_py_file, 'r', encoding='utf-8') as f:
    he_py = f.read()

target_he_pptx = """    add_card(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="יתרונות ואתגרים ב-4-Leg Series-End VSI",
             items=[
                 "ניצולת DC מלאה (Ma = 1.0) ב-4 ענפים בלבד (8 מתגים במקום 12).",
                 "מנוע PMSM בסלילים פתוחים להעלאת צפיפות ההספק והמומנט.",
                 "אתגר ה-ZSC: היעדר נקודת כוכב צפה יוצר מסלול סגור לזרמי סדרה אפס.",
                 "צימוד פאזות: מיתוג ענף 4 משפיע בו-זמנית על כל זרמי הפאזות."
             ])"""

repl_he_pptx = """    add_card(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="יתרונות ואתגרים ב-4-Leg Series-End VSI",
             items=[
                 "ניצולת DC מלאה (Ma = 1.0) ב-4 ענפים בלבד (8 מתגים במקום 12).",
                 "מנוע PMSM בסלילים פתוחים להעלאת צפיפות ההספק והמומנט.",
                 "מימוש חומרתי ייעודי (Altium): מודולי GaN מהירים (Power_Swech - GUN_ V2) ומדי זרם מבודדים (Isolated_Current_Sensor _V2_1).",
                 "אתגר ה-ZSC: היעדר נקודת כוכב צפה יוצר מסלול סגור לזרמי סדרה אפס.",
                 "צימוד פאזות: מיתוג ענף 4 משפיע בו-זמנית על כל זרמי הפאזות."
             ])"""

if target_he_pptx in he_py:
    he_py = he_py.replace(target_he_pptx, repl_he_pptx)
    with open(he_py_file, 'w', encoding='utf-8') as f:
        f.write(he_py)
    print("[OK] Updated generate_hebrew_presentation.py")
else:
    print("[WARN] Target not found in generate_hebrew_presentation.py")

print("Done.")
