#!/usr/bin/env python3
"""
Generator stron per-domena — Kancelaria Adwokacka Magdalena Idzik-Cieśla
Uruchomienie: python3 build.py
Tworzy: {klucz}/index.html dla każdej domeny (assets: ../assets/)
"""

import os
import shutil

DISTRICTS = [
    dict(
        name="Bemowo", name_gen="Bemowa", name_loc="Bemowie", key="bemowo",
        domain="rozwodbemowo.pl", url="https://rozwodbemowo.pl/",
        accent="#8B1A3A", accent_light="#C13C6A", accent_bg="#FDF0F4",
        neighborhoods="Chrzanów, Jelonki Północne, Jelonki Południowe, Lotnisko, Wola Ulrychów, Górce",
        court="Sąd Okręgowy w Warszawie", court_addr="al. Solidarności 127, Warszawa",
        t_ini="KM", t_name="Katarzyna M.",
        t_quote="Potrzebowałam adwokata z doświadczeniem blisko Bemowa. Pani mecenas przeprowadziła mnie przez całą sprawę krok po kroku — wyrok zgodny z oczekiwaniami.",
        t_topic="Sprawa rozwodowa · Bemowo",
    ),
    dict(
        name="Bielany", name_gen="Bielan", name_loc="Bielanach", key="bielany",
        domain="rozwodbielany.pl", url="https://rozwodbielany.pl/",
        accent="#1A4E8B", accent_light="#4A7FC1", accent_bg="#EEF4FB",
        neighborhoods="Marymont, Chomiczówka, Wrzeciono, Słodowiec, Młociny, Placówka",
        court="Sąd Okręgowy w Warszawie", court_addr="al. Solidarności 127, Warszawa",
        t_ini="TB", t_name="Tomasz B.",
        t_quote="Sprawa była skomplikowana, ale pani mecenas znała każdy szczegół. Polecam mieszkańcom Bielan i całej północnej Warszawy.",
        t_topic="Podział majątku · Bielany",
    ),
    dict(
        name="Żoliborz", name_gen="Żoliborza", name_loc="Żoliborzu", key="zoliborz",
        domain="rozwodzoliborz.pl", url="https://rozwodzoliborz.pl/",
        accent="#5B2D8E", accent_light="#8B5EC1", accent_bg="#F3EEF9",
        neighborhoods="Stary Żoliborz, Sady Żoliborskie, Piaski, Potok, Marymont-Ruda",
        court="Sąd Okręgowy w Warszawie", court_addr="al. Solidarności 127, Warszawa",
        t_ini="EK", t_name="Ewa K.",
        t_quote="Mieszkam na Żoliborzu i szukałam adwokata, który naprawdę słucha. Pani mecenas była dokładnie tym, czego potrzebowałam. Profesjonalizm i spokój.",
        t_topic="Opieka nad dziećmi · Żoliborz",
    ),
    dict(
        name="Wola", name_gen="Woli", name_loc="Woli", key="wola",
        domain="rozwodwola.pl", url="https://rozwodwola.pl/",
        accent="#8B3A1A", accent_light="#C46A3C", accent_bg="#FDF0E9",
        neighborhoods="Czyste, Mirów, Odolany, Ulrychów, Koło, Szymańów",
        court="Sąd Okręgowy w Warszawie", court_addr="al. Solidarności 127, Warszawa",
        t_ini="RN", t_name="Robert N.",
        t_quote="Sprawny kontakt, konkretne informacje, zero owijania w bawełnę. Sprawa z Woli zakończona szybciej niż przewidywał sąd. Polecam.",
        t_topic="Sprawa rozwodowa · Wola",
    ),
    dict(
        name="Ochota", name_gen="Ochoty", name_loc="Ochocie", key="ochota",
        domain="rozwodochota.pl", url="https://rozwodochota.pl/",
        accent="#1A6B5B", accent_light="#3CA48B", accent_bg="#EEFAF7",
        neighborhoods="Rakowiec, Stara Ochota, Szczęśliwice, Filtry",
        court="Sąd Okręgowy w Warszawie", court_addr="al. Solidarności 127, Warszawa",
        t_ini="MJ", t_name="Marta J.",
        t_quote="Jako mieszkanka Ochoty doceniam dostępność kancelarii. Konsultacja online zorganizowana w ciągu doby, sprawa poprowadzona znakomicie.",
        t_topic="Separacja prawna · Ochota",
    ),
    dict(
        name="Mokotów", name_gen="Mokotowa", name_loc="Mokotowie", key="mokotow",
        domain="rozwodmokotow.pl", url="https://rozwodmokotow.pl/",
        accent="#2D4A6B", accent_light="#5A7FA8", accent_bg="#EEF2F8",
        neighborhoods="Stary Mokotów, Służewiec, Sadyba, Wierzbno, Sielce, Ksawerów",
        court="Sąd Okręgowy w Warszawie", court_addr="al. Solidarności 127, Warszawa",
        t_ini="AS", t_name="Aleksandra S.",
        t_quote="Polecam kancelarię wszystkim z Mokotowa. Profesjonalne podejście, pełna dyskrecja i wynik, który satysfakcjonuje.",
        t_topic="Podział majątku · Mokotów",
    ),
    dict(
        name="Tarchomin", name_gen="Tarchomina", name_loc="Tarchominie", key="tarchomin",
        domain="rozwodtarchomin.pl", url="https://rozwodtarchomin.pl/",
        accent="#4A6B1A", accent_light="#7FA83C", accent_bg="#F2F7EE",
        neighborhoods="Tarchomin, Henryków, Nowodwory, Białołęka Dworska",
        court="Sąd Okręgowy w Warszawie", court_addr="al. Solidarności 127, Warszawa",
        t_ini="KW", t_name="Krzysztof W.",
        t_quote="Z Tarchomina do Warszawy bywa daleko, ale konsultacja online rozwiązała ten problem. Świetna komunikacja i wyniki powyżej oczekiwań.",
        t_topic="Sprawa rozwodowa · Tarchomin",
    ),
    dict(
        name="Legionowo", name_gen="Legionowa", name_loc="Legionowie", key="legionowo",
        domain="rozwodlegionowo.pl", url="https://rozwodlegionowo.pl/",
        accent="#1A5E6B", accent_light="#3C9AA8", accent_bg="#EEF8FA",
        neighborhoods="centrum Legionowa, Piaski, Przymorze, os. Sobieskiego",
        court="właściwy sąd okręgowy", court_addr="pomagamy ustalić właściwy sąd dla Twojego miejsca zamieszkania",
        t_ini="AW", t_name="Anna W.",
        t_quote="Bałam się, że stracę kontakt z dziećmi. Pani mecenas skutecznie zawalczyła o moje prawa. Warunki, które ustaliliśmy, są dobre dla całej rodziny.",
        t_topic="Opieka nad dziećmi · Legionowo",
    ),
    dict(
        name="Łomianki", name_gen="Łomianek", name_loc="Łomiankach", key="lomianki",
        domain="rozwodlomianki.pl", url="https://rozwodlomianki.pl/",
        accent="#2D6B1A", accent_light="#5AA83C", accent_bg="#EEF8EE",
        neighborhoods="centrum Łomianek, Dąbrowa, Kiełpin, Łomianki Górne, Kazuń",
        court="Sąd Okręgowy w Warszawie", court_addr="al. Solidarności 127, Warszawa",
        t_ini="PT", t_name="Piotr T.",
        t_quote="Sprawny kontakt, zawsze dostępni gdy potrzebowałem odpowiedzi. Podział majątku zakończony szybciej niż myślałem. Merytoryczna pomoc na każdym etapie.",
        t_topic="Podział majątku · Łomianki",
    ),
    dict(
        name="Jabłonna", name_gen="Jabłonny", name_loc="Jabłonnie", key="jablonna",
        domain="rozwodjablonna.pl", url="https://rozwodjablonna.pl/",
        accent="#6B5B1A", accent_light="#A89040", accent_bg="#FAF7EE",
        neighborhoods="Jabłonna, Chotomów, Skierdy, Rajszew, Dąbrowa Chotomowska, Trzciany",
        court="właściwy sąd okręgowy", court_addr="pomagamy ustalić właściwy sąd dla Twojego miejsca zamieszkania",
        t_ini="DK", t_name="Dorota K.",
        t_quote="Mieszkam pod Jabłonną i nie spodziewałam się tak sprawnej obsługi. Konsultacja online, szybka analiza i pełne zaangażowanie. Bardzo polecam.",
        t_topic="Sprawa rozwodowa · Jabłonna",
    ),
]

