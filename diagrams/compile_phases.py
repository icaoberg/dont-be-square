#!/usr/bin/env python3
import re
import os
import subprocess
import shutil

os.makedirs('.temp', exist_ok=True)
os.makedirs('views', exist_ok=True)

phases = {
    'phase1_fair_structures_comparison.md': 'phase1_fair_structures_comparison',
    'phase2_multi_version_evaluation.md': 'phase2_multi_version_evaluation',
    'phase3_multi_assay_evaluation.md': 'phase3_multi_assay_evaluation',
    'phase4_fair_evaluation_hubmap.md': 'phase4_fair_evaluation_hubmap',
    'phase5_metadata_fair_scoring.md': 'phase5_metadata_fair_scoring'
}

env = dict(os.environ)
env['PUPPETEER_EXECUTABLE_PATH'] = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

for md_file, name in phases.items():
    print(f'Processing {name}...')
    try:
        with open(md_file, 'r') as f:
            content = f.read()
        match = re.search(r'```mermaid\s*\n(.*?)```', content, re.DOTALL)
        if match:
            mermaid_code = match.group(1).strip()
            mmd_path = f'.temp/{name}.mmd'
            png_path = f'views/{name}.png'
            
            with open(mmd_path, 'w') as f:
                f.write(mermaid_code)
            
            result = subprocess.run(
                ['/opt/homebrew/bin/mmdc', '-i', mmd_path, '-o', png_path,
                 '-t', 'neutral', '-b', 'white', '-w', '2400', '-H', '1800'],
                env=env,
                capture_output=True,
                text=True
            )
            
            if os.path.exists(png_path):
                size = os.path.getsize(png_path)
                print(f'  ✓ {name}.png created ({size//1024}KB)')
            else:
                print(f'  ✗ {name}.png failed')
                if result.stderr:
                    print(f'    Error: {result.stderr[:150]}')
        else:
            print(f'  ✗ No mermaid code found in {md_file}')
    except Exception as e:
        print(f'  ✗ Error: {e}')

shutil.rmtree('.temp', ignore_errors=True)

created = [f for f in os.listdir('views') if f.startswith('phase') and f.endswith('.png')]
print(f'\nTotal phase diagrams: {len(created)}')
for f in sorted(created):
    print(f'  - {f}')
