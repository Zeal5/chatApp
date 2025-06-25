from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics
from chats.models import ChatRoom
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import Http404
from .serializers import ChatRoomSerializer, CustomAuthTokenSerializer

User = get_user_model()

class ChatHistoryAPIView(generics.ListAPIView):
    queryset = ChatRoom.objects.prefetch_related("messages").all()
    permission_classes = [IsAdminUser]
    serializer_class = ChatRoomSerializer


class ChatHistoryByUserAPIView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        other_username = self.kwargs.get("username")

        current_user = self.request.user

        #Check if user exists
        get_object_or_404(User, username=other_username)

        sorted_names = sorted([current_user.username.strip(), other_username.strip()])
        room_name = f"{sorted_names[0]}_{sorted_names[1]}"

        queryset = ChatRoom.objects.filter(name=room_name).prefetch_related("messages")

        if not queryset.exists():
            raise Http404


        return queryset


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
