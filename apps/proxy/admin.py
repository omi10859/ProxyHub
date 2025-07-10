from django.contrib import admin

from .models import Service, ProxyRequestLog

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_url', 'is_active', 'created_on', 'modified_on')
    list_filter = ('is_active',)
    search_fields = ('name', 'base_url')

@admin.register(ProxyRequestLog)
class ProxyRequestLogAdmin(admin.ModelAdmin):
    list_display = ('created_on', 'api_key', 'downstream_service', 'path', 'method', 'response_status', 'duration_ms')
    search_fields = ('api_key', 'downstream_service', 'path', 'method', 'response_status')
    list_filter = ('downstream_service', 'method', 'response_status')
    readonly_fields = ('created_on',)