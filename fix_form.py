#!/usr/bin/env python3
"""
fix_form.py — Usuwa zduplikowany handler Web3Forms z inline <script>
i kopiuje naprawiony page.js do wszystkich katalogów.
"""

import re
import glob
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
MASTER_PAGE_JS = os.path.join(ROOT, "bemowo", "assets", "page.js")

INLINE_JS_PAT = re.compile(
    r'\n\(function \(\) \{\n  var form.*?'
    r'alert\(\'Coś poszło nie tak\. Sprawdź połączenie i spróbuj ponownie\.\'\);\n'
    r'      submitBtn\.disabled = false;\n'
    r'      submitBtn\.textContent = \'Wyślij i umów konsultację →\';\n'
    r'    \}\n  \}\);\n\}\)\(\);',
    re.DOTALL,
)


def fix_html(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if "(function ()" not in html:
        return False
    cleaned = INLINE_JS_PAT.sub("", html)
    if cleaned == html:
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(cleaned)
    return True


def copy_page_js(src):
    for dst_dir in glob.glob(os.path.join(ROOT, "*", "assets")):
        dst = os.path.join(dst_dir, "page.js")
        if os.path.abspath(dst) != os.path.abspath(src) and os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"  ✓  {os.path.relpath(dst, ROOT)}")
    # root assets
    root_dst = os.path.join(ROOT, "assets", "page.js")
    if os.path.exists(root_dst):
        shutil.copy2(src, root_dst)
        print(f"  ✓  assets/page.js")


def main():
    print("── Usuwanie zduplikowanego inline JS ──")
    for path in sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(path, ROOT)
        if "domain-config-guide" in rel or "dziekujemy" in rel:
            continue
        if fix_html(path):
            print(f"  ✓  {rel}")

    print("\n── Kopiowanie naprawionego page.js ──")
    copy_page_js(MASTER_PAGE_JS)
    print("\nGotowe.")


if __name__ == "__main__":
    main()
