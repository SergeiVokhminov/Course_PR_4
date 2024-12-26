from django.db import models

from users.models import User


class Recipient(models.Model):
    """Модель получателя рассылки."""
    email = models.EmailField(
        unique=True, verbose_name="Электронная почта", help_text="Введите адрес электронной почты получателя"
    )
    first_name = models.CharField(max_length=250, verbose_name="Имя получателя")
    last_name = models.CharField(max_length=250, verbose_name="Фамилия получателя")
    patronymic = models.CharField(max_length=250, null=True, blank=True, verbose_name="Отчество получателя")
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="URL",
        help_text="Уникальное имя формируется из фамилии и имени",
    )
    comment = models.TextField(
        verbose_name="Комментарий", blank=True, null=True, help_text="Введите комментарий"
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="recipient", verbose_name="Владелец"
    )

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["first_name", "last_name", "slug"]


class Message(models.Model):
    """Модель сообщения."""
    subject = models.CharField(max_length=100, verbose_name="Тема сообщения", help_text="Введите тему сообщения")
    text = models.TextField(verbose_name="Текст сообщения", help_text="Введите текст сообщения")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="message", verbose_name="Владелец"
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["subject"]


class Mailing(models.Model):
    """Модель рассылки."""
    FINISHED = "завершена"
    CREATED = "создана"
    ACTIVE = "запущена"
    STATUS_CHOICES = [(CREATED, "создана"), (ACTIVE, "запущена"), (FINISHED, "завершена")]
    start_sending = models.DateTimeField(verbose_name="Начало рассылки", null=True, blank=True)
    end_sending = models.DateTimeField(verbose_name="Окончание рассылки", null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name="Статус рассылки",
        help_text="Выберите статус рассылки",
        choices=STATUS_CHOICES,
        default=CREATED,
    )
    message = models.ForeignKey(
        Message, on_delete=models.SET_NULL, verbose_name="Сообщение", help_text="Выберите сообщение для рассылки",
        null=True, blank=True
    )
    recipients = models.ManyToManyField(
        Recipient, verbose_name="Получатели", help_text="Выберите получателей для рассылки"
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="newsletter", verbose_name="Владелец"
    )

    def __str__(self):
        return f"{self.message.subject} - {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["status", "message"]
        # permissions = [
        #     ("can_finish_mailing", "can finish mailing"),
        # ]


class Mailing_Attempts(models.Model):
    """Модель попыток рассылки."""
    SUCCESS = "успешно"
    FAILURE = "неуспешно"
    ATTEMPT_STATUS_CHOICES = [(SUCCESS, "успешно"), (FAILURE, "неуспешно")]
    attempt_date = models.DateTimeField(
        verbose_name="Дата попытки", help_text="Введите дату и время попытки", auto_now_add=True
    )
    attempt_status = models.CharField(
        max_length=100,
        verbose_name="Статус попытки",
        help_text="Введите статус",
        choices=ATTEMPT_STATUS_CHOICES,
        default=SUCCESS,
    )
    mail_server_response = models.TextField(
        verbose_name="Ответ сервера почты", help_text="Введите ответ сервера почты", null=True, blank=True
    )
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name="Рассылка", help_text="Выберите рассылку для попытки",
        null=True, blank=True,
    )

    def __str__(self):
        return f"{self.mailing.message.subject} - {self.attempt_status} - {self.mail_server_response} - {self.attempt_date}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ["attempt_date", "attempt_status", "mailing"]
