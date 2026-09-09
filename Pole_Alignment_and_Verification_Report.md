<div dir="rtl">

# 📋 דוח סיכום הנדסי סופי ומקיף: כיול מיקום קטבים, פענוח אינקודר וחומרת תקשורת DFR0845 (OEMER QS 100S)

---

## 🏆 1. תוצאת הכיול הסופית והמסקנות המרכזיות

* **מנוע נבדק**: **OEMER QS 100S** (מספר סידורי `25M0147`, $P = 4$ קטבים, $p = 2$ זוגות קטבים, $580\text{ RPM}$, $19.3\text{ Hz}$).
* **אינקודר אבסולוטי**: **SICK SFM60 HIPERFACE** ($32,768$ צעדים לסיבוב יחיד / 15-ביט, $1024\text{ Sin/Cos}$).
* **זווית היסט קטבים מכוילת סופית ($\theta_{\text{offset}}$)**:
  $$\mathbf{\theta_{\text{offset}} = 58.98^\circ \approx 59.0^\circ \quad (1.0295\text{ rad})}$$
* **דיוק ופיזור שגיאה על פני כל 360 מעלות מכניות (13 שלבים)**:
  * **שגיאה מרבית**: **$\pm 0.34^\circ$ בלבד!**
  * **סטיית תקן (RMS)**: **$\pm 0.21^\circ$ בלבד!**
  * **סגירת סיבוב מלא (שלב 13' מול שלב 1)**: **$0.00^\circ$ שגיאה (התאמה אבסולוטית של $360.00^\circ$)!**

---

## 🧭 2. הגדרה מעמיקה: מיקום קטבים ואפסים ביחס לאינקודר האבסולוטי (Poles & Zeros)

בבקרת FOC (Field Oriented Control), קיימות **3 נקודות ייחוס זוויתיות מרכזיות** המגדירות את תנועת הרוטור:

```
          [ אפס מכני של האינקודר (θm,abs = 0°) ]
                         │
                         │  היסט זוויתי קבוע: θoffset = 58.98° (1.0295 rad)
                         ▼
        [ ציר השטף המגנטי של הרוטור (d-axis) ]
                         │
                         │  קשר חשמלי: θe = (2 · θm,abs + θoffset) mod 360°
                         ▼
          [ אפס חשמלי של הסטטור (θe = 0°) ]
```

### א. אפס מכני אבסולוטי של האינקודר ($\theta_{m,\text{abs}} = 0.00^\circ$, צעד 0)
* **מהות**: נקודת ה-Zero Index האופטית המוטבעת פיזית על הדיסק של חיישן **SICK SFM60**.
* **זווית חשמלית בנקודה זו**:
  $$\theta_e = (2 \cdot 0.00^\circ + 58.98^\circ) = \mathbf{58.98^\circ_e}$$

### ב. קוטב צפוני ראשי 1 (North Pole 1 / $d$-axis 1, $\theta_e = 0.0^\circ$)
* **מיקום מכני אבסולוטי**: **$\theta_{m,\text{abs}} = 330.56^\circ$** (קריאת צעדים: `30,088`).
* **מהות**: זהו המיקום הפיזי שאליו ננעל הרוטור כאשר מזרימים זרם DC מוגבל בפאזה $U (+) \rightarrow (V+W) (-)$ במחזור הראשון.

### ג. קוטב צפוני ראשי 2 (North Pole 2 / $d$-axis 2, $\theta_e = 360.0^\circ \equiv 0.0^\circ$)
* **מיקום מכני אבסולוטי**: **$\theta_{m,\text{abs}} = 150.34^\circ$** (קריאת צעדים: `13,684`).
* **מהות**: מכיוון שהמנוע הוא בעל **$p = 2$ זוגות קטבים**, קיימים 2 קטבים צפוניים בסיבוב מכני אחד. קוטב 2 מרוחק בדיוק **$180.00^\circ$ מכני** מקוטב 1 ($330.56^\circ - 180.00^\circ = 150.56^\circ \approx 150.34^\circ$).

### ד. קטבים דרומיים (South Poles, $\theta_e = 180.0^\circ, 540.0^\circ$)
* **קוטב דרומי 1 ($\theta_e = 180^\circ$)**: נמצא ב-**$\theta_{m,\text{abs}} = 60.60^\circ$** (צעדים: `5,516`, שלב 4).
* **קוטב דרומי 2 ($\theta_e = 540^\circ \equiv 180^\circ$)**: נמצא ב-**$\theta_{m,\text{abs}} = 240.56^\circ$** (צעדים: `21,896`, שלב 10).

---

## 📐 3. נוסחת ההמרה הרגעית ל-FOC ב-Typhoon HIL

$${\large \theta_e = \left( 2 \cdot \theta_{m,\text{abs}} + 58.98^\circ \right) \pmod{360^\circ}}$$

ברדיאנים:
$${\large \theta_e \text{ [rad]} = \left( 2 \cdot \theta_{m,\text{rad}} + 1.0295 \text{ rad} \right) \pmod{2\pi}}$$

---

## 📊 4. טבלת תוצאות המדידות בפועל ומיפוי כל 13 השלבים

| שלב (#) | מחזור | חיבור בספק DC | $\theta_e$ חשמלי | $\theta_m$ צפוי | קריאה גולמית (32-bit SCADA) | צעדים (15-bit) | $\theta_m$ נמדד | הפרש צעד משלב 1 | שגיאת צעד | $\theta_{\text{offset}}$ מחושב | משמעות פיזיקלית / סטטוס |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | מחזור 1 | $U (+) \rightarrow (V+W) (-)$ | $0.0^\circ$ | **$0.0^\circ$ (Ref)** | `18216328` | 30,088 | **$330.56^\circ$** | **$0.00^\circ$** | ייחוס | **$58.89^\circ$** | 🔴 **קוטב צפוני 1 (d-axis)** |
| **2** | מחזור 1 | $(U+V) (+) \rightarrow W (-)$ | $60.0^\circ$ | **$+30.0^\circ$** | `18219040` | 32 | **$0.35^\circ$** | **$+29.79^\circ$** | $-0.21^\circ$ | **$59.30^\circ$** | 🟢 **וקטור V2** |
| **3** | מחזור 1 | $V (+) \rightarrow (U+W) (-)$ | $120.0^\circ$ | **$+60.0^\circ$** | `18221786` | 2,778 | **$30.52^\circ$** | **$+59.96^\circ$** | $-0.04^\circ$ | **$58.96^\circ$** | 🟢 **וקטור V3** |
| **4** | מחזור 1 | $(V+W) (+) \rightarrow U (-)$ | $180.0^\circ$ | **$+90.0^\circ$** | `18224524` | 5,516 | **$60.60^\circ$** | **$+90.04^\circ$** | $+0.04^\circ$ | **$58.80^\circ$** | 🔵 **קוטב דרומי 1** |
| **5** | מחזור 1 | $W (+) \rightarrow (U+V) (-)$ | $240.0^\circ$ | **$+120.0^\circ$** | `18227260` | 8,252 | **$90.66^\circ$** | **$+120.10^\circ$** | $+0.10^\circ$ | **$58.68^\circ$** | 🟢 **וקטור V5** |
| **6** | מחזור 1 | $(W+U) (+) \rightarrow V (-)$ | $300.0^\circ$ | **$+150.0^\circ$** | `18229984` | 10,976 | **$120.59^\circ$** | **$+150.03^\circ$** | $+0.03^\circ$ | **$58.83^\circ$** | 🟢 **וקטור V6** |
| **7** | מחזור 2 | $U (+) \rightarrow (V+W) (-)$ | $360.0^\circ$ | **$+180.0^\circ$** | `18232692` | 13,684 | **$150.34^\circ$** | **$+179.78^\circ$** | $-0.22^\circ$ | **$59.33^\circ$** | 🔴 **קוטב צפוני 2 (חצי סיבוב)** |
| **8** | מחזור 2 | $(U+V) (+) \rightarrow W (-)$ | $420.0^\circ$ | **$+210.0^\circ$** | `18235444` | 16,436 | **$180.57^\circ$** | **$+210.01^\circ$** | $+0.01^\circ$ | **$58.86^\circ$** | 🟢 **וקטור V2'** |
| **9** | מחזור 2 | $V (+) \rightarrow (U+W) (-)$ | $480.0^\circ$ | **$+240.0^\circ$** | `18238156` | 19,148 | **$210.37^\circ$** | **$+239.81^\circ$** | $-0.19^\circ$ | **$59.27^\circ$** | 🟢 **וקטור V3'** |
| **10** | מחזור 2 | $(V+W) (+) \rightarrow U (-)$ | $540.0^\circ$ | **$+270.0^\circ$** | `18240904` | 21,896 | **$240.56^\circ$** | **$+270.00^\circ$** | **$0.00^\circ$** | **$58.89^\circ$** | 🔵 **קוטב דרומי 2** |
| **11** | מחזור 2 | $W (+) \rightarrow (U+V) (-)$ | $600.0^\circ$ | **$+300.0^\circ$** | `18243618` | 24,610 | **$270.37^\circ$** | **$+299.82^\circ$** | $-0.18^\circ$ | **$59.25^\circ$** | 🟢 **וקטור V5'** |
| **12** | מחזור 2 | $(W+U) (+) \rightarrow V (-)$ | $660.0^\circ$ | **$+330.0^\circ$** | `18246366` | 27,358 | **$300.56^\circ$** | **$+330.01^\circ$** | $+0.01^\circ$ | **$58.87^\circ$** | 🟢 **וקטור V6'** |
| **13'** | סיום | $U (+) \rightarrow (V+W) (-)$ | $720.0^\circ$ | **$+360.0^\circ$** | `18249096` | 30,088 | **$330.56^\circ$** | **$+360.00^\circ$** | **$0.00^\circ$** | **$58.89^\circ$** | 🟢 **סגירת סיבוב מושלמת** |

---

## 🔌 5. מפרט חיווט ואינטגרציית מודול DFRobot DFR0845

מודול **DFRobot Gravity DFR0845** הוא ממיר RS-485 ל-UART אקטיבי ומבודד (3000V).

### טבלת חיבורי חומרה מלאה:
* **צד UART (מחבר Gravity 4 פינים אל Typhoon HIL404 DIO):**
  * `+` (VCC) $\rightarrow$ פין **5V** (או 3.3V) ב-HIL404 DIO.
  * `–` (GND) $\rightarrow$ פין **GND** ב-HIL404 DIO.
  * `T` (TXD) $\rightarrow$ פין **DI1** (Digital Input ב-HIL404).
  * `R` (RXD) $\rightarrow$ פין **DO1** (Digital Output ב-HIL404).
* **צד RS-485 (טרמינל ברגים אל אינקודר SICK SFM60):**
  * `A` $\rightarrow$ SICK **Pin 7 (Data +)**.
  * `B` $\rightarrow$ SICK **Pin 8 (Data -)**.
  * `GND` $\rightarrow$ SICK **Pin 2 (GND / 0V)** + סיכוך (Shield).
  * `12V` $\rightarrow$ SICK **Pin 1 (Us אספקת מתח 7-12V)**.

### 💡 פתרון בעיית עכבת ה-UART (2.5V בקו DO1 $\rightarrow$ R):
* **הבעיה**: מעגל ה-Level Shifter של ה-DFR0845 כולל נגד Pull-Up פנימי של $10\text{k}\Omega$ ל-VCC, מה שגרם למתח בקו `R` לרדת רק ל-2.5V במקום ל-0V.
* **הפתרון שנבדק ואושר**: חיבור נגד **Pull-Down של $1\text{k}\Omega$** (או בטווח $470\ \Omega - 1\text{k}\Omega$) **בין פין `R` לבין `GND`**.
* **התוצאה**: מתח ה-LOW יורד כעת ל-**$0.35\text{V} - 0.45\text{V}$** (רמת Logic LOW תקינה), והתקשורת הסדרתית פועלת באופן חלק.

---

## 🔌 6. מפרט ואינטגרציה לכרטיס Digilent Pmod RS485 (פתרון מושלם ל-5V)

כרטיס ה-**Digilent Pmod RS485** (מבוסס רכיב **Analog Devices ADM2582E**) תומך בעבודה ב-**5V מלא ($3.0\text{V} - 5.5\text{V}$)** עם כניסות CMOS בעלות עכבה אינסופית (High-Z) ללא מחלקי מתח.

### טבלת חיבורי Digilent Pmod RS485:
* **צד ה-UART (מחבר J2 בן 6 פינים מול Typhoon HIL404):**
  * `Pin 1 (~RE)` $\longleftrightarrow$ **קצר (Jumper) לפין 4 (`DE`)**.
  * `Pin 2 (TXD)` $\longleftrightarrow$ פין **`DO1`** ב-HIL404 (כניסת שידור UART).
  * `Pin 3 (RXD)` $\longleftrightarrow$ פין **`DI1`** ב-HIL404 (קליטת תשובות).
  * `Pin 4 (DE)` $\longleftrightarrow$ **קצר לפין 1 (`~RE`)**.
  * `Pin 5 (GND)` $\longleftrightarrow$ פין **`GND`** ב-HIL404 DIO.
  * `Pin 6 (VCC)` $\longleftrightarrow$ פין **`5V` (VCC)** ב-HIL404 DIO.
* **צד ה-RS485 (טרמינל ברגים J1 מול אינקודר SICK SFM60 ב-Half Duplex):**
  * **הדק `A` + הדק `Y` (קצר יחד)** $\longleftrightarrow$ **SICK Pin 7 (Data+)**.
  * **הדק `B` + הדק `Z` (קצר יחד)** $\longleftrightarrow$ **SICK Pin 8 (Data-)**.
  * **הדק `GND`** $\longleftrightarrow$ **SICK Pin 2 (GND/0V) + Shield**.
* **ג'מפר `JP1` (Termination):** סגור (Loaded) להפעלת נגד סיום קו של **$120\ \Omega$**.

---

## 💻 6. קוד C המוטמע במודל `PMSM_Position_Reader_HIL404_v1.tse`

```c
// ============================================================================
// Typhoon HIL404 - High Resolution Electrical Angle & FOC Commutation
// Motor: OEMER QS 100S (4 Poles, p = 2) | Feedback: SICK SFM60 HIPERFACE
// Calibrated from 13-Step Full 360° Mechanical Revolution Lab Protocol
// ============================================================================

#define POLE_PAIRS 2                                   // 4 Poles (p = 2)
#define TWO_PI     (2.0 * 3.14159265358979323846)

// Calibrated Pole Position Offset Angle (From Full 360° Lab Protocol)
#define THETA_OFFSET_DEG 58.98
#define THETA_OFFSET_RAD (58.98 * (3.14159265358979323846 / 180.0)) // 1.0295 rad

// 1. Calculate Instantaneous Electrical Angle for Park & Clarke Transformations
double theta_e = fmod(POLE_PAIRS * hires_rad + THETA_OFFSET_RAD, TWO_PI);
if (theta_e < 0.0) {
    theta_e += TWO_PI;
}

// 2. Output electrical angle in degrees for SCADA monitoring
double theta_e_deg = theta_e * (180.0 / 3.14159265358979323846);
```

---

## 📂 7. קישורים ישירים לקבצי הפרויקט

* 📄 **דוח ה-PDF הרשמי להדפסה (A4 5 עמודים)**: [OEMER_QS100S_Pole_Alignment_Report_A4.pdf](file:///c:/Users/maximr/OneDrive%20-%20ac.sce.ac.il/Barabi/2025%20Eli%20&%20Max/PMSM/OEMER_QS100S_Pole_Alignment_Report_A4.pdf)
* 🌐 **דוח סיכום ומסקנות HTML**: [DOC_10_Pole_Alignment_Final_Experiment_Summary.html](file:///c:/Users/maximr/OneDrive%20-%20ac.sce.ac.il/Barabi/2025%20Eli%20&%20Max/PMSM/HTML_Reports/DOC_10_Pole_Alignment_Final_Experiment_Summary.html)
* 📊 **טופס המדידות המלא (DOC 09)**: [DOC_09_Pole_Alignment_Measurement_Protocol.html](file:///c:/Users/maximr/OneDrive%20-%20ac.sce.ac.il/Barabi/2025%20Eli%20&%20Max/PMSM/HTML_Reports/DOC_09_Pole_Alignment_Measurement_Protocol.html)
* ⚙️ **מודל הסימולציה ב-Typhoon HIL**: [PMSM_Position_Reader_HIL404_v1.tse](file:///c:/Users/maximr/OneDrive%20-%20ac.sce.ac.il/Barabi/2025%20Eli%20&%20Max/PMSM/HIL_PMSM/PMSM_Position_Reader_HIL404_v1.tse)
* 🎛️ **פאנל ה-SCADA המכויל**: [PANEL_Position_Monitor_v1.cus](file:///c:/Users/maximr/OneDrive%20-%20ac.sce.ac.il/Barabi/2025%20Eli%20&%20Max/PMSM/HIL_PMSM/PANEL_Position_Monitor_v1.cus)
* 🏠 **פורטל הניווט הראשי**: [index.html](file:///c:/Users/maximr/OneDrive%20-%20ac.sce.ac.il/Barabi/2025%20Eli%20&%20Max/PMSM/index.html)

</div>
