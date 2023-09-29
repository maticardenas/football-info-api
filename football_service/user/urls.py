from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("", views.UserView.as_view(), name="user"),
    path("<int:pk>/", views.UserDetailView.as_view(), name="user-detail"),
    path("me/", views.ManageUserView.as_view(), name="me"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
]
