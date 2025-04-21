from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid


class PoliceOfficerManager(BaseUserManager):
    def create_user(self, uid, full_name, phone, password=None):
        if not uid:
            raise ValueError("Police UID is required")
        officer = self.model(uid=uid, full_name=full_name, phone=phone)
        officer.set_password(password)
        officer.save(using=self._db)
        return officer

    def create_superuser(self, uid, full_name, phone, password):
        officer = self.create_user(uid, full_name, phone, password)
        officer.is_admin = True
        officer.is_superuser = True  # ✅ Grant superuser permissions
        officer.is_staff = True  # ✅ Make the user a staff member
        officer.save(using=self._db)
        return officer


class PoliceOfficer(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    full_name = models.CharField(max_length=255)
    uid = models.CharField(max_length=20, unique=True)  # Police UID
    phone = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = PoliceOfficerManager()

    USERNAME_FIELD = "uid"
    REQUIRED_FIELDS = ["full_name", "phone"]

    def __str__(self):
        return self.full_name


class Audio(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    audio_file = models.FileField(upload_to='audio_files/')
    transcribed_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audio {self.id}"


class FIR(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    case_id = models.CharField(max_length=20, unique=True)
    # ✅ Fix: Ensure it's a ForeignKey
    audio = models.ForeignKey(
        Audio, on_delete=models.SET_NULL, null=True, blank=True)
    original_text = models.TextField()
    fir_text = models.TextField()
    fir_pdf = models.FileField(upload_to='fir_pdfs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.case_id:
            self.case_id = f"CASE-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"FIR {self.case_id}"
