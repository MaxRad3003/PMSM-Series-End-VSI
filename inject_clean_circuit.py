import os
from circuit_code_template import get_render_circuit_code

def inject_clean_circuit(filepath, is_hebrew=True):
    print(f"Injecting safe circuit code into {filepath} (Hebrew={is_hebrew})...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    s = content.find('// Canvas 4: Dynamic Electronic Circuit Simulation')
    if s == -1:
        s = content.find('function renderCircuitCanvas()')
    e = content.find('function renderErrorOrbitCanvas()')

    if s == -1 or e == -1:
        print(f"ERROR: Could not locate markers in {filepath}! s={s}, e={e}")
        return False

    code = get_render_circuit_code(is_hebrew).strip() + "\n\n    "
    new_content = content[:s] + code + content[e:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully injected into {filepath}!")
    return True

if __name__ == '__main__':
    inject_clean_circuit('generate_hebrew_presentation.py', True)
    inject_clean_circuit('generate_html_presentation.py', False)
