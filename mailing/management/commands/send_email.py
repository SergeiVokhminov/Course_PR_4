from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        topic = input("Введите тему сообщения: ")
        message = input("Введите текст сообщения: ")
        recipient = input("Введите электронную почту получателя: ")
        recipient_list = [recipient]
        email_from = settings.EMAIL_HOST_USER
        try:
            send_mail(topic, message, email_from, recipient_list)
            print("Сообщение успешно отправлено")
        except Exception as f:
            print(f"Ошибка при отправке сообщения: {str(f)}")
