with open("generate_hebrew_presentation.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('id="slide-switching-error-demo"')
out_path = r"C:\Users\maxra\.gemini\antigravity-ide\brain\1aa6e997-d5e2-4b09-b625-94a9763a52f6\scratch\slide10_html_body.txt"
with open(out_path, "w", encoding="utf-8") as f_out:
    f_out.write(text[idx:idx+6000])
print("written slide10_html_body.txt")
