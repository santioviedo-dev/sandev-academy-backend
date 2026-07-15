from django.contrib import admin
from .models import Assessment, Question, Choice, Submission, Answer


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'assessment_type', 'passing_score', 'is_published')
    list_filter = ('assessment_type', 'is_published')
    search_fields = ('title', 'course__title')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'question_type', 'order', 'points')
    inlines = [ChoiceInline]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'assessment', 'status', 'score', 'submitted_at')
    list_filter = ('status',)
    inlines = [AnswerInline]