from selina.models.timestamp import TimeStampModel
from django.db import models
from selinaapp.models.cart_group import CartGroup
from selinaapp.models.book import Book

class Cart(TimeStampModel):
    class Meta:
        db_table = 'cart'
        app_label = "selinaapp"
        
    id = models.AutoField(primary_key=True)
    cart_group = models.ForeignKey(CartGroup, on_delete=models.CASCADE, related_name='cart')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=True, default=1)
    is_deleted = models.BooleanField(null=True, blank=True, default=False)