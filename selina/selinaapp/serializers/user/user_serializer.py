from rest_framework import serializers
from selinaapp.models.user import User
from selinaapp.utils import Util
from urllib.parse import quote, quote_plus
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ['id', 'email', 'fullname']
        fields = '__all__'
        
    # def to_representation(self, instance):
    #     #representation = super(UserSerializer, self).to_representation(instance)
    #     _re = super().to_representation(instance)
    #     # Encode the avatar_url when generating the response
    #     #print(_re['avatar_url'])
    #     print(_re['avatar_url'])
    #     _re['avatar_url'] = quote_plus(_re['avatar_url'])
    #     print(_re['avatar_url'])
    #     # print("checkkkk")
    #     return _re
    
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
    
    # def update(self, instance, validated_data):
    #     avatar = validated_data.get('avatar_url')
    #     #instance.email = validated_data.get('email', instance.email)
    #     instance.fullname = validated_data.get('fullname')
    #     instance.phone = validated_data.get('phone')
    #     instance.address = validated_data.get('address')
    #     instance.gender = validated_data.get('gender')
    #     if avatar:
    #         file_path = f'avatars/{instance.id}_{avatar.name}'
    #         avatar_url = Util.upload_image(avatar, file_path)
    #         print(avatar_url)
    #         instance.avatar_url = avatar_url
        
    #     instance.save()
    
    #     return instance