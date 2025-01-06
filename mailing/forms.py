from django import forms
from django.core.exceptions import ValidationError

from .models import Mailing, Message, Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ("email", "first_name", "last_name", "comment")

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите адрес электронной почты"}
        )
        self.fields["first_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите имя"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите фамилию"})
        self.fields["comment"].widget.attrs.update({"class": "form-control", "placeholder": "Введите комментарий"})


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
        fields = ("mailing_name", "message", "recipients")

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields["mailing_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите название рассылки"}
        )
        self.fields["message"].widget.attrs.update({"class": "form-control"})
        self.fields["recipients"].widget.attrs.update({"class": "form-control"})
