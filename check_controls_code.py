with open("generate_hebrew_presentation.py", "r", encoding="utf-8") as f:
    text = f.read()

idx_c = text.find('class="demo-controls-bar"')
out1 = text[idx_c:idx_c+1400]

idx_f = text.find('window.setDemoFault')
out2 = text[idx_f:idx_f+2200]

with open(r"C:\Users\maxra\.gemini\antigravity-ide\brain\1aa6e997-d5e2-4b09-b625-94a9763a52f6\scratch\controls_code.txt", "w", encoding="utf-8") as f_out:
    f_out.write("=== CONTROLS BAR HTML ===\n" + out1 + "\n\n=== JS FUNCTIONS ===\n" + out2)

print("written controls_code.txt")
