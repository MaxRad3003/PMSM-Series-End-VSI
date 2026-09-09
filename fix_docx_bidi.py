"""
Fix BiDi (Bidirectional) Hebrew & English mixed text rendering in Word (.docx)
Ensures exact word order in Microsoft Word:
"בקרה אופטימלית מבוססת עדיפות שגיאה עבור ממיר Series-End למנועי PMSM ודיכוי זרמי סדר אפס"
"""

import os
from pathlib import Path
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_cover_docx():
    script_dir = Path(r"C:\Users\maximr\OneDrive - ac.sce.ac.il\Barabi\2025 Eli & Max\PMSM")
    logo_path = script_dir / "Images" / "sce_official_header.png"
    output_path = script_dir / "עבודת_גמר_דף_שער_מקסים_רדקין_חדש.docx"

    doc = docx.Document()

    # Configure Margins (A4)
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

    # Set Header with Logo
    header = section.header
    header_p = header.paragraphs[0]
    header_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if logo_path.exists():
        hrun = header_p.add_run()
        hrun.add_picture(str(logo_path), width=Inches(6.25))

    def set_p_bidi(p):
        pPr = p._p.get_or_add_pPr()
        bidi = OxmlElement('w:bidi')
        bidi.set(qn('w:val'), '1')
        pPr.append(bidi)

    def add_run(p, text, is_hebrew=True, font_size=16, bold=True, font_name="David"):
        run = p.add_run(text)
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.color.rgb = RGBColor(0, 0, 0)
        
        rPr = run._r.get_or_add_rPr()
        
        # Fonts
        rFonts = OxmlElement('w:rFonts')
        if is_hebrew:
            rFonts.set(qn('w:ascii'), font_name)
            rFonts.set(qn('w:hAnsi'), font_name)
            rFonts.set(qn('w:cs'), font_name)
            rFonts.set(qn('w:hint'), 'cs')
        else:
            rFonts.set(qn('w:ascii'), 'Times New Roman')
            rFonts.set(qn('w:hAnsi'), 'Times New Roman')
            rFonts.set(qn('w:cs'), font_name)
        rPr.append(rFonts)

        # Bold complex script
        if bold:
            bCs = OxmlElement('w:bCs')
            rPr.append(bCs)

        # RTL flag on the run
        if is_hebrew:
            rtl = OxmlElement('w:rtl')
            rtl.set(qn('w:val'), '1')
            rPr.append(rtl)
        else:
            rtl = OxmlElement('w:rtl')
            rtl.set(qn('w:val'), '0')
            rPr.append(rtl)

        return run

    def add_para(space_before=0, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        set_p_bidi(p)
        return p

    # Spacing from header
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_after = Pt(10)

    # 1. English Title
    p_en = doc.add_paragraph()
    p_en.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_en.paragraph_format.space_after = Pt(8)
    p_en.paragraph_format.line_spacing = 1.15
    add_run(p_en, "Hardware-Efficient Optimal Error-Priority Control for Series-End VSI With ZSC Suppression", is_hebrew=False, font_size=18, bold=True)

    # 2. Hebrew Title (with embedded English terms in exact reading order)
    p_he = add_para(space_before=0, space_after=28)
    add_run(p_he, "בקרה אופטימלית מבוססת תעדוף שגיאה עבור ממיר ", is_hebrew=True, font_size=18, bold=True)
    add_run(p_he, "Series-End", is_hebrew=False, font_size=18, bold=True)
    add_run(p_he, " למנועי ", is_hebrew=True, font_size=18, bold=True)
    add_run(p_he, "PMSM", is_hebrew=False, font_size=18, bold=True)
    add_run(p_he, " ודיכוי זרמי סדרה אפס", is_hebrew=True, font_size=18, bold=True)

    # 3. Project Category & Report
    p_cat = add_para(space_before=0, space_after=8)
    add_run(p_cat, "פרויקט הנדסי", is_hebrew=True, font_size=20, bold=True)

    p_rep = add_para(space_before=0, space_after=32)
    add_run(p_rep, "דו\"ח מסכם פרויקט גמר", is_hebrew=True, font_size=17, bold=True)

    # 4. Degree Requirement
    p_deg = add_para(space_before=0, space_after=28)
    add_run(p_deg, "הוכן לשם מילוי דרישות לקבלת תואר שני בהנדסה ", is_hebrew=True, font_size=15, bold=True)
    add_run(p_deg, "M.Sc.", is_hebrew=False, font_size=15, bold=True)

    # 5. Author
    p_auth_lbl = add_para(space_before=0, space_after=6)
    add_run(p_auth_lbl, "מאת", is_hebrew=True, font_size=15, bold=True)

    p_auth = add_para(space_before=0, space_after=28)
    add_run(p_auth, "מקסים רדקין ", is_hebrew=True, font_size=18, bold=True)
    add_run(p_auth, "307072827", is_hebrew=True, font_size=18, bold=True)

    # 6. Advisor
    p_adv = add_para(space_before=0, space_after=32)
    add_run(p_adv, "בהנחיית ד\"ר אלי גד ברבי", is_hebrew=True, font_size=19, bold=True)

    # 7. Department and College
    p_d1 = add_para(space_before=0, space_after=4)
    add_run(p_d1, "הוגש למחלקה להנדסת חשמל ואלקטרוניקה", is_hebrew=True, font_size=16, bold=True)

    p_d2 = add_para(space_before=0, space_after=4)
    add_run(p_d2, "המכללה האקדמית להנדסה סמי שמעון", is_hebrew=True, font_size=16, bold=True)

    p_d3 = add_para(space_before=0, space_after=38)
    add_run(p_d3, "באר שבע", is_hebrew=True, font_size=15, bold=True)

    # 8. Footer Dates table (Hebrew on right, Gregorian on left)
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Set table to BiDi RTL
    tblPr = table._tbl.tblPr
    tblBidi = OxmlElement('w:bidiVisual')
    tblPr.append(tblBidi)

    # Remove borders
    tblBorders = parse_xml(
        r'<w:tblBorders %s><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/></w:tblBorders>'
        % nsdecls('w')
    )
    tblPr.append(tblBorders)

    # Cell 0 (Right in visual BiDi table): Hebrew Date
    cell_he = table.cell(0, 0)
    cell_he.width = Inches(3.1)
    p_he_date = cell_he.paragraphs[0]
    p_he_date.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_p_bidi(p_he_date)
    add_run(p_he_date, "אלול תשפ\"ו", is_hebrew=True, font_size=16, bold=True)

    # Cell 1 (Left in visual BiDi table): Gregorian Date
    cell_en = table.cell(0, 1)
    cell_en.width = Inches(3.1)
    p_en_date = cell_en.paragraphs[0]
    p_en_date.alignment = WD_ALIGN_PARAGRAPH.LEFT
    add_run(p_en_date, "ספטמבר 2026", is_hebrew=False, font_size=16, bold=True)

    try:
        doc.save(str(output_path))
        print(f"[OK] Generated Word cover page successfully:\n{output_path}")
    except PermissionError:
        alt_path = script_dir / "עבודת_גמר_דף_שער_מקסים_רדקין_חדש_מתוקן.docx"
        doc.save(str(alt_path))
        print(f"[NOTE] Original docx is open in Word. Saved updated version to:\n{alt_path}")

if __name__ == "__main__":
    create_cover_docx()
