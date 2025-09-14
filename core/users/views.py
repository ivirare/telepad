from rest_framework.response import Response
from .serializers import TelegramAuthSerializer
from django.contrib.auth import login, logout
from rest_framework import permissions, status, views, generics


class LoginAPIView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TelegramAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        created = serializer.validated_data["created"]

        login(request, user, backend="users.backends.TelegramAuthBackend")

        if created:
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_200_OK

        return Response(serializer.data, status=status_code)


class LogoutAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )
