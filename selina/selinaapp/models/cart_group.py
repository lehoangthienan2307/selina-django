from selina.models.timestamp import TimeStampModel
from django.db import models
from selinaapp.models.user import User

class CartGroup(TimeStampModel):
    class Meta:
        db_table = 'cart_group'
        app_label = "selinaapp"
        
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_buyer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_seller')
    is_deleted = models.BooleanField(null=True, blank=True, default=False)