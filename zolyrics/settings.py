import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# 1. BASE CONFIG & ENV
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# 2. APPS & MIDDLEWARE
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'lyrics',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 3. DATABASE (NEON DB)
# Neon is serverless; we use conn_max_age & health_checks to keep connections stable.
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# 4. TEMPLATES & URLS
ROOT_URLCONF = 'zolyrics.urls'
WSGI_APPLICATION = 'zolyrics.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'lyrics.context_processors.site_context',
            ],
        },
    },
]

# 5. STATIC & MEDIA (LOCAL)
# Since Cloudinary is gone, we serve these from the local filesystem.
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
# This enables compression and long-term caching for better performance
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 6. CACHE & SECURITY
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'zolyrics_cache_table',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 7. ZOLYRICS CUSTOM SETTINGS
SITE_NAME = 'ZoLyrics'
SITE_TAGLINE = 'Your #1 Source for Song Lyrics'
SITE_URL = 'https://zolyrics.in'
OG_IMAGE_URL = 'https://res.cloudinary.com/dqquazig1/image/upload/v1771701592/chhohhreivung_tmkq5m.jpg'
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
ADSENSE_PUBLISHER_ID = os.getenv('ADSENSE_PUBLISHER_ID')
ADSENSE_ENABLED = not DEBUG