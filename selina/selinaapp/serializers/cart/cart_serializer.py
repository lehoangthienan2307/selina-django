from rest_framework import serializers
from selinaapp.models.cart import Cart
from selinaapp.models.book import Book
from selinaapp.models.cart_group import CartGroup

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
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
        quantity = attrs.get("quantity")
        book = attrs.get("book")
        print(book.quantity)
        if quantity <= 0:
            raise serializers.ValidationError({"message":"Số lượng sách không hợp lệ"})
        if quantity > book.quantity:
            raise serializers.ValidationError({"message":"Số lượng sách không đủ"})
        return super().validate(attrs)
    
    def create(self, validated_data):
        book = validated_data.get('book')        
        quantity = validated_data.get('quantity')
        buyer = self.context['request'].user
        seller = book.seller_info

        cart_group = CartGroup.objects.filter(buyer=buyer, seller=seller, is_deleted=False).first()
        if cart_group:
            cart = Cart.objects.filter(cart_group=cart_group, book=book, is_deleted=False).first()
            if cart:
                cart.quantity += quantity
                cart.save()
                return cart
               # it should return object instance in create method
        else:
            cart_group = CartGroup.objects.create(buyer=buyer, seller=seller)

        validated_data['cart_group'] = cart_group
        return super().create(validated_data)
    
        # cart = Cart.objects.filter(cart_group__buyer=buyer, cart_group__seller=seller, book=book, is_deleted=False).first()
        # if cart:
        #     cart.quantity += quantity
        #     cart.save()
        # else:
        #     cart_group = CartGroup.objects.filter(buyer=buyer, seller=seller, is_deleted=False).first()
        #     pass
            
        # cart_group = CartGroup.objects.filter(buyer=buyer, seller=seller, is_deleted=False).first()
        # if not cart_group:
        #     cart_group = CartGroup.objects.create(buyer=buyer, seller=seller)
        # 
        # validated_data['cart_group'] = cart_group

        # return super().create(validated_data)