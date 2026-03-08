from django.contrib import admin
from django.utils.html import format_html
from .models import Song, Artist, Genre, UserSubmission, NewsletterSubscriber



@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'show_in_footer']
    list_editable = ['show_in_footer']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'song_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    def song_count(self, obj):
        return obj.songs.count()
    song_count.short_description = 'Songs'


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'genre', 'featured', 'trending', 'published', 'youtube_preview']
    list_filter = ['featured', 'trending', 'published', 'genre']
    search_fields = ['title', 'artist__name']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['featured', 'trending', 'published']
    raw_id_fields = ['artist']
    fields = ['title', 'slug', 'artist','composer','genre', 'cover_url', 'youtube_id', 'lyrics', 'featured', 'trending', 'published']

    def youtube_preview(self, obj):
        if obj.youtube_id:
            return format_html('<a href="https://youtube.com/watch?v={}" target="_blank">▶ Watch</a>', obj.youtube_id)
        return '—'
    youtube_preview.short_description = 'YouTube'


@admin.register(UserSubmission)
class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = ['song_title', 'artist_name', 'status', 'created_at']
    list_filter = ['status']
    list_editable = ['status']


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at']


admin.site.site_header = 'ZoLyrics Admin'
admin.site.site_title = 'ZoLyrics'
admin.site.index_title = 'Dashboard'