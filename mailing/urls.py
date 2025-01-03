from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (HomeView, MainPageView, MessageListView, MessageDetailsView, MessageCreateView,
                           MessageUpdateView, MessageDeleteView, MailingListView, MailingCreateView, MailingDetailsView,
                           MailingUpdateView, MailingDeleteView, RecipientListView, RecipientDetailsView,
                           RecipientCreateView, RecipientUpdateView, RecipientDeleteView, MessageInfoView,
                           MailingInfoView, RecipientInfoView)

app_name = MailingConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("main/", MainPageView.as_view(), name="main"),
    path("message_info/", MessageInfoView.as_view(), name="message_info"),
    path("mailing_info/", MailingInfoView.as_view(), name="mailing_info"),
    path("recipient_info/", RecipientInfoView.as_view(), name="recipient_info"),
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path('message/<int:pk>/', MessageDetailsView.as_view(), name='message_detail'),
    path("message/update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"),
    path("message/delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"),
    path('mailing-list/', MailingListView.as_view(), name='mailing_list'),
    path("mailing/create/", MailingCreateView.as_view(), name="mailing_create"),
    path('mailing/<int:pk>/', MailingDetailsView.as_view(), name='mailing_detail'),
    path("mailing/update/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),
    path('recipient_list/', RecipientListView.as_view(), name='recipient_list'),
    path("recipient/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path('recipient/<int:pk>/', RecipientDetailsView.as_view(), name='recipient_detail'),
    path("recipient/update/<int:pk>/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipient/delete/<int:pk>/", RecipientDeleteView.as_view(), name="recipient_delete"),

    # path("mailing_send/<int:pk>/", MailingSendView.as_view(), name="mailing_send"),
    # path("mailing_report/<int:pk>/", MailingReportView.as_view(), name="mailing_report"),
    # path("disabling_mailing/<int:pk>/", DisabledMailingView.as_view(), name="disabling_mailing"),
]
