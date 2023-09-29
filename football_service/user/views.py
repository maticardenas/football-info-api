from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import AuthTokenSerializer, UserSerializer


class UserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = get_user_model().objects.create(**serializer.validated_data)
        user.set_password(serializer.validated_data["password"])
        user.save()

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_staff:
            return get_user_model().objects.all()
        else:
            # If the user is not staff, return only the current user
            return get_user_model().objects.filter(id=user.id)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    queryset = get_user_model().objects.all()


class CreateTokenView(ObtainAuthToken):  # ObtainAuthToken is a view that comes with DRF
    serializer_class = AuthTokenSerializer
    renderer_classes = (
        api_settings.DEFAULT_RENDERER_CLASSES
    )  # This is needed to view the endpoint in the browser


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
