from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ClubSerializer
from .models import Clubs
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiParameter
from datetime import time


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
    # permission_classes = [IsAuthenticated]
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
    # permission_classes = [IsAuthenticated]
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


class ClubSearchView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='weekday',
                type=OpenApiTypes.INT,
                description='星期幾 (0=星期一, 1=星期二, ..., 6=星期日)'
            ),
            OpenApiParameter(
                name='start_time_after',
                type=OpenApiTypes.STR,
                description='開始時間晚於此時間 (格式: HH:MM)'
            ),
            OpenApiParameter(
                name='start_time_before',
                type=OpenApiTypes.STR,
                description='開始時間早於此時間 (格式: HH:MM)'
            ),
            OpenApiParameter(
                name='available_at',
                type=OpenApiTypes.STR,
                description='在此時間點正在開會的分會 (格式: HH:MM)'
            ),
        ],
        responses={200: 'ClubSerializer(many=True)'},
        tags=["Clubs"],
        summary="搜尋分會",
        description="根據開會時間搜尋分會"
    )
    def get(self, request):
        from .models import Clubs
        from .serializers import ClubSerializer  # 你需要創建這個序列化器
        
        queryset = Clubs.objects.all()
        
        # 按星期搜尋
        weekday = request.query_params.get('weekday')
        if weekday is not None:
            try:
                queryset = queryset.filter(meeting_weekday=int(weekday))
            except ValueError:
                return Response({'error': 'weekday 必須是 0-6 的整數'}, status=400)
        
        # 按開始時間範圍搜尋
        start_time_after = request.query_params.get('start_time_after')
        if start_time_after:
            try:
                time_obj = time.fromisoformat(start_time_after)
                queryset = queryset.filter(meeting_start_time__gte=time_obj)
            except ValueError:
                return Response({'error': 'start_time_after 格式錯誤，應為 HH:MM'}, status=400)
        
        start_time_before = request.query_params.get('start_time_before')
        if start_time_before:
            try:
                time_obj = time.fromisoformat(start_time_before)
                queryset = queryset.filter(meeting_start_time__lte=time_obj)
            except ValueError:
                return Response({'error': 'start_time_before 格式錯誤，應為 HH:MM'}, status=400)
        
        # 搜尋特定時間點正在開會的分會
        available_at = request.query_params.get('available_at')
        if available_at:
            try:
                time_obj = time.fromisoformat(available_at)
                queryset = queryset.filter(
                    meeting_start_time__lte=time_obj,
                    meeting_end_time__gte=time_obj
                )
            except ValueError:
                return Response({'error': 'available_at 格式錯誤，應為 HH:MM'}, status=400)
        
        serializer = ClubSerializer(queryset, many=True)
        return Response(serializer.data)