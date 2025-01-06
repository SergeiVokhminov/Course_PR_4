from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page

from users.apps import UsersConfig
from users.views import (UserRegisterView,  UserInfoView, UserListView, UserDetailsView, UserUpdateView, BlockUserView,
                         UnblockUserView, email_verification, UserForgotPasswordView, UserPasswordResetConfirmView)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="mailing:home"), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("user_info/", UserInfoView.as_view(), name="user_info"),
    path("user_list/", cache_page(60)(UserListView.as_view()), name="user_list"),
    path("user/<int:pk>/", UserDetailsView.as_view(), name="user_detail"),
    path("user/update/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
    path("user/block/<int:pk>/", BlockUserView.as_view(), name="user_block"),
    path("user/unblock/<int:pk>/", UnblockUserView.as_view(), name="user_unblock"),
    path("email_confirm/<str:token>/", email_verification, name="email_verification"),
    path("password_reset/", UserForgotPasswordView.as_view(), name="password_reset"),
    path("set_new_password/<uidb64>/<token>/", UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
