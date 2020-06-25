from django.contrib import admin
from app.models import EstimateSession


@admin.register(EstimateSession)
class EstimateSessionView(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'date_created', 'date_modified')
    ordering = ('-id',)
    # search_fields = ('resource_name', 'user', 'msisdn')
