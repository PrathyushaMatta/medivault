from django.db import models
from django.utils import timezone
from datetime import timedelta
from core.models.users import User

class OTP(models.Model):
    PURPOSE_CHOICES = [
        ('register', 'Register'),
        ('login', 'Login'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
  # ✅ store phone even if user not created yet
    otp_code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=2)
        super().save(*args, **kwargs)

    def has_expired(self) -> bool:
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"OTP for {self.phone_number} ({self.purpose})"
