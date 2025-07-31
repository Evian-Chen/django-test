from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ClubSerializer
from .models import Clubs
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes


# GET /list/
@extend_schema(
    request=ClubSerializer,
    responses={
        200: ClubSerializer(many=True),
        404: OpenApiResponse(description="找不到社團")
    },
    tags=["Clubs"],
    summary="取得所有社團",
    description="取得所有社團的列表"
)
class ClubListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        clubs = Clubs.objects.all()
        serializer = ClubSerializer(clubs, many=True)
        return Response(serializer.data)


# POST /create/
@extend_schema(
    request=ClubSerializer,
    responses={
        201: ClubSerializer,
        400: OpenApiResponse(description="輸入資料錯誤")
    },
    tags=["Clubs"],
    summary="建立新社團",
    description="使用者可以提交社團的詳細資訊來建立新社團"
)
class ClubCreateView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ClubSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


# PUT /update/<int:pk>/
@extend_schema(
    request=ClubSerializer,
    responses={
        200: ClubSerializer,
        400: OpenApiResponse(description="輸入資料錯誤"),
        404: OpenApiResponse(description="找不到社團")
    },
    tags=["Clubs"],
    summary="更新社團資訊",
    description="使用者可以更新指定社團的詳細資訊"
)
class ClubUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, name):
        club = Clubs.objects.get(name=name)
        serializer = ClubSerializer(club, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


# DELETE /delete/<int:pk>/
@extend_schema(
    responses={
        204: None,
        404: OpenApiResponse(description="找不到社團")
    },
    tags=["Clubs"],
    summary="刪除社團",
    description="使用者可以刪除指定的社團"
)
class ClubDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, name):
        club = get_object_or_404(Clubs, name=name)
        club.delete()
        return Response(status=204)


# GET /detail/<str:name>/
@extend_schema(
    responses={
        200: ClubSerializer,
        404: OpenApiResponse(description="找不到社團")
    },
    tags=["Clubs"],
    summary="取得社團詳細資訊",
    description="使用者可以根據社團名稱獲取該社團的詳細資訊"
)
class ClubDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, name):
        club = get_object_or_404(Clubs, name=name)
        serializer = ClubSerializer(club)
        return Response(serializer.data)