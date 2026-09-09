with open("generate_hebrew_presentation.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('let demoRunning = true;')
if idx == -1:
    idx = text.find('demoRunning')
print('demoRunning at:', idx)
out_path = r"C:\Users\maxra\.gemini\antigravity-ide\brain\1aa6e997-d5e2-4b09-b625-94a9763a52f6\scratch\slide10_js_demo.txt"
with open(out_path, "w", encoding="utf-8") as f_out:
    f_out.write(text[idx-200:idx+4000])
print("written slide10_js_demo.txt")
