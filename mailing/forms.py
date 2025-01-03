from django import forms
from django.core.exceptions import ValidationError

from .models import Mailing, Message, Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ("email", "first_name", "last_name", "patronymic", "comment")

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите адрес электронной почты"}
        )
        self.fields["first_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите имя"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите фамилию"})
        self.fields["patronymic"].widget.attrs.update({"class": "form-control", "placeholder": "Введите отчество"})
        self.fields["comment"].widget.attrs.update({"class": "form-control", "placeholder": "Введите комментарий"})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Recipient.objects.filter(email=email).exists():
            raise ValidationError("Такой адрес электронной почты уже существует в БД!")
        return email


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("topic", "text")

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields["topic"].widget.attrs.update({"class": "form-control", "placeholder": "Введите тему сообщения"})
        self.fields["text"].widget.attrs.update({"class": "form-control", "placeholder": "Введите текст сообщения"})


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ("start_sending", "end_sending", "status", "message", "recipients")

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields["start_sending"].widget.attrs.update({"class": "form-control", "type": "datetime-local"})
        self.fields["end_sending"].widget.attrs.update({"class": "form-control", "type": "datetime-local"})
        self.fields["recipients"].widget.attrs.update({"class": "form-control"})
        self.fields["status"].widget.attrs.update({"class": "form-control"})
        self.fields["message"].widget.attrs.update({"class": "form-control"})
