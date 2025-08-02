# # custom_auth/serializers.py
# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import UserProfile

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'email']

# class UserProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
    
#     class Meta:
#         model = UserProfile
#         fields = ['user', 'role', 'phone', 'department', 'created_at']

# class RegisterSerializer(serializers.ModelSerializer):
#     password_confirm = serializers.CharField(write_only=True)
#     role = serializers.CharField(write_only=True, required=False)
#     phone = serializers.CharField(write_only=True, required=False)
#     department = serializers.CharField(write_only=True, required=False)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'role', 'phone', 'department']
#         extra_kwargs = {'password': {'write_only': True}}

#     def validate(self, data):
#         if data['password'] != data['password_confirm']:
#             raise serializers.ValidationError({"password": "Passwords do not match."})
#         return data

#     def create(self, validated_data):
#         validated_data.pop('password_confirm')
#         role = validated_data.pop('role', 'end_user')
#         phone = validated_data.pop('phone', None)
#         department = validated_data.pop('department', None)
        
#         user = User.objects.create_user(**validated_data)
#         UserProfile.objects.create(user=user, role=role, phone=phone, department=department)
#         return user

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'role', 'phone', 'department', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=False)
    department = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'role', 'phone', 'department']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        role = validated_data.pop('role', 'end_user')
        phone = validated_data.pop('phone', None)
        department = validated_data.pop('department', None)
        
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, role=role, phone=phone, department=department)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data['user'] = user
                return data
        raise serializers.ValidationError('Invalid credentials')

    def get_user(self, obj):
        user_obj = obj['user']
        profile = UserProfile.objects.get(user=user_obj)
        serializer = UserProfileSerializer(profile)
        return serializer.data