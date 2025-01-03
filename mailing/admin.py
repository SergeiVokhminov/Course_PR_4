from django.contrib import admin

from mailing.models import Recipient, Message, Mailing, Mailing_Attempts


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "patronymic", "comment", "owner")
    search_fields = ("email", "last_name")
    list_filter = ("email", "last_name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "text", "owner")
    search_fields = ("topic",)
    list_filter = ("topic",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_sending", "end_sending", "status", "message", "owner")
    search_fields = ("status", "message")
    list_filter = ("status", "message")


@admin.register(Mailing_Attempts)
class MailingAttemptsAdmin(admin.ModelAdmin):
    list_display = ("id", "attempt_date", "attempt_status", "mail_server_response", "mailing", "owner")
    search_fields = ("attempt_status", "mailing")
    list_filter = ("attempt_status", "mailing")
