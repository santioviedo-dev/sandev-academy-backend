import uuid
from django.db import models
from apps.users.models import User
from apps.courses.models import Course, Lesson


class Assessment(models.Model):
    class AssessmentType(models.TextChoices):
        AUTO = 'auto', 'Corrección automática'
        MANUAL = 'manual', 'Corrección manual'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assessments')
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='assessments',
        null=True, blank=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assessment_type = models.CharField(max_length=10, choices=AssessmentType.choices)
    passing_score = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'evaluación'
        verbose_name_plural = 'evaluaciones'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.course.title} — {self.title}'


class Question(models.Model):
    class QuestionType(models.TextChoices):
        MULTIPLE_CHOICE = 'multiple_choice', 'Opción múltiple'
        TRUE_FALSE = 'true_false', 'Verdadero / Falso'
        OPEN = 'open', 'Respuesta abierta'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=20, choices=QuestionType.choices)
    statement = models.TextField()
    order = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'pregunta'
        verbose_name_plural = 'preguntas'
        ordering = ['order']

    def __str__(self):
        return f'{self.assessment.title} — pregunta {self.order}'


class Choice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'opción'
        verbose_name_plural = 'opciones'

    def __str__(self):
        return f'{self.question} — {self.text[:50]}'


class Submission(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendiente de revisión'
        REVIEWED = 'reviewed', 'Revisada'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='submissions')
    enrollment = models.ForeignKey(
        'enrollments.Enrollment', on_delete=models.CASCADE, related_name='submissions'
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    score = models.PositiveIntegerField(null=True, blank=True)
    teacher_feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'entrega'
        verbose_name_plural = 'entregas'
        ordering = ['-submitted_at']
        constraints = [
            models.UniqueConstraint(
                fields=['assessment', 'enrollment'], name='unique_submission'
            )
        ]

    def __str__(self):
        return f'{self.enrollment} — {self.assessment.title}'


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    response_text = models.TextField(blank=True)
    selected_choice = models.ForeignKey(
        Choice, on_delete=models.SET_NULL, null=True, blank=True, related_name='answers'
    )
    is_correct = models.BooleanField(null=True, blank=True)
    points_earned = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'respuesta'
        verbose_name_plural = 'respuestas'
        constraints = [
            models.UniqueConstraint(
                fields=['submission', 'question'], name='unique_answer'
            )
        ]

    def __str__(self):
        return f'{self.submission} — pregunta {self.question.order}'