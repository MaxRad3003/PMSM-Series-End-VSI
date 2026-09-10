# -*- coding: utf-8 -*-
"""
Module containing enriched, didactic, and pedagogical texts for Chapters 1, 2, 4, 5, 6, 7.
"""

def get_didactic_css():
    return '''
        /* Didactic Pedagogical Callout Cards */
        .didactic-box {
            border-radius: 14px;
            padding: 22px 26px;
            margin: 26px 0;
            position: relative;
            line-height: 1.7;
            box-shadow: var(--shadow-card);
            font-size: 14.5px;
        }
        .didactic-box h4 {
            margin: 0 0 10px 0;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 16px;
            font-family: 'Rubik', sans-serif;
            font-weight: 700;
        }
        .didactic-intuition {
            background: linear-gradient(135deg, rgba(0, 210, 255, 0.08), rgba(16, 185, 129, 0.06));
            border: 1px solid rgba(0, 210, 255, 0.35);
            border-right: 5px solid var(--accent-cyan);
        }
        .didactic-intuition h4 { color: var(--accent-cyan); }

        .didactic-math {
            background: linear-gradient(135deg, rgba(157, 80, 187, 0.08), rgba(59, 130, 246, 0.08));
            border: 1px solid rgba(157, 80, 187, 0.35);
            border-right: 5px solid var(--accent-purple);
        }
        .didactic-math h4 { color: #c4b5fd; }

        .didactic-pitfall {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(245, 158, 11, 0.06));
            border: 1px solid rgba(239, 68, 68, 0.35);
            border-right: 5px solid var(--accent-rose);
        }
        .didactic-pitfall h4 { color: #fca5a5; }

        .didactic-lab {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(0, 210, 255, 0.06));
            border: 1px solid rgba(16, 185, 129, 0.35);
            border-right: 5px solid var(--accent-green);
        }
        .didactic-lab h4 { color: #6ee7b7; }

        /* Step-by-step numerical walkthrough container */
        .walkthrough-box {
            background: rgba(5, 8, 17, 0.9);
            border: 1px solid rgba(245, 158, 11, 0.35);
            border-radius: 14px;
            padding: 24px;
            margin: 26px 0;
            box-shadow: var(--shadow-card);
        }
        .walkthrough-box h4 {
            color: var(--accent-amber);
            font-size: 16.5px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .step-item {
            display: flex;
            gap: 14px;
            margin-bottom: 16px;
            align-items: flex-start;
        }
        .step-num {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: var(--accent-amber);
            color: #000;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 13px;
            flex-shrink: 0;
            margin-top: 2px;
        }
        .step-content {
            flex: 1;
            font-size: 14px;
            color: var(--text-main);
            line-height: 1.6;
        }
        .step-content strong {
            color: #fff;
        }
    '''

