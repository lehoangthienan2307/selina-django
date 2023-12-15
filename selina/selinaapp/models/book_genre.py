from selina.models.timestamp import TimeStampModel
from django.db import models
from selinaapp.models.book import Book
from selinaapp.models.genre import Genre

class BookGenre(TimeStampModel):
    class Meta:
        db_table = 'book_genre'
        app_label = "selinaapp"
        unique_together = (('book_id', 'genre_id'),)
        
    book = models.ForeignKey(Book, on_delete=models.CASCADE, primary_key=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(null=True, blank=True, default=False)