# 🎵 ZoLyrics — Django Lyrics Website

A full-featured, AdSense-ready lyrics website built with Django. Dark editorial design with gold accents, YouTube integration, smart search with autocomplete, and everything you need to rank on Google and monetize with AdSense.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Create cache table
python manage.py createcachetable

# 4. Create superuser (for admin panel)
python manage.py createsuperuser

# 5. Collect static files
python manage.py collectstatic

# 6. Start the server
python manage.py runserver
```

Visit: http://127.0.0.1:8000  
Admin: http://127.0.0.1:8000/admin

---

## 📦 Project Structure

```
zolyrics/
├── zolyrics/               # Django project settings
│   ├── settings.py         # ← Configure AdSense, YouTube API, etc.
│   ├── urls.py
│   └── wsgi.py
├── lyrics/                 # Main app
│   ├── models.py           # Song, Artist, Album, Genre models
│   ├── views.py            # All page views
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin panel configuration
│   ├── sitemaps.py         # SEO sitemaps
│   ├── context_processors.py
│   └── templates/lyrics/   # All HTML templates
├── templates/
│   └── base.html           # Master layout (header, footer, AdSense)
├── static/
│   ├── css/main.css        # All styles
│   └── js/main.js          # Autocomplete, theme, newsletter
└── requirements.txt
```

---

## ⚙️ Configuration (settings.py)

### Enable Google AdSense
```python
ADSENSE_PUBLISHER_ID = 'ca-pub-XXXXXXXXXXXXXXXX'  # Your AdSense publisher ID
ADSENSE_ENABLED = True  # Enable after AdSense approval
```

AdSense slots are pre-placed in optimal positions:
- Top banner (above fold — highest CPM)
- Below hero section
- Above/below lyrics (most viewed area on the page)
- Sidebar sticky ad
- Artist pages
- Submit page

### YouTube API (for search)
```python
YOUTUBE_API_KEY = 'YOUR_API_KEY'
```
Get a free API key at https://console.cloud.google.com

### For each song, just add the YouTube video ID (e.g. `dQw4w9WgXcQ`) in the admin panel. The video player will appear automatically.

---

## 🎨 Design Features

- **Dark editorial theme** with gold accent color
- **Light mode toggle** (saved to localStorage)
- **Google Fonts**: Syne (headings) + DM Sans (body) + Instrument Serif (accents)
- **Animated song cards** with scroll reveal
- **Mobile-first responsive** design
- **Lyrics font size controls** (A- / A+)
- **Copy lyrics** button
- **Web Share API** for native mobile sharing

---

## 🔍 SEO Features

- **Sitemap.xml** at `/sitemap.xml`
- **Structured data** (JSON-LD MusicComposition schema on every lyrics page)
- **Meta descriptions** auto-generated for every song
- **Canonical URLs** to prevent duplicate content
- **Breadcrumb navigation**
- Optimized `<title>` tags: "Song Title Lyrics — Artist Name | ZoLyrics"

---

## 💡 AdSense Best Practices (Already Implemented)

1. **Above-the-fold ad** — top banner loads first
2. **In-content ads** — above and below the lyrics (most read section)
3. **Sidebar sticky ad** — stays visible as user scrolls lyrics
4. **Privacy Policy page** — required for AdSense approval
5. **Terms of Service** — required for AdSense approval
6. **Original content** — song meanings, trivia, credits per song
7. **Fast loading** — minimal JS, lazy-loaded images

---

## 📊 Admin Panel Features

- Add/edit songs, artists, albums, genres
- Mark songs as **Featured** or **Trending** 
- Manage **User Submissions** (approve/reject)
- Preview YouTube links directly from the song list
- Bulk publish/unpublish songs
- Newsletter subscriber management

---

## 🌐 Production Deployment

### Using Gunicorn + Nginx:
```bash
# Install whitenoise for static files
pip install whitenoise gunicorn

# Add to MIDDLEWARE in settings.py:
# 'whitenoise.middleware.WhiteNoiseMiddleware',

# Start gunicorn
gunicorn zolyrics.wsgi:application --bind 0.0.0.0:8000
```

### Environment Variables (production):
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=zolyrics.com,www.zolyrics.com
DATABASE_URL=postgres://...
```

---

## 📋 Adding Content

### Via Admin Panel (easiest):
1. Go to `/admin/`
2. Add Genres first (Pop, Hip-Hop, R&B, Rock, etc.)
3. Add Artists (with image URL from Wikipedia/artist website)
4. Add Albums
5. Add Songs — paste lyrics with `[Verse 1]` / `[Chorus]` formatting
6. Add YouTube video ID in the "youtube_id" field

### Lyrics Format:
```
[Verse 1]
First line of verse
Second line of verse

[Pre-Chorus]
Pre-chorus line

[Chorus]
Chorus first line
Chorus second line

[Bridge]
Bridge lyrics here
```

---

## 🔗 URL Structure

```
/                           → Homepage
/search/?q=query            → Search results
/artist/taylor-swift/       → Artist page
/artist/taylor-swift/album/midnights/ → Album page
/lyrics/taylor-swift/anti-hero/  → Song lyrics page
/genre/pop/                 → Genre page
/trending/                  → Most viewed songs
/artists/                   → A-Z artist browser
/submit/                    → Community lyrics submission
/sitemap.xml                → SEO sitemap
/admin/                     → Admin dashboard
```

---

## 📱 Features Summary

| Feature | Status |
|---------|--------|
| Lyrics pages | ✅ |
| YouTube video player | ✅ |
| Search with autocomplete | ✅ |
| Artist profiles | ✅ |
| Album pages | ✅ |
| Genre pages | ✅ |
| Trending songs | ✅ |
| A-Z artist browser | ✅ |
| Community submissions | ✅ |
| Newsletter signup | ✅ |
| Google AdSense (6 placements) | ✅ |
| Dark/light mode | ✅ |
| Mobile responsive | ✅ |
| SEO sitemap | ✅ |
| Structured data (JSON-LD) | ✅ |
| Song meanings & trivia | ✅ |
| Song credits (writers/producers) | ✅ |
| Copy lyrics button | ✅ |
| Share button | ✅ |
| Font size controls | ✅ |
| Admin panel | ✅ |
