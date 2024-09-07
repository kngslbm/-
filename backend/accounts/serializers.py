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
    
    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        # Exclude password fields on PUT requests
        if self.context['request'].method == 'PUT':
            self.fields.pop('password1', None)
            self.fields.pop('password2', None)
        
    def validate(self, data):
        if self.context['request'].method == 'POST':
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
    
    def update(self, instance, validated_data):
        profile_image = validated_data.pop('profile_image', None)
        if profile_image:
            instance.profile_image = profile_image

        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.intro = validated_data.get("intro", instance.intro)
        
        instance.save()
        return instance