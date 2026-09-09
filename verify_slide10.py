from playwright.sync_api import sync_playwright
from pathlib import Path

pmsm_dir = Path(r"c:\Users\maxra\OneDrive - ac.sce.ac.il\Barabi\2025 Eli & Max\PMSM")
html_url = (pmsm_dir / "OEPC_SE_VSI_PMSM_Presentation_HE.html").as_uri()
out_screenshot = Path(r"C:\Users\maxra\.gemini\antigravity-ide\brain\1aa6e997-d5e2-4b09-b625-94a9763a52f6\slide_10_triggered_view.png")

errors = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 900})
    page.on("console", lambda msg: print(f"[CONSOLE {msg.type}] {msg.text}") if msg.type in ["error"] else None)
    page.on("pageerror", lambda err: errors.append(str(err)))
    page.goto(html_url)
    page.wait_for_timeout(1000)
    
    # Navigate to Slide 10
    page.evaluate("updateSlide(9);")
    page.wait_for_timeout(2000) # Let the simulation run for 2 seconds
    
    # Check scope mode button
    btn_text = page.locator("#btn-demo-scope-mode").text_content()
    print("Scope button found, length:", len(btn_text))

    # Take screenshot
    page.screenshot(path=str(out_screenshot), full_page=False)
    print("Screenshot saved successfully!")
    
    # Test toggle scope mode
    page.click("#btn-demo-scope-mode")
    page.wait_for_timeout(1000)
    btn_text2 = page.locator("#btn-demo-scope-mode").text_content()
    print("Scope button after toggle, length:", len(btn_text2))

    # Test slider speed change
    page.evaluate("updateDemoSpeed('0.2');")
    page.wait_for_timeout(500)
    speed_txt = page.locator("#demo-speed-val").text_content()
    print(f"Speed readout after 0.2x: '{speed_txt.strip()}'")

    browser.close()

if errors:
    print(f"FAILED with errors: {errors}")
else:
    print("SUCCESS: 0 console or page errors!")