ALL_DOMAINS = [
    ("Warszawa",  "https://rozwod.waw.pl/"),
    ("Bemowo",    "https://rozwodbemowo.pl/"),
    ("Bielany",   "https://rozwodbielany.pl/"),
    ("Żoliborz",  "https://rozwodzoliborz.pl/"),
    ("Wola",      "https://rozwodwola.pl"),
    ("Ochota",    "https://rozwodochota.pl/"),
    ("Mokotów",   "https://rozwodmokotow.pl/"),
    ("Tarchomin", "https://rozwodtarchomin.pl/"),
    ("Legionowo", "https://rozwodlegionowo.pl/"),
    ("Łomianki",  "https://rozwodlomianki.pl/"),
    ("Jabłonna",  "https://rozwodjablonna.pl/"),
]


def footer_links_html(current_url):
    items = []
    for name, url in ALL_DOMAINS:
        if url == current_url:
            continue
        items.append(f'          <li><a href="{url}">{name}</a></li>')
    return "\n".join(items)


def build_page(d):
    footer = footer_links_html(d["url"])

    if "właściwy" in d["court"]:
        court_faq = (
            f"Właściwy sąd zależy od miejsca Twojego zameldowania. "
            f"Skontaktuj się z nami — pomożemy ustalić właściwy sąd okręgowy "
            f"i przygotujemy wszystkie dokumenty potrzebne do złożenia pozwu."
        )
    else:
        court_faq = (
            f"Dla mieszkańców {d['name']} właściwy jest <strong>{d['court']}</strong> "
            f"przy {d['court_addr']}. Kancelaria reprezentuje klientów przed tym sądem "
            f"w sprawach rozwodowych, o podział majątku i opiekę nad dziećmi."
        )

    return f"""<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Adwokat rozwodowy {d['name']} — Kancelaria Magdalena Idzik-Cieśla. Rozwód, podział majątku, opieka nad dziećmi. Bezpłatna konsultacja 30 minut. Tel. 605 089 552.">
  <meta name="robots" content="index, follow">
  <title>Adwokat rozwodowy {d['name']} | Kancelaria Magdalena Idzik-Cieśla</title>
  <link rel="canonical" href="{d['url']}">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pl_PL">
  <meta property="og:site_name" content="Kancelaria Magdalena Idzik-Cieśla">
  <meta property="og:title" content="Adwokat rozwodowy {d['name']} | Kancelaria Magdalena Idzik-Cieśla">
  <meta property="og:description" content="Pomoc w sprawach o rozwód, alimenty, dzieci i podział majątku na {d['name_loc']}.">
  <meta property="og:url" content="{d['url']}">
  <meta property="og:image" content="{d['url']}assets/{d['key']}.png">
  <meta property="og:image:secure_url" content="{d['url']}assets/{d['key']}.png">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Adwokat rozwodowy {d['name']} - Kancelaria Magdalena Idzik-Cieśla">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Adwokat rozwodowy {d['name']} | Kancelaria Magdalena Idzik-Cieśla">
  <meta name="twitter:description" content="Rozwód, alimenty, dzieci i majątek - pomoc prawna na {d['name_loc']}.">
  <meta name="twitter:image" content="{d['url']}assets/{d['key']}.png">

  <script>
    window.SITE_CONFIG = {{
      district:     "{d['name']}",
      districtKey:  "{d['key']}",
      accentColor:  "{d['accent']}",
      accentLight:  "{d['accent_light']}",
      accentBg:     "{d['accent_bg']}"
    }};
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "LegalService",
    "name": "Kancelaria Adwokacka Magdalena Idzik-Cieśla",
    "description": "Adwokat rozwodowy {d['name']} — pomoc prawna w sprawach rozwodowych, podziału majątku i opieki nad dziećmi.",
    "url": "{d['url']}",
    "telephone": "+48605089552",
    "email": "kancelaria@idzik.org.pl",
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "ul. Ceramiczna 5E/79",
      "addressLocality": "Warszawa",
      "postalCode": "03-126",
      "addressCountry": "PL"
    }},
    "areaServed": {{"@type": "Place", "name": "{d['name']}, Warszawa"}},
    "priceRange": "$$",
    "openingHours": "Mo-Fr 08:00-18:00"
  }}
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600;1,700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>

<div class="ticker-wrap" aria-label="Obszary działania kancelarii">
  <div class="ticker-track" id="ticker-track"></div>
</div>

<header class="nav">
  <div class="nav-inner">
    <a href="{d['url']}" class="nav-logo" aria-label="Strona główna">
      <span class="nav-logo-name">Kancelaria Adwokacka</span>
      <span class="nav-logo-sub">Magdalena Idzik‑Cieśla</span>
    </a>
    <nav class="nav-links nav-desktop" id="nav-desktop" aria-label="Nawigacja główna">
      <a href="#pomoc"   class="nav-link">Zakres pomocy</a>
      <a href="#proces"  class="nav-link">Jak działamy</a>
      <a href="#opinie"  class="nav-link">Opinie</a>
      <a href="#faq"      class="nav-link">FAQ</a>
      <a href="blog.html" class="nav-link" style="color:var(--accent);font-weight:600;">Blog</a>
      <a href="#kontakt"  class="btn nav-cta">Bezpłatna konsultacja</a>
    </nav>
    <button class="hamburger" id="hamburger" aria-label="Menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<main>

<!-- HERO -->
<section class="hero section" style="padding-top:clamp(4rem,8vw,6rem);padding-bottom:clamp(3rem,6vw,5rem);background:var(--bg);">
  <div class="container">
    <div class="hero-2col" style="display:grid;grid-template-columns:1fr 1fr;gap:3.5rem;align-items:center;">
      <div>
        <p class="hero-eyebrow" style="justify-content:flex-start;">
          <span class="hero-eyebrow-dot"></span>
          Kancelaria Adwokacka · {d['name']}
        </p>
        <h1 style="text-align:left;margin:0 0 1.25rem;font-size:clamp(1.9rem,3.2vw,2.9rem);">
          Skuteczna pomoc prawna<br>w <em>najtrudniejszym</em> momencie
        </h1>
        <p class="hero-sub" style="text-align:left;margin:0 0 2rem;max-width:100%;">
          Rozwód, podział majątku, opieka nad dziećmi — przeprowadzimy Cię przez cały
          proces jasno, dyskretnie i po Twojej stronie.
        </p>
        <div class="hero-actions" style="justify-content:flex-start;margin-bottom:2rem;">
          <a href="#kontakt" class="btn btn-primary btn-lg">Umów bezpłatną konsultację →</a>
          <a href="tel:+48605089552" class="btn btn-outline btn-lg">📞 605 089 552</a>
        </div>
        <div class="hero-trust" style="justify-content:flex-start;flex-direction:column;align-items:flex-start;gap:.6rem;">
          <span class="hero-trust-item">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M12 3L5.5 10 2 6.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            Bezpłatna konsultacja 30 min
          </span>
          <span class="hero-trust-item">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M12 3L5.5 10 2 6.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            Pełna dyskrecja
          </span>
          <span class="hero-trust-item">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M12 3L5.5 10 2 6.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            {d['name']} i okolice · Warszawa
          </span>
          <span class="hero-trust-item">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M12 3L5.5 10 2 6.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            Konsultacje online
          </span>
        </div>
      </div>
      <div style="position:relative;border-radius:var(--radius-lg);overflow:hidden;box-shadow:var(--shadow-lg);background:var(--navy);align-self:stretch;min-height:320px;">
        <video id="hero-video"
          src="https://github.com/user-attachments/assets/7c593bf7-b8ff-47d8-af33-d6ca0661c832"
          playsinline controls preload="metadata"
          style="position:absolute;inset:0;width:100%;height:100%;display:block;object-fit:cover;"></video>
        <div id="video-overlay" onclick="playVideo()" style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;transition:opacity .3s;background:rgba(15,31,56,.42);z-index:1;">
          <div id="play-btn" style="width:72px;height:72px;border-radius:50%;background:rgba(255,255,255,.13);backdrop-filter:blur(12px);border:1.5px solid rgba(255,255,255,.35);display:flex;align-items:center;justify-content:center;transition:transform .2s,background .2s;">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="white" style="margin-left:4px"><path d="M8 5v14l11-7z"/></svg>
          </div>
          <p style="margin-top:1rem;font-family:var(--serif);font-size:.95rem;font-style:italic;color:rgba(255,255,255,.85);letter-spacing:.02em;">Posłuchaj o kancelarii</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- STATYSTYKI -->
<div class="stats-bar">
  <div class="container">
    <div class="stats-inner">
      <div class="stat-item">
        <div class="stat-number" data-count="15" data-suffix="+">15+</div>
        <div class="stat-label">Lat doświadczenia</div>
      </div>
      <div class="stat-item">
        <div class="stat-number" data-count="850" data-suffix="+">850+</div>
        <div class="stat-label">Zakończonych spraw</div>
      </div>
      <div class="stat-item">
        <div class="stat-number" data-count="97" data-suffix="%">97%</div>
        <div class="stat-label">Klientów poleca dalej</div>
      </div>
      <div class="stat-item">
        <div class="stat-number" data-count="11">11</div>
        <div class="stat-label">Lokalizacji w Mazowieckiem</div>
      </div>
    </div>
  </div>
</div>

<!-- PASEK LOKALIZACJI -->
<div class="location-strip">
  <div class="container">
    <div class="location-strip-inner">
      <span class="location-chip">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
        ul. Ceramiczna 5E/79, Warszawa
      </span>
      <span class="location-chip">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
        ul. Bolkowska 2A/28, Warszawa
      </span>
      <span class="location-chip" style="font-weight:600;color:var(--accent);">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
        {d['name']} · online
      </span>
    </div>
  </div>
</div>

<!-- SEKCJA LOKALNA SEO -->
<div style="background:var(--accent-bg);padding:2.25rem 0;border-bottom:1px solid rgba(0,0,0,.06);">
  <div class="container">
    <div style="max-width:760px;margin:0 auto;text-align:center;">
      <h2 style="font-size:clamp(1.15rem,2vw,1.4rem);margin:0 0 .65rem;font-family:var(--serif);">
        Adwokat rozwodowy <strong>{d['name']}</strong> — pomoc prawna blisko Ciebie
      </h2>
      <p style="color:var(--text-muted);font-size:.93rem;line-height:1.75;margin:0;">
        Obsługujemy klientów z <strong>{d['name']}</strong> i sąsiednich osiedli:
        <strong>{d['neighborhoods']}</strong>.
        Sprawy rodzinne i rozwodowe prowadzimy przed <strong>{d['court']}</strong>
        ({d['court_addr']}). Oferujemy konsultacje stacjonarne w Warszawie
        oraz online — bez konieczności dojazdów.
      </p>
    </div>
  </div>
</div>

<!-- PROBLEMY -->
<section class="section" id="pomoc">
  <div class="container">
    <div class="pain-grid">
      <div>
        <div class="section-header">
          <p class="section-label">Rozumiem Twoją sytuację</p>
          <h2 class="section-title">To jeden z najtrudniejszych<br>momentów. <em>Nie musisz</em><br>przez to przechodzić sam.</h2>
          <p class="section-desc">
            Każda sprawa jest inna. Niezależnie od tego, jak skomplikowana jest Twoja sytuacja —
            masz prawo do rzetelnej i ludzkiej pomocy prawnej.
          </p>
        </div>
        <div class="pain-items">
          <div class="pain-item">
            <div class="pain-icon">⚖️</div>
            <div>
              <h4>Nie wiem od czego zacząć</h4>
              <p>Wyjaśniamy każdy krok po ludzku — od złożenia pozwu aż po prawomocny wyrok. Bez żargonu, bez ukrytych kosztów.</p>
            </div>
          </div>
          <div class="pain-item">
            <div class="pain-icon">🏠</div>
            <div>
              <h4>Obawiamy się o mieszkanie i majątek</h4>
              <p>Zadbamy o sprawiedliwy podział — nieruchomości, oszczędności, firma, kredyt hipoteczny. Każdy przypadek analizujemy indywidualnie.</p>
            </div>
          </div>
          <div class="pain-item">
            <div class="pain-icon">👶</div>
            <div>
              <h4>Dzieci są dla mnie najważniejsze</h4>
              <p>Pomagamy ustalić plan wychowawczy, który zabezpieczy ich dobro i zagwarantuje realny kontakt z obojgiem rodziców.</p>
            </div>
          </div>
          <div class="pain-item">
            <div class="pain-icon">🤝</div>
            <div>
              <h4>Chcę to zakończyć polubownie</h4>
              <p>Mediacja jest często szybsza i tańsza. Wspieramy ugodowe rozwiązania wszędzie tam, gdzie to możliwe i korzystne dla Ciebie.</p>
            </div>
          </div>
        </div>
      </div>
      <div>
        <div class="pain-quote-block">
          <blockquote>
            „Kiedy trafiłam do kancelarii, czułam się całkowicie zagubiona. Pani mecenas spokojnie wyjaśniła mi każdy krok. Po raz pierwszy od miesięcy poczułam, że mam kogoś po swojej stronie."
          </blockquote>
          <cite>— Klientka kancelarii, {d['name']} 2024</cite>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- USŁUGI -->
<section class="section" style="background: var(--bg-card);">
  <div class="container">
    <div class="section-header section-center text-center">
      <p class="section-label">Zakres pomocy</p>
      <h2 class="section-title">Czym możemy <em>Ci pomóc</em></h2>
      <p class="section-desc">Kompleksowa obsługa prawna w sprawach rodzinnych — od pierwszej rozmowy do prawomocnego wyroku.</p>
    </div>
    <div class="services-grid">
      <div class="service-card">
        <div class="service-num">01</div>
        <h3>Rozwód</h3>
        <p>Pozew, reprezentacja przed sądem, negocjacje ze stroną przeciwną. Obsługujemy zarówno sprawy polubowne, jak i sporne.</p>
        <div class="service-tags">
          <span class="tag">Z orzekaniem o winie</span>
          <span class="tag">Bez orzekania</span>
          <span class="tag">Separacja</span>
        </div>
      </div>
      <div class="service-card">
        <div class="service-num">02</div>
        <h3>Podział majątku</h3>
        <p>Szczegółowa analiza składników majątku wspólnego, negocjacje oraz reprezentacja w postępowaniu sądowym lub notarialnym.</p>
        <div class="service-tags">
          <span class="tag">Nieruchomości</span>
          <span class="tag">Firmy</span>
          <span class="tag">Kredyty</span>
        </div>
      </div>
      <div class="service-card">
        <div class="service-num">03</div>
        <h3>Opieka i alimenty</h3>
        <p>Ustalenie planu wychowawczego, wysokości alimentów oraz prawa do kontaktów z dzieckiem. Pomoc przy zmianie ustalonych warunków.</p>
        <div class="service-tags">
          <span class="tag">Plan wychowawczy</span>
          <span class="tag">Alimenty</span>
          <span class="tag">Kontakty</span>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- PROCES -->
<section class="section process-section" id="proces">
  <div class="container">
    <div class="section-header section-center text-center">
      <p class="section-label">Jak działamy</p>
      <h2 class="section-title">Cztery kroki do <em>nowego początku</em></h2>
      <p class="section-desc">Przejrzysty, przewidywalny proces — bez niespodzianek i prawniczego żargonu.</p>
    </div>
    <div class="process-steps">
      <div class="process-step">
        <div class="step-badge">1</div>
        <h4>Bezpłatna konsultacja</h4>
        <p>30 minut bez zobowiązań. Opowiadasz o swojej sytuacji — odpowiadamy na najważniejsze pytania i oceniamy możliwości.</p>
      </div>
      <div class="process-step">
        <div class="step-badge">2</div>
        <h4>Analiza i strategia</h4>
        <p>Dokładnie analizujemy dokumenty i okoliczności. Opracowujemy indywidualną strategię działania dostosowaną do Twojej sprawy.</p>
      </div>
      <div class="process-step">
        <div class="step-badge">3</div>
        <h4>Reprezentacja</h4>
        <p>Przygotowujemy pisma, prowadzimy negocjacje i reprezentujemy Cię przed sądem. Jesteś informowany na każdym etapie.</p>
      </div>
      <div class="process-step">
        <div class="step-badge">4</div>
        <h4>Wyrok i nowy etap</h4>
        <p>Prawomocny wyrok z pewnością, że wszystkie kluczowe kwestie zostały właściwie zabezpieczone.</p>
      </div>
    </div>
  </div>
</section>

<!-- OPINIE -->
<section class="section" id="opinie">
  <div class="container">
    <div class="section-header section-center text-center">
      <p class="section-label">Opinie klientów</p>
      <h2 class="section-title">Co mówią <em>nasi klienci</em></h2>
    </div>
    <div class="testimonials-grid">
      <div class="testimonial">
        <div class="t-stars">★★★★★</div>
        <p class="t-quote">„Profesjonalizm i spokój — to co zapamiętałem. Sprawa była skomplikowana, ale przez cały czas miałem poczucie, że wszystko jest pod kontrolą. Serdecznie polecam."</p>
        <div class="t-author">
          <div class="t-avatar">MK</div>
          <div>
            <div class="t-name">Marek K.</div>
            <div class="t-meta">Sprawa rozwodowa · Warszawa</div>
          </div>
        </div>
      </div>
      <div class="testimonial">
        <div class="t-stars">★★★★★</div>
        <p class="t-quote">„{d['t_quote']}"</p>
        <div class="t-author">
          <div class="t-avatar">{d['t_ini']}</div>
          <div>
            <div class="t-name">{d['t_name']}</div>
            <div class="t-meta">{d['t_topic']}</div>
          </div>
        </div>
      </div>
      <div class="testimonial">
        <div class="t-stars">★★★★★</div>
        <p class="t-quote">„Sprawny kontakt, zawsze dostępni gdy potrzebowałem odpowiedzi. Każde pytanie wyjaśnione na bieżąco. Merytoryczna pomoc na każdym etapie."</p>
        <div class="t-author">
          <div class="t-avatar">JN</div>
          <div>
            <div class="t-name">Jacek N.</div>
            <div class="t-meta">Podział majątku · Warszawa</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- FAQ -->
<section class="section faq-section" id="faq">
  <div class="container">
    <div class="faq-layout">
      <div class="faq-sticky">
        <p class="section-label no-line">Najczęstsze pytania</p>
        <h2 class="section-title">Odpowiadamy<br>na <em>Twoje</em><br>pytania</h2>
        <p class="section-desc" style="margin-bottom:2rem">
          Nie znajdziesz tu odpowiedzi? Zadzwoń — oddzwonimy w ciągu 2 godzin w dni robocze.
        </p>
        <a href="tel:+48605089552" class="btn btn-primary">📞 605 089 552</a>
      </div>
      <div class="faq-list">
        <div class="faq-item">
          <button class="faq-btn">
            Który sąd rozpatruje sprawy rozwodowe z {d['name']}?
            <span class="faq-icon">+</span>
          </button>
          <div class="faq-body">
            <p>{court_faq}</p>
          </div>
        </div>
        <div class="faq-item">
          <button class="faq-btn">
            Ile trwa sprawa rozwodowa w Polsce?
            <span class="faq-icon">+</span>
          </button>
          <div class="faq-body">
            <p>Czas zależy od wielu czynników. Rozwód bez orzekania o winie, gdy obie strony się zgadzają i nie ma spornych kwestii dotyczących dzieci, może trwać 3–6 miesięcy. Sprawy sporne z dziećmi i podziałem majątku — często rok lub dłużej. Podczas pierwszej konsultacji ocenimy realny czas dla Twojej sprawy.</p>
          </div>
        </div>
        <div class="faq-item">
          <button class="faq-btn">
            Ile kosztuje pomoc adwokata w sprawie rozwodowej?
            <span class="faq-icon">+</span>
          </button>
          <div class="faq-body">
            <p>Honorarium zależy od stopnia skomplikowania sprawy i ustalane jest indywidualnie. Do kosztów dochodzi opłata sądowa od pozwu (600 zł) i ewentualnie koszty biegłych. Przed podpisaniem umowy przedstawiamy pełne, transparentne wynagrodzenie — bez niespodzianek.</p>
          </div>
        </div>
        <div class="faq-item">
          <button class="faq-btn">
            Czy mogę uzyskać rozwód bez orzekania o winie?
            <span class="faq-icon">+</span>
          </button>
          <div class="faq-body">
            <p>Tak — jeśli obie strony się zgadzają, sąd orzeka rozwód bez ustalania winy. To szybsze i mniej kosztowne rozwiązanie, nierzadko korzystniejsze dla obu stron i dla dzieci. Doradzimy, która opcja jest lepsza w Twoim konkretnym przypadku.</p>
          </div>
        </div>
        <div class="faq-item">
          <button class="faq-btn">
            Co z mieszkaniem i kredytem hipotecznym po rozwodzie?
            <span class="faq-icon">+</span>
          </button>
          <div class="faq-body">
            <p>Podział majątku — w tym nieruchomości i kredytów — może być przeprowadzony w trakcie sprawy lub po jej zakończeniu. Możliwe scenariusze to: sprzedaż i podział ceny, spłata jednego małżonka, lub ustanowienie współwłasności. Omówimy wszystkie opcje i ich skutki prawne oraz finansowe.</p>
          </div>
        </div>
        <div class="faq-item">
          <button class="faq-btn">
            Czy mogę skonsultować się online lub przez telefon?
            <span class="faq-icon">+</span>
          </button>
          <div class="faq-body">
            <p>Tak. Prowadzimy konsultacje przez Teams, Zoom lub telefon dla klientów z całej Polski, w tym z {d['name']} i okolic. Stacjonarnie przyjmujemy przy ul. Ceramicznej 5E/79 oraz ul. Bolkowskiej 2A/28 w Warszawie. Pierwsza konsultacja 30 minut jest zawsze bezpłatna.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- KONTAKT -->
<section class="contact-section" id="kontakt">
  <div class="container">
    <div class="section-header section-center text-center">
      <p class="section-label">Bezpłatna konsultacja</p>
      <h2 class="section-title">Zrób pierwszy krok<br><em>w swoim tempie</em></h2>
      <p class="section-desc">
        Nie musisz wiedzieć wszystkiego od razu. Wystarczy jeden formularz lub telefon.
        Resztą zajmiemy się my.
      </p>
    </div>
    <form id="contact-form" action="https://formspree.io/f/mkokeava" method="POST" class="form-card">
      <input type="hidden" name="_next" value="{d['url']}/dziekujemy.html">
      <input type="hidden" name="_subject" value="Nowe zapytanie z {d['domain']}">
      <input type="text" name="_gotcha" style="display:none">
      <div class="form-card-title">Umów bezpłatną konsultację</div>
      <p class="form-card-sub">Oddzwonimy w ciągu 2 godzin w dni robocze (8:00–18:00).</p>
      <div class="form-row">
        <div class="form-group">
          <label for="imie">Imię *</label>
          <input type="text" id="imie" name="imie" placeholder="Jan" required autocomplete="given-name">
        </div>
        <div class="form-group">
          <label for="tel">Telefon *</label>
          <input type="tel" id="tel" name="telefon" placeholder="+48 605 089 552" required autocomplete="tel">
        </div>
      </div>
      <div class="form-group">
        <label for="email">E-mail</label>
        <input type="email" id="email" name="email" placeholder="jan@example.com" autocomplete="email">
      </div>
      <div class="form-group">
        <label for="temat">Czego dotyczy sprawa? *</label>
        <select id="temat" name="temat" required>
          <option value="" disabled selected>Wybierz temat</option>
          <option>Rozwód bez orzekania o winie</option>
          <option>Rozwód z orzeczeniem o winie</option>
          <option>Podział majątku wspólnego</option>
          <option>Opieka nad dziećmi / alimenty</option>
          <option>Separacja prawna</option>
          <option>Inne</option>
        </select>
      </div>
      <div class="form-group">
        <label for="wiadomosc">Krótki opis sytuacji (opcjonalnie)</label>
        <textarea id="wiadomosc" name="wiadomosc" placeholder="W kilku zdaniach opisz swoją sytuację..."></textarea>
      </div>
      <button type="submit" class="form-submit">Wyślij i umów konsultację →</button>
      <p class="form-notice">
        🔒 Dane są bezpieczne i chronione. Kontaktując się z kancelarią, wyrażasz zgodę
        na przetwarzanie danych osobowych w celu obsługi zapytania.
      </p>
      <div id="form-success" style="display:none; text-align:center; padding:1.5rem 0;">
        <div style="font-size:2rem; margin-bottom:.75rem;">✅</div>
        <div style="font-family:var(--serif);font-size:1.25rem;font-weight:700;color:var(--navy);margin-bottom:.4rem;">Dziękujemy!</div>
        <p style="font-size:.9rem;color:var(--text-muted);font-weight:300;">Oddzwonimy do Ciebie w ciągu 2 godzin w dni robocze.</p>
      </div>
    </form>
    <div style="text-align:center; margin-top:2.5rem; display:flex; gap:2rem; justify-content:center; flex-wrap:wrap;">
      <a href="tel:+48605089552" class="btn btn-white btn-lg">📞 605 089 552</a>
      <a href="mailto:kancelaria@idzik.org.pl" class="btn btn-white btn-lg">✉ kancelaria@idzik.org.pl</a>
    </div>
  </div>
</section>
</main>

<!-- STOPKA -->
<footer>
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">Kancelaria Adwokacka Magdalena Idzik‑Cieśla</div>
        <p class="footer-tagline">
          Dyskretna i skuteczna pomoc prawna w sprawach rodzinnych.
          {d['name']} · Warszawa i Mazowieckie — od ponad 12 lat.
        </p>
        <div class="footer-contact">
          <a href="tel:+48605089552">📞 605 089 552</a>
          <a href="mailto:kancelaria@idzik.org.pl">✉ kancelaria@idzik.org.pl</a>
        </div>
      </div>
      <div class="footer-col">
        <h5>Usługi</h5>
        <ul>
          <li><a href="#pomoc">Rozwód</a></li>
          <li><a href="#pomoc">Podział majątku</a></li>
          <li><a href="#pomoc">Opieka nad dziećmi</a></li>
          <li><a href="#pomoc">Alimenty</a></li>
          <li><a href="#pomoc">Mediacja</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Lokalizacje</h5>
        <ul>
          <li>ul. Ceramiczna 5E/79</li>
          <li>03-126 Warszawa</li>
          <li style="margin-top:.5rem">ul. Bolkowska 2A/28</li>
          <li>01-466 Warszawa</li>
          <li style="margin-top:.5rem"><a href="#">Konsultacje online</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Inne domeny</h5>
        <ul>
{footer}
        </ul>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container" style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:.5rem;">
      <span>© 2025 Kancelaria Adwokacka Magdalena Idzik-Cieśla. Wszelkie prawa zastrzeżone.</span>
      <span>
        <a href="/polityka-prywatnosci.html" style="color:inherit;text-decoration:none;">Polityka prywatności</a>
        &nbsp;·&nbsp;
        <a href="/rodo.html" style="color:inherit;text-decoration:none;">RODO</a>
      </span>
    </div>
  </div>
</footer>

<script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>
<script src="assets/page.js"></script>
<script>
function playVideo() {{
  const video   = document.getElementById('hero-video');
  const overlay = document.getElementById('video-overlay');
  video.play();
  anime({{ targets: overlay, opacity: [1, 0], duration: 400, easing: 'easeOutCubic',
    complete: () => {{ overlay.style.display = 'none'; }} }});
}}
document.addEventListener('DOMContentLoaded', () => {{
  const video   = document.getElementById('hero-video');
  const overlay = document.getElementById('video-overlay');
  if (!video) return;
  video.addEventListener('ended', () => {{
    overlay.style.display = 'flex';
    anime({{ targets: overlay, opacity: [0, 1], duration: 400, easing: 'easeOutCubic' }});
  }});
  const btn = document.getElementById('play-btn');
  if (btn) {{
    btn.addEventListener('mouseover', () => {{ btn.style.transform = 'scale(1.1)'; btn.style.background = 'rgba(255,255,255,.22)'; }});
    btn.addEventListener('mouseout',  () => {{ btn.style.transform = 'scale(1)';   btn.style.background = 'rgba(255,255,255,.12)'; }});
  }}
}});
</script>
</body>
</html>"""


