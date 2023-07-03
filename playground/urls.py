from django.urls import path
from .views import SubscribeEmailView, TaskStatusView

urlpatterns = [
    path("subscribe", SubscribeEmailView.as_view()),
    path("task_status/<str:task_id>", TaskStatusView.as_view()),
]
