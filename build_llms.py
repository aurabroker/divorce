#!/usr/bin/env python3
"""
build_llms.py — Generator plików llms.txt i robots.txt dla sieci domen
Kancelaria Adwokacka Magdalena Idzik-Cieśla

Uruchomienie:
    python3 build_llms.py

Dla każdej domeny generuje:
  - llms.txt        → spełnia specyfikację llmstxt.org (H1 + blockquote + sekcje H2)
  - llms-full.txt   → pełna wersja z rozwinięciem treści podstron (bez linków zewnętrznych)
  - robots.txt      → zoptymalizowany pod AI crawlery (search bots ✓, training bots ✗)

Pliki trafiają do katalogu <key>/ obok katalogu build.py,
tak jak robi to oryginalny build.py.
"""

import os
import sys
import textwrap
from pathlib import Path

# ─── KONFIGURACJA DOMEN ────────────────────────────────────────────────────────
# Identyczna jak DISTRICTS w build.py — możesz też zaimportować stamtąd:
#   from build import DISTRICTS
# Tutaj jest samowystarczalna kopia, żeby skrypt działał standalone.

DISTRICTS = [
    dict(
        name="Warszawa",
        namegen="Warszawy",
        key="warszawa",
        domain="rozwod.waw.pl",
        url="https://rozwod.waw.pl",
        is_main=True,
        court="Sąd Okręgowy w Warszawie",
        courtaddr="al. Solidarności 127, Warszawa",
        neighborhoods="Śródmieście, Praga, Ursynów, Wilanów, Żoliborz, Wola, Mokotów, Bemowo, Bielany, Ochota, Tarchomin",
    ),
    dict(
        name="Bemowo",
        namegen="Bemowa",
        key="bemowo",
        domain="rozwodbemowo.pl",
        url="https://rozwodbemowo.pl",
        is_main=False,
        court="Sąd Okręgowy w Warszawie",
        courtaddr="al. Solidarności 127, Warszawa",
        neighborhoods="Chrzanów, Jelonki Północne, Jelonki Południowe, Lotnisko, Wola Ulrychów, Górce",
    ),
    dict(
        name="Bielany",
        namegen="Bielan",
        key="bielany",
        domain="rozwodbielany.pl",
        url="https://rozwodbielany.pl",
        is_main=False,
        court="Sąd Okręgowy w Warszawie",
        courtaddr="al. Solidarności 127, Warszawa",
        neighborhoods="Marymont, Chomiczówka, Wrzeciono, Słodowiec, Młociny, Placówka",
    ),
    dict(
        name="Żoliborz",
        namegen="Żoliborza",
        key="zoliborz",
        domain="rozwodzoliborz.pl",
        url="https://rozwodzoliborz.pl",
        is_main=False,
        court="Sąd Okręgowy w Warszawie",
        courtaddr="al. Solidarności 127, Warszawa",
        neighborhoods="Stary Żoliborz, Sady Żoliborskie, Piaski, Potok, Marymont-Ruda",
    ),
    dict(
        name="Wola",
        namegen="Woli",
        key="wola",
        domain="rozwodwola.pl",
        url="https://rozwodwola.pl",
        is_main=False,
        court="Sąd Okręgowy w Warszawie",
        courtaddr="al. Solidarności 127, Warszawa",
        neighborhoods="Czyste, Mirów, Odolany, Ulrychów, Koło, Szymańów",
    ),
    dict(
        name="Ochota",
        namegen="Ochoty",
        key="ochota",
        domain="rozwodochota.pl",
        url="https://rozwodochota.pl",
        is_main=False,
        court="Sąd Okręgowy w Warszawie",
        courtaddr="al. Solidarności 127, Warszawa",
        neighborhoods="Rakowiec, Stara Ochota, Szczęśliwice, Filtry",
    ),
    dict(
        name="Mokotów",
        namegen="Mokotowa",
        key="mokotow",
        domain="rozwodmokotow.pl",
        url="https://rozwodmokotow.pl",
        is_main=False,
        court="Sąd Okręgowy w Warszawie",
        courtaddr="al. Solidarności 127, Warszawa",
        neighborhoods="Stary Mokotów, Służewiec, Sadyba, Wierzbno, Sielce, Ksawerów",
    ),
    dict(
        name="Tarchomin",
        namegen="Tarchomina",
        key="tarchomin",
        domain="rozwodtarchomin.pl",
        url="https://rozwodtarchomin.pl",
        is_main=False,
        court="Sąd Okręgowy w Warszawie",
        courtaddr="al. Solidarności 127, Warszawa",
        neighborhoods="Tarchomin, Henryków, Nowodwory, Białołęka Dworska",
    ),
    dict(
        name="Legionowo",
        namegen="Legionowa",
        key="legionowo",
        domain="rozwodlegionowo.pl",
        url="https://rozwodlegionowo.pl",
        is_main=False,
        court="właściwy sąd okręgowy",
        courtaddr="pomagamy ustalić właściwy sąd dla Twojego miejsca zamieszkania",
        neighborhoods="centrum Legionowa, Piaski, Przymorze, os. Sobieskiego",
    ),
    dict(
        name="Łomianki",
        namegen="Łomianek",
        key="lomianki",
        domain="rozwodlomianki.pl",
        url="https://rozwodlomianki.pl",
        is_main=False,
        court="Sąd Okręgowy w Warszawie",
        courtaddr="al. Solidarności 127, Warszawa",
        neighborhoods="centrum Łomianek, Dąbrowa, Kiełpin, Łomianki Górne, Kazuń",
    ),
    dict(
        name="Jabłonna",
        namegen="Jabłonny",
        key="jablonna",
        domain="rozwodjablonna.pl",
        url="https://rozwodjablonna.pl",
        is_main=False,
        court="właściwy sąd okręgowy",
        courtaddr="pomagamy ustalić właściwy sąd dla Twojego miejsca zamieszkania",
        neighborhoods="Jabłonna, Chotomów, Skierdy, Rajszew, Dąbrowa Chotomowska, Trzciany",
    ),
]

