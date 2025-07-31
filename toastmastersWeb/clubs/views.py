from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ClubSerializer
from .models import Clubs
from django.shortcuts import get_object_or_404

# Create your views here.

# GET /list/
class ClubListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        clubs = Clubs.objects.all()
        serializer = ClubSerializer(clubs, many=True)
        return Response(serializer.data)

# POST /create/
class ClubCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ClubSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

# PUT /update/<int:pk>/
class ClubUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        club = Clubs.objects.get(pk=pk)
        serializer = ClubSerializer(club, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

# DELETE /delete/<int:pk>/
class ClubDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        club = get_object_or_404(Clubs, pk=pk)
        club.delete()
        return Response(status=204)

# GET /detail/<str:name>/
class ClubDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, name):
        club = get_object_or_404(Clubs, name=name)
        serializer = ClubSerializer(club)
        return Response(serializer.data)