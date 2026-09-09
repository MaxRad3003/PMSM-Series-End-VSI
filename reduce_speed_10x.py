import re

def reduce_speed_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace 0.0006 * demoSpeed with 0.00006 * demoSpeed (exact 10x reduction)
    if '0.0006 * demoSpeed' in content:
        content = content.replace('0.0006 * demoSpeed', '0.00006 * demoSpeed')
        print(f"[{filepath}] Replaced 0.0006 * demoSpeed -> 0.00006 * demoSpeed")
    else:
        print(f"[{filepath}] WARNING: '0.0006 * demoSpeed' not found!")

    # 2. In stepDemoOnce: reduce step size from 0.0008 to 0.00008
    if 'stepOepcPipeline(0.0008);' in content:
        content = content.replace('stepOepcPipeline(0.0008);', 'stepOepcPipeline(0.00008);')
        print(f"[{filepath}] Replaced stepOepcPipeline(0.0008) -> stepOepcPipeline(0.00008)")

    with open(filepath, 'w', encoding='utf-8') as f_out:
        f_out.write(content)
    print(f"[{filepath}] Done!")

reduce_speed_in_file('generate_hebrew_presentation.py')
reduce_speed_in_file('generate_html_presentation.py')
