from django.urls import path

from playground import consumers

urlpatterns = [
    path("ws/task_status/<str:task_id>/", consumers.TaskStatusConsumer.as_asgi()),
]
