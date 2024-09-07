from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    intro = serializers.CharField(required=False, allow_blank=True)
    profile_image = serializers.ImageField(required=False, allow_empty_file=True)
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'intro', "profile_image")
        
    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("password1 and password2 aren't matched")
        return data
    
    def create(self, validated_data):
        profile_image = validated_data.pop('profile_image', None)
        user = get_user_model()(
            username=validated_data["username"],
            email=validated_data["email"],
            intro=validated_data.get("intro", None),
        )
        user.set_password(validated_data["password1"])
        
        if profile_image:
            user.profile_image = profile_image
        
        user.save()
        return user