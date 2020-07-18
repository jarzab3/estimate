from django.contrib import admin
from app.models import EstimateSession, SessionEntry
from django.forms import ModelForm, PasswordInput
from django import forms


class EstimateSessionForm(ModelForm):
    session_password = forms.CharField(widget=PasswordInput())

    class Meta:
        model = EstimateSession
        fields = '__all__'


@admin.register(EstimateSession)
class EstimateSessionView(admin.ModelAdmin):
    list_display = ('id', 'name', 'session_admin_user', 'code', 'date_created', 'date_modified')
    ordering = ('-id',)
    # search_fields = ('resource_name', 'user', 'msisdn')
    form = EstimateSessionForm


@admin.register(SessionEntry)
class SessionEntryView(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'estimate_session', 'channel', 'score', 'date_created')
    ordering = ('-id',)
    # search_fields = ('resource_name', 'user', 'msisdn')
