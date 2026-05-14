/* Kancelaria Adwokacka — blog.js
   Ładuje artykuły z Supabase per-domena, obsługuje 2-kolumnowy czytnik i deep linking.
   Domena filtrowania czytana z window.SITE_CONFIG.domain (ustawiane w blog.html).
*/

const SB_URL = 'https://kukvgsjrmrqtzhkszzum.supabase.co';
const SB_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt1a3Znc2pybXJxdHpoa3N6enVtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI5MTI0NzYsImV4cCI6MjA4ODQ4ODQ3Nn0.wOB-4CJTcRksSUY7WD7CXEccTKNxPIVF8AT8hczS5zY';

let _sbClient = null;
function getSB() {
  if (!_sbClient) _sbClient = supabase.createClient(SB_URL, SB_KEY);
  return _sbClient;
}

const CARD_EMOJIS = ['⚖️', '👨‍👩‍👧', '🏠', '📋', '🤝', '💼', '⚡', '🛡️'];

/* ── Pobierz listę artykułów ── */
async function loadBlogPosts() {
  const grid   = document.getElementById('blog-grid');
  const domain = window.SITE_CONFIG?.domain || '';

  try {
    const { data, error } = await getSB()
      .from('aura_articles')
      .select('id, title, excerpt, tags, published_at, created_at, cover_image')
      .eq('status', 'published')
      .contains('platforms', [domain])
      .order('published_at', { ascending: false });

    if (error) throw error;

    if (!data || data.length === 0) {
      grid.innerHTML = '<div class="blog-empty">Brak opublikowanych artykułów. Wróć wkrótce.</div>';
      return;
    }

    grid.innerHTML = data.map((art, idx) => {
      const mainTag = art.tags?.length ? art.tags[0] : 'Prawo rodzinne';
      const emoji   = CARD_EMOJIS[idx % CARD_EMOJIS.length];
      const dateStr = new Date(art.published_at || art.created_at)
        .toLocaleDateString('pl-PL', { day: 'numeric', month: 'long', year: 'numeric' });
      const thumb = art.cover_image
        ? `<div class="blog-card-thumb" style="padding:0;">
             <img src="${art.cover_image}" alt="${escHtml(art.title)}" loading="lazy">
           </div>`
        : `<div class="blog-card-thumb">${emoji}</div>`;

      return `
        <article class="blog-card" data-article-id="${art.id}" role="button" tabindex="0"
                 aria-label="Czytaj artykuł: ${escHtml(art.title)}">
          ${thumb}
          <div class="blog-card-body">
            <div class="blog-card-tag">${escHtml(mainTag)}</div>
            <h2 class="blog-card-title">${escHtml(art.title)}</h2>
            <p class="blog-card-excerpt">${escHtml(art.excerpt || 'Kliknij, aby przeczytać…')}</p>
            <div class="blog-card-footer">
              <span class="blog-card-date">${dateStr}</span>
              <span class="blog-card-cta">Czytaj →</span>
            </div>
          </div>
        </article>`;
    }).join('');

  } catch (err) {
    console.error('Błąd ładowania artykułów:', err);
    grid.innerHTML = '<div class="blog-error">Wystąpił błąd podczas ładowania artykułów. Spróbuj ponownie.</div>';
  }
}

/* ── Otwórz czytnik artykułu ── */
async function openArticle(id) {
  const { data, error } = await getSB()
    .from('aura_articles')
    .select('*')
    .eq('id', id)
    .single();

  if (error || !data) {
    alert('Nie udało się pobrać artykułu. Spróbuj ponownie.');
    return;
  }

  const dateStr = new Date(data.published_at || data.created_at)
    .toLocaleDateString('pl-PL', { day: 'numeric', month: 'long', year: 'numeric' });

  document.getElementById('reader-tags').innerHTML = (data.tags || [])
    .map(t => `<span class="reader-tag">${escHtml(t)}</span>`)
    .join('');

  document.getElementById('reader-title').textContent = data.title;
  document.getElementById('reader-date').textContent  = `Opublikowano: ${dateStr}`;
  document.getElementById('reader-content').innerHTML = data.content || '';

  const imgSrc = data.cover_image || data.image_url || data.featured_image || null;
  const imgWrap = document.getElementById('reader-image-wrap');
  if (imgSrc) {
    imgWrap.innerHTML = `<img src="${imgSrc}" alt="${escHtml(data.title)}" loading="lazy">`;
    imgWrap.style.minHeight = '';
    imgWrap.style.justifyContent = '';
  } else {
    imgWrap.innerHTML = CARD_EMOJIS[0];
    imgWrap.style.minHeight = '160px';
    imgWrap.style.justifyContent = 'center';
  }

  document.getElementById('blog-list-view').style.display   = 'none';
  document.getElementById('article-reader-view').style.display = 'block';
  window.scrollTo(0, 0);
  history.pushState(null, '', '#article-' + id);
}

/* ── Zamknij czytnik ── */
function closeArticle() {
  document.getElementById('article-reader-view').style.display = 'none';
  document.getElementById('blog-list-view').style.display      = 'block';
  window.scrollTo(0, 0);
  history.pushState(null, '', window.location.pathname);
}

/* ── Kopiuj link ── */
function copyArticleLink() {
  const url = window.location.href;
  navigator.clipboard?.writeText(url).then(() => {
    showCopyFeedback();
  }).catch(() => {
    prompt('Skopiuj ten link ręcznie:', url);
  });
}

function showCopyFeedback() {
  const btn = document.getElementById('copy-link-btn');
  if (!btn) return;
  const orig = btn.textContent;
  btn.textContent = '✓ Skopiowano!';
  setTimeout(() => { btn.textContent = orig; }, 2000);
}

/* ── Routing przez hash ── */
async function handleRouting() {
  const hash = window.location.hash.replace('#', '');
  if (hash.startsWith('article-')) {
    await openArticle(hash.replace('article-', ''));
  }
}

/* ── Pomocnicza: escape HTML ── */
function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/* ── Event listeners ── */
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('blog-grid')?.addEventListener('click', e => {
    const card = e.target.closest('article[data-article-id]');
    if (card) openArticle(card.dataset.articleId);
  });

  document.getElementById('blog-grid')?.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') {
      const card = e.target.closest('article[data-article-id]');
      if (card) { e.preventDefault(); openArticle(card.dataset.articleId); }
    }
  });

  document.getElementById('close-article-btn')?.addEventListener('click', closeArticle);
  document.getElementById('copy-link-btn')?.addEventListener('click', copyArticleLink);

  window.addEventListener('hashchange', () => {
    const hash = window.location.hash.replace('#', '');
    hash.startsWith('article-') ? openArticle(hash.replace('article-', '')) : closeArticle();
  });

  loadBlogPosts();
  handleRouting();
});
