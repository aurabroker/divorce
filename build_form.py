#!/usr/bin/env python3
"""
build_form.py — Migracja formularzy z Formspree → Web3Forms
Kancelaria Adwokacka Magdalena Idzik-Cieśla

Co robi:
  1. Znajduje wszystkie pliki HTML z formularzem Formspree
  2. Zamienia <form> na wersję Web3Forms (fetch + FormData)
  3. Zmienia name= pól na konwencję Web3Forms
  4. Dodaje JS z obsługą submit, blokadą przycisku, komunikatami PL
  5. Usuwa niepotrzebne ukryte pola Formspree
"""

import re
import glob
import os

ACCESS_KEY = "be1e4321-2444-4205-a5de-2ba21c3d68dc"
ENDPOINT   = "https://api.web3forms.com/submit"

FORM_JS = """
(function () {
  var form      = document.getElementById('contact-form');
  var submitBtn = document.getElementById('submit-btn');
  if (!form || !submitBtn) return;

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    var formData = new FormData(form);
    formData.append('access_key', '""" + ACCESS_KEY + """');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Wysyłanie…';
    try {
      var res  = await fetch('""" + ENDPOINT + """', { method: 'POST', body: formData });
      var data = await res.json();
      if (res.ok) {
        var successBox = document.getElementById('form-success');
        if (successBox) { successBox.style.display = 'block'; }
        form.reset();
        submitBtn.textContent = 'Wysłano ✓';
      } else {
        alert('Błąd: ' + (data.message || 'Spróbuj ponownie.'));
        submitBtn.disabled = false;
        submitBtn.textContent = 'Wyślij i umów konsultację →';
      }
    } catch (_) {
      alert('Coś poszło nie tak. Sprawdź połączenie i spróbuj ponownie.');
      submitBtn.disabled = false;
      submitBtn.textContent = 'Wyślij i umów konsultację →';
    }
  });
})();"""


def find_html_files(root="."):
    seen, result = set(), []
    for p in glob.glob(os.path.join(root, "**", "*.html"), recursive=True):
        ap = os.path.abspath(p)
        if ap not in seen:
            seen.add(ap)
            result.append(ap)
    return result


def process_file(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()

    # Tylko pliki z formularzem kancelarii
    if "contact-form" not in html:
        return False

    changed = False

    # 1. Zamień tag <form> z Formspree → brak action/method
    new_form_tag = '<form id="contact-form" class="form-card">'

    multiline = re.compile(
        r'<form\s*\n\s*id="contact-form"\s*\n\s*action="[^"]*"\s*\n\s*method="POST"\s*\n\s*class="form-card"\s*\n\s*>',
        re.MULTILINE,
    )
    singleline = re.compile(
        r'<form\s+id="contact-form"\s+action="[^"]*"\s+method="POST"\s+class="form-card">'
    )

    for pat in (multiline, singleline):
        if pat.search(html):
            html = pat.sub(new_form_tag, html)
            changed = True
            break

    # 2. Usuń ukryte pola Formspree (z opcjonalnymi komentarzami)
    formspree_hidden = re.compile(
        r'[ \t]*(?:<!--[^\n]*(?:przekierowanie|temat|honeypot|antyspam)[^\n]*-->\n)?'
        r'[ \t]*<input\s[^>]*name="(?:_next|_subject|_gotcha)"[^>]*>\n?',
        re.IGNORECASE,
    )
    before = html
    html = formspree_hidden.sub("", html)
    if html != before:
        changed = True

    # 3. Dodaj access_key jako pierwsze ukryte pole (jeśli jeszcze nie ma)
    if 'name="access_key"' not in html and new_form_tag in html:
        html = html.replace(
            new_form_tag,
            new_form_tag + '\n      <input type="hidden" name="access_key" value="' + ACCESS_KEY + '">',
        )
        changed = True

    # 4. Zmień name= pól na konwencję Web3Forms
    renames = [
        # imię: id=imie name=imie → name=name
        (r'\bname="imie"', 'name="name"'),
        # telefon: id=tel name=telefon → name=phone
        (r'\bname="telefon"', 'name="phone"'),
        # wiadomość: id=wiadomosc name=wiadomosc → name=message
        (r'\bname="wiadomosc"', 'name="message"'),
    ]
    for pat, repl in renames:
        before = html
        html = re.sub(pat, repl, html)
        if html != before:
            changed = True

    # 5. Dodaj id="submit-btn" do przycisku submit (jeśli nie ma)
    if 'id="submit-btn"' not in html:
        # Dopasuj <button ... class="form-submit"> w dowolnej kolejności atrybutów
        btn_pat = re.compile(r'<button\b([^>]*\bclass="form-submit"[^>]*)>')
        if btn_pat.search(html):
            html = btn_pat.sub(r'<button id="submit-btn"\1>', html)
            changed = True

    # 6. Wstrzyknij JS przed zamknięciem ostatniego <script> inline (przed </body>)
    if 'web3forms' not in html:
        # Szukamy wzorca </script>\n</body> lub </script></body>
        close_body = re.compile(r'(</script>)(\s*</body>)', re.IGNORECASE)
        if close_body.search(html):
            html = close_body.sub(FORM_JS + r'\n\1\2', html, count=1)
        else:
            html = html.replace("</body>", "<script>" + FORM_JS + "\n</script>\n</body>", 1)
        changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    return False


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    files = find_html_files(root)

    skip_patterns = ["domain-config-guide", "dziekujemy", "__pycache__"]

    processed, skipped = [], []
    for path in sorted(files):
        rel = os.path.relpath(path, root)
        if any(s in rel for s in skip_patterns):
            skipped.append(rel)
            continue
        if process_file(path):
            processed.append(rel)
            print(f"  ✓  {rel}")
        else:
            skipped.append(rel)

    print(f"\nZaktualizowano: {len(processed)} plik(ów)")
    if skipped:
        print(f"Pominięto:      {len(skipped)} plik(ów)")


if __name__ == "__main__":
    main()
