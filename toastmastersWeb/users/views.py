from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes
from django.shortcuts import get_object_or_404

User = get_user_model()  # according to the AUTH_USER_MODEL setting


@extend_schema(
    request=RegisterSerializer,
    responses={
        201: UserSerializer,
        400: OpenApiResponse(description="輸入資料錯誤")
    },
    tags=["Authentication"],
    summary="註冊新使用者",
    description="使用者填寫帳號、密碼、email 與 display_name 來建立新帳號，成功後回傳 JWT token 與使用者資訊"
)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "註冊成功",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "display_name": user.display_name
                },
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=LoginSerializer,
    responses={
        200: OpenApiTypes.OBJECT,
        401: OpenApiResponse(description="帳號或密碼錯誤")
    },
    tags=["Authentication"],
    summary="登入",
    description="輸入帳號與密碼，驗證成功後回傳 access 與 refresh token"
)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"]
            )
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "登入成功",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                })
            return Response({"error": "帳號或密碼錯誤"}, status=401)
        return Response(serializer.errors, status=400)


@extend_schema(
    request=LogoutSerializer,
    responses={204: None},
    tags=["Authentication"],
    summary="登出",
    description="將 refresh token 加入黑名單，使其失效"
)
class LogoutView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = RefreshToken(serializer.validated_data["refresh"])
                token.blacklist()
                return Response({"message": "已成功登出"}, status=204)
            except Exception:
                return Response({"error": "無效的 token"}, status=400)
        return Response(serializer.errors, status=400)


@extend_schema(
    responses={
        200: UserSerializer,
        404: OpenApiResponse(description="找不到使用者")
    },
    tags=["User Profile"],
    summary="取得或更新使用者資料",
    description="使用者可以查看或更新自己的個人資料"
)
class UserProfileView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)