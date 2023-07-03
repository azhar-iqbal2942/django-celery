from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

from .serializers import EmailSubscribeSerializer
from .tasks import mail_chimp_subscribe


class SubscribeEmailView(APIView):
    def post(self, request):
        try:
            serializer = EmailSubscribeSerializer(data=request.data)
            if serializer.is_valid():
                task = mail_chimp_subscribe.delay(serializer.data.get("email"))
                return Response(
                    data={"task_id": task.task_id}, status=status.HTTP_201_CREATED
                )
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskStatusView(APIView):
    def get(self, request, task_id: str):
        if not task_id:
            return Response(data={"message": "task_id is required"})

        task = AsyncResult(task_id)
        state = task.state
        if state == "FAILURE":
            error = str(task.result)
            response = {
                "state": state,
                "error": error,
            }
        else:
            response = {
                "state": state,
            }

        return Response(data=response)
