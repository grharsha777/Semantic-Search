#!/usr/bin/env python3
"""Patch a Jupyter notebook to remove hardcoded GEMINI_API_KEY and produce a secure copy.
Usage: python scripts/fix_notebook_secrets.py /path/to/"Semantic Search.ipynb"
"""
import json
import re
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: fix_notebook_secrets.py /path/to/" + '"Semantic Search.ipynb"')
        sys.exit(1)
    src = Path(sys.argv[1])
    if not src.exists():
        print(f"Notebook not found: {src}")
        sys.exit(1)
    dst = src.with_name(src.stem + ".secure" + src.suffix)

    nb = json.loads(src.read_text(encoding='utf-8'))
    changed = False

    # Add a top-level loader cell if not present
    if not any(cell.get('cell_type') == 'code' and any('load_dotenv()' in s for s in cell.get('source', [])) for cell in nb.get('cells', [])):
        loader = {
            'cell_type': 'code',
            'metadata': {'language': 'python'},
            'source': [
                'import os',
                'from dotenv import load_dotenv',
                'load_dotenv()',
                ''
            ]
        }
        nb['cells'].insert(0, loader)
        changed = True

    pattern = re.compile(r"GEMINI_API_KEY\s*=\s*[\"'][^\"']+[\"']")

    for cell in nb.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue
        new_src = []
        for line in cell.get('source', []):
            if pattern.search(line):
                # Replace hardcoded assignment with env-based check
                new_src.extend([
                    "GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')",
                    "if not GEMINI_API_KEY:",
                    "    raise RuntimeError('GEMINI_API_KEY not set. See .env.example')",
                    ""
                ])
                changed = True
            else:
                new_src.append(line)
        cell['source'] = new_src

    if changed:
        dst.write_text(json.dumps(nb, indent=2), encoding='utf-8')
        print(f"Patched notebook written to: {dst}")
    else:
        print("No hardcoded GEMINI_API_KEY occurrences found. No changes made.")

if __name__ == '__main__':
    main()
