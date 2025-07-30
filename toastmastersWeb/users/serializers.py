from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError

User = get_user_model() # 獲取當前使用的 User Model

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password_confirm = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password', 'password_confirm')
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'password_confirm': {'write_only': True},
#         }

#     def validate(self, data):
#         # 驗證密碼是否一致
#         if data['password'] != data['password_confirm']:
#             raise ValidationError({"password_confirm": "密碼不匹配。"})
#         return data

#     def create(self, validated_data):
#         # 移除 password_confirm 字段，因為 User Model 中沒有這個字段
#         validated_data.pop('password_confirm')
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password']
#         )
#         return user

# class UserProfileSerializer(serializers.ModelSerializer):
#     # 這是一個簡單的用戶資料序列化器，用於 GET /users/me/
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'display_name', 'profile_picture_url', 'date_joined')
#         read_only_fields = ('username', 'email', 'date_joined') # 這些字段通常不允許用戶自行修改