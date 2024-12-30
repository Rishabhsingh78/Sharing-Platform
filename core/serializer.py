from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from django.utils.translation import gettext_lazy as _

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']
        extra_kwargs = {'password':{'write_only' : True}}

    def create(self,validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            password=validated_data['password'],
            email = validated_data['email']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if not username and password:
            raise serializers.ValidationError("Both Username and Password are required")
        
        user = authenticate(username = username,password= password)
        if not user:
            raise serializers.ValidationError("Username and password is Invalid")
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return {
            'user' : user,
            'token' : tokens
        }


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'body', 'author', 'created_at']  # Specify required fields

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)  # Nested answers
    tags = TagListSerializerField()

    class Meta:
        model = Question
        fields = ['id', 'title', 'body', 'tags', 'author', 'created_at', 'updated_at', 'answers']
        read_only_fields = ['author', 'answers']  # Author and answers are read-only

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = '__all__'
        