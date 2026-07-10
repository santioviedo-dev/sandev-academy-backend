from django.contrib import admin
from .models import Course, Module, Lesson, Resource, LiveSession


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'modality', 'status', 'created_by', 'created_at')
    list_filter = ('modality', 'status')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'lesson_type', 'order')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'resource_type')


@admin.register(LiveSession)
class LiveSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'scheduled_at', 'duration_minutes')