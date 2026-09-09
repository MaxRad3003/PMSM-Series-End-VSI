with open("generate_hebrew_presentation.py", "r", encoding="utf-8") as f:
    text = f.read()

# Let's locate where renderOscilloscopeCanvas, renderGateTracesCanvas, demoLoop are defined
idx_osc = text.find('function renderOscilloscopeCanvas()')
idx_gate = text.find('function renderGateTracesCanvas()')
idx_orbit = text.find('function renderErrorOrbitCanvas()')
idx_loop = text.find('function demoLoop()')
idx_controls = text.find('class="demo-controls-bar"')

print(f"idx_osc: {idx_osc}")
print(f"idx_gate: {idx_gate}")
print(f"idx_orbit: {idx_orbit}")
print(f"idx_loop: {idx_loop}")
print(f"idx_controls: {idx_controls}")
