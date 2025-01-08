from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    """Форма регистрации."""
    phone_number = forms.CharField(max_length=15, required=False, label="Номер телефона")
    nickname = forms.CharField(max_length=100, required=True, label="Никнейм")

    class Meta:
        model = User
        fields = ["email", "nickname", "phone_number", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите адрес электронной почты"}
        )
        self.fields["nickname"].widget.attrs.update({"class": "form-control", "placeholder": "Введите никнейм"})
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите номер телефона"}
        )
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})

    def clean_email_address(self):
        email_address = self.cleaned_data.get("email")
        if User.objects.filter(email=email_address).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Этот адрес электронной почты уже зарегистрирован!")
        return email_address


class UserForm(forms.ModelForm):
    """Форма обновления данных."""
    nickname = forms.CharField(max_length=100, required=True, label="Никнейм")

    class Meta:
        model = User
        fields = ("nickname", "first_name", "last_name", "phone_number", "avatar", "country")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["nickname"].widget.attrs.update({"class": "form-control", "placeholder": "Введите никнейм"})
        self.fields["first_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите имя"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите фамилию"})
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите номер телефона"}
        )
        self.fields["avatar"].widget.attrs.update({"class": "form-control", "placeholder": "Загрузите фотографию"})
        self.fields["country"].widget.attrs.update({"class": "form-control", "placeholder": "Введите страну проживания"})

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры.")
        return phone_number

    def clean_email_address(self):
        email_address = self.cleaned_data.get("email")
        if User.objects.filter(email=email_address).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Этот адрес электронной почты уже зарегистрирован!")
        return email_address


class UserForgotPasswordForm(PasswordResetForm):
    """Запрос на восстановление пароля."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class UserSetNewPasswordForm(SetPasswordForm):
    """Изменение пароля после подтверждения."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})