# Domeny lokalne (poza główną) — dla sekcji ## Lokalizacje w głównym llms.txt
LOCAL_DOMAINS = [d for d in DISTRICTS if not d.get("is_main")]
MAIN_DOMAIN = next(d for d in DISTRICTS if d.get("is_main"))

# ─── SEKCJE TREŚCI (wspólne dla wszystkich domen) ─────────────────────────────

SERVICES = [
    ("Rozwód i separacja",          "Pozew o rozwód, reprezentacja przed sądem, negocjacje. Obsługujemy sprawy polubowne i sporne, z orzekaniem o winie i bez."),
    ("Podział majątku",             "Analiza majątku wspólnego, nieruchomości, firm i kredytów hipotecznych. Postępowanie sądowe lub notarialne."),
    ("Opieka nad dziećmi i alimenty","Plan wychowawczy, ustalenie kontaktów z dzieckiem, dochodzenie lub zmiana alimentów. Priorytetem jest dobro dzieci."),
    ("Władza rodzicielska",         "Ograniczenie, zawieszenie lub pozbawienie władzy rodzicielskiej. Zmiana dotychczasowych ustaleń sądowych."),
    ("Separacja prawna",            "Orzeczenie separacji jako etap poprzedzający rozwód lub samodzielna instytucja prawna."),
    ("Mediacja rodzinna",           "Wsparcie w ugodowym zakończeniu sporu — szybciej, taniej i mniej konfliktowo niż droga sądowa."),
]

FAQ = [
    ("Ile trwa sprawa rozwodowa?",
     "Rozwód bez orzekania o winie przy zgodzie obu stron — 3–6 miesięcy. Sporne sprawy z podziałem majątku i kwestiami dzieci — często ponad rok. Kancelaria oceni realny czas dla Twojej sprawy podczas bezpłatnej konsultacji."),
    ("Ile kosztuje adwokat w sprawie rozwodowej?",
     "Wynagrodzenie jest ustalane indywidualnie zależnie od stopnia skomplikowania sprawy. Do tego dochodzi opłata sądowa od pozwu (600 zł) i ewentualne koszty biegłych. Pełna wycena jest przedstawiana przed podpisaniem umowy — bez ukrytych kosztów."),
    ("Czy można uzyskać rozwód bez orzekania o winie?",
     "Tak — jeśli obie strony wyrażają zgodę, sąd orzeka rozwód bez ustalania winy. Jest to szybsze, tańsze i mniej konfliktowe rozwiązanie, często korzystniejsze dla dzieci."),
    ("Co z mieszkaniem i kredytem po rozwodzie?",
     "Podział majątku (w tym nieruchomości i kredytów hipotecznych) może nastąpić w trakcie lub po sprawie rozwodowej. Możliwe opcje: sprzedaż i podział ceny, spłata jednego małżonka, ustanowienie współwłasności. Kancelaria omówi wszystkie scenariusze."),
    ("Czy konsultacja jest bezpłatna?",
     "Tak — pierwsza konsultacja (30 minut) jest zawsze bezpłatna, stacjonarnie lub online (Teams/Zoom/telefon)."),
]

