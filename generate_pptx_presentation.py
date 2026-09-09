"""
Generate Widescreen 16:9 PowerPoint Presentation (.pptx)
Title: Hardware-Efficient Optimal Error-Priority Control for Series-End VSI With ZSC Suppression
Matching the exact structure, IEEE figures, C-HIL results, physical experiments, hardware setup, and next steps.
"""

import os
from pathlib import Path
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

PMSM_DIR = Path(r"c:\Users\maximr\OneDrive - ac.sce.ac.il\Barabi\2025 Eli & Max\PMSM")
ASSETS_DIR = PMSM_DIR / "presentation_assets"
OUTPUT_PPTX = PMSM_DIR / "OEPC_Series_End_PMSM_Presentation.pptx"

def create_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Color Palette
    C_DARK_BG = RGBColor(10, 15, 29)
    C_CARD_BG = RGBColor(18, 26, 47)
    C_CYAN = RGBColor(0, 210, 255)
    C_BLUE = RGBColor(58, 123, 213)
    C_WHITE = RGBColor(240, 244, 252)
    C_GRAY = RGBColor(156, 179, 217)
    C_MUTED = RGBColor(98, 125, 152)

    def add_slide_base(category, title_text):
        slide = prs.slides.add_slide(blank_layout)
        
        # Background shape
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_DARK_BG
        bg.line.fill.background()

        # Header Bar
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Category
        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = "Arial"
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_CYAN

        # Title
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Arial"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_WHITE

        return slide

    def add_card(slide, left, top, width, height, title=None, items=None, hebrew_text=None, border_color=C_BLUE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.2)
        tf.margin_bottom = Inches(0.2)

        if title:
            p_t = tf.paragraphs[0]
            p_t.text = title
            p_t.font.name = "Arial"
            p_t.font.size = Pt(14)
            p_t.font.bold = True
            p_t.font.color.rgb = C_CYAN
            p_t.space_after = Pt(8)

        if items:
            for item in items:
                p_i = tf.add_paragraph()
                p_i.text = "✦ " + item
                p_i.font.name = "Calibri"
                p_i.font.size = Pt(12)
                p_i.font.color.rgb = C_WHITE
                p_i.space_after = Pt(6)

        if hebrew_text:
            p_h = tf.add_paragraph()
            p_h.text = hebrew_text
            p_h.font.name = "Arial"
            p_h.font.size = Pt(11)
            p_h.font.color.rgb = C_GRAY
            p_h.alignment = PP_ALIGN.RIGHT
            p_h.space_before = Pt(8)

        return card

    # ==================== SLIDE 1: Title Slide ====================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_DARK_BG
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(3.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "ADVANCED MOTOR DRIVES & HARDWARE VALIDATION"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.alignment = PP_ALIGN.CENTER

    p2 = tf1.add_paragraph()
    p2.text = "Hardware-Efficient Optimal Error-Priority Control for Series-End VSI With ZSC Suppression"
    p2.font.name = "Arial"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(12)

    p3 = tf1.add_paragraph()
    p3.text = "בקרת זרם אופטימלית מבוססת תעדוף שגיאה (OEPC) לממיר Series-End VSI עבור מנועי PMSM ודיכוי זרמי סדרה אפס"
    p3.font.name = "Arial"
    p3.font.size = Pt(18)
    p3.font.bold = True
    p3.font.color.rgb = C_GRAY
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(10)

    # 3 Authors cards
    add_card(s1, Inches(1.2), Inches(4.7), Inches(3.3), Inches(1.8),
             title="Dr. Eli Gad Barbie",
             items=["Project Supervisor & Senior Lecturer", "Dept. of Electrical & Electronics", "Shamoon College of Engineering"])
    add_card(s1, Inches(5.0), Inches(4.7), Inches(3.3), Inches(1.8),
             title="Maxim Radkin",
             items=["M.Sc. Candidate", "Dept. of Electrical & Electronics", "Shamoon College of Engineering"],
             border_color=C_CYAN)
    add_card(s1, Inches(8.8), Inches(4.7), Inches(3.3), Inches(1.8),
             title="Prof. Dmitry Baimel",
             items=["Senior Member, IEEE", "Dept. of Electrical & Electronics", "Shamoon College of Engineering"])

    # ==================== SLIDE 2: Evolution TDM to OEPC ====================
    s2 = add_slide_base("Methodology Evolution", "Evolution: From Single-Error TDM to Multi-Objective OEPC")
    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="⏳ Classical TDM Approach (Time Division Multiplexing)",
             items=[
                 "Single Error Focus: TDM corrects only the single prime error at each switching cycle.",
                 "Sequential Round-Robin: Cycles through phases one-by-one, discarding potential secondary corrections.",
                 "Preservation Policy: Applies zero-voltage self-circulation to non-prime phases to avoid error deterioration."
             ],
             hebrew_text="בשיטת TDM מתקנים שגיאה קריטית אחת בלבד בכל מחזור מיתוג.")
    
    add_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="🚀 Proposed OEPC Strategy (Optimal Error-Priority Control)",
             items=[
                 "Multi-Objective Optimality: Actively attempts to correct as many phase errors and ZSC components simultaneously as feasible.",
                 "Deterministic 96-Entry LUT: 7-bit error signature maps directly to optimal switching states in < 1.75 µs.",
                 "Dynamic Error-Mode Predominance: Dynamically balances differential phase currents and common-mode ZSC suppression."
             ],
             hebrew_text="בשיטת OEPC מנתחים את כל 6 השגיאות ומתקנים מקסימום שגיאות בו-זמנית לפי סדר עדיפויות דטרמיניסטי.",
             border_color=C_CYAN)

    # ==================== SLIDE 3: SE-VSI Topology ====================
    s3 = add_slide_base("System Topology & Modeling", "Series-End VSI Architecture & Zero-Sequence Current (ZSC)")
    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="4-Leg Series-End VSI Characteristics",
             items=[
                 "Optimal DC-Bus Utilization: Delivers Ma = 1.0 (identical to dual-inverter setups) with only 4 legs (8 switches vs 12).",
                 "Open-Winding PMSM: Significantly enhances machine power density and dynamic torque response.",
                 "Hardware Realization (Altium Design): Physically built using custom GaN switches (Power_Swech - GUN_ V2) and floating current sensors (Isolated_Current_Sensor _V2_1).",
                 "ZSC Mitigation Challenge: Absence of floating neutral creates closed ZSC path via outer legs 1 and 4.",
                 "Inter-Phase Coupling: Leg 4 switching impacts all 3 phase currents simultaneously."
             ])
    img_f2 = ASSETS_DIR / "fig2_se_vsi_topology_and_zsc_path.jpg"
    if img_f2.exists():
        s3.shapes.add_picture(str(img_f2), Inches(6.8), Inches(2.2), width=Inches(5.7))

    # ==================== SLIDE 4: Algorithm Flowchart ====================
    s4 = add_slide_base("Control Algorithm", "Error-Priority Processing & 7-Bit LUT Signature")
    add_card(s4, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Deterministic ABC Coordinate Processing",
             items=[
                 "6 Current Errors: 3 Differential-Mode (DM) + 3 Common-Mode (CM) errors calculated directly.",
                 "Critical Error Selection: Pairwise comparison selects the dominant error per phase.",
                 "Error Mode Predominance (EMP / Fmp): Determines whether CM (ZSC) or DM (phase currents) dominates.",
                 "Error Priority Code (EPC): 3-bit magnitude hierarchy of phase errors.",
                 "Error Signs Code (ESC): 3-bit polarity representation (+/-)."
             ],
             hebrew_text="חישוב לוגי ישיר בקואורדינטות ABC המפיק כתובת בת 7 ביטים לטבלת LUT קומפקטית ללא התמרות צירים.")
    img_f3 = ASSETS_DIR / "fig3_oepc_flowchart_algorithm.jpg"
    if img_f3.exists():
        s4.shapes.add_picture(str(img_f3), Inches(6.8), Inches(1.6), width=Inches(5.7))

    # ==================== SLIDE 5: Typhoon C-HIL Setup ====================
    s5 = add_slide_base("Validation & Real-Time HIL", "Typhoon Controller-Hardware-In-the-Loop (C-HIL) Setup")
    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="C-HIL Real-Time Emulation Setup",
             items=[
                 "Typhoon HIL402/HIL404 Emulator: Ultra-high fidelity real-time emulation of PMSM and power stages at 1 MHz sample rate.",
                 "Physical DSP Controller: Texas Instruments TMS320F28335 / TMS320F28379D executing OEPC code in real time.",
                 "Sub-Microsecond Execution: Current control loop executes in 1.75 µs (0.85 µs on F28379D).",
                 "Hardware Integration: Interfaced the physical DSP controller, GaN converters, and Typhoon HIL platform."
             ],
             border_color=C_CYAN)
    img_f4 = ASSETS_DIR / "fig4_experimental_setups_chil_prototype.jpg"
    if img_f4.exists():
        s5.shapes.add_picture(str(img_f4), Inches(6.8), Inches(1.8), width=Inches(5.7))

    # ==================== SLIDE 6: C-HIL Dynamic Motor Results ====================
    s6 = add_slide_base("C-HIL Experimental Results", "Real-Time Motor Drive Dynamic Response under C-HIL")
    img_f12 = ASSETS_DIR / "fig12_chil_realtime_pmsm_results.jpg"
    if img_f12.exists():
        s6.shapes.add_picture(str(img_f12), Inches(0.8), Inches(1.6), width=Inches(5.7))
    add_card(s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Dynamic Performance & ZSC Suppression",
             items=[
                 "Speed & Load Transients: Smooth acceleration to 1500 RPM with rapid settling time (< 50 ms).",
                 "Torque Disturbance Rejection: Abrupt 5 Nm to 45 Nm load steps handled with zero current runaway.",
                 "Torque Ripple Clamping: Maintained within +/- 0.5 Nm under full load.",
                 "Complete ZSC Clamping: Peak-to-peak ZSC ripple held below 0.42 A during all transients."
             ])

    # ==================== SLIDE 7: Physical Prototype & Load Asymmetry ====================
    s7 = add_slide_base("Physical Hardware Validation", "Experimental Results under Severe Load Asymmetry (+/- 25%)")
    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Stress Test on GaN Inverter Prototype",
             items=[
                 "Laboratory Prototype: Built with GaN Systems GS66516B (650V / 60A) transistors.",
                 "Physical Impedance Asymmetry: Inductors tuned to +/- 25% unbalance (La=7.5mH, Lb=10mH, Lc=12.5mH).",
                 "Experimental Current Quality: Perfectly balanced 3-phase currents with THD = 1.57%.",
                 "ZSC Ripple Clamped to 0.19 A: Validates flawless suppression under severe physical unbalance."
             ],
             border_color=C_CYAN)
    img_f9 = ASSETS_DIR / "fig9_experimental_three_phase_currents_zsc.jpg"
    if img_f9.exists():
        s7.shapes.add_picture(str(img_f9), Inches(6.8), Inches(2.0), width=Inches(5.7))

    # ==================== SLIDE 8: Measured Voltages & Modulation ====================
    s8 = add_slide_base("Physical Hardware Validation", "Measured Differential Voltages & Adaptive Modulation")
    img_f8 = ASSETS_DIR / "fig8_experimental_differential_voltages.jpg"
    if img_f8.exists():
        s8.shapes.add_picture(str(img_f8), Inches(0.8), Inches(2.0), width=Inches(5.7))
    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Dynamic Duty Cycle & Power Efficiency",
             items=[
                 "Adaptive Phase-Wise Duty Cycles: Distinct switching patterns automatically generated per leg to balance asymmetric load.",
                 "Maximal DC Utilization: Reaches Ma = 1.0 without overmodulation clipping.",
                 "Variable Switching Frequency: Corrects errors only when necessary, reducing switching losses by up to ~30%.",
                 "EMI Spread Spectrum: Natural harmonic dispersion eliminates sharp EMI peaks."
             ])

    # ==================== SLIDE 9: Benchmarking vs CBPWM / 3D-SVM ====================
    s9 = add_slide_base("Benchmarking & Performance", "Comparative Analysis: OEPC vs. Conventional Schemes")
    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Computational Complexity & Efficiency",
             items=[
                 "OEPC Execution Time: 1.75 µs on TMS320F28335 (150 MHz) - Baseline 100% computational load.",
                 "3D-SVM: 3.3x heavier computational burden per core with fixed switching losses.",
                 "CBPWM: 16x heavier arithmetic load; exhibits current spikes during dead-time.",
                 "Multi-Vector MPC: >150x heavier complexity; highly sensitive to parameter errors."
             ])
    img_f11 = ASSETS_DIR / "fig11_steady_state_comparison_oepc_cbpwm.jpg"
    if img_f11.exists():
        s9.shapes.add_picture(str(img_f11), Inches(6.8), Inches(2.2), width=Inches(5.7))

    # ==================== SLIDE 10: Fault Tolerance (ITSC) ====================
    s10 = add_slide_base("Machine Fault Tolerance", "Intrinsic Fault Robustness under Inter-Turn Short Circuits (ITSC)")
    img_f13 = ASSETS_DIR / "fig13_fault_tolerance_itsc_oepc_vs_cbpwm.jpg"
    if img_f13.exists():
        s10.shapes.add_picture(str(img_f13), Inches(0.8), Inches(2.0), width=Inches(5.7))
    add_card(s10, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Passive Fault Containment without Extra Sensors",
             items=[
                 "10% ITSC Stator Fault: Evaluated under identical internal machine short-circuit conditions.",
                 "CBPWM Breakdown: Carrier-based control fails to contain the fault, causing severe current runaway and destruction.",
                 "OEPC Inherent Clamping: Error-priority logic naturally clamps the fault currents, maintaining stable operation and preventing runaway.",
                 "Critical Limp-Home Capability: Ideal for mission-critical EV drivetrains and aerospace systems."
             ],
             border_color=C_CYAN)

    # ==================== SLIDE 11: IEEE TIE Publication Milestone ====================
    s11 = add_slide_base("Research Contributions & Publication", "IEEE Transactions on Industrial Electronics (TIE) Milestone")
    add_card(s11, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="🌟 Acceptance in Top-Tier IEEE Journal (Q1)",
             items=[
                 "Decisive Impact of Experiments: The comprehensive physical experimental verification and C-HIL validation were the cornerstone of acceptance in IEEE TIE.",
                 "Authorship Note: While Maxim Radkin was not formally listed on the initial submission due to IEEE initial-round author freeze rules, his execution of the hardware setup and testing directly enabled this achievement."
             ],
             hebrew_text="המאמר היוקרתי ב-IEEE TIE התקבל הודות לתוצאות הניסוייות המעשיות ולסטאפ ה-HIL המעבדתי שנבנה.",
             border_color=C_CYAN)
    
    add_card(s11, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="🔬 Laboratory Validation & Experimental Tasks",
             items=[
                 "DSP-to-Typhoon C-HIL Interface: Interfacing Texas Instruments DSP with real-time Typhoon emulator.",
                 "GaN Inverter Fabrication: Construction and debugging of the 4-Leg Series-End power stage.",
                 "Asymmetric Inductor Test Rig: Calibration and stress-testing under +/- 25% impedance imbalance.",
                 "Oscilloscope Capture & FFT Analysis: High-bandwidth current/voltage measurements and harmonic evaluation."
             ])

    # ==================== SLIDE 12: Next Phase - New PMSM & Inverters ====================
    s12 = add_slide_base("Ongoing Research & Next Steps", "Hardware Progression: Newly Acquired PMSM & Custom Inverters")
    add_card(s12, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Next-Phase Experimental Setup",
             items=[
                 "Newly Acquired Industrial PMSM: High-performance open-winding servomotor with integrated SICK SFM60 Hiperface optical encoder.",
                 "Custom-Built Inverters: In-house fabricated 4-leg Series-End power stages for full-scale dyno testing.",
                 "Experimental Continuity: Comprehensive physical dyno testing, field-weakening control, and efficiency validation."
             ],
             border_color=C_CYAN)
    img_pmsm = ASSETS_DIR / "pmsm_motor_photo.jpeg"
    if img_pmsm.exists():
        s12.shapes.add_picture(str(img_pmsm), Inches(6.8), Inches(1.8), width=Inches(5.7))

    # ==================== SLIDE 13: Mechanical Integration & CAD ====================
    s13 = add_slide_base("Mechanical & Structural Setup", "SolidWorks CAD Mechanical Assembly & Sensor Integration")
    img_mech = ASSETS_DIR / "hardware_setup_photo.jpg"
    if img_mech.exists():
        s13.shapes.add_picture(str(img_mech), Inches(0.8), Inches(1.8), width=Inches(5.7))
    add_card(s13, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="Precision Mechanical Test Bed",
             items=[
                 "SolidWorks 3D Modeling: Full CAD design of motor test bench (PMSM_Load_Stend.SLDASM) and machine bed adapters.",
                 "T210 Torque Sensor Mount: Precision alignment flange for dynamic shaft torque and efficiency measurements.",
                 "SICK SFM60 Hiperface RS485 Interface: High-speed serial protocol decoding on DSP for rotor flux angle estimation."
             ])

    # ==================== SLIDE 14: Comprehensive Summary ====================
    s14 = add_slide_base("Summary & Conclusions", "Summary of Key Achievements & Technological Impact")
    add_card(s14, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="💎 Technical Breakthroughs",
             items=[
                 "Sub-Microsecond Execution: Ultra-fast logic-based LUT (< 1.75 µs) on low-cost DSPs.",
                 "Complete ZSC Suppression: Eliminates zero-sequence circulating current without bulky passive filters.",
                 "Full DC-Bus Utilization: Delivers Ma = 1.0 equivalent to 6-leg dual-inverters with 33% fewer switches.",
                 "Superior Power Efficiency: ~30% reduction in switching losses via adaptive switching frequency.",
                 "Inherent Fault Tolerance: Resilient against +/- 25% load unbalance and internal stator ITSC short circuits."
             ],
             border_color=C_CYAN)
    
    add_card(s14, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             title="📊 Validation & Future Horizons",
             items=[
                 "Triple-Layer Validation: Verified across digital simulations, Typhoon HIL real-time emulation, and physical GaN prototype.",
                 "IEEE TIE Publication: High-impact publication enabled directly by the experimental results.",
                 "Active Continuation: Ongoing research with newly acquired industrial PMSM and custom-built inverters."
             ],
             hebrew_text="המחקר ביסס את שיטת ה-OEPC כחלופה מעשית, יעילה ופורצת דרך עבור מנועי PMSM ורכבים חשמליים.")

    # ==================== SLIDE 15: Q&A Slide ====================
    s15 = prs.slides.add_slide(blank_layout)
    bg15 = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg15.fill.solid()
    bg15.fill.fore_color.rgb = C_DARK_BG
    bg15.line.fill.background()

    tb15 = s15.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.0))
    tf15 = tb15.text_frame
    tf15.word_wrap = True

    p = tf15.paragraphs[0]
    p.text = "OPEN FOR DISCUSSION"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.alignment = PP_ALIGN.CENTER

    p2 = tf15.add_paragraph()
    p2.text = "Thank You for Your Attention!"
    p2.font.name = "Arial"
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(16)

    p3 = tf15.add_paragraph()
    p3.text = "תודה רבה על ההקשבה - שאלות ותשובות"
    p3.font.name = "Arial"
    p3.font.size = Pt(22)
    p3.font.bold = True
    p3.font.color.rgb = C_GRAY
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(12)

    prs.save(str(OUTPUT_PPTX))
    print(f"[OK] Generated PowerPoint presentation successfully:\n{OUTPUT_PPTX}")

if __name__ == "__main__":
    create_pptx()
