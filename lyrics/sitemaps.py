from django.contrib.sitemaps import Sitemap
from .models import Song, Artist


class LyricsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Song.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_at


class ArtistSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Artist.objects.all()