CONTACT = dict(
    phone="605 089 552",
    phone_href="tel:+48605089552",
    email="kancelaria@idzik.org.pl",
    address1="ul. Ceramiczna 5E/79, 03-126 Warszawa",
    address2="ul. Bolkowska 2A/28, 01-466 Warszawa",
    hours="poniedziałek–piątek 8:00–18:00",
)


# ─── GENERATORY ───────────────────────────────────────────────────────────────

def _services_list(url: str) -> list[str]:
    """Tworzy listę linków do usług (wszystkie prowadzą do strony głównej domeny)."""
    return [f"- [{name}]({url}/): {desc}" for name, desc in SERVICES]


def _faq_list() -> list[str]:
    """Zwraca listę pytań FAQ jako Markdown."""
    lines = []
    for q, a in FAQ:
        lines.append(f"- **{q}** — {a}")
    return lines


def build_llms(d: dict) -> str:
    """
    Generuje llms.txt zgodny ze specyfikacją llmstxt.org:
      H1 → blockquote (≤50 słów) → opcjonalne akapity → sekcje H2 z listami linków.
    """
    url = d["url"].rstrip("/")
    name = d["name"]
    namegen = d.get("namegen", name)
    is_main = d.get("is_main", False)
    court = d["court"]
    courtaddr = d.get("courtaddr", "")
    neighborhoods = d.get("neighborhoods", "")

    # ── Blockquote ──────────────────────────────────────────────
    if is_main:
        bq = (
            "> Kancelaria Adwokacka Magdalena Idzik-Cieśla — adwokat rozwodowy Warszawa. "
            "Kompleksowa pomoc prawna w sprawach o rozwód, separację, alimenty, "
            "opiekę nad dziećmi i podział majątku. Bezpłatna konsultacja 30 min."
        )
    else:
        bq = (
            f"> Adwokat rozwodowy {name} — Kancelaria Adwokacka Magdalena Idzik-Cieśla. "
            f"Pomoc prawna w sprawach rodzinnych dla klientów z {namegen} i okolic: "
            f"rozwód, alimenty, opieka nad dziećmi, podział majątku. Bezpłatna konsultacja."
        )

    # ── Opis (akapity bez nagłówków) ─────────────────────────────
    if is_main:
        desc_lines = [
            "Kancelaria specjalizuje się wyłącznie w prawie rodzinnym i prowadzi sprawy przed sądami okręgowymi na terenie całego Mazowsza, w tym Warszawy i miejscowości podwarszawskich.",
            f"Obsługiwane obszary: {neighborhoods}.",
            f"Sąd właściwy dla klientów z Warszawy: {court}, {courtaddr}.",
            "Kancelaria posiada ponad 12 lat doświadczenia, zakończyła ponad 850 spraw i oferuje konsultacje stacjonarne (ul. Ceramiczna 5E/79 i ul. Bolkowska 2A/28, Warszawa) oraz online.",
            "Treści na tej stronie mają charakter informacyjny i nie stanowią porady prawnej. Kancelaria odpowiada wyłącznie za treści opublikowane w domenach wymienionych w sekcji ## Lokalizacje.",
        ]
    else:
        court_note = (
            f"Sprawy dla klientów z {namegen} są prowadzone przed {court}"
            f"{f', {courtaddr}' if courtaddr and 'pomagamy' not in courtaddr else ' — kancelaria pomoże ustalić właściwy sąd'}."
        )
        desc_lines = [
            f"Lokalny landing page kancelarii dedykowany klientom z {namegen} i okolicznych osiedli: {neighborhoods}.",
            court_note,
            "Kancelaria oferuje konsultacje stacjonarne w Warszawie (ul. Ceramiczna 5E/79 i ul. Bolkowska 2A/28) oraz online — bez konieczności dojazdu.",
            "Strona służy wyłącznie do pozyskiwania zapytań i prezentacji zakresu usług. Nie zawiera treści prawniczych ani porad prawnych.",
        ]

    # ── Sekcje H2 ────────────────────────────────────────────────
    main_pages = [
        f"- [Strona główna]({url}/): główna publiczna strona tej domeny.",
        f"- [Mapa strony]({url}/sitemap.xml): indeks URL w formacie XML dla crawlerów.",
        f"- [Zasady dla robotów]({url}/robots.txt): polityka dostępu dla crawlerów AI i wyszukiwarek.",
    ]

    services = _services_list(url)
    faq = _faq_list()

    if is_main:
        locations = ["## Lokalizacje"] + [
            f"- [{loc['name']}]({loc['url']}/): lokalny landing page dla {loc['namegen']}."
            for loc in LOCAL_DOMAINS
        ]
    else:
        locations = [
            "## Optional",
            f"- [Główna witryna kancelarii]({MAIN_DOMAIN['url']}/): centralna strona kancelarii — pełna oferta, dane kontaktowe, wszystkie lokalizacje.",
        ]

    # ── Złożenie pliku ───────────────────────────────────────────
    parts = [
        f"# Kancelaria Adwokacka Magdalena Idzik-Cieśla",
        "",
        bq,
        "",
        *desc_lines,
        "",
        "## Główne strony",
        *main_pages,
        "",
        "## Zakres pomocy",
        *services,
        "",
        "## FAQ",
        *faq,
        "",
        "## Kontakt",
        f"- [Kontakt z kancelarią]({url}/): formularz kontaktowy i możliwość umówienia konsultacji.",
        f"- Telefon: [{CONTACT['phone']}]({CONTACT['phone_href']})",
        f"- E-mail: [{CONTACT['email']}](mailto:{CONTACT['email']})",
        f"- Godziny pracy: {CONTACT['hours']}",
        f"- Adres 1: {CONTACT['address1']}",
        f"- Adres 2: {CONTACT['address2']}",
        "",
        *locations,
        "",
    ]
    return "\n".join(parts)


