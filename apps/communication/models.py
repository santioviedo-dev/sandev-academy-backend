import uuid
from django.db import models
from apps.users.models import User
from apps.courses.models import Course


class Thread(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Abierto'
        CLOSED = 'closed', 'Cerrado'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='threads')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads_created')
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='threads_assigned'
    )
    subject = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'hilo'
        verbose_name_plural = 'hilos'
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.subject} ({self.course.title})'


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'mensaje'
        verbose_name_plural = 'mensajes'
        ordering = ['sent_at']

    def __str__(self):
        return f'{self.sender.email} → {self.thread.subject} ({self.sent_at:%d/%m/%Y %H:%M})'