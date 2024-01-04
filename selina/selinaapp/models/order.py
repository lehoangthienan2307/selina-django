from selina.models.timestamp import TimeStampModel
from django.db import models
from selinaapp.models.cart_group import CartGroup

class Order(TimeStampModel):
    class Meta:
        db_table = 'order'
        app_label = "selinaapp"

    class Status(models.TextChoices):
        REJECTED = "rejected"
        DELIVERING = "delivering"
        WAITING = "waiting"
        DELIVERED = "delivered"
        CANCELLED = "cancelled"

    id = models.AutoField(primary_key=True)
    cart_group = models.ForeignKey(CartGroup, on_delete=models.CASCADE, related_name='cart_order')
    delivered_to = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    total_price = models.FloatField()
    status = models.CharField(max_length=255, null=False, choices=Status.choices, default=Status.WAITING)
    payment_method = models.CharField(max_length=20, default='direct_payment')
    is_deleted = models.BooleanField(null=True, blank=True, default=False)