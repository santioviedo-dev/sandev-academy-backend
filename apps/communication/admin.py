from django.contrib import admin
from .models import Thread, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'sent_at')


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('subject', 'course', 'author', 'assigned_to', 'status', 'updated_at')
    list_filter = ('status',)
    search_fields = ('subject', 'author__email', 'course__title')
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'thread', 'is_read', 'sent_at')
    list_filter = ('is_read',)