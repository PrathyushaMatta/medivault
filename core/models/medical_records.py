from django.db import models
from core.models.users import User
from core.utils.encryption import encrypt_bytes, decrypt_bytes
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)
class MedicalFile(models.Model):
    CATEGORY_CHOICES = [
        ('prescription', 'Prescription'),
        ('blood_test', 'Blood Test'),
        ('xray', 'X-Ray'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    file_name = models.CharField(max_length=255,editable=False)
    file_encrypted = models.BinaryField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def set_file(self, file):
        """Encrypt and save uploaded file content"""
        try:
            # ⚠️ Avoid reading very large files fully into memory
            file_content = file.read()
            encrypted = encrypt_bytes(file_content)  
            self.file_encrypted = encrypted
            self.file_name = file.name
        except Exception as e:
            logger.error(f"Error encrypting file {file.name}: {e}")
            raise

    def get_file(self):
        try:
            decrypted = decrypt_bytes(self.file_encrypted)
            return ContentFile(decrypted, name=self.file_name)
        except:
            return None

    def __str__(self):
        return f"{self.file_name} ({self.category})"