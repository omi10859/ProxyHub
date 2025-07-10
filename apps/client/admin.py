from django.contrib import admin
from .models import ClientKey

@admin.register(ClientKey)
class ClientKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'key')
    search_fields = ('name', )
