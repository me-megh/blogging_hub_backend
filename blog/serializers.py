# serializers.py

from rest_framework import serializers
from .models import BlogPost
from django.contrib.auth.models import User

from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email']
    
    def validate(self, data):
        # Check if password and confirm_password match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords must match."})
        return data

    def create(self, validated_data):
        # Remove confirm_password from validated_data before saving
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  
class BlogPostSerializer(serializers.ModelSerializer):
    # Ensure that the 'author' field is populated with the username instead of id
    author = serializers.CharField(source='author.username', read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)  # Handling image field

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'description', 'author', 'created_at', 'image']

    def update(self, instance, validated_data):
        # Ensure the logged-in user is the author when updating a post
        user = self.context['request'].user  # Get the authenticated user
        validated_data['author'] = user  # Ensure the logged-in user is the author

        # Update other fields as required
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)

        # Save and return the updated instance
        instance.save()
        return instance
    