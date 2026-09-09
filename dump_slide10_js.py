with open("generate_hebrew_presentation.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('// Slide 11 (Interactive OEPC 96-LUT Switching & Closed-Loop Simulation)')
if idx == -1:
    idx = text.find('slide-switching-error-demo')
    idx = text.find('<script>', idx)
out_path = r"C:\Users\maxra\.gemini\antigravity-ide\brain\1aa6e997-d5e2-4b09-b625-94a9763a52f6\scratch\slide10_js_top.txt"
with open(out_path, "w", encoding="utf-8") as f_out:
    f_out.write(text[idx:idx+3500])
print("written slide10_js_top.txt")
