import uuid
from django.db import models
from apps.users.models import User
from apps.courses.models import Course, Lesson, LiveSession


class Enrollment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Activa'
        COMPLETED = 'completed', 'Completada'
        CANCELLED = 'cancelled', 'Cancelada'

    class PaymentStatus(models.TextChoices):
        FREE = 'free', 'Gratuito'
        PENDING = 'pending', 'Pendiente'
        PAID = 'paid', 'Pagado'
        REFUNDED = 'refunded', 'Reembolsado'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    payment_status = models.CharField(
        max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.FREE
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'inscripción'
        verbose_name_plural = 'inscripciones'
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_enrollment')
        ]

    def __str__(self):
        return f'{self.student.email} → {self.course.title}'


class LessonProgress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_records')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'progreso de lección'
        verbose_name_plural = 'progreso de lecciones'
        constraints = [
            models.UniqueConstraint(fields=['enrollment', 'lesson'], name='unique_lesson_progress')
        ]

    def __str__(self):
        return f'{self.enrollment} — {self.lesson.title}'


class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='attendances')
    live_session = models.ForeignKey(LiveSession, on_delete=models.CASCADE, related_name='attendances')
    attended = models.BooleanField(default=False)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'asistencia'
        verbose_name_plural = 'asistencias'
        constraints = [
            models.UniqueConstraint(fields=['enrollment', 'live_session'], name='unique_attendance')
        ]

    def __str__(self):
        return f'{self.enrollment} — {self.live_session.title}'