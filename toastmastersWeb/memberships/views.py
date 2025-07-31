from django.shortcuts import render
from .models import Memberships
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import MembershipsSerializer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes

@extend_schema(
    request=MembershipsSerializer,
    responses={
        200: MembershipsSerializer(many=True),
        404: OpenApiResponse(description="找不到分會會員資料")
    },
    tags=["Memberships"],
    summary="處理特定 membership 的 CRUD 操作",
    description="根據 membership ID 查詢、更新或刪除特定 membership"
)
class MembershipsDetailView(APIView):
    def get(self, request, pk):
        membership = get_object_or_404(Memberships, pk=pk)
        serializer = MembershipsSerializer(membership)
        return Response(serializer.data)
    
    def put(self, request, pk):
        membership = get_object_or_404(Memberships, pk=pk)
        serializer = MembershipsSerializer(membership, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        membership = get_object_or_404(Memberships, pk=pk)
        membership.delete()
        return Response(status=204)


@extend_schema(
    request=MembershipsSerializer,
    responses={
        200: MembershipsSerializer(many=True),
        404: OpenApiResponse(description="找不到用戶的 memberships")
    },
    tags=["Memberships"],
    summary="只處理查詢某用戶的所有 memberships",
    description="根據用戶 ID 查詢所有該用戶的 memberships"
)
class MembershipsUserView(APIView):    
    def get(self, request, user_id):
        memberships = Memberships.objects.filter(user_id=user_id)
        serializer = MembershipsSerializer(memberships, many=True)
        return Response(serializer.data)


@extend_schema(
    request=MembershipsSerializer,
    responses={
        200: MembershipsSerializer(many=True),
        400: OpenApiResponse(description="輸入資料錯誤")
    },
    tags=["Memberships"],
    summary="列出或創建 memberships",
    description="列出所有 memberships 或創建新的 membership"
)
class MembershipsListCreateView(APIView):    
    def get(self, request):
        memberships = Memberships.objects.all()
        serializer = MembershipsSerializer(memberships, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MembershipsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@extend_schema(
    request=MembershipsSerializer,
    responses={
        200: MembershipsSerializer(many=True),
        404: OpenApiResponse(description="找不到分會會員資料")
    },
    tags=["Memberships"],
    summary="取得某個分會的所有會員資料",
    description="根據分會名稱查詢所有會員的資料"
)
class MembershipsClubView(APIView):
    # permission_classes = [AllowAny]

    def get(self, request, name):
        membership = Memberships.objects.filter(club__name=name)
        if not membership.exists():
            return Response({'error': '找不到該分會的會員資料'}, status=404)
        serializer = MembershipsSerializer(membership, many=True)
        return Response(serializer.data)