from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=10, default='🎵')
    show_in_footer = models.BooleanField(default=False, help_text="Show this genre in the footer")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('genre_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Artist(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    bio = models.TextField(blank=True)
    image_url = models.URLField(blank=True, help_text="Paste an image URL")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('artist_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def song_count(self):
        return self.songs.count()


class Song(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    composer = models.CharField(max_length=300, blank=True, help_text="Composer name(s), e.g. 'Phuahtu'")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    lyrics = models.TextField()
    youtube_id = models.CharField(max_length=20, blank=True, help_text="YouTube video ID — the part after ?v= e.g. dQw4w9WgXcQ")
    cover_url = models.URLField(blank=True, help_text="Album/song cover image URL")
    views = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['slug', 'artist']

    def __str__(self):
        return f"{self.artist.name} - {self.title}"

    def get_absolute_url(self):
        return reverse('song_detail', kwargs={'artist_slug': self.artist.slug, 'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def increment_views(self):
        Song.objects.filter(pk=self.pk).update(views=models.F('views') + 1)

    @property
    def youtube_embed_url(self):
        if self.youtube_id:
            return f"https://www.youtube.com/embed/{self.youtube_id}?rel=0&modestbranding=1"
        return None

    @property
    def formatted_lyrics(self):
        import re
        lines = re.sub(r'\[([^\]]+)\]', r'<span class="lyrics-section">\1</span>', self.lyrics)
        return lines


class UserSubmission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    artist_name = models.CharField(max_length=200)
    song_title = models.CharField(max_length=300)
    lyrics = models.TextField()
    youtube_id = models.CharField(max_length=20, blank=True)
    submitted_by = models.EmailField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.artist_name} - {self.song_title}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email