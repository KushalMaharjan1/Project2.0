from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'category', 'location', 'date', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'location', 'contact')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Item Information', {
            'fields': ('title', 'status', 'category')
        }),
        ('Details', {
            'fields': ('location', 'date', 'description', 'contact', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-created_at',)
