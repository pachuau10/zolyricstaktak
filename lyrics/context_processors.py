from django.conf import settings
from .models import Genre


def site_context(request):
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'ZoLyrics'),
        'SITE_TAGLINE': getattr(settings, 'SITE_TAGLINE', 'Your #1 Source for Song Lyrics'),
        'ADSENSE_PUBLISHER_ID': getattr(settings, 'ADSENSE_PUBLISHER_ID', ''),
        'ADSENSE_ENABLED': getattr(settings, 'ADSENSE_ENABLED', False),
        'OG_IMAGE_URL': getattr(settings, 'OG_IMAGE_URL', ''),
        'footer_genres': Genre.objects.filter(show_in_footer=True),
    }