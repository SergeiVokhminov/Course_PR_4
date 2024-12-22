from django.contrib import admin

from .models import Mailing, Mailing_Attempts, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "comment")
    search_fields = ("email", "last_name")
    list_filter = ("email", "last_name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "text")
    search_fields = ("subject",)
    list_filter = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_sending", "end_sending", "status", "message")
    search_fields = ("status", "message")
    list_filter = ("status", "message")


# Register your models here.
@admin.register(Mailing_Attempts)
class MailingAttemptsAdmin(admin.ModelAdmin):
    list_display = ("id", "attempt_date", "attempt_status", "mail_server_response", "mailing")
    search_fields = ("attempt_status", "mailing")
    list_filter = ("attempt_status", "mailing")
