import sys

def patch_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already patched
    if 'PMSM_Project_Book.html' in content:
        print("index.html is already patched with PMSM_Project_Book.html!")
        return True

    # 1. Add filter button
    target_btn = '<button class="filter-btn active" data-filter="all">הכל (All)</button>'
    replacement_btn = '''<button class="filter-btn active" data-filter="all">הכל (All)</button>
        <button class="filter-btn" data-filter="deliverables" style="background:linear-gradient(135deg, rgba(0,210,255,0.2), rgba(59,130,246,0.25)); border-color:#00d2ff; color:#fff; font-weight:700;">⭐ תוצרי הפרויקט הראשיים</button>'''
    
    if target_btn in content:
        content = content.replace(target_btn, replacement_btn)
        print("  [+] Filter button added!")

    # 2. Add Deliverables Section at top of content (before section 0)
    deliverables_html = '''    <!-- SECTION -1: PRIMARY CAPSTONE DELIVERABLES (FOR ADVISOR) -->
    <div class="section-title">
      <span style="background: linear-gradient(135deg, #00d2ff, #3b82f6);"></span>
      ⭐ תוצרי הפרויקט הראשיים למנחה (ספר הפרויקט, המצגות האינטראקטיביות ומאמר המחקר)
    </div>

    <div class="grid" id="deliverablesGrid">

      <!-- CARD 1: FULL PROJECT BOOK (HTML) -->
      <div class="card" data-category="deliverables report" data-keywords="ספר הפרויקט project book oepc pmsm series-end vsi latex דוח גמר תזה">
        <div class="card-top">
          <div class="card-header">
            <div class="card-icon-title">
              <div class="card-icon" style="background: rgba(0, 210, 255, 0.15); color: #00d2ff; font-size:1.5rem;">📖</div>
              <div>
                <div class="card-title" style="color: #00d2ff; font-size: 1.2rem;">ספר הפרויקט המלא (HTML חי אינטראקטיבי)</div>
                <span class="code-tag">PMSM_Project_Book.html</span>
              </div>
            </div>
          </div>
          <p class="card-desc">ספר הפרויקט המקיף (מעל 2,230 שורות): רקע תיאורטי, משוואות מתמטיות (LaTeX/MathJax), מודל ממיר Series-End VSI, אלגוריתם OEPC מלא עם טבלת 96-LUT, ניתוח אי-סימטריה ותוצאות C-HIL מעבדתיות.</p>
          <div class="card-tags">
            <span class="badge badge-cyan">ספר פרויקט רשמי</span>
            <span class="badge badge-emerald">2,230+ שורות</span>
            <span class="badge badge-purple">LaTeX & MathJax</span>
            <span class="badge badge-amber">טבלאות ואיורים</span>
          </div>
        </div>
        <div class="card-actions">
          <a href="PMSM_Project_Book.html" target="_blank" class="btn btn-primary" style="background: linear-gradient(135deg, #00d2ff, #0072ff); font-size:0.95rem; font-weight:700;">📖 פתח ספר פרויקט (HTML) ↗</a>
          <a href="עבודת_גמר_דף_שער_מקסיים_רדקין_חדש_מתוקן.docx" download class="btn btn-secondary" title="הורד דף שער רשמי DOCX">📄 דף שער</a>
        </div>
      </div>

      <!-- CARD 2: INTERACTIVE HEBREW PRESENTATION -->
      <div class="card" data-category="deliverables" data-keywords="מצגת אינטראקטיבית עברית oepc 18 שקפים מעגל סימולציה אוסצילוסקופ">
        <div class="card-top">
          <div class="card-header">
            <div class="card-icon-title">
              <div class="card-icon" style="background: rgba(16, 185, 129, 0.15); color: #10b981; font-size:1.5rem;">⚡</div>
              <div>
                <div class="card-title" style="color: #6ee7b7; font-size: 1.2rem;">מצגת אינטראקטיבית למנחה (עברית)</div>
                <span class="code-tag">OEPC_SE_VSI_PMSM_Presentation_HE.html</span>
              </div>
            </div>
          </div>
          <p class="card-desc">18 שקפים אינטראקטיביים: שקף 6 מפענח 96-LUT בזמן-אמת, שקף 10 סימולטור מעגל אלקטרוני חי (איור 2: מיתוגים, חלקיקי זרם זורמים ומתחים) עם אוסצילוסקופ מיוצב ו-5 תרחישי תקלות.</p>
          <div class="card-tags">
            <span class="badge badge-emerald">18 שקפים</span>
            <span class="badge badge-cyan">מעגל איור 2 חי</span>
            <span class="badge badge-amber">Triggered Scope</span>
            <span class="badge badge-rose">5 תרחישי תקלה</span>
          </div>
        </div>
        <div class="card-actions">
          <a href="OEPC_SE_VSI_PMSM_Presentation_HE.html" target="_blank" class="btn btn-primary" style="background: linear-gradient(135deg, #10b981, #059669); font-size:0.95rem; font-weight:700;">⚡ הפעל מצגת אינטראקטיבית (עברית) ↗</a>
          <a href="OEPC_Series_End_PMSM_Presentation_HE.pptx" download class="btn btn-secondary" title="הורד מצגת PPTX">📥 PPTX</a>
        </div>
      </div>

      <!-- CARD 3: INTERACTIVE ENGLISH PRESENTATION -->
      <div class="card" data-category="deliverables" data-keywords="english interactive presentation oepc ieee conference 18 slides">
        <div class="card-top">
          <div class="card-header">
            <div class="card-icon-title">
              <div class="card-icon" style="background: rgba(139, 92, 246, 0.15); color: #8b5cf6; font-size:1.5rem;">🌐</div>
              <div>
                <div class="card-title" style="color: #c4b5fd; font-size: 1.2rem;">Interactive Presentation (English)</div>
                <span class="code-tag">OEPC_SE_VSI_PMSM_Presentation.html</span>
              </div>
            </div>
          </div>
          <p class="card-desc">Full 18-slide presentation in English adhering to IEEE TIE standards with full interactive simulations, 96-LUT vector decoder, real-time circuit schematic and triggered oscilloscope.</p>
          <div class="card-tags">
            <span class="badge badge-purple">18 Slides EN</span>
            <span class="badge badge-cyan">Fig. 2 Circuit</span>
            <span class="badge badge-emerald">IEEE TIE</span>
          </div>
        </div>
        <div class="card-actions">
          <a href="OEPC_SE_VSI_PMSM_Presentation.html" target="_blank" class="btn btn-primary" style="background: linear-gradient(135deg, #8b5cf6, #6d28d9); font-size:0.95rem; font-weight:700;">🌐 Open English Presentation ↗</a>
          <a href="OEPC_Series_End_PMSM_Presentation.pptx" download class="btn btn-secondary" title="Download PPTX">📥 PPTX</a>
        </div>
      </div>

      <!-- CARD 4: IEEE TIE RESEARCH PAPER -->
      <div class="card" data-category="deliverables datasheet" data-keywords="ieee tie research paper oepc series-end vsi article מאמר מחקר">
        <div class="card-top">
          <div class="card-header">
            <div class="card-icon-title">
              <div class="card-icon" style="background: rgba(245, 158, 11, 0.15); color: #f59e0b; font-size:1.5rem;">📄</div>
              <div>
                <div class="card-title" style="color: #fde68a;">מאמר המחקר המקורי – IEEE TIE</div>
                <span class="code-tag">Hardware-Efficient_Optimal_Error-Priority_Control...pdf</span>
              </div>
            </div>
          </div>
          <p class="card-desc">מאמר המחקר מתוך IEEE Transactions on Industrial Electronics: פיתוח טופולוגיית Series-End VSI, משוואות הבקרה, הוכחת דיכוי זרמי סדרה אפס (ZSC) וטבלת 96 המצבים.</p>
          <div class="card-tags">
            <span class="badge badge-amber">IEEE TIE Official</span>
            <span class="badge badge-blue">מאמר בסיס</span>
            <span class="badge">PDF</span>
          </div>
        </div>
        <div class="card-actions">
          <a href="Hardware-Efficient_Optimal_Error-Priority_Control_for_Series-End_VSI_With_ZSC_Suppression.pdf" target="_blank" class="btn btn-secondary" style="flex:1;">📄 פתח מאמר PDF ↗</a>
        </div>
      </div>

      <!-- CARD 5: POLE ALIGNMENT LAB REPORT -->
      <div class="card" data-category="deliverables report" data-keywords="pole alignment oemer qs100s hiperface report כיול קטבים דוח מעבדה">
        <div class="card-top">
          <div class="card-header">
            <div class="card-icon-title">
              <div class="card-icon" style="background: rgba(239, 68, 68, 0.15); color: #ef4444; font-size:1.5rem;">🎯</div>
              <div>
                <div class="card-title" style="color: #fca5a5;">דוח כיול ויישור קטבים למנוע OEMER QS 100S</div>
                <span class="code-tag">OEMER_QS100S_Pole_Alignment_Report_A4.pdf</span>
              </div>
            </div>
          </div>
          <p class="card-desc">דוח הנדסי מפורט בפורמט A4: שיטת יישור קטבים סטטי (Static DC Alignment), הגדרת היסט אינקודר SICK SFM60 HIPERFACE, אימות עם אנליזר וחיבור למערכת הבקרה.</p>
          <div class="card-tags">
            <span class="badge badge-rose">דוח כיול A4</span>
            <span class="badge">OEMER QS 100S</span>
            <span class="badge">SICK HIPERFACE</span>
          </div>
        </div>
        <div class="card-actions">
          <a href="OEMER_QS100S_Pole_Alignment_Report_A4.pdf" target="_blank" class="btn btn-secondary" style="flex:1;">🎯 פתח דוח כיול PDF ↗</a>
          <a href="Pole_Alignment_and_Verification_Report.md" target="_blank" class="btn btn-secondary">📝 MD</a>
        </div>
      </div>

      <!-- CARD 6: ADVISOR PORTAL PACKAGE -->
      <div class="card" data-category="deliverables tools" data-keywords="advisor portal package zip חבילת מנחה הורדה">
        <div class="card-top">
          <div class="card-header">
            <div class="card-icon-title">
              <div class="card-icon" style="background: rgba(59, 130, 246, 0.15); color: #3b82f6; font-size:1.5rem;">📦</div>
              <div>
                <div class="card-title" style="color: #93c5fd;">ערכת מנחה אופליין מלאה (Advisor Portal)</div>
                <span class="code-tag">OEPC_PMSM_Presentation_Package/</span>
              </div>
            </div>
          </div>
          <p class="card-desc">תיקייה עצמאית הכוללת שער מנחה ייעודי (START_HERE), סקריפטי הפעלה בלחיצה אחת (.bat), ואפשרות להורדה כארכיון ZIP שלם לעבודה ללא תלות ברשת.</p>
          <div class="card-tags">
            <span class="badge badge-blue">שער מנחה ייעודי</span>
            <span class="badge badge-emerald">Offline-Ready</span>
          </div>
        </div>
        <div class="card-actions">
          <a href="OEPC_PMSM_Presentation_Package/START_HERE_Advisor_Portal.html" target="_blank" class="btn btn-primary" style="background: linear-gradient(135deg, #3b82f6, #1d4ed8);">🚀 פתח שער מנחה ↗</a>
        </div>
      </div>

    </div>

'''
    
    target_section0 = '<!-- SECTION 0: OEMER Official Motor Library -->'
    if target_section0 in content:
        content = content.replace(target_section0, deliverables_html + '\n    ' + target_section0)
        print("  [+] Deliverables section added successfully!")
    else:
        print("  [-] Could not locate SECTION 0 marker!")
        return False

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] index.html updated successfully!")
    return True

if __name__ == '__main__':
    patch_index()
