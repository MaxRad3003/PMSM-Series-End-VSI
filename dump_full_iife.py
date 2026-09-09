with open("generate_hebrew_presentation.py", "r", encoding="utf-8") as f:
    text = f.read()

idx_start = text.find('// --- 3. SLIDE 11: OEPC SWITCHING & CLOSED-LOOP ERROR CORRECTION ENGINE ---')
idx_end = text.find('})();', idx_start) + 5

with open(r"C:\Users\maxra\.gemini\antigravity-ide\brain\1aa6e997-d5e2-4b09-b625-94a9763a52f6\scratch\full_slide10_iife.js", "w", encoding="utf-8") as f_out:
    f_out.write(text[idx_start:idx_end])

print(f"Dumped full slide 10 IIFE: {idx_end - idx_start} characters")