def get_chapter1_html():
    return r'''id="ch-01">
                    <span class="chapter-badge">פרק 01</span>
                    <h2>רקע מדעי, אתגרי הנע חשמלי וטופולוגיית Series-End VSI</h2>
                    
                    <p>
                        במערכות הנע תעשייתיות מתקדמות, רכבים חשמליים (<span class="en-term">EV</span>) ורחפני תעופה, ממירי מתח מסורתיים בעלי שתי רמות (<span class="en-term">2-Level VSI</span>) מתקרבים לגבול יכולתם הפיזיקלית. המגבלות המרכזיות כוללות:
                    </p>
                    <ul class="bullet-list">
                        <li><strong>מתחי פריצה והפסדי מיתוג:</strong> מתח ה-DC המלא נופל ישירות על כל טרנזיסטור, מה שמחייב שימוש ברכיבי סיליקון בעלי עמידות מתח כפולה ומגדיל משמעותית את הפסדי המיתוג.</li>
                        <li><strong>עיוות הרמוני כולל (THD גבוה):</strong> מתח המוצא בעל 2 רמות בלבד יוצר קפיצות מתח חדות ($dv/dt$ קיצוני), המחייבות מסננים מגושמים ומגבירות רעש אלקטרומגנטי (EMI).</li>
                        <li><strong>מתחי Common-Mode וזרמי מיסבים:</strong> מיתוג מהיר גורם למתחי ציפה גבוהים בנקודת הנייטרל, המובילים לפריקות קשתיות במיסבי המנוע (Bearing Currents) וקיצור דרמטי באורך חיי המערכת.</li>
                    </ul>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/fig1_se_vsi_system_overview.jpg" alt="SE-VSI System Architecture" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 1.1:</strong> ארכיטקטורת המערכת הכוללת: מנוע PMSM בעל קצוות סלילים פתוחים (Open-End Windings) המוזן מממיר Series-End VSI עם קבלי ציפה ובקרת OEPC.</div>
                    </div>

                    <h3>טופולוגיית סלילים פתוחים בטור (Series-End VSI) — לא כוכב ולא משולש!</h3>
                    <p>
                        במנוע תלת-פאזי קונבנציונלי, שלושת הסלילים מחוברים בקצה אחד בנקודת כוכב משותפת ($N$) או במשולש ($\Delta$). לעומת זאת, בטופולוגיית <strong>Open-End Winding (OW-PMSM)</strong> כל ששת קצות הסלילים מנותקים ונגישים פיזית לחיבור חיצוני.
                    </p>
                    <p>
                        בטופולוגיית <strong>Series-End VSI (איור 1.2 להלן, לפי איור 2 מהמאמר)</strong>, סלילי המנוע מחוברים <strong>בטור ישיר בין 4 ענפי הממיר העוקבים</strong> ($L_1, L_2, L_3, L_4$):
                    </p>
                    <ul class="bullet-list">
                        <li><strong>סליל פאזה A ($Z_a$):</strong> מחובר בין אמצע ענף 1 ($v_1$) לבין אמצע ענף 2 ($v_2$). מתח הפאזה הינו: $v_a = v_1 - v_2$.</li>
                        <li><strong>סליל פאזה B ($Z_b$):</strong> מחובר בין אמצע ענף 2 ($v_2$) לבין אמצע ענף 3 ($v_3$). מתח הפאזה הינו: $v_b = v_2 - v_3$.</li>
                        <li><strong>סליל פאזה C ($Z_c$):</strong> מחובר בין אמצע ענף 3 ($v_3$) לבין אמצע ענף 4 ($v_4$). מתח הפאזה הינו: $v_c = v_3 - v_4$.</li>
                    </ul>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/fig2_se_vsi_topology_and_zsc_path.jpg" alt="SE-VSI Topology & ZSC Path" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 1.2 (איור 2 מהמאמר):</strong> סכמת המעגל החשמלי של ממיר Series-End VSI בעל 4 ענפים ($L_1-L_4$) וסלילי מנוע טוריים ($Z_a, Z_b, Z_c$). קו החצים האדום ממחיש את מסלול הלולאה הסגור שבו עלול להתפתח זרם סדרה אפס ($i_0$).</div>
                    </div>

                    <div class="didactic-box didactic-intuition">
                        <h4>💡 אינטואיציה פיזיקלית: מדוע חיבור טורי בין ענפים מייצר 4 רמות מתח אפקטיביות?</h4>
                        מכיוון שמתח כל פאזה נגזר מהפרש הפוטנציאלים בין שני ענפים עוקבים ($v_x = v_k - v_{k+1}$), וכל ענף יכול להתחבר לפוטנציאל $+V_{dc}/2$ או $-V_{dc}/2$, מתח הפאזה יכול לקבל רמות מיתוג מגוונות: $+V_{dc}$, $+V_{dc}/2$, $0$, $-V_{dc}/2$, $-V_{dc}$. התוצאה היא <strong>מתח רב-רמתי (Multi-level)</strong> בעל איכות גל עילאית, המושג באמצעות ספק DC יחיד וארבעה ענפים בלבד!
                    </div>

                    <h3>אתגר זרמי סדרה אפס (Zero-Sequence Current - ZSC) בלולאה הסגורה</h3>
                    <p>
                        אולם, ליתרון העצום של החיבור הטורי יש מחיר פיזיקלי קריטי. נבחן את סכום המתחים הנופלים על שלושת סלילי המנוע לאורך המסלול הטורי:
                    </p>

                    <div class="math-block">
                        $$\sum_{x \in \{a,b,c\}} v_x = v_a + v_b + v_c = (v_1 - v_2) + (v_2 - v_3) + (v_3 - v_4) = v_1 - v_4$$
                    </div>

                    <p>
                        <strong>שים לב לתוצאה המפתיעה:</strong> המתח הכולל של הלולאה תלוי אך ורק בהפרש המיתוג בין הענף הראשון ($L_1$) לענף האחרון ($L_4$)!
                    </p>
                    <ul class="bullet-list">
                        <li>אם $v_1 = v_4$, אזי סכום המתחים הוא אפס, ולא מתפתח זרם סדרה אפס.</li>
                        <li>אם $v_1 \neq v_4$ (למשל, ענף 1 מחובר למתח העליון $+V_{dc}$ וענף 4 לאדמה $0$), נופל מתח DC מלא על סכום שלושת הסלילים בטור!</li>
                    </ul>

                    <div class="didactic-box didactic-math">
                        <h4>📐 פיתוח מתמטי: משוואת הדינמיקה של זרם הסדרה האפס ($i_0$)</h4>
                        נגדיר את זרם הסדרה האפס כסכום זרמי הפאזות:
                        $$i_0 = \frac{i_a + i_b + i_c}{3}$$
                        משוואת המתחים של רכיב הסדרה האפס במנוע PMSM נתונה על-ידי:
                        $$v_0 = \frac{v_a + v_b + v_c}{3} = \frac{v_1 - v_4}{3} = R_0 i_0 + L_0 \frac{di_0}{dt} + e_0$$
                        כאשר $R_0$ היא התנגדות הסדרה האפס, $L_0$ היא השראות הסדרה האפס של הסטטור, ו-$e_0$ הוא הכא"מ המושרה של הרמוניה שלישית (שבמנועי PMSM סינוסואידליים הינו זניח).
                    </div>

                    <div class="didactic-box didactic-pitfall">
                        <h4>⚠️ מלכודת הנדסית: מדוע השראות $L_0$ נמוכה כל כך ומהווה סכנה למנוע?</h4>
                        במנועי PMSM סימטריים, השטף המגנטי שיוצרים זרמי סדרה אפס ($i_0$) הוא הומופולרי (זהה בכל שלושת הפאזות בזמן ובמרחב). כתוצאה מכך, <strong>אין שום שטף הדדי בין הפאזות</strong> שמסייע בבלימת הזרם! השראות $L_0$ קטנה בדרך כלל פי 3 עד פי 5 מההשראות הסינכרונית ($L_d, L_q$).<br>
                        <strong>המשמעות ההרסנית:</strong> אפילו הפרש מתח מזערי או פעימת מיתוג קצרה בין $v_1$ ל-$v_4$ גורמים לנגזרת זרם ענקית ($di_0/dt = \Delta v / L_0$). זרם ה-ZSC מתפרץ לממדים של אמפרים רבים, מעוות את זרמי הפאזה לגל דמוי טרפז, גורם לחימום קטלני של הסטטור ומפיל את הממיר על זרם יתר!
                    </div>
                </section>

                <!-- ============================================================ -->
                <!-- CHAPTER 2: OEPC ALGORITHM & 96-LUT                           -->
                <!-- ============================================================ -->
                <section class="chapter-section" '''

