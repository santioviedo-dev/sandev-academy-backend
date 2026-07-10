import uuid
from django.db import models
from django.utils.text import slugify
from apps.users.models import User


class Course(models.Model):
    class Modality(models.TextChoices):
        ASYNC = 'async', 'Asincrónico'
        SYNC = 'sync', 'Sincrónico'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Borrador'
        PUBLISHED = 'published', 'Publicado'
        ARCHIVED = 'archived', 'Archivado'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    modality = models.CharField(max_length=10, choices=Modality.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    thumbnail = models.ImageField(upload_to='courses/thumbnails/', blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='courses_created'
    )
    completion_requires_score = models.BooleanField(default=False)
    min_completion_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'curso'
        verbose_name_plural = 'cursos'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Module(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'módulo'
        verbose_name_plural = 'módulos'
        ordering = ['order']

    def __str__(self):
        return f'{self.course.title} — {self.title}'


class Lesson(models.Model):
    class LessonType(models.TextChoices):
        VIDEO = 'video', 'Video'
        TEXT = 'text', 'Texto'
        MIXED = 'mixed', 'Mixto'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    lesson_type = models.CharField(max_length=10, choices=LessonType.choices, default=LessonType.TEXT)
    order = models.PositiveIntegerField(default=0)
    is_free_preview = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'lección'
        verbose_name_plural = 'lecciones'
        ordering = ['order']

    def __str__(self):
        return f'{self.module.title} — {self.title}'


class Resource(models.Model):
    class ResourceType(models.TextChoices):
        VIDEO = 'video', 'Video'
        PDF = 'pdf', 'PDF'
        LINK = 'link', 'Enlace externo'
        FILE = 'file', 'Archivo'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=10, choices=ResourceType.choices)
    url = models.URLField(blank=True)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'recurso'
        verbose_name_plural = 'recursos'
        ordering = ['order']

    def __str__(self):
        return f'{self.lesson.title} — {self.title}'


class LiveSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='live_sessions')
    title = models.CharField(max_length=200)
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    meeting_url = models.URLField(blank=True)
    platform = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'sesión en vivo'
        verbose_name_plural = 'sesiones en vivo'
        ordering = ['scheduled_at']

    def __str__(self):
        return f'{self.course.title} — {self.title}'