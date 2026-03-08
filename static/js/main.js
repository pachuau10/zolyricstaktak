// ZoLyrics — Main JavaScript

// ── THEME ──
const themeToggle = document.getElementById('themeToggle');
const savedTheme = localStorage.getItem('zolyrics-theme') || 'dark';
document.documentElement.setAttribute('data-theme', savedTheme);
if (themeToggle) {
  themeToggle.querySelector('.theme-icon').textContent = savedTheme === 'light' ? '🌙' : '☀️';
  themeToggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('zolyrics-theme', next);
    themeToggle.querySelector('.theme-icon').textContent = next === 'light' ? '🌙' : '☀️';
  });
}

// ── MOBILE MENU ──
const mobileBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.getElementById('mobileMenu');
if (mobileBtn && mobileMenu) {
  mobileBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
  });
}

// ── SEARCH AUTOCOMPLETE ──
const searchInput = document.getElementById('globalSearch');
const suggestionsBox = document.getElementById('searchSuggestions');
let searchTimeout;

if (searchInput && suggestionsBox) {
  searchInput.addEventListener('input', () => {
    clearTimeout(searchTimeout);
    const q = searchInput.value.trim();
    if (q.length < 2) {
      suggestionsBox.classList.remove('active');
      suggestionsBox.innerHTML = '';
      return;
    }
    searchTimeout = setTimeout(() => fetchSuggestions(q), 250);
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-search')) {
      suggestionsBox.classList.remove('active');
    }
  });
}

async function fetchSuggestions(q) {
  try {
    const res = await fetch(`/search/suggest/?q=${encodeURIComponent(q)}`);
    const data = await res.json();
    renderSuggestions(data.results);
  } catch (e) {}
}

function renderSuggestions(results) {
  if (!results.length) {
    suggestionsBox.classList.remove('active');
    return;
  }
  suggestionsBox.innerHTML = results.map(r => `
    <a href="${r.url}" class="suggestion-item">
      <span class="suggestion-icon">${r.icon}</span>
      <div>
        <div class="suggestion-title">${r.title}</div>
        <div class="suggestion-sub">${r.subtitle}</div>
      </div>
    </a>
  `).join('');
  suggestionsBox.classList.add('active');
}

// ── NEWSLETTER ──
const newsletterForm = document.getElementById('newsletterForm');
const newsletterMsg = document.getElementById('newsletterMsg');
if (newsletterForm) {
  newsletterForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = newsletterForm.querySelector('input[name="email"]').value;
    const csrf = newsletterForm.querySelector('[name="csrfmiddlewaretoken"]').value;
    try {
      const res = await fetch('/newsletter/subscribe/', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded', 'X-CSRFToken': csrf},
        body: `email=${encodeURIComponent(email)}`
      });
      const data = await res.json();
      if (newsletterMsg) {
        newsletterMsg.textContent = data.message || 'Subscribed! 🎉';
        newsletterMsg.style.color = data.success ? '#39d98a' : '#ff4d6d';
      }
      if (data.success) newsletterForm.reset();
    } catch (e) {}
  });
}

// ── STICKY HEADER SCROLL ──
let lastScroll = 0;
const header = document.getElementById('siteHeader');
window.addEventListener('scroll', () => {
  const scroll = window.scrollY;
  if (scroll > 100) {
    header?.classList.add('scrolled');
  } else {
    header?.classList.remove('scrolled');
  }
  lastScroll = scroll;
}, { passive: true });

// ── SMOOTH REVEAL ANIMATIONS ──
const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -40px 0px' };
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
      revealObserver.unobserve(entry.target);
    }
  });
}, observerOptions);

document.querySelectorAll('.song-card, .artist-card, .result-item, .trending-item, .latest-item').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(16px)';
  el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
  revealObserver.observe(el);
});

// ── LYRICS SCROLL PROGRESS ──
const lyricsContent = document.getElementById('lyricsContent');
if (lyricsContent) {
  // Add subtle line highlight on scroll
  let readProgress = 0;
  window.addEventListener('scroll', () => {
    const rect = lyricsContent.getBoundingClientRect();
    const total = lyricsContent.offsetHeight;
    const visible = window.innerHeight - rect.top;
    readProgress = Math.min(100, Math.max(0, (visible / total) * 100));
  }, { passive: true });
}

// Smooth CSS variables light/dark transition
document.addEventListener('DOMContentLoaded', () => {
  document.body.style.transition = 'background 0.3s, color 0.3s';
});
