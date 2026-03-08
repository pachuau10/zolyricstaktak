from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, F
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views import View
from .models import Song, Artist, Genre, UserSubmission, NewsletterSubscriber
import json


def home(request):
    featured_songs = Song.objects.filter(featured=True, published=True).select_related('artist')[:6]
    trending_songs = Song.objects.filter(trending=True, published=True).order_by('-views').select_related('artist')[:10]
    latest_songs = Song.objects.filter(published=True).order_by('-created_at').select_related('artist')[:12]
    top_artists = Artist.objects.order_by('name')[:8]
    genres = Genre.objects.filter(show_in_footer=True)
    
    context = {
        'featured_songs': featured_songs,
        'trending_songs': trending_songs,
        'latest_songs': latest_songs,
        'top_artists': top_artists,
        'genres': genres,
        'page_title': 'ZoLyrics — Song Lyrics, Translations & More',
    }
    return render(request, 'lyrics/home.html', context)


def song_detail(request, artist_slug, slug):
    song = get_object_or_404(Song, slug=slug, artist__slug=artist_slug, published=True)
    song.increment_views()
    
    related_songs = Song.objects.filter(
        artist=song.artist, published=True
    ).exclude(pk=song.pk).order_by('-views')[:6]
    
    same_genre_songs = Song.objects.filter(
        genre=song.genre, published=True
    ).exclude(pk=song.pk).select_related('artist').order_by('-views')[:6]
    
    context = {
        'song': song,
        'related_songs': related_songs,
        'same_genre_songs': same_genre_songs,
        'page_title': f"{song.title} Lyrics — {song.artist.name} | ZoLyrics",
        'meta_description': f"{song.title} lyrics by {song.artist.name}. Read the full {song.title} lyrics on ZoLyrics.",
        'og_title': f"{song.title} Lyrics by {song.artist.name}",
    }
    return render(request, 'lyrics/song_detail.html', context)


def artist_detail(request, slug):
    artist = get_object_or_404(Artist, slug=slug)
    songs = Song.objects.filter(artist=artist, published=True).order_by('-views')
    paginator = Paginator(songs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'artist': artist,
        'page_obj': page_obj,
        'page_title': f"{artist.name} Lyrics | ZoLyrics",
        'meta_description': f"Find all {artist.name} song lyrics on ZoLyrics. {artist.song_count} songs available.",
    }
    return render(request, 'lyrics/artist_detail.html', context)




def genre_detail(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    songs = Song.objects.filter(genre=genre, published=True).select_related('artist').order_by('-views')
    artists = Artist.objects.filter(songs__genre=genre).distinct().order_by('name')[:12]
    
    paginator = Paginator(songs, 24)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'genre': genre,
        'page_obj': page_obj,
        'artists': artists,
        'page_title': f"{genre.name} Lyrics | ZoLyrics",
    }
    return render(request, 'lyrics/genre_detail.html', context)


def search(request):
    query = request.GET.get('q', '').strip()
    filter_type = request.GET.get('type', 'all')
    songs = []
    artists = []
    albums = []
    if query:
        if filter_type in ('all', 'songs'):
            songs = Song.objects.filter(
                Q(title__icontains=query) | Q(lyrics__icontains=query) | Q(artist__name__icontains=query),
                published=True
            ).select_related('artist').order_by('-views')[:30]
        
        if filter_type in ('all', 'artists'):
            artists = Artist.objects.filter(
                Q(name__icontains=query) | Q(bio__icontains=query)
            ).order_by('name')[:12]
        

    
    context = {
        'query': query,
        'songs': songs,
        'artists': artists,
        'albums': albums,
        'filter_type': filter_type,
        'total_results': len(songs) + len(artists),
        'page_title': f'Search: {query} | ZoLyrics' if query else 'Search Lyrics | ZoLyrics',
    }
    return render(request, 'lyrics/search.html', context)


@require_GET
def search_suggest(request):
    """AJAX autocomplete endpoint."""
    query = request.GET.get('q', '').strip()
    results = []
    if len(query) >= 2:
        songs = Song.objects.filter(
            Q(title__icontains=query) | Q(artist__name__icontains=query),
            published=True
        ).select_related('artist').order_by('-views')[:5]
        
        artists = Artist.objects.filter(name__icontains=query).order_by('name')[:3]
        
        for s in songs:
            results.append({
                'type': 'song',
                'title': s.title,
                'subtitle': s.artist.name,
                'url': s.get_absolute_url(),
                'icon': '🎵'
            })
        for a in artists:
            results.append({
                'type': 'artist',
                'title': a.name,
                'subtitle': f"{a.song_count} songs",
                'url': a.get_absolute_url(),
                'icon': '🎤'
            })
    return JsonResponse({'results': results})


def artists_list(request):
    letter = request.GET.get('letter', '')
    artists = Artist.objects.all().order_by('name')
    if letter:
        artists = artists.filter(name__istartswith=letter)
    
    paginator = Paginator(artists, 30)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    context = {
        'page_obj': page_obj,
        'alphabet': alphabet,
        'current_letter': letter,
        'page_title': 'All Artists | ZoLyrics',
    }
    return render(request, 'lyrics/artists_list.html', context)


def submit_lyrics(request):
    if request.method == 'POST':
        artist_name = request.POST.get('artist_name', '').strip()
        song_title = request.POST.get('song_title', '').strip()
        lyrics = request.POST.get('lyrics', '').strip()
        youtube_id = request.POST.get('youtube_id', '').strip()
        email = request.POST.get('email', '').strip()
        
        if artist_name and song_title and lyrics:
            UserSubmission.objects.create(
                artist_name=artist_name,
                song_title=song_title,
                lyrics=lyrics,
                youtube_id=youtube_id,
                submitted_by=email,
            )
            messages.success(request, '🎉 Thanks! Your submission is under review and will be live soon.')
            return redirect('submit_lyrics')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    context = {'page_title': 'Submit Lyrics | ZoLyrics'}
    return render(request, 'lyrics/submit_lyrics.html', context)


def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            _, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                return JsonResponse({'success': True, 'message': 'Subscribed! 🎉'})
            return JsonResponse({'success': True, 'message': 'Already subscribed!'})
    return JsonResponse({'success': False})


def about(request):
    return render(request, 'lyrics/about.html', {'page_title': 'About ZoLyrics'})


def privacy_policy(request):
    return render(request, 'lyrics/privacy.html', {'page_title': 'Privacy Policy | ZoLyrics'})


def terms(request):
    return render(request, 'lyrics/terms.html', {'page_title': 'Terms of Service | ZoLyrics'})


def trending(request):
    songs = Song.objects.filter(published=True).order_by('-views').select_related('artist')
    paginator = Paginator(songs, 30)
    page_obj = paginator.get_page(request.GET.get('page'))
    context = {
        'page_obj': page_obj,
        'page_title': 'Trending Lyrics | ZoLyrics',
    }
    return render(request, 'lyrics/trending.html', context)