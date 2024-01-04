from rest_framework import serializers
from selinaapp.utils import Util
from selinaapp.serializers.user.user_serializer import UserSerializer
from selinaapp.models.book import Book

class BookSerializer(serializers.ModelSerializer):
    seller_info = UserSerializer(many=False, read_only=True, fields=('id', 'email', 'fullname', 'phone', 'address', 'gender', 'avatar_url', 'user_type'))
    class Meta:
        model = Book
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = str(instance.image)
        return representation
    
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        excludes = kwargs.pop('excludes', None)
        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if excludes is not None:
            for field_name in excludes:
                self.fields.pop(field_name)
    
    def create(self, validated_data):
        # request = self.context.get('request')
        # seller_info = request.user if request and request.user.is_authenticated else None
        # validated_data['seller_info'] = seller_info
        image = validated_data.get('image')
        if image:
            file_path = f'books/{image.name}'
            image_url = Util.upload_image(image, file_path)
            validated_data["image"] = image_url
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        image = validated_data.get('image')
        if image is not None:
            file_path = f'books/{image.name}'
            image_url = Util.upload_image(image, file_path)
            validated_data["image"] = image_url

        return super().update(instance, validated_data)