def build_dziekujemy(d):
    return f"""<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dziękujemy | Kancelaria Idzik-Cieśla</title>
  <meta name="robots" content="noindex, nofollow">
  <link rel="canonical" href="{d['url']}/dziekujemy.html">
  <script>
    window.SITE_CONFIG = {{
      district:     "{d['name']}",
      districtKey:  "{d['key']}",
      accentColor:  "{d['accent']}",
      accentLight:  "{d['accent_light']}",
      accentBg:     "{d['accent_bg']}"
    }};
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600;1,700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
<div class="ticker-wrap" aria-label="Obszary działania kancelarii">
  <div class="ticker-track" id="ticker-track"></div>
</div>
<header class="nav">
  <div class="nav-inner">
    <a href="{d['url']}" class="nav-logo" aria-label="Strona główna">
      <span class="nav-logo-name">Kancelaria Adwokacka</span>
      <span class="nav-logo-sub">Magdalena Idzik‑Cieśla</span>
    </a>
  </div>
</header>
<main>
<section class="section" style="min-height:60vh;display:flex;align-items:center;">
  <div class="container">
    <div style="max-width:560px;margin:0 auto;text-align:center;padding:4rem 0;">
      <div style="font-size:3.5rem;margin-bottom:1.5rem;">✅</div>
      <h1 style="font-size:clamp(1.8rem,3vw,2.5rem);margin-bottom:1rem;">Dziękujemy za wiadomość!</h1>
      <p style="color:var(--text-muted);font-size:1.05rem;line-height:1.7;margin-bottom:2rem;">
        Oddzwonimy do Ciebie w ciągu <strong>2 godzin</strong> w dni robocze (8:00–18:00).
        Jeśli wolisz zadzwonić sam — jesteśmy dostępni pod numerem poniżej.
      </p>
      <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;margin-bottom:2.5rem;">
        <a href="tel:+48605089552" class="btn btn-primary btn-lg">📞 605 089 552</a>
        <a href="{d['url']}" class="btn btn-outline btn-lg">← Wróć na stronę</a>
      </div>
      <p style="font-size:.85rem;color:var(--text-muted);">
        Kancelaria Adwokacka Magdalena Idzik-Cieśla &nbsp;·&nbsp; {d['name']}
      </p>
    </div>
  </div>
</section>
</main>
<script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>
<script src="assets/page.js"></script>
</body>
</html>"""


def build_robots(d):
    return f"""User-agent: *
Allow: /
Disallow: /dziekujemy.html

Sitemap: {d['url']}/sitemap.xml
"""


def build_sitemap(d, lastmod="2026-05-05"):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{d['url']}/</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_src = os.path.join(base_dir, "assets")

    for d in DISTRICTS:
        out_dir = os.path.join(base_dir, d["key"])
        os.makedirs(out_dir, exist_ok=True)

        # Kopiuj pliki z assets/ do folderu domeny (nadpisuj, zachowaj PNG dzielnicy)
        assets_dst = os.path.join(out_dir, "assets")
        os.makedirs(assets_dst, exist_ok=True)
        for fname in os.listdir(assets_src):
            src_file = os.path.join(assets_src, fname)
            if os.path.isfile(src_file):
                shutil.copy2(src_file, os.path.join(assets_dst, fname))

        files = {
            "index.html":       build_page(d),
            "dziekujemy.html":  build_dziekujemy(d),
            "robots.txt":       build_robots(d),
            "sitemap.xml":      build_sitemap(d),
        }
        for fname, content in files.items():
            with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
                f.write(content)

        print(f"✓  {d['key']}/  ({d['domain']})")
    print(f"\nWygenerowano {len(DISTRICTS)} domen × 4 pliki + assets/.")


if __name__ == "__main__":
    main()
