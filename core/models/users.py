from django.db import models
from core.utils.encryption import encrypt_text, decrypt_text
import hashlib

class User(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    aadhaar_encrypted = models.TextField()
    aadhaar_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    address = models.TextField(blank=True, null=True) 


    def set_aadhaar(self, aadhaar_number):
        # Generate hash first
        aadhaar_hash = hashlib.sha256(aadhaar_number.encode()).hexdigest()

        # Check for duplicates
        if User.objects.filter(aadhaar_hash=aadhaar_hash).exists():
            raise ValueError("This Aadhaar number is already registered.")

        # Encrypt and store
        self.aadhaar_encrypted = encrypt_text(aadhaar_number)
        self.aadhaar_hash = aadhaar_hash

    def get_aadhaar(self):
        try:
            return decrypt_text(self.aadhaar_encrypted)
        except Exception:
            return "Invalid"

    def masked_aadhaar(self):
        decrypted = self.get_aadhaar()
        return "********" + decrypted[-4:] if decrypted and decrypted != "Invalid" else None
    masked_aadhaar.short_description = "Aadhaar"

    def __str__(self):
        return f"{self.name} ({self.phone_number})"