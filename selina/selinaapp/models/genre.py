from selina.models.timestamp import TimeStampModel
from django.db import models

class Genre(TimeStampModel):
    class Meta:
        db_table = 'genre'
        app_label = "selinaapp"
        
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    desc = models.TextField(max_length=1000, null=False, blank=True, default="")
    is_deleted = models.BooleanField(null=True, blank=True, default=False)