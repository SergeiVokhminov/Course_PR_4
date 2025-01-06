from django.db import models

from users.models import User


class Recipient(models.Model):
    """Модель получателя рассылки."""
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    first_name = models.CharField(max_length=250, verbose_name="Имя получателя")
    last_name = models.CharField(max_length=250, verbose_name="Фамилия получателя")
    patronymic = models.CharField(max_length=250, null=True, blank=True, verbose_name="Отчество получателя")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="recipients", verbose_name="Владелец"
    )

    def __str__(self):
        return f"{self.first_name}.{self.last_name} - {self.email}"

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["email", "first_name", "last_name"]


class Message(models.Model):
    """Модель сообщения."""
    topic = models.CharField(max_length=100, verbose_name="Тема сообщения")
    text = models.TextField(verbose_name="Текст сообщения")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="messages", verbose_name="Владелец"
    )

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["topic"]


class Mailing(models.Model):
    """Модель рассылки."""
    FINISHED = "завершена"
    CREATED = "создана"
    ACTIVE = "запущена"
    STATUS_CHOICES = [(CREATED, "создана"), (ACTIVE, "запущена"), (FINISHED, "завершена")]
    mailing_name = models.CharField(max_length=100, verbose_name="Название рассылки", null=True, blank=True)
    start_sending = models.DateTimeField(verbose_name="Начало рассылки", null=True, blank=True)
    end_sending = models.DateTimeField(verbose_name="Окончание рассылки", null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name="Статус рассылки",
        help_text="Выберите статус рассылки",
        choices=STATUS_CHOICES,
        default="CREATED"
    )
    message = models.ForeignKey(
        Message, on_delete=models.SET_NULL, verbose_name="Сообщение", help_text="Выберите сообщение для рассылки",
        null=True, blank=True
    )
    recipients = models.ManyToManyField(
        Recipient, verbose_name="Получатели", help_text="Выберите получателей для рассылки"
    )
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="mailings", verbose_name="Владелец"
    )

    def __str__(self):
        return f"{self.mailing_name} - {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["status", "message"]
        permissions = [("can_finish_mailing", "can finish mailing")]


class MailingAttempts(models.Model):
    """Модель попыток рассылки."""
    SUCCESS = "успешно"
    FAILURE = "не успешно"
    ATTEMPT_STATUS_CHOICES = [(SUCCESS, "успешно"), (FAILURE, "не успешно")]
    attempt_date = models.DateTimeField(verbose_name="Дата и время попытки", auto_now_add=True)
    attempt_status = models.CharField(
        max_length=100,
        verbose_name="Статус попытки",
        choices=ATTEMPT_STATUS_CHOICES,
        default="SUCCESS"
    )
    mail_server_response = models.TextField(verbose_name="Ответ сервера почты", null=True, blank=True)
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name="Рассылка", null=True, blank=True, related_name="attempts")
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        on_delete=models.CASCADE,
        related_name="mailing_attempts",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.attempt_date} - {self.attempt_status}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ["attempt_date", "attempt_status", "mailing"]
