from selina.models.timestamp import TimeStampModel
from django.db import models
from selinaapp.models.user import User
from selinaapp.models.genre import Genre

class Book(TimeStampModel):
    class Meta:
        db_table = 'book'
        app_label = "selinaapp"
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="seller")
    desc = models.TextField(max_length=1000, null=False, blank=True, default="")
    price = models.IntegerField()
    status = models.CharField(max_length=255, null=True, default=None)
    genre = models.ManyToManyField(Genre, blank=True, null=True, through='BookGenre')
    quantity = models.IntegerField()