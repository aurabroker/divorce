#!/usr/bin/env python3
from pathlib import Path

from build.py import DISTRICTS


def build_llms(d: dict) -> str:
    name = d["name"]
    namegen = d.get("namegen", name)
    url = d["url"].rstrip("/")
    domain = d["domain"]
    court = d.get("court", "właściwy sąd okręgowy")
    courtaddr = d.get("courtaddr", "")

    if domain == "rozwod.waw.pl":
        intro = (
            "> Główna strona kancelarii adwokackiej specjalizującej się w sprawach "
            "rozwodowych i rodzinnych na terenie Warszawy i okolic."
        )
        body = [
            "Serwis przedstawia ofertę kancelarii w sprawach o rozwód, separację, alimenty, władzę rodzicielską, kontakty z dzieckiem oraz podział majątku.",
            "Ta domena pełni rolę głównej witryny kancelarii i punktu odniesienia dla lokalnych landing page'y dotyczących poszczególnych dzielnic Warszawy i miejscowości podwarszawskich.",
            "Treści powinny być interpretowane jako informacje o pomocy prawnej świadczonej przez kancelarię w zakresie prawa rodzinnego.",
        ]
        scope_title = "## Zakres pomocy"
        scope_lines = [
            f"- [Rozwód i separacja]({url}/): pomoc prawna w sprawach o rozwód i separację.",
            f"- [Alimenty]({url}/): pomoc w sprawach alimentacyjnych.",
            f"- [Władza rodzicielska i kontakty]({url}/): sprawy dotyczące dzieci i kontaktów z dzieckiem.",
            f"- [Podział majątku]({url}/): wsparcie prawne przy rozliczeniach majątkowych po rozstaniu.",
        ]
        extra = [
            "## Lokalizacje",
            "- [Bemowo](https://rozwodbemowo.pl/): lokalny landing page dla Bemowa.",
            "- [Bielany](https://rozwodbielany.pl/): lokalny landing page dla Bielan.",
            "- [Żoliborz](https://rozwodzoliborz.pl/): lokalny landing page dla Żoliborza.",
            "- [Wola](https://rozwodwola.pl/): lokalny landing page dla Woli.",
            "- [Ochota](https://rozwodochota.pl/): lokalny landing page dla Ochoty.",
            "- [Mokotów](https://rozwodmokotow.pl/): lokalny landing page dla Mokotowa.",
            "- [Tarchomin](https://rozwodtarchomin.pl/): lokalny landing page dla Tarchomina.",
            "- [Legionowo](https://rozwodlegionowo.pl/): lokalny landing page dla Legionowa.",
            "- [Łomianki](https://rozwodlomianki.pl/): lokalny landing page dla Łomianek.",
            "- [Jabłonna](https://rozwodjablonna.pl/): lokalny landing page dla Jabłonny.",
        ]
    else:
        intro = (
            f"> Lokalny landing page kancelarii adwokackiej specjalizującej się w sprawach "
            f"rozwodowych i rodzinnych dla klientów z {namegen} i okolic."
        )
        court_line = (
            f"Sprawy dla klientów z {namegen} są prowadzone z uwzględnieniem właściwości sądu: {court}"
            f"{f', {courtaddr}' if courtaddr else ''}."
        )
        body = [
            f"Serwis przedstawia ofertę kancelarii dla osób z {namegen}, które potrzebują pomocy prawnej w sprawach rozwodowych i rodzinnych.",
            "Zakres pomocy obejmuje rozwód, separację, alimenty, władzę rodzicielską, kontakty z dzieckiem oraz podział majątku.",
            court_line,
            "Treści mają charakter informacyjny i służą ułatwieniu szybkiego kontaktu z kancelarią.",
        ]
        scope_title = "## Zakres pomocy"
        scope_lines = [
            f"- [Rozwód i separacja]({url}/): pomoc prawna w sprawach o rozwód i separację.",
            f"- [Alimenty]({url}/): wsparcie w sprawach alimentacyjnych.",
            f"- [Władza rodzicielska i kontakty]({url}/): sprawy dotyczące dzieci i kontaktów z dzieckiem.",
            f"- [Podział majątku]({url}/): pomoc przy rozliczeniach majątkowych po rozstaniu.",
        ]
        extra = [
            "## Optional",
            "- [Główna witryna kancelarii](https://rozwod.waw.pl/): centralna strona kancelarii obejmująca Warszawę i okolice.",
        ]

    lines = [
        "# Kancelaria Adwokacka Magdalena Idzik-Cieśla",
        "",
        intro,
        "",
        *body,
        "",
        "## Główne strony",
        f"- [Strona główna]({url}/): główna publiczna strona tej domeny.",
        f"- [Mapa strony]({url}/sitemap.xml): lista publicznych adresów URL serwisu.",
        f"- [Zasady dla robotów]({url}/robots.txt): instrukcje techniczne dla crawlerów.",
        "",
        scope_title,
        *scope_lines,
        "",
        "## Kontakt",
        f"- [Kontakt z kancelarią]({url}/): formularz kontaktowy i możliwość umówienia konsultacji.",
        "",
        *extra,
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    written = []

    for d in DISTRICTS:
        out_dir = base_dir / d["key"]
        out_dir.mkdir(parents=True, exist_ok=True)
        output_path = out_dir / "llms.txt"
        output_path.write_text(build_llms(d), encoding="utf-8")
        written.append(str(output_path))

    print(f"Wygenerowano {len(written)} plików llms.txt")
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