def build_llms_full(d: dict) -> str:
    """
    Generuje llms-full.txt — jedna wiadomość z pełną treścią wszystkich kluczowych
    sekcji strony, bez konieczności podążania za linkami.
    Przeznaczony dla agentów AI i narzędzi typu Cursor / GitHub Copilot.
    """
    url = d["url"].rstrip("/")
    name = d["name"]
    namegen = d.get("namegen", name)
    is_main = d.get("is_main", False)
    court = d["court"]
    courtaddr = d.get("courtaddr", "")
    neighborhoods = d.get("neighborhoods", "")

    if is_main:
        intro = (
            "Kancelaria Adwokacka Magdalena Idzik-Cieśla to kancelaria specjalizująca się wyłącznie "
            "w prawie rodzinnym i sprawach rozwodowych, działająca na terenie Warszawy i Mazowsza od ponad 12 lat. "
            "Kancelaria zakończyła ponad 850 spraw i oferuje konsultacje stacjonarne oraz online."
        )
    else:
        intro = (
            f"Lokalny landing page Kancelarii Adwokackiej Magdaleny Idzik-Cieśla dedykowany klientom z {namegen}. "
            f"Kancelaria prowadzi sprawy rodzinne i rozwodowe dla mieszkańców {namegen} i okolic: {neighborhoods}. "
            f"Właściwy sąd: {court}{f', {courtaddr}' if courtaddr and 'pomagamy' not in courtaddr else ''}."
        )

    services_full = "\n\n".join(
        f"### {name}\n{desc}" for name, desc in SERVICES
    )

    faq_full = "\n\n".join(
        f"**Pytanie:** {q}\n\n**Odpowiedź:** {a}" for q, a in FAQ
    )

    parts = [
        f"# Kancelaria Adwokacka Magdalena Idzik-Cieśla — {name} (pełna treść)",
        "",
        "## O kancelarii",
        "",
        intro,
        "",
        "## Zakres pomocy",
        "",
        services_full,
        "",
        "## Najczęściej zadawane pytania (FAQ)",
        "",
        faq_full,
        "",
        "## Dane kontaktowe",
        "",
        f"- **Telefon:** {CONTACT['phone']}",
        f"- **E-mail:** {CONTACT['email']}",
        f"- **Adres 1:** {CONTACT['address1']}",
        f"- **Adres 2:** {CONTACT['address2']}",
        f"- **Godziny pracy:** {CONTACT['hours']}",
        f"- **Konsultacje online:** tak (Teams, Zoom, telefon)",
        "",
        "## Lokalizacja obsługiwanego obszaru",
        "",
        f"Obsługiwany obszar: {name}{f' ({neighborhoods})' if neighborhoods else ''}.",
        f"Sąd właściwy: {court}{f', {courtaddr}' if courtaddr and 'pomagamy' not in courtaddr else ''}.",
        "",
        "## Strona internetowa",
        "",
        f"- Główna strona domeny: {url}/",
        f"- Mapa strony: {url}/sitemap.xml",
        f"- Zasady dla robotów: {url}/robots.txt",
        f"- Indeks LLM: {url}/llms.txt",
        "",
    ]
    return "\n".join(parts)