def get_chapter2_html():
    return r'''id="ch-02">
                    <span class="chapter-badge">פרק 02</span>
                    <h2>אלגוריתם בקרת שגיאה אופטימלית (OEPC) ומבנה טבלת 96 המצבים</h2>

                    <h3>המגבלות של שיטות הבקרה הקיימות: מדוע נדרש OEPC?</h3>
                    <p>
                        בספרות המדעית הוצעו מספר גישות לטיפול באתגר ה-ZSC בממירי סדרה, אך כולן סובלות מנחיתות מהותית:
                    </p>
                    <ul class="bullet-list">
                        <li><strong>שיטת חלוקת הזמן (TDM - Time-Division Multiplexing):</strong> מחלקת כל מחזור מיתוג לשני חצאים מובחנים — מחצית לבקרת זרמי הפאזות הדיפרנציאליים, ומחצית שנייה לדיכוי ה-ZSC. גישה זו "מבזבזת" 50% מזמן המיתוג, מגדילה משמעותית את הריפל, ומגבילה את רוחב הפס הדינמי של מהירות המנוע.</li>
                        <li><strong>אפנון וקטורי מוגבל (CBPWM with Zero-State Selection):</strong> מגבילה את מרחב הוקטורים רק לוקטורים שבהם $v_1 = v_4$. הגבלה זו מפחיתה בכ-15% את ניצולת מתח ה-DC ומאלצת הזרקת מתחי Common-Mode מורכבים.</li>
                    </ul>

                    <p>
                        <strong>מהפכת ה-OEPC (Optimal Error-Priority Control):</strong> במקום להתפשר על חלוקת זמן או להגביל את הממיר, אלגוריתם ה-OEPC ממפה בזמן-אמת את <strong>כל שש שגיאות הזרם של המערכת</strong>, ממיין אותן לפי חומרתן, ובוחר פסיקת מיתוג יחידה מתוך טבלת 96-LUT שמתקנת <strong>בו-זמנית</strong> הן את הפאזה בעלת השגיאה הדחופה ביותר והן את זרם ה-ZSC!
                    </p>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/fig3_oepc_flowchart_algorithm.jpg" alt="OEPC Flowchart Algorithm" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 2.1:</strong> תרשים זרימה פדגוגי של אלגוריתם ה-OEPC: דגימת זרמים, חישוב 6 שגיאות, מיון עדיפות, קביעת ביט פאזה מועדפת ($F_{mp}$), הרכבת כתובת 7 ביטים ושליפת וקטור המיתוג בצעד שעון יחיד.</div>
                    </div>

                    <h3>הגדרה דידקטית של 6 שגיאות הזרם</h3>
                    <p>
                        בכל מחזור בקרה (בתדר דגימה של $20\text{ kHz}$ עד $50\text{ kHz}$), נדגמים הזרמים הרגעיים $i_a, i_b, i_c$, ומחושב רכיב ה-ZSC: $i_0 = (i_a+i_b+i_c)/3$.<br>
                        מול ערכי הייחוס המבוקשים מהבקר העליון ($i_a^*, i_b^*, i_c^*$ ו-$i_0^* = 0$), מוגדרות 6 שגיאות:
                    </p>

                    <div class="math-block">
                        $$\begin{aligned}
                        e_a &= i_a^* - i_a, \quad &e_b &= i_b^* - i_b, \quad &e_c &= i_c^* - i_c \quad &\text{[Phase Errors]} \\
                        e_{ab} &= e_a - e_b, \quad &e_{bc} &= e_b - e_c, \quad &e_{ca} &= e_c - e_a \quad &\text{[Line-to-Line Errors]}
                        \end{aligned}$$
                    </div>

                    <h3>מיון עדיפויות בחומרה (Hardware Priority Sorting)</h3>
                    <p>
                        כדי להבטיח זמני תגובה של ננו-שניות ב-FPGA או ב-DSP, מתבצעת השוואה מהירה בין הערכים המוחלטים של שגיאות הפאזה: $|e_a|, |e_b|, |e_c|$.<br>
                        קיימות בדיוק $3! = 6$ תמורות אפשריות של סדר השגיאות, המקודדות לקוד עדיפות <strong>$S_{sel}$ בן 3 ביטים</strong>:
                    </p>

                    <div class="table-container">
                        <table class="styled-table">
                            <thead>
                                <tr>
                                    <th>סדר עדיפות שגיאות (EPO)</th>
                                    <th>משמעות הנדסית</th>
                                    <th>קוד עדיפות בינארי ($S_{sel}$)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td>$|e_a| \gt |e_b| \gt |e_c|$</td><td>פאזה A דחופה ביותר, אחריה B, ו-C הקטנה ביותר</td><td><code>000_2</code> (ABC)</td></tr>
                                <tr><td>$|e_a| \gt |e_c| \gt |e_b|$</td><td>פאזה A דחופה ביותר, אחריה C, ו-B הקטנה ביותר</td><td><code>001_2</code> (ACB)</td></tr>
                                <tr><td>$|e_b| \gt |e_a| \gt |e_c|$</td><td>פאזה B דחופה ביותר, אחריה A, ו-C הקטנה ביותר</td><td><code>010_2</code> (BAC)</td></tr>
                                <tr><td>$|e_b| \gt |e_c| \gt |e_a|$</td><td>פאזה B דחופה ביותר, אחריה C, ו-A הקטנה ביותר</td><td><code>011_2</code> (BCA)</td></tr>
                                <tr><td>$|e_c| \gt |e_a| \gt |e_b|$</td><td>פאזה C דחופה ביותר, אחריה A, ו-B הקטנה ביותר</td><td><code>100_2</code> (CAB)</td></tr>
                                <tr><td>$|e_c| \gt |e_b| \gt |e_a|$</td><td>פאזה C דחופה ביותר, אחריה B, ו-A הקטנה ביותר</td><td><code>101_2</code> (CBA)</td></tr>
                            </tbody>
                        </table>
                    </div>

                    <h3>קביעת ביט הפאזה המועדפת ($F_{mp}$) ודיכוי ה-ZSC</h3>
                    <p>
                        ביט ה-<strong>$F_{mp}$ (Favored Mode Priority)</strong> הוא "המוח" של אלגוריתם ה-OEPC. הוא מכריע האם להפעיל תיקון זרם דיפרנציאלי חזק או לתת עדיפות עליונה לריסון ה-ZSC:
                    </p>
                    <ul class="bullet-list">
                        <li>אם גודל זרם ה-ZSC חורג מגבול מוגדר ($|i_0| \gt \Delta i_{0,\text{tol}}$) ונדרש תיקון חירום &larr; נקבע <strong>$F_{mp} = 0$</strong>. במצב זה נבחר וקטור מיתוג המפעיל מתח נגדי חריף של $v_1 - v_4$ לדיכוי מיידי של ה-ZSC.</li>
                        <li>אם זרם ה-ZSC נמצא בתחום הסביר ($|i_0| \le \Delta i_{0,\text{tol}}$) ושגיאת הפאזות דומיננטית &larr; נקבע <strong>$F_{mp} = 1$</strong>. במצב זה המערכת מתמקדת במעקב סינוסואידלי מדויק של זרמי העבודה.</li>
                    </ul>

                    <h3>הרכבת כתובת ה-LUT בת 7 ביטים ושליפת וקטור המיתוג</h3>
                    <p>
                        כתובת הגישה לטבלת ה-LUT מורכבת משרשור שלושה שדות בינאריים:
                    </p>
                    <div class="math-block">
                        $$\text{Address (7 Bits)} = \underbrace{F_{mp}}_{1 \text{ Bit}} \;\Big|\; \underbrace{S_{sel}}_{3 \text{ Bits}} \;\Big|\; \underbrace{S_{sgn}}_{3 \text{ Bits}}$$
                    </div>
                    <ul class="bullet-list">
                        <li><strong>$F_{mp}$ (ביט 6):</strong> דגל עדיפות ZSC מול פאזות ($0$ או $1$).</li>
                        <li><strong>$S_{sel}$ (ביטים 5..3):</strong> קוד עדיפות השגיאה (000 עד 101, סה"כ 6 מצבים).</li>
                        <li><strong>$S_{sgn}$ (ביטים 2..0):</strong> סימני השגיאה של שלושת הפאזות: $\text{sign}(e_a), \text{sign}(e_b), \text{sign}(e_c)$ ($0$ לשלילי, $1$ לחיובי). מתוך 8 קומבינציות סימנים, $111$ ו-$000$ אינן מתקיימות במערכת מאוזנת ללא ZSC קיצוני.</li>
                    </ul>
                    <p>
                        סך כל הכתובות הפעילות בטבלה: $2 \times 6 \times 8 = 96$ מצבים!
                    </p>

                    <!-- NUMERICAL WALKTHROUGH BOX -->
                    <div class="walkthrough-box">
                        <h4>🔍 דוגמה מספרית מודרכת: חישוב צעד-אחר-צעד של אלגוריתם ה-OEPC</h4>
                        <p style="color:var(--text-muted); margin-bottom:14px;">
                            נניח כי ברגע דגימה מסוים נתונים זרמי הייחוס והזרמים הנמדדים הבאים:
                        </p>
                        <div class="step-item">
                            <span class="step-num">1</span>
                            <div class="step-content">
                                <strong>ערכי זרם רגעיים:</strong><br>
                                ייחוס מבוקש: $i_a^* = +4.0\text{A}, \quad i_b^* = -2.0\text{A}, \quad i_c^* = -2.0\text{A}$ (סכום $= 0$).<br>
                                זרם נמדד בפועל: $i_a = +3.2\text{A}, \quad i_b = -1.7\text{A}, \quad i_c = -2.1\text{A}$.<br>
                                זרם סדרה אפס קיים: $i_0 = (3.2 - 1.7 - 2.1)/3 = -0.20\text{A}$.
                            </div>
                        </div>
                        <div class="step-item">
                            <span class="step-num">2</span>
                            <div class="step-content">
                                <strong>חישוב שגיאות הזרם:</strong><br>
                                $e_a = i_a^* - i_a = 4.0 - 3.2 = \mathbf{+0.80\text{A}}$ (חיובי, פאזה A בחסר זרם גדול!)<br>
                                $e_b = i_b^* - i_b = -2.0 - (-1.7) = \mathbf{-0.30\text{A}}$ (שלילי)<br>
                                $e_c = i_c^* - i_c = -2.0 - (-2.1) = \mathbf{+0.10\text{A}}$ (חיובי)
                            </div>
                        </div>
                        <div class="step-item">
                            <span class="step-num">3</span>
                            <div class="step-content">
                                <strong>מיון גדלי שגיאות (Hardware Sorting):</strong><br>
                                $|e_a| = 0.80\text{A} \quad\gt\quad |e_b| = 0.30\text{A} \quad\gt\quad |e_c| = 0.10\text{A}$<br>
                                סדר העדיפות הינו: $\mathbf{ABC}$ &larr; קוד עדיפות: $S_{sel} = \mathbf{000_2}$.
                            </div>
                        </div>
                        <div class="step-item">
                            <span class="step-num">4</span>
                            <div class="step-content">
                                <strong>קוד סימני שגיאה ($S_{sgn}$):</strong><br>
                                $e_a \gt 0 \rightarrow 1, \quad e_b \lt 0 \rightarrow 0, \quad e_c \gt 0 \rightarrow 1$<br>
                                קוד סימנים: $S_{sgn} = \mathbf{101_2}$.
                            </div>
                        </div>
                        <div class="step-item">
                            <span class="step-num">5</span>
                            <div class="step-content">
                                <strong>קביעת דגל $F_{mp}$ והרכבת הכתובת:</strong><br>
                                נניח כי $|i_0| = 0.20\text{A}$ נמצא בגבול המותר, ושגיאת פאזה A ($0.8\text{A}$) דורשת תיקון דחוף &larr; $F_{mp} = \mathbf{1}$.<br>
                                כתובת ה-7 ביטים המורכבת:<br>
                                $$\text{Address} = [F_{mp} \mid S_{sel} \mid S_{sgn}] = [1 \mid 000 \mid 101] = \mathbf{1000101_2} = \mathbf{69_{10}}$$
                            </div>
                        </div>
                        <div class="step-item">
                            <span class="step-num">6</span>
                            <div class="step-content">
                                <strong>שליפת וקטור המיתוג מתוך ה-LUT:</strong><br>
                                בכתובת $69$, הטבלה מחזירה את הוקטור: $\mathbf{V_{14} = [S_1, S_2, S_3, S_4] = [1, 0, 1, 1]}$.<br>
                                <strong>ניתוח פיזיקלי של מתחי הפאזה המתקבלים:</strong><br>
                                $v_a = v_1 - v_2 = +V_{dc} - 0 = \mathbf{+V_{dc}}$ &larr; דוחף בעוצמה מקסימלית זרם חיובי לפאזה A לתיקון מיידי של שגיאת $+0.80\text{A}$!<br>
                                $v_b = v_2 - v_3 = 0 - (+V_{dc}) = \mathbf{-V_{dc}}$ &larr; מתקן במקביל את שגיאת פאזה B!<br>
                                $v_c = v_3 - v_4 = +V_{dc} - (+V_{dc}) = \mathbf{0V}$ &larr; פאזה C עם השגיאה הקטנה ביותר ($0.1\text{A}$) אינה מקבלת מתח מיותר!<br>
                                הפרש רגלי הקצה: $v_1 - v_4 = +V_{dc} - (+V_{dc}) = \mathbf{0V}$ &larr; <strong>אינו מפתח ZSC חדש!</strong> תיקון מושלם ואופטימלי בצעד שעון בודד!
                            </div>
                        </div>
                    </div>

                    <h3>מדגם מתוך טבלת 96 המצבים המוטמעת ב-FPGA</h3>
                    <div class="table-container">
                        <table class="styled-table">
                            <thead>
                                <tr>
                                    <th>אינדקס</th>
                                    <th>סדר עדיפות (EPO)</th>
                                    <th>קוד $S_{sel}$</th>
                                    <th>קוד $S_{sgn}$</th>
                                    <th>$F_{mp}$</th>
                                    <th>וקטור מיתוג ($S_1 S_2 S_3 S_4$)</th>
                                    <th>מתחי פאזה אפקטיביים ($v_a, v_b, v_c$)</th>
                                    <th>השפעה פיזיקלית מתקנת</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="highlight-row">
                                    <td>01</td>
                                    <td>ABC</td>
                                    <td>000</td>
                                    <td>101</td>
                                    <td>1 (DM)</td>
                                    <td><code>1011</code></td>
                                    <td>$+V_{dc},\; -V_{dc},\; 0$</td>
                                    <td>תיקון מואץ $+i_a$ ו-$-i_b$ ללא עירור ZSC</td>
                                </tr>
                                <tr>
                                    <td>02</td>
                                    <td>ABC</td>
                                    <td>000</td>
                                    <td>100</td>
                                    <td>1 (DM)</td>
                                    <td><code>1000</code></td>
                                    <td>$+V_{dc},\; 0,\; 0$</td>
                                    <td>הזרקת פולס חיובי לפאזה A והרגעת שאר הפאזות</td>
                                </tr>
                                <tr class="highlight-row">
                                    <td>03</td>
                                    <td>CAB</td>
                                    <td>100</td>
                                    <td>011</td>
                                    <td>0 (CM)</td>
                                    <td><code>0110</code></td>
                                    <td>$-V_{dc},\; 0,\; +V_{dc}$</td>
                                    <td>דיכוי חירום של רכיב ה-ZSC ע"י איזון מתחי קצה</td>
                                </tr>
                                <tr>
                                    <td>04</td>
                                    <td>BCA</td>
                                    <td>011</td>
                                    <td>110</td>
                                    <td>1 (DM)</td>
                                    <td><code>1101</code></td>
                                    <td>$0,\; +V_{dc},\; -V_{dc}$</td>
                                    <td>תיקון משולב של פאזה B ופאזה C</td>
                                </tr>
                                <tr class="highlight-row">
                                    <td>05</td>
                                    <td>CBA</td>
                                    <td>101</td>
                                    <td>111</td>
                                    <td>1 (DM)</td>
                                    <td><code>1010</code></td>
                                    <td>$+V_{dc},\; -V_{dc},\; +V_{dc}$</td>
                                    <td>תיקון סימולטני של שלוש הפאזות במקביל</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </section>

                <!-- ============================================================ -->
                <!-- CHAPTER 3: INTERACTIVE LAB                                   -->
                <!-- ============================================================ -->
                <section class="chapter-section" '''

