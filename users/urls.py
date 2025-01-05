from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (UserRegisterView, UserListView, UserDetailsView, UserUpdateView, BlockUserView,
                         email_verification, UserForgotPasswordView, UserPasswordResetConfirmView, UserInfoView)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="mailing:home"), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("email_confirm/<str:token>/", email_verification, name="email_verification"),
    path("password-reset/", UserForgotPasswordView.as_view(), name="password_reset"),
    path("set-new-password/<uidb64>/<token>/", UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("user_list/", UserListView.as_view(), name="user_list"),
    path("user/<int:pk>/", UserDetailsView.as_view(), name="user_detail"),
    path("user/<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
    path("user/<int:pk>/block", BlockUserView.as_view(), name="user_block"),
    path("user_info/", UserInfoView.as_view(), name="user_info"),
]
