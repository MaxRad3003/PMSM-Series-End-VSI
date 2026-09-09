with open(r"C:\Users\maxra\.gemini\antigravity-ide\brain\1aa6e997-d5e2-4b09-b625-94a9763a52f6\scratch\full_slide10_iife.js", "r", encoding="utf-8") as f:
    text = f.read()

idx_step = text.find('function stepOepcPipeline(dt)')
idx_update = text.find('function updateDemoUI()')
idx_osc = text.find('function renderOscilloscopeCanvas()')
idx_gate = text.find('function renderGateTracesCanvas()')
idx_orbit = text.find('function renderErrorOrbitCanvas()')
idx_lut = text.find('function getOepcLutMapping(')

print(f"idx_step: {idx_step}")
print(f"idx_update: {idx_update}")
print(f"idx_osc: {idx_osc}")
print(f"idx_gate: {idx_gate}")
print(f"idx_orbit: {idx_orbit}")
print(f"idx_lut: {idx_lut}")