def build_robots(d: dict) -> str:
    """
    Generuje robots.txt zoptymalizowany pod kątem AI:
    - Przepuszcza search boty (OAI-SearchBot, PerplexityBot, Claude-SearchBot itd.)
    - Blokuje training boty (GPTBot, ClaudeBot, Google-Extended itd.)
    - Dodaje explicit Allow: /llms.txt i /sitemap.xml
    - Nie blokuje strony /dziekujemy.html (noindex w HTML wystarczy)
    """
    url = d["url"].rstrip("/")
    return textwrap.dedent(f"""\
        # robots.txt — {d['domain']}
        # Ostatnia aktualizacja: 2026-05-11
        #
        # Strategia:
        #   ✅ Zezwalamy na search/inference boty (cytowania w wynikach AI)
        #   🚫 Blokujemy training boty (ochrona treści przed użyciem do trenowania modeli)
        #
        # ─── WYSZUKIWARKI ────────────────────────────────────────────────
        User-agent: Googlebot
        Allow: /
        Disallow: /dziekujemy.html

        User-agent: Bingbot
        Allow: /
        Disallow: /dziekujemy.html

        # ─── AI SEARCH / INFERENCE (przepuszczamy — zależy nam na cytowaniach) ─
        User-agent: OAI-SearchBot
        Allow: /

        User-agent: ChatGPT-User
        Allow: /

        User-agent: Claude-User
        Allow: /

        User-agent: Claude-SearchBot
        Allow: /

        User-agent: PerplexityBot
        Allow: /

        User-agent: Perplexity-User
        Allow: /

        User-agent: YouBot
        Allow: /

        User-agent: GoogleOther
        Allow: /

        # ─── AI TRAINING (blokujemy — nie chcemy oddawać treści do trenowania) ─
        User-agent: GPTBot
        Disallow: /

        User-agent: ClaudeBot
        Disallow: /

        User-agent: Google-Extended
        Disallow: /

        User-agent: CCBot
        Disallow: /

        User-agent: Meta-ExternalAgent
        Disallow: /

        User-agent: FacebookBot
        Disallow: /

        User-agent: Bytespider
        Disallow: /

        User-agent: Applebot-Extended
        Disallow: /

        # ─── DOMYŚLNE ────────────────────────────────────────────────────
        User-agent: *
        Allow: /
        Disallow: /dziekujemy.html

        # ─── PLIKI AI / INDEKS ───────────────────────────────────────────
        # Explicit allow dla plików metadanych (ważne gdy masz catch-all worker)
        Allow: /llms.txt
        Allow: /llms-full.txt
        Allow: /sitemap.xml
        Allow: /robots.txt

        # ─── SITEMAP ─────────────────────────────────────────────────────
        Sitemap: {url}/sitemap.xml
    """)


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main() -> None:
    base_dir = Path(__file__).resolve().parent

    results = []
    for d in DISTRICTS:
        out_dir = base_dir if d.get("is_main") else base_dir / d["key"]
        out_dir.mkdir(parents=True, exist_ok=True)

        files = {
            "llms.txt":      build_llms(d),
            "llms-full.txt": build_llms_full(d),
            "robots.txt":    build_robots(d),
        }

        for fname, content in files.items():
            path = out_dir / fname
            path.write_text(content, encoding="utf-8")
            results.append(path)

    print(f"✅ Wygenerowano {len(results)} plików dla {len(DISTRICTS)} domen:\n")
    for p in results:
        kb = p.stat().st_size / 1024
        print(f"   {str(p.relative_to(base_dir)):<45} ({kb:.1f} KB)")

    print(f"""
─────────────────────────────────────────────
NASTĘPNE KROKI:
1. Wdróż pliki na domeny (scp / git push / Cloudflare Worker override)
2. Sprawdź każdą domenę ręcznie:
     curl -I https://DOMENA.pl/llms.txt        → oczekiwany: 200, text/plain
     curl -I https://DOMENA.pl/llms-full.txt   → oczekiwany: 200, text/plain
     curl -I https://DOMENA.pl/robots.txt      → oczekiwany: 200, text/plain
3. Zgłoś llms.txt do Google Search Console (jako dodatkowy URL do indeksowania)
4. Jeśli Worker ma fallback do index.html — dodaj wyjątek dla /llms*.txt /robots.txt
─────────────────────────────────────────────
""")


if __name__ == "__main__":
    main()
