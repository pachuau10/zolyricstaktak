from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('search/suggest/', views.search_suggest, name='search_suggest'),
    path('artists/', views.artists_list, name='artists_list'),
    path('artist/<slug:slug>/', views.artist_detail, name='artist_detail'),
    path('lyrics/<slug:artist_slug>/<slug:slug>/', views.song_detail, name='song_detail'),
    path('genre/<slug:slug>/', views.genre_detail, name='genre_detail'),
    path('trending/', views.trending, name='trending'),
    path('submit/', views.submit_lyrics, name='submit_lyrics'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('terms/', views.terms, name='terms'),
]