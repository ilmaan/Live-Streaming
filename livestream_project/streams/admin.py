from django.contrib import admin
from .models import Stream

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ['title', 'stream_id', 'host_name', 'is_active', 'created_at', 'viewer_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'stream_id', 'host_name']
    readonly_fields = ['stream_id', 'created_at', 'updated_at']