def get_chapter4_and_5_html():
    return r'''id="ch-04">
                    <span class="chapter-badge">פרק 04</span>
                    <h2>אימות סימולטיבי ב-PSIM ו-Typhoon C-HIL בזמן אמת</h2>

                    <h3>ארכיטקטורת מערך ה-C-HIL המעבדתי בזמן אמת</h3>
                    <p>
                        לפני מעבר לחיבור מנוע ומתח גבוה אמיתי, כלל האלגוריתם עבר אימות מלא בטכנולוגיית <strong>Controller Hardware-in-the-Loop (C-HIL)</strong>. במערך זה:
                    </p>
                    <ul class="bullet-list">
                        <li><strong>מודל ה-PMSM וממיר ה-SE-VSI</strong> סומלצו במחשב זמן-אמת ייעודי של חברת <strong>Typhoon HIL404</strong> בצעד חישוב זעיר של $1.0\,\mu\text{s}$.</li>
                        <li><strong>בקר ה-OEPC</strong> רץ על כרטיס הבקרה הפיזי (DSP/Microcontroller) שנדגם ומיתג את אותות ה-PWM ישירות דרך כניסות/יציאות דיגיטליות ואנלוגיות (GPIO & ADC) מהירות.</li>
                    </ul>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/fig4_experimental_setups_chil_prototype.jpg" alt="Experimental Setups C-HIL & Prototype" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 4.1:</strong> עמדת הניסוי המעבדתית: מודל ה-C-HIL בזמן אמת עם סימולטור Typhoon HIL404, לוחות הבקרה הפיזיים, כרטיסי הבידוד והדיינו.</div>
                    </div>

                    <h3>תוצאות תגובה דינמית לשינויי מדרגת מומנט ומהירות</h3>
                    <p>
                        נבדק מעקב הזרם תחת שינויי מדרגה חדים בזרם ה-q (מומנט) מ-$0\text{A}$ ל-$6\text{A}$ ותחת שינויי מהירות של המנוע.
                    </p>
                    <div class="fig-wrapper">
                        <img src="presentation_assets/fig10_pmsm_dynamic_response_speed_torque.jpg" alt="Dynamic Response Speed & Torque" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 4.2:</strong> תגובה דינמית של מנוע ה-PMSM: זרמי פאזה $i_a, i_b, i_c$, מהירות הרוטור ומומנט אלקטרומגנטי תחת מדרגת עומס. הבקר מתייצב תוך פחות מ-2 מילי-שניות ללא שום תופעות מעבר מזיקות!</div>
                    </div>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/fig12_chil_realtime_pmsm_results.jpg" alt="C-HIL Real-Time Results" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 4.3:</strong> מדידות C-HIL בזמן אמת: מעקב זרמי הפאזות ברוחב פס גבוה והוכחת דיכוי ה-ZSC לאפס מוחלט ($i_0 \approx 0.01\text{A}$).</div>
                    </div>

                    <h3>אימות תחת חוסר איזון פיזי קיצוני בסלילים ($\pm 25\%$)</h3>
                    <p>
                        אחד האתגרים הגדולים של ממירי Series-End הוא רגישותם לאי-סימטריה בסלילי המנוע (עקב פגמי ייצור, התחממות לא שווה, או הזדקנות בידוד). בקרת PWM רגילה קורסת בתנאים אלה ומפתחת זרם ZSC הרסני.
                    </p>
                    <div class="fig-wrapper">
                        <img src="presentation_assets/fig6_oepc_asymmetric_response.jpg" alt="OEPC Asymmetric Response" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 4.4:</strong> ביצועי OEPC תחת אי-סימטריה של 25%: זרמי הפאזה נשמרים עגולים וסימטריים לחלוטין, וזרם ה-ZSC מרוסן לגמרי!</div>
                    </div>
                </section>

                <!-- ============================================================ -->
                <!-- CHAPTER 5: FAULT TOLERANCE (ITSC)                            -->
                <!-- ============================================================ -->
                <section class="chapter-section" id="ch-05">
                    <span class="chapter-badge">פרק 05</span>
                    <h2>חסינות אינהרנטית לתקלות קצר פנימיות במנוע (ITSC)</h2>

                    <h3>הסכנה בתקלת קצר בין כריכות (Inter-Turn Short Circuit - ITSC)</h3>
                    <p>
                        תקלת ITSC היא התקלה הפנימית השכיחה והמסוכנת ביותר במנועי PMSM. כאשר בידוד הכריכות נפרץ ונוצר קצר בין מספר ליפופים באותה פאזה, נוצרת לולאת קצר מקומית שבה זורם זרם עצום המושרה מהמגנטים הקבועים. זרם זה מאיץ את שריפת המנוע, גורם לאי-סימטריה חריפה בעכבות הסטטור, ויוצר תנודות מומנט עזות.
                    </p>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/fig13_fault_tolerance_itsc_oepc_vs_cbpwm.jpg" alt="Fault Tolerance ITSC: OEPC vs CBPWM" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 5.1:</strong> השוואה ישירה תחת תקלת ITSC קשה: בקרת CBPWM רגילה (משמאל) מפתחת עיוות קיצוני בזרמים וזרם ZSC ענק; לעומתה בקרת OEPC (מימין) שומרת על מסלול מעגלי מושלם ומרסנת את הזרם התקול!</div>
                    </div>

                    <div class="didactic-box didactic-lab">
                        <h4>🔬 תובנה מדעית מתוצאות הניסוי באיור 5.1</h4>
                        בקרת OEPC אינה דורשת זיהוי מפורש (Fault Diagnosis) של התקלה כדי לפעול! מעצם הגדרתה, כאשר פאזה מקצרת וזרמה מתעוות, שגיאת הזרם של אותה פאזה מזנקת מיד ומקבלת עדיפות עליונה ב-LUT ($S_{sel}$). הממיר "מזריק" מתח נגדי שמאלץ את הזרם להישאר סינוסואידלי ומגן על המנוע מהתחממות קטסטרופלית!
                    </div>
                </section>

                <!-- ============================================================ -->
                <!-- CHAPTER 6: MOTOR CHARACTERIZATION & POLE ALIGNMENT           -->
                <!-- ============================================================ -->
                <section class="chapter-section" '''

