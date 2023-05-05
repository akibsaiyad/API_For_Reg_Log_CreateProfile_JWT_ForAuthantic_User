from .models import Profile,Blog
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','first_name', 'last_name')
        extra_kwargs = {
            'password':{'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],    
        password = validated_data['password'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'])
        return user
        


class ProfileSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user', 'role')



class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        if profile_data is not None:
            instance.profile.address = profile_data['user']
            instance.profile.save()
        return super().update(instance, validated_data)

    

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


   
    

class BlogSummarySerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'

    def get_content(self, obj):
        if self.context['request'].user.is_authenticated:
            return obj.content
        else:

            if obj.content:
                return obj.content[:5]
                
            else:
                return ''
