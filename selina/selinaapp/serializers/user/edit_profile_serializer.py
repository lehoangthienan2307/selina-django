from rest_framework import serializers
from selinaapp.models.user import User
from selinaapp.utils import Util


class EditProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.ImageField(required=False, allow_empty_file=True)
    class Meta:
        model = User
        fields = ['fullname', 'password', 'avatar_url', 'phone', 'gender', 'address']
       
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.avatar_url:
            representation['avatar_url'] = instance.avatar_url

        return representation
    
    def update(self, instance, validated_data):
        avatar = validated_data.get('avatar_url')
        print(avatar)
        #instance.email = validated_data.get('email', instance.email)
        instance.fullname = validated_data.get('fullname')
        instance.phone = validated_data.get('phone')
        instance.address = validated_data.get('address')
        instance.gender = validated_data.get('gender')
        if avatar:
            file_path = f'avatars/{instance.id}_{avatar.name}'
            avatar_url = Util.upload_image(avatar, file_path)
            instance.avatar_url = avatar_url

        
        instance.save()
    
        return instance