def get_chapter6_and_7_html():
    return r'''id="ch-06">
                    <span class="chapter-badge">פרק 06</span>
                    <h2>אפיון, כיול מנוע OEMER QS 100S ופענוח אינקודר SICK HIPERFACE</h2>

                    <h3>מפרט טכני של מנוע ה-PMSM המעבדתי (OEMER Motori Elettrici)</h3>
                    <p>
                        במסגרת המחקר המעבדתי, שולב מנוע סרוו סינכרוני תעשייתי מתקדם מתוצרת חברת <strong>OEMER (איטליה)</strong> מדגם <strong>QS 100S</strong>, המצויד באינקודר אבסולוטי מתקדם <strong>SICK Stegmann SFM60</strong> עם ממשק <strong>HIPERFACE</strong>.
                    </p>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/pmsm_motor_photo.jpeg" alt="OEMER QS100S Motor" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 6.1:</strong> מנוע ה-PMSM המעבדתי: OEMER QS 100S עם אינקודר אופטי אבסולוטי SICK SFM60.</div>
                    </div>

                    <div class="table-container">
                        <table class="styled-table">
                            <thead>
                                <tr><th>פרמטר מנוע</th><th>ערך נומינלי</th><th>הערות הנדסיות</th></tr>
                            </thead>
                            <tbody>
                                <tr><td>דגם המנוע</td><td><strong>OEMER QS 100S</strong></td><td>מנוע סרוו סינכרוני מגנטים קבועים</td></tr>
                                <tr><td>מומנט נומינלי ($T_n$)</td><td>$18.5\text{ Nm}$</td><td>עד $45\text{ Nm}$ בשיא (Peak)</td></tr>
                                <tr><td>זרם נומינלי ($I_n$)</td><td>$14.2\text{ A}$</td><td>זרם אפקטיבי (RMS)</td></tr>
                                <tr><td>מהירות נומינלית ($n_n$)</td><td>$3000\text{ RPM}$</td><td>מהירות מקסימלית $6000\text{ RPM}$</td></tr>
                                <tr><td>מספר זוגות קטבים ($p$)</td><td><strong>4 זוגות קטבים (8 קטבים)</strong></td><td>יחס תדר חשמלי למכני: $f_e = 4 \times f_m$</td></tr>
                                <tr><td>סוג אינקודר</td><td><strong>SICK SFM60 HIPERFACE</strong></td><td>ערוצי Sin/Cos אנלוגיים 1024ppr + ערוץ RS-485 דיגיטלי</td></tr>
                            </tbody>
                        </table>
                    </div>

                    <h3>פרוטוקול כיול ויישור קטבים סטטי (DC Alignment Protocol)</h3>
                    <p>
                        במנועי PMSM, בקרת הזרם (FOC/OEPC) חייבת לדעת בדיוק מוחלט את הזווית החשמלית של המגנט הקבוע של הרוטור ביחס לציר פאזה A של הסטטור. אי-התאמה של אפילו $5^\circ$ גורמת לאובדן מומנט וזרמי יתר.
                    </p>
                    <p>
                        לצורך כך פותח <strong>פרוטוקול כיול קטבים מלא בן 13 שלבים</strong> (מתועד במלואו בדוח ה-PDF הרשמי שבאתר):
                    </p>

                    <div class="walkthrough-box">
                        <h4>🎯 עקרון שיטת ה-Static DC Alignment שבוצעה במעבדה</h4>
                        <div class="step-item">
                            <span class="step-num">1</span>
                            <div class="step-content">
                                <strong>הזרקת זרם DC מבוקר:</strong> ספק כוח מיוצב מחובר בין פאזה A (חיובי) לפאזות B ו-C המקוצרות יחד (שלילי).
                            </div>
                        </div>
                        <div class="step-item">
                            <span class="step-num">2</span>
                            <div class="step-content">
                                <strong>יישור הרוטור לציר $\theta_e = 0^\circ$:</strong> הזרם יוצר שדה מגנטי סטטורי קבוע לחלוטין לאורך ציר d. הרוטור "ננעל" פיזית בדיוק מושלם מול השדה הסטטורי.
                            </div>
                        </div>
                        <div class="step-item">
                            <span class="step-num">3</span>
                            <div class="step-content">
                                <strong>קריאת זווית האינקודר האבסולוטית:</strong> באמצעות פקודות תקשורת HIPERFACE דרך RS-485, נדגמת הזווית הנמדדת ונקבעת כהיסט הייחוס: $\theta_{\text{offset}} = \theta_{\text{raw}}$.
                            </div>
                        </div>
                    </div>

                    <h3>פתרון עכבת התקשורת במודול DFRobot DFR0845</h3>
                    <p>
                        בניסויי המעבדה התגלתה שגיאת תקשורת עקב החזרות אותות (Reflections) בקו ה-RS-485 של האינקודר. התקלה נפתרה בהצלחה באמצעות הוספת נגד תיאום עכבות של $120\,\Omega$ בין קווי A ו-B והגדרת זמני השהיה קפדניים של פרוטוקול ה-HIPERFACE (9600 Baud, 8-E-1).
                    </p>
                </section>

                <!-- ============================================================ -->
                <!-- CHAPTER 7: ALTIUM HARDWARE DESIGN                            -->
                <!-- ============================================================ -->
                <section class="chapter-section" id="ch-07">
                    <span class="chapter-badge">פרק 07</span>
                    <h2>תכנון ומימוש כרטיסי החומרה ב-Altium Designer</h2>

                    <h3>שלושת כרטיסי החומרה שתוכננו לפרויקט</h3>
                    <p>
                        להשלמת הפלטפורמה המעבדתית תוכננו, נותחו ועוצבו 3 כרטיסי מעגלים מודפסים (PCB) רב-שכבתיים בתוכנת <strong>Altium Designer</strong>:
                    </p>

                    <div class="fig-wrapper">
                        <img src="presentation_assets/hardware_setup_photo.jpg" alt="Laboratory Inverter & Altium Modules" onclick="openModal(this.src)">
                        <div class="fig-caption"><strong>איור 7.1:</strong> מודולי החומרה המעבדתיים, כרטיסי המדידה המבודדים ועמדת הניסוי של ממיר ההספק.</div>
                    </div>

                    <div class="grid-3col">
                        <div class="info-card">
                            <h4>⚡ 1. כרטיס מתח מבודד</h4>
                            <p style="font-size:13px; color:var(--text-muted);">
                                <strong>Isolated HV Measurement V2.1:</strong> מודד מתחי DC גבוהים עד $800\text{V}$ באמצעות מגבר בידוד אופטי ומחלק מתח נגדי מדויק ($0.1\%$), עם מתח בידוד גלווני של $5\text{kV}$ להגנה על כרטיסי המיקרו-בקר.
                            </p>
                        </div>
                        <div class="info-card">
                            <h4>🧲 2. כרטיס חיישן זרם</h4>
                            <p style="font-size:13px; color:var(--text-muted);">
                                <strong>Isolated Current Sensor V2.1:</strong> מבוסס חיישני אפקט הול (Hall Effect) מהירים ברוחב פס של $200\text{kHz}$, לדגימה מדויקת של זרמי הפאזות ורכיב ה-ZSC ללא הפרעות ומגע חשמלי.
                            </p>
                        </div>
                        <div class="info-card">
                            <h4>🔌 3. כרטיס מיתוג הספק</h4>
                            <p style="font-size:13px; color:var(--text-muted);">
                                <strong>Power Switch - GUN V2:</strong> ענף מיתוג הספק מהיר מבוסס מוליכים מתקדמים (GaN/SiC) ודרייברים מבודדים עם הגנות קצר, Dead-time מובנה וניתוב זרמי פריקה מהירים.
                            </p>
                        </div>
                    </div>

                    <h3>שיקולי Layout וניתוב אותות מהירים</h3>
                    <p>
                        בשל קפיצות המתח החדות ($dv/dt$) בממיר, הוקפד על הפרדה פיזית מלאה בין משטחי האדמה (Ground Planes) של מתח גבוה לאדמת הבקרה השקטה, מזעור לולאות השראות פיזור בדרייברים, ושימוש בסיכוך דיפרנציאלי.
                    </p>
                </section>

                <!-- ============================================================ -->
                <!-- CHAPTER 8: MECHANICAL BENCH & DYNO                           -->
                <!-- ============================================================ -->
                <section class="chapter-section" '''
