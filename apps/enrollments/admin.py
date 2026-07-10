from django.contrib import admin
from .models import Enrollment, LessonProgress, Attendance


class LessonProgressInline(admin.TabularInline):
    model = LessonProgress
    extra = 0


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'payment_status', 'enrolled_at')
    list_filter = ('status', 'payment_status')
    search_fields = ('student__email', 'course__title')
    inlines = [LessonProgressInline]


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'live_session', 'attended', 'recorded_at')