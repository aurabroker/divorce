/* ============================================================
   Kancelaria Adwokacka Magdalena Idzik-Cieśla
   page.js — animacje (anime.js), ticker, FAQ, formularz
   ============================================================ */

/* ── KONFIGURACJA DOMENY ──────────────────────────────────────
   Każda strona ustawia window.SITE_CONFIG przed załadowaniem
   tego pliku. Przykład:
   window.SITE_CONFIG = {
     district: "Bielany",
     districtKey: "bielany",
     accentColor: "#4A6FA5",
     accentLight: "#7A9FCC",
     accentBg: "#EEF3FA"
   };
────────────────────────────────────────────────────────────── */

const SITE_CONFIG = window.SITE_CONFIG || {
  district: "Warszawa",
  districtKey: "warszawa",
  accentColor: "#8B5E1A",
  accentLight: "#C49A3C",
  accentBg: "#FDF6E9"
};

/* ── LISTA DZIELNIC / DOMEN ────────────────────────────────── */
const DISTRICTS = [
  { name: "Warszawa",   url: "https://rozwod.waw.pl",          key: "warszawa" },
  { name: "Bemowo",     url: "https://rozwodbemowo.pl",         key: "bemowo" },
  { name: "Bielany",    url: "https://rozwodbielany.pl",        key: "bielany" },
  { name: "Żoliborz",   url: "https://rozwodzoliborz.pl",       key: "zoliborz" },
  { name: "Wola",       url: "https://rozwodwola.pl",           key: "wola" },
  { name: "Ochota",     url: "https://rozwodochota.pl",         key: "ochota" },
  { name: "Mokotów",    url: "https://rozwodmokotow.pl",        key: "mokotow" },
  { name: "Tarchomin",  url: "https://rozwodtarchomin.pl",      key: "tarchomin" },
  { name: "Legionowo",  url: "https://rozwodlegionowo.pl",      key: "legionowo" },
  { name: "Łomianki",   url: "https://rozwodlomianki.pl",       key: "lomianki" },
  { name: "Jabłonna",   url: "https://rozwodjablonna.pl",       key: "jablonna" },
];

/* ── INICJALIZACJA ────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
  applyTheme();
  initTicker();
  initNav();
  initAnimations();
  initFAQ();
  initForm();
  initForm2();
  initScrollHighlight();
});

/* ── TEMAT (KOLORY AKCENTU) ──────────────────────────────── */
function applyTheme() {
  const r = document.documentElement.style;
  r.setProperty("--accent",       SITE_CONFIG.accentColor);
  r.setProperty("--accent-light", SITE_CONFIG.accentLight);
  r.setProperty("--accent-bg",    SITE_CONFIG.accentBg);
}

/* ── TICKER ──────────────────────────────────────────────── */
function initTicker() {
  const wrap = document.getElementById("ticker-track");
  if (!wrap) return;

  // Generuj zawartość tickera (podwójna lista dla płynnej pętli)
  const items = [...DISTRICTS, ...DISTRICTS];
  wrap.innerHTML = items.map(d => `
    <span class="ticker-item${d.key === SITE_CONFIG.districtKey ? " active-district" : ""}">
      <a href="${d.url}">${d.name}</a>
    </span>
  `).join("");

  // Oblicz szerokość jednej kopii
  const singleWidth = DISTRICTS.length * 180;

  anime({
    targets: "#ticker-track",
    translateX: [`0px`, `-${singleWidth}px`],
    duration: DISTRICTS.length * 2200,
    easing: "linear",
    loop: true
  });
}

/* ── NAWIGACJA MOBILNA ───────────────────────────────────── */
function initNav() {
  const hamburger = document.getElementById("hamburger");
  const navDesktop = document.getElementById("nav-desktop");
  if (!hamburger || !navDesktop) return;

  hamburger.addEventListener("click", () => {
    const isOpen = navDesktop.classList.toggle("open");
    hamburger.setAttribute("aria-expanded", isOpen);
    const spans = hamburger.querySelectorAll("span");
    if (isOpen) {
      anime({ targets: spans[0], rotate: 45,  translateY: 6.5, duration: 200, easing: "easeInOutSine" });
      anime({ targets: spans[1], opacity: 0,              duration: 200, easing: "easeInOutSine" });
      anime({ targets: spans[2], rotate: -45, translateY: -6.5, duration: 200, easing: "easeInOutSine" });
    } else {
      anime({ targets: spans[0], rotate: 0, translateY: 0, duration: 200, easing: "easeInOutSine" });
      anime({ targets: spans[1], opacity: 1,               duration: 200, easing: "easeInOutSine" });
      anime({ targets: spans[2], rotate: 0, translateY: 0, duration: 200, easing: "easeInOutSine" });
    }
  });

  // Zamknij menu po kliknięciu linku
  navDesktop.querySelectorAll("a").forEach(a => {
    a.addEventListener("click", () => {
      navDesktop.classList.remove("open");
      anime({ targets: hamburger.querySelectorAll("span")[0], rotate: 0, translateY: 0, duration: 200 });
      anime({ targets: hamburger.querySelectorAll("span")[1], opacity: 1, duration: 200 });
      anime({ targets: hamburger.querySelectorAll("span")[2], rotate: 0, translateY: 0, duration: 200 });
    });
  });
}

/* ── ANIMACJE (anime.js + IntersectionObserver) ───────────── */
function initAnimations() {
  // Hero — sekwencja wejścia
  const heroSequence = [
    { targets: ".hero-eyebrow", translateY: [20, 0], opacity: [0, 1], duration: 600, delay: 100 },
    { targets: ".hero h1",      translateY: [30, 0], opacity: [0, 1], duration: 700, delay: 0 },
    { targets: ".hero-sub",     translateY: [20, 0], opacity: [0, 1], duration: 600, delay: 0 },
    { targets: ".hero-actions", translateY: [15, 0], opacity: [0, 1], duration: 500, delay: 0 },
    { targets: ".hero-trust",   translateY: [10, 0], opacity: [0, 1], duration: 500, delay: 0 },
  ];

  let delay = 0;
  heroSequence.forEach(cfg => {
    const el = document.querySelector(cfg.targets);
    if (!el) return;
    anime({ ...cfg, easing: "easeOutCubic", delay: delay + (cfg.delay || 0) });
    delay += 180;
  });

  // Statystyki — liczniki
  const stats = document.querySelectorAll(".stat-number[data-count]");
  if (stats.length) {
    const statsObs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        const el = e.target;
        const target = parseInt(el.dataset.count, 10);
        const suffix = el.dataset.suffix || "";
        const prefix = el.dataset.prefix || "";
        const counter = { value: 0 };
        anime({
          targets: counter,
          value: target,
          round: 1,
          duration: 1600,
          easing: "easeOutExpo",
          update: function() {
            el.textContent = prefix + Math.round(counter.value) + suffix;
          }
        });
        statsObs.unobserve(el);
      });
    }, { threshold: 0.5 });
    stats.forEach(s => statsObs.observe(s));
  }

  // Pozostałe sekcje — fade-up przy scroll
  const fadeEls = document.querySelectorAll(
    ".service-card, .testimonial, .process-step, .pain-item, .faq-item, .section-header"
  );

  const fadeObs = new IntersectionObserver((entries) => {
    const visible = entries.filter(e => e.isIntersecting).map(e => e.target);
    if (!visible.length) return;

    anime({
      targets: visible,
      translateY: [24, 0],
      opacity: [0, 1],
      duration: 650,
      delay: anime.stagger(80),
      easing: "easeOutCubic"
    });
    visible.forEach(el => fadeObs.unobserve(el));
  }, { threshold: 0.1 });

  fadeEls.forEach(el => {
    el.style.opacity = "0";
    el.style.transform = "translateY(24px)";
    fadeObs.observe(el);
  });
}

/* ── FAQ ACCORDION ───────────────────────────────────────── */
function initFAQ() {
  document.querySelectorAll(".faq-item").forEach(item => {
    const btn  = item.querySelector(".faq-btn");
    const body = item.querySelector(".faq-body");
    if (!btn || !body) return;

    btn.addEventListener("click", () => {
      const isOpen = item.classList.contains("open");

      // Zamknij wszystkie
      document.querySelectorAll(".faq-item.open").forEach(other => {
        const otherBody = other.querySelector(".faq-body");
        other.classList.remove("open");
        anime({
          targets: otherBody,
          maxHeight: 0,
          duration: 280,
          easing: "easeInCubic"
        });
      });

      // Otwórz kliknięty (jeśli nie był otwarty)
      if (!isOpen) {
        item.classList.add("open");
        const contentH = body.scrollHeight;
        anime({
          targets: body,
          maxHeight: [0, contentH + 20],
          duration: 360,
          easing: "easeOutCubic"
        });
      }
    });
  });
}

/* ── FORMULARZ → WEB3FORMS ───────────────────────────────── */
const W3F_ENDPOINT = "https://api.web3forms.com/submit";
const W3F_KEY      = "be1e4321-2444-4205-a5de-2ba21c3d68dc";

function initForm() {
  const form = document.getElementById("contact-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const btn = form.querySelector(".form-submit");
    const originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = "Wysyłanie...";

    const data = new FormData(form);
    data.append("access_key", W3F_KEY);

    try {
      const res  = await fetch(W3F_ENDPOINT, { method: "POST", body: data });
      let json = {};
      try { json = await res.json(); } catch { json = {}; }

      if (res.ok) {
        showFormSuccess(form, btn);
      } else {
        showFormError(btn, originalText, json.message);
      }
    } catch {
      showFormError(btn, originalText);
    }
  });
}

function showFormSuccess(form, btn) {
  const success = document.getElementById("form-success");
  if (success) {
    form.style.display = "none";
    success.style.display = "block";
    anime({
      targets: success,
      opacity: [0, 1],
      translateY: [-10, 0],
      duration: 500,
      easing: "easeOutCubic"
    });
  } else {
    btn.textContent = "✓ Wiadomość wysłana. Oddzwonimy wkrótce!";
    btn.style.background = "#2E6B1F";
  }
}

function showFormError(btn, originalText, message) {
  btn.disabled = false;
  btn.textContent = message ? "Błąd: " + message : "Błąd — spróbuj ponownie";
  btn.style.background = "#A32D2D";
  setTimeout(() => {
    btn.textContent = originalText;
    btn.style.background = "";
  }, 4000);
}

/* ── FORMULARZ DODATKOWY (id="form") ────────────────────── */
function initForm2() {
  const form = document.getElementById("form");
  if (!form) return;
  const submitBtn = form.querySelector('button[type="submit"]');
  if (!submitBtn) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    formData.append("access_key", "c878bdb5-3d83-4f09-b0c3-0c9bd2138663");

    const originalText = submitBtn.textContent;
    submitBtn.textContent = "Sending...";
    submitBtn.disabled = true;

    try {
      const response = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        body: formData
      });

      let data = {};
      try { data = await response.json(); } catch { data = {}; }

      if (response.ok) {
        alert("Success! Your message has been sent.");
        form.reset();
      } else {
        alert("Error: " + (data.message || "Please try again."));
      }
    } catch {
      alert("Something went wrong. Please try again.");
    } finally {
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    }
  });
}

/* ── SCROLL SPY (aktywny link w nav) ────────────────────── */
function initScrollHighlight() {
  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll(".nav-link[href^='#']");
  if (!sections.length || !navLinks.length) return;

  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      const id = e.target.getAttribute("id");
      const link = document.querySelector(`.nav-link[href="#${id}"]`);
      if (link) link.classList.toggle("active-link", e.isIntersecting);
    });
  }, { rootMargin: "-40% 0px -40% 0px" });

  sections.forEach(s => obs.observe(s));
}
