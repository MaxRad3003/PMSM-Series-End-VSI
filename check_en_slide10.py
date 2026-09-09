with open("generate_html_presentation.py", "r", encoding="utf-8") as f:
    text_en = f.read()

idx_en_osc = text_en.find('function renderOscilloscopeCanvas()')
idx_en_controls = text_en.find('class="demo-controls-bar"')

print("EN idx_en_osc:", idx_en_osc)
print("EN idx_en_controls:", idx_en_controls)
