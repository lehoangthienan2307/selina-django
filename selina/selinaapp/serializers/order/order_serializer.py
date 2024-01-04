from rest_framework import serializers
from selinaapp.models.order import Order
from selinaapp.models.cart_group import CartGroup
from selinaapp.models.cart import Cart

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        excludes = kwargs.pop('excludes', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if excludes is not None:
            for field_name in excludes:
                self.fields.pop(field_name)
    
    def validate(self, attrs):
        buyer = self.context['request'].user
        cart_group = attrs.get('cart_group')
        if cart_group is None:
            cart_group = self.instance.cart_group
        if cart_group.buyer != buyer:
            raise serializers.ValidationError({"Cart group không hợp lệ"})
        return super().validate(attrs)
    
    def create(self, validated_data):
        # Check quantity
        cart_group = validated_data.get('cart_group')
        #cart_items = cart_group.cart.all() 
        #check not deleted
        cart_items = Cart.objects.filter(cart_group=cart_group, is_deleted=False)
        total_price = 0
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.book.quantity:
                raise serializers.ValidationError({"Số lượng sách " + cart_item.book_id.name + " không đủ"})
            total_price += cart_item.book.price * cart_item.quantity
        #total_price = sum(cart_item.book.price * cart_item.quantity for cart_item in cart_items)
        validated_data['total_price'] = total_price

        cart_group.is_deleted = True
        cart_group.save()
        #decrease quantity of books
        return super().create(validated_data)
    
    
    