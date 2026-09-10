/**
 * =====================================================================
 * PMSM Research Portal - Access Control & Authentication Guard
 * Client-Side SHA-256 Auth Shield
 * =====================================================================
 */

(function () {
    // Valid password hashes (SHA-256)
    // Default valid passwords: 'pmsm2025', 'pmsm2026', 'barabi2025'
    const VALID_HASHES = [
        '39c2b03ffd024fcf5e24ce754c34b5970f50881b33e7a94d01cf2b6ce5308b3d', // pmsm2025
        '5904a035a72633c035212149374e91b2f490ac68c55e2b8ec0e0fbdc9fb84411', // pmsm2026
        '1f8840d6060cd389ce6f7006f8d31d69948749417490f63c85f05a6046274beb'  // barabi2025
    ];

    const AUTH_STORAGE_KEY = 'pmsm_authorized_session_v1';

    // Hash helper using native SubtleCrypto
    async function hashPassword(plainText) {
        const encoder = new TextEncoder();
        const data = encoder.encode(plainText.trim());
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }

    // Check if already authenticated in this session or local storage
    function isAuthorized() {
        try {
            const token = localStorage.getItem(AUTH_STORAGE_KEY) || sessionStorage.getItem(AUTH_STORAGE_KEY);
            return token && VALID_HASHES.includes(token);
        } catch (e) {
            return false;
        }
    }

    // Lock page style
    function injectStyles() {
        if (document.getElementById('pmsm-auth-styles')) return;
        const style = document.createElement('style');
        style.id = 'pmsm-auth-styles';
        style.textContent = `
            #pmsm-auth-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: radial-gradient(circle at 50% 35%, #0f172a 0%, #070a14 55%, #030712 100%);
                z-index: 999999999;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Heebo', system-ui, -apple-system, sans-serif;
                direction: rtl;
                color: #f3f4f6;
                padding: 1.5rem;
                box-sizing: border-box;
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                transition: opacity 0.4s ease, visibility 0.4s ease;
            }

            .pmsm-auth-card {
                background: rgba(17, 24, 39, 0.85);
                border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 20px;
                width: 100%;
                max-width: 440px;
                padding: 2.5rem 2rem;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8), 0 0 35px rgba(59, 130, 246, 0.15);
                text-align: center;
                position: relative;
                overflow: hidden;
            }

            .pmsm-auth-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #3b82f6, #06b6d4, #8b5cf6, #10b981);
            }

            .pmsm-auth-icon {
                width: 64px;
                height: 64px;
                margin: 0 auto 1.25rem;
                background: rgba(59, 130, 246, 0.12);
                border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 28px;
                box-shadow: 0 0 20px rgba(59, 130, 246, 0.2);
            }

            .pmsm-auth-title {
                font-size: 1.45rem;
                font-weight: 800;
                margin-bottom: 0.5rem;
                background: linear-gradient(135deg, #ffffff 40%, #93c5fd 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .pmsm-auth-subtitle {
                font-size: 0.95rem;
                color: #9ca3af;
                margin-bottom: 1.75rem;
                line-height: 1.5;
            }

            .pmsm-auth-form {
                display: flex;
                flex-direction: column;
                gap: 1rem;
            }

            .pmsm-input-wrap {
                position: relative;
                display: flex;
                align-items: center;
            }

            .pmsm-auth-input {
                width: 100%;
                background: rgba(10, 15, 29, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 12px;
                padding: 0.9rem 1.2rem;
                color: #ffffff;
                font-size: 1.05rem;
                outline: none;
                transition: all 0.2s ease;
                box-sizing: border-box;
                letter-spacing: 1px;
                text-align: center;
            }

            .pmsm-auth-input:focus {
                border-color: #3b82f6;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25);
            }

            .pmsm-auth-btn {
                background: linear-gradient(135deg, #2563eb, #0284c7);
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 0.9rem 1.5rem;
                font-size: 1rem;
                font-weight: 700;
                cursor: pointer;
                transition: all 0.2s ease;
                box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
            }

            .pmsm-auth-btn:hover {
                background: linear-gradient(135deg, #1d4ed8, #0369a1);
                transform: translateY(-1px);
                box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6);
            }

            .pmsm-auth-btn:active {
                transform: translateY(0);
            }

            .pmsm-auth-error {
                color: #f87171;
                font-size: 0.85rem;
                font-weight: 600;
                margin-top: 0.5rem;
                min-height: 1.2rem;
                display: none;
            }

            .pmsm-auth-remember {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                color: #9ca3af;
                font-size: 0.85rem;
                margin-top: 0.5rem;
                cursor: pointer;
            }

            .pmsm-auth-shake {
                animation: pmsmShake 0.4s ease-in-out;
            }

            @keyframes pmsmShake {
                0%, 100% { transform: translateX(0); }
                20%, 60% { transform: translateX(-8px); }
                40%, 80% { transform: translateX(8px); }
            }

            /* Logout Lock Button in corner */
            .pmsm-lock-btn {
                position: fixed;
                bottom: 16px;
                left: 16px;
                z-index: 99999;
                background: rgba(17, 24, 39, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 30px;
                color: #9ca3af;
                padding: 6px 14px;
                font-size: 0.78rem;
                font-weight: 600;
                cursor: pointer;
                backdrop-filter: blur(8px);
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 6px;
                font-family: system-ui, sans-serif;
            }

            .pmsm-lock-btn:hover {
                background: rgba(239, 68, 68, 0.15);
                border-color: rgba(239, 68, 68, 0.4);
                color: #fca5a5;
            }
        `;
        document.head.appendChild(style);
    }

    // Build the lock overlay
    function createOverlay() {
        injectStyles();

        const isHe = document.documentElement.lang === 'he' || document.querySelector('html[dir="rtl"]') !== null || true;

        const overlay = document.createElement('div');
        overlay.id = 'pmsm-auth-overlay';
        overlay.innerHTML = `
            <div class="pmsm-auth-card" id="pmsm-auth-card">
                <div class="pmsm-auth-icon">🔒</div>
                <div class="pmsm-auth-title">${isHe ? 'מרכז מחקר ובקרה: PMSM' : 'PMSM Research Portal'}</div>
                <div class="pmsm-auth-subtitle">${isHe ? 'טופולוגיית Series-End VSI ובקרת OEPC<br><span style="color:#60a5fa; font-size:0.85rem;">גישה מוגבלת למנחה ולחברי צוות המחקר</span>' : 'Series-End VSI & OEPC Control<br><span style="color:#60a5fa; font-size:0.85rem;">Authorized Academic & Research Access Only</span>'}</div>
                
                <form class="pmsm-auth-form" id="pmsm-auth-form" onsubmit="return false;">
                    <div class="pmsm-input-wrap">
                        <input type="password" id="pmsm-auth-input" class="pmsm-auth-input" placeholder="${isHe ? 'הזן סיסמת גישה...' : 'Enter Access Code...'}" autocomplete="current-password" autofocus required />
                    </div>
                    
                    <button type="submit" id="pmsm-auth-submit" class="pmsm-auth-btn">
                        <span>🔓</span> ${isHe ? 'כניסה למערכת' : 'Unlock Portal'}
                    </button>
                    
                    <div class="pmsm-auth-remember">
                        <label style="cursor:pointer; display:flex; align-items:center; gap:6px;">
                            <input type="checkbox" id="pmsm-remember-me" checked style="accent-color:#2563eb;" />
                            <span>${isHe ? 'זכור אותי במכשיר זה' : 'Remember on this device'}</span>
                        </label>
                    </div>

                    <div id="pmsm-auth-error" class="pmsm-auth-error">
                        ${isHe ? '⚠️ סיסמה שגויה. אנא נסה שנית.' : '⚠️ Invalid access code. Please try again.'}
                    </div>
                </form>
            </div>
        `;

        document.body.appendChild(overlay);

        const form = document.getElementById('pmsm-auth-form');
        const input = document.getElementById('pmsm-auth-input');
        const card = document.getElementById('pmsm-auth-card');
        const errorMsg = document.getElementById('pmsm-auth-error');
        const rememberMe = document.getElementById('pmsm-remember-me');

        setTimeout(() => input.focus(), 150);

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const val = input.value;
            if (!val) return;

            const hash = await hashPassword(val);
            if (VALID_HASHES.includes(hash)) {
                // Correct password!
                if (rememberMe.checked) {
                    localStorage.setItem(AUTH_STORAGE_KEY, hash);
                } else {
                    sessionStorage.setItem(AUTH_STORAGE_KEY, hash);
                }

                // Unlock animation
                overlay.style.opacity = '0';
                setTimeout(() => {
                    overlay.remove();
                    addLockCornerButton();
                }, 400);
            } else {
                // Incorrect password
                card.classList.remove('pmsm-auth-shake');
                void card.offsetWidth; // trigger reflow
                card.classList.add('pmsm-auth-shake');
                errorMsg.style.display = 'block';
                input.value = '';
                input.focus();
            }
        });
    }

    // Add discreet logout/lock button in lower-left corner
    function addLockCornerButton() {
        if (document.getElementById('pmsm-lock-corner-btn')) return;
        const btn = document.createElement('button');
        btn.id = 'pmsm-lock-corner-btn';
        btn.className = 'pmsm-lock-btn';
        btn.innerHTML = '🔒 <span>נעילת גישה</span>';
        btn.title = 'לחץ לנעילת האתר והתנתקות';
        btn.addEventListener('click', () => {
            localStorage.removeItem(AUTH_STORAGE_KEY);
            sessionStorage.removeItem(AUTH_STORAGE_KEY);
            window.location.reload();
        });
        document.body.appendChild(btn);
    }

    // Initialize Guard
    function initGuard() {
        if (isAuthorized()) {
            addLockCornerButton();
        } else {
            createOverlay();
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initGuard);
    } else {
        initGuard();
    }
})();
