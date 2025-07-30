from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView # 登入 View
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken # 登出相關

from .serializers import RegisterSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# class RegisterView(APIView):
#     permission_classes = [permissions.AllowAny] # 註冊允許任何人訪問

#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             # 註冊成功後，可以選擇自動登入並返回 Token
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 "message": "用戶註冊成功",
#                 "user": UserProfileSerializer(user).data,
#                 "access": str(refresh.access_token),
#                 "refresh": str(refresh),
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CustomTokenObtainPairView(TokenObtainPairView):
#     # 如果你想客製化登入響應，可以在這裡擴展
#     pass

# class LogoutView(APIView):
#     permission_classes = [permissions.IsAuthenticated] # 登出需要認證

#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist() # 將 refresh token 加入黑名單，使其失效

#             # 額外：也可以將 Access Token 加入黑名單，但通常 Access Token 壽命短，不需這樣做
#             # if 'HTTP_AUTHORIZATION' in request.META:
#             #     access_token_str = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
#             #     OutstandingToken.objects.filter(token=access_token_str).update(blacklisted_token__is_blacklisted=True)

#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except KeyError:
#             return Response({"detail": "需要提供 refresh token。"}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e: # 處理 token 無效等其他錯誤
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# # 獲取和更新當前用戶資料
# class MeView(APIView):
#     permission_classes = [permissions.IsAuthenticated] # 只有認證用戶才能訪問

#     def get(self, request):
#         serializer = UserProfileSerializer(request.user)
#         return Response(serializer.data)

#     def patch(self, request):
#         # 允許部分更新，比如修改 display_name, profile_picture_url
#         serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)