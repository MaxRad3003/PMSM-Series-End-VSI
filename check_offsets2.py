with open(r"C:\Users\maxra\.gemini\antigravity-ide\brain\1aa6e997-d5e2-4b09-b625-94a9763a52f6\scratch\full_slide10_iife.js", "r", encoding="utf-8") as f:
    text = f.read()

idx_loop = text.find('function demoLoop()')
idx_win = text.find('window.toggleDemoPlay')
idx_fault = text.find('window.setDemoFault')

print(f"idx_loop: {idx_loop}")
print(f"idx_win: {idx_win}")
print(f"idx_fault: {idx_fault}")
