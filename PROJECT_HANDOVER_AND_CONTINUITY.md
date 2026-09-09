# תיעוד מסירה והמשך עבודה ממחשב אחר (Project Handover & Continuity Guide)

> **פרויקט:** בקרת זרם אופטימלית מבוססת תעדוף שגיאה (OEPC) עבור ממיר Series-End VSI למנועי PMSM ודיכוי זרמי סדרה אפס  
> **מחבר (סטודנט):** מקסים רדקין (ת.ז. 307072827), מועמד לתואר שני .M.Sc  
> **מנחה ראשי:** ד"ר אלי גד ברבי, מרצה בכיר  
> **שותף למחקר:** פרופ' דמיטרי ביימל, Senior Member IEEE  
> **מוסד:** המכללה האקדמית להנדסה ע"ש סמי שמעון (SCE), המחלקה להנדסת חשמל ואלקטרוניקה  
> **פרסום מדעי:** *IEEE Transactions on Industrial Electronics (IEEE TIE, 2026)*  
> **תיקייה משותפת (OneDrive):** `c:\Users\maximr\OneDrive - ac.sce.ac.il\Barabi\2025 Eli & Max\PMSM`  
> **תאריך עדכון אחרון:** 09 ספטמבר 2026

---

## 📌 1. תמונת מצב עדכנית (Current Status)
כל התוצרים המרכזיים של פרויקט הגמר נבדקו, שודרגו, אומתו ונארזו לערכת הפצה מושלמת למנחה הפרויקט (ד"ר אלי ברבי). התיקייה מסונכרנת בענן ה-OneDrive המוסדי של SCE, כך שכל קובץ שנערך זמין לעבודה מיידית מכל מחשב אחר.

### עיקרי העדכונים האחרונים שבוצעו:
1. **הטמעה מלאה של טבלת 96-LUT המקורית (`OEPC_LUT96.xlsx`):**
   - כל 96 השורות של טבלת הניתוב האופטימלית מ-`OEPC_LUT96.xlsx` הוטמעו ישירות במנוע ה-JavaScript של המצגות (בעברית ובאנגלית).
   - **חישוב מתמטי בזמן אמת של חתימת 7-ביט:** חישוב $P_{ab}, P_{bc}, P_{ca}$ (סדר עדיפויות), $S_{mx}, S_{md}, S_{mn}$ (סימני שגיאות מקסימום, אמצע ומינימום) ו-$F_{mp}$ (דגל סדרה-אפס).
   - כתובת בינארית מלאה: $\text{Idx} = (P_{ab}\ll 6) | (P_{bc}\ll 5) | (P_{ca}\ll 4) | (S_{mx}\ll 3) | (S_{md}\ll 2) | (S_{mn}\ll 1) | F_{mp}$ (אינדקסים 16 עד 111).
   - תצוגת חתימת 7-ביט זוהרת בזמן אמת `[EPO | ESC | EMP]` לצד מספר השורה המדויק באקסל (#1 עד #96).
   - **צפיין אינטראקטיבי מלא ל-96-LUT:** חלונית מודאלית (Modal) עם הטבלה המלאה, איתור וסימון השורה הפעילה בזמן אמת, מנגנון גלילה אוטומטית (Auto-scroll), ומנוע חיפוש/סינון מהיר לפי פרמוטציה, וקטור או השפעה.
2. **שקף 6 (מפענח 96-LUT ומישור $\alpha-\beta$):**
   - ביטול כל סימוני ה-LaTeX הגולמיים והיפוכי ה-BiDi/RTL; מעבר לטיפוגרפיה מתמטית מבודדת כיווניות באמצעות `<bdi class="math-term">`.
   - תיקון ישויות שגויות (החלפת `&vec;&epsilon;` ב-`<b>&epsilon;</b>` תקני).
   - עיצוב מחודש, ברור ומרווח של כרטיס ההחלטה: תגיות בולטות לעדיפות סדרה אפס (CM - ענבר) מול דיפרנציאלית (DM - כחול ציאן), גריד דו-עמודי למצב המיתוג של 4 הענפים `[L1 L2 L3 L4]`, ובלוק הסבר מפורט לעליונות OEPC על פני TDM.
   - הוספת צירי $\alpha$ ו-$\beta$, סימון ששת הסקטורים ($S_1 \dots S_6$), וחיבור אירועי `oninput` ו-`setPresetErrors` לכל 4 הסליידרים והתרחישים המוכנים.
2. **שקף 10 (סימולטור מנוע PMSM ואוסצילוסקופ):**
   - פתרון מוחלט לבעיית "האותות רצים מהר מדי": הטמעת **מצב גל מיוצב (Triggered Scope Sync)** הננעל למעבר האפס ומציג בדיוק 2 מחזורים סינוסיים יציבים ללא ריצוד.
   - הוספת מתג מצבי סנכרון: 📌 גל מיוצב (Triggered) מול 🌊 גלילה איטית (Slow Roll 0.2x).
   - האטת תנועת וקטור המרחב (Lissajous) לסיבוב אחיד ונינוח של 3.5 שניות עם נקודת סמן מוארת.
   - הוספת כרטיס הסבר פיזיקלי דינמי המתעדכן בזמן אמת בלחיצה על אלגוריתמי הבקרה (OEPC, TDM, PWM).
   - הוספת תרשים זרימה תלת-שלבי מפורט (דגימה וחישוב ZSC $\rightarrow$ תעדוף שגיאות ב-LUT $\rightarrow$ הפעלת וקטור מיתוג ישיר ב-1.75&mu;s).
3. **כפתור מסך מלא (Fullscreen Toggle):**
   - הוטמע כפתור `⛶ מסך מלא` יוקרתי בכותרת העליונה (Header) ובסרגל הניווט התחתון (Footer).
   - תמיכה בקיצור מקשים במקלדת: הקשה על **`F`** מעבירה למסך מלא ובחזרה.
   - הרחבה רספונסיבית חלקה ל-`100vw`/`100vh` המנצלת את מלוא שטח המסך.
4. **ערכת הפצה ארוזה ועצמאית למנחה הפרויקט (Advisor Package):**
   - יצירת תיקיית הפצה ייעודית: `OEPC_PMSM_Presentation_Package` (וגרסה עברית: `ערכת_מצגת_למנחה_OEPC_PMSM`).
   - דף נחיתה ופורטל ראשי: `START_HERE_Advisor_Portal.html` / `התחל_כאן_פורטל_למנחה.html`.
   - קובצי הרצה מהירים (Windows Batch): `Open_Presentation_HE.bat`, `Open_Presentation_EN.bat`.
   - קובץ ארכיון קומפקטי ומוכן לשליחה: **`OEPC_PMSM_Presentation_For_Advisor.zip`** (כ-4.9 מגה-בייט בלבד).
   - עצמאות מלאה (100% Offline): הורדת עותק מקומי של MathJax (`presentation_assets/tex-mml-chtml.js`) כך שהמצגת נפתחת ומציגה את כל המשוואות והסימולציות גם במחשב ללא חיבור לאינטרנט.

---

## 📂 2. מפת הקבצים והתוצרים המרכזיים (Deliverables Map)

### א. ערכת ההפצה למנחה הפרויקט
* **קובץ ה-ZIP המוכן לשליחה במייל/ענן:**
  [`OEPC_PMSM_Presentation_For_Advisor.zip`](OEPC_PMSM_Presentation_For_Advisor.zip)
* **תיקיית הערכה המלאה:**
  [`OEPC_PMSM_Presentation_Package/`](OEPC_PMSM_Presentation_Package/)
* **דף הנחיתה הראשי:**
  [`START_HERE_Advisor_Portal.html`](OEPC_PMSM_Presentation_Package/START_HERE_Advisor_Portal.html)
* **קובץ הנחיות טקסט למנחה:**
  [`README_מדריך_למנחה_הפרויקט.txt`](OEPC_PMSM_Presentation_Package/README_מדריך_למנחה_הפרויקט.txt)

---

### ב. מצגות אינטראקטיביות ו-PowerPoint (18 שקפים, 16:9 Widescreen)

| שפה | מצגת דפדפן (HTML אינטראקטיבי + סימולציות) | מצגת PowerPoint רשמית (PPTX) |
| :--- | :--- | :--- |
| **עברית (RTL)** | [`OEPC_SE_VSI_PMSM_Presentation_HE.html`](OEPC_SE_VSI_PMSM_Presentation_HE.html) | [`OEPC_Series_End_PMSM_Presentation_HE.pptx`](OEPC_Series_End_PMSM_Presentation_HE.pptx) |
| **אנגלית (LTR)** | [`OEPC_SE_VSI_PMSM_Presentation.html`](OEPC_SE_VSI_PMSM_Presentation.html) | [`OEPC_Series_End_PMSM_Presentation.pptx`](OEPC_Series_End_PMSM_Presentation.pptx) |

---

### ג. ספר הסיכום המקיף ודפי השער
1. **ספר ה-HTML האינטראקטיבי המלא (Academic Monograph & E-Book):**
   - [`ספר_סיכום_פרויקט_PMSM.html`](ספר_סיכום_פרויקט_PMSM.html) / [`PMSM_Project_Book.html`](PMSM_Project_Book.html)
2. **דף שער רשמי לתזה (OpenXML BiDi Isolation):**
   - [`עבודת_גמר_דף_שער_מקסים_רדקין_חדש_מתוקן.docx`](עבודת_גמר_דף_שער_מקסים_רדקין_חדש_מתוקן.docx)
   - דף שער אינטרנטי A4 להדפסה: [`cover_page.html`](cover_page.html)

---

## 🛠️ 3. סקריפטים לאוטומציה ובנייה מחדש (Automation Scripts)

במידה ועורכים טקסט או מעוניינים להדר מחדש את כלל התוצרים:

```powershell
# 1. פתיחת התיקייה בטרמינל (PowerShell)
cd "C:\Users\maximr\OneDrive - ac.sce.ac.il\Barabi\2025 Eli & Max\PMSM"

# 2. הידור המצגות והספר מחדש (HTML + PowerPoint)
python generate_hebrew_presentation.py
python generate_html_presentation.py
python generate_pptx_presentation.py
python generate_project_book.py

# 3. אריזה מחדש של ערכת המנחה וקובץ ה-ZIP
python package_presentation.py

# 4. סנכרון וגיבוי היסטוריית השיחות של Antigravity
python sync_history.py
```

---

## 💻 4. כיצד להמשיך עבודה ממחשב אחר (Instructions for Other Computer)

1. **פתיחה ב-VS Code / Antigravity:**
   - במחשב השני, פתח את סביבת העבודה:
     `c:\Users\maximr\OneDrive - ac.sce.ac.il\Barabi\PMSM.code-workspace`
2. **הצגת המצגת:**
   - דאבל-קליק על `Open_Presentation_HE.bat` או על `OEPC_SE_VSI_PMSM_Presentation_HE.html`.
   - מעבר שקפים באמצעות חצי מקלדת או כפתורים. כניסה למסך מלא בלחיצה על המקש `F`.
3. **המשך שיחה עם סוכן ה-AI:**
   - במידה וסוכן חדש מתחיל שיחה, הנחה אותו:
     *"קרא תחילה את קובץ `PROJECT_HANDOVER_AND_CONTINUITY.md` ואת תיקיית `antigravity_history` להבנת המצב והמשך העבודה."*

---

## 🎯 5. צעדים מומלצים להמשך (Next Steps)
1. **העברת קובץ ה-ZIP למנחה הפרויקט:** שליחת `OEPC_PMSM_Presentation_For_Advisor.zip` לד"ר אלי ברבי לקבלת משוב סופי.
2. **הדגמה חיה:** הרצת שקף 6 (מפענח LUT) ושקף 10 (אוסצילוסקופ מיוצב) להמחשת הישגי המחקר ועליונות OEPC על פני TDM ו-PWM.
3. **המשך עבודת המעבדה:** שילוב המנוע התעשייתי החדש (OEMER/SEW) שנרכש יחד עם מודולי ה-GaN וחיישני הזרם שנבנו במעבדה.
