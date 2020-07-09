from django.contrib import admin
from app.models import EstimateSession, SessionEntry


@admin.register(EstimateSession)
class EstimateSessionView(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'date_created', 'date_modified')
    ordering = ('-id',)
    # search_fields = ('resource_name', 'user', 'msisdn')


@admin.register(SessionEntry)
class SessionEntryView(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'estimate_session', 'channel', 'score', 'date_created')
    ordering = ('-id',)
    # search_fields = ('resource_name', 'user', 'msisdn')
