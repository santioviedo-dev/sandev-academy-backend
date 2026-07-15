import uuid
from django.db import models


class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enrollment = models.OneToOneField(
        'enrollments.Enrollment', on_delete=models.CASCADE, related_name='certificate'
    )
    certificate_number = models.CharField(max_length=50, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    file_url = models.URLField(blank=True)

    class Meta:
        verbose_name = 'certificado'
        verbose_name_plural = 'certificados'
        ordering = ['-issued_at']

    def __str__(self):
        return f'Certificado {self.certificate_number} — {self.enrollment}'

    def save(self, *args, **kwargs):
        if not self.certificate_number:
            self.certificate_number = f'CERT-{str(self.id).upper()[:8]}'
        super().save(*args, **kwargs)