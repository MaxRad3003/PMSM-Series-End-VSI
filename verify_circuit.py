from playwright.sync_api import sync_playwright
from pathlib import Path

pmsm_dir = Path(r"c:\Users\maxra\OneDrive - ac.sce.ac.il\Barabi\2025 Eli & Max\PMSM")
html_url = (pmsm_dir / "OEPC_SE_VSI_PMSM_Presentation_HE.html").as_uri()
out_screenshot = Path(r"C:\Users\maxra\.gemini\antigravity-ide\brain\1aa6e997-d5e2-4b09-b625-94a9763a52f6\slide_10_circuit_simulation_view.png")

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
    page.wait_for_timeout(2500) # Let the simulation & circuit run
    
    # Check circuit canvas visibility
    circ_box = page.locator("#demo-circuit-canvas").bounding_box()
    print("Circuit canvas bounding box:", circ_box)

    # Take screenshot
    page.screenshot(path=str(out_screenshot), full_page=False)
    print("Screenshot saved successfully!")
    
    # Test Tab switching: Click Matrix tab
    page.click("#btn-tab-matrix")
    page.wait_for_timeout(500)
    matrix_disp = page.locator("#panel2-view-matrix").evaluate("el => getComputedStyle(el).display")
    print("Matrix view display:", matrix_disp)

    # Click Circuit tab back
    page.click("#btn-tab-circuit")
    page.wait_for_timeout(500)
    circ_disp = page.locator("#panel2-view-circuit").evaluate("el => getComputedStyle(el).display")
    print("Circuit view display:", circ_disp)

    browser.close()

if errors:
    print(f"FAILED with errors: {errors}")
else:
    print("SUCCESS: 0 console or page errors!")
