import secrets

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, UpdateView

from users.forms import UserRegisterForm, UserUpdateForm, UserForgotPasswordForm, UserSetNewPasswordForm
from users.models import User


class UserRegisterView(CreateView):
    """Контроллер регистрации профиля."""
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """Верификация зарегистрированного пользователя."""
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email_confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Пожалуйста, перейдите по ссылке {url} для подтверждения почты",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    """Контроллер верификации почты."""
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect("users:login")


class UserDetailsView(DetailView):
    """Контроллер отображения профиля пользователя."""
    model = User
    template_name = "users/user_detail.html"


class UserUpdateView(UpdateView):
    """Контроллер обновления профиля пользователя."""
    model = User
    form_class = UserUpdateForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("mailing:main")


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """Контроллер по сбросу пароля по почте."""
    form_class = UserForgotPasswordForm
    template_name = "user_password_reset.html"
    success_url = reverse_lazy("mailing:main")
    success_message = "Письмо с инструкцией по восстановлению пароля отправлена на ваш email"
    email_template_name = "users/password_reset_mail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Запрос на восстановление пароля"
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """Контроллер установки нового пароля."""

    form_class = UserSetNewPasswordForm
    template_name = "user_password_set_new.html"
    success_url = reverse_lazy("mailing:main")
    success_message = "Пароль успешно изменен. Можете авторизоваться на сайте."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Установить новый пароль"
        return context


class UserListView(LoginRequiredMixin, ListView):
    """Контроллер отображения списка пользователей сервиса."""

    model = User
    template_name = "users_list.html"


class BlockUserView(LoginRequiredMixin, View):
    """Контроллер блокировки пользователей сервиса."""

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if not request.user.has_perm("can_block_user"):
            return HttpResponseForbidden("У вас нет прав на это действие.")

        user.is_active = False
        user.save()
        return redirect("users:users_list")