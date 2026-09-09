with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if 'section-title' in l or 'OEPC_SE_VSI' in l:
        print(f'{i+1}: {l.strip()[:100]}')
