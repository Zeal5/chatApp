from django.urls import path
from .views import ChatHistoryAPIView, CustomObtainAuthToken, ChatHistoryByUserAPIView


urlpatterns = [
    path("chat_history/", ChatHistoryAPIView.as_view(), name="chat_history"),
    path(
        "chat_history/<str:username>",
        ChatHistoryByUserAPIView.as_view(),
        name="chat_history_by_user",
    ),
    path("token_auth/", CustomObtainAuthToken.as_view(), name="api_token_auth"),
]
