from django.db import models
import uuid
from django.contrib.auth.models import User


class EstimateSession(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.TextField(null=False, max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    code = models.IntegerField()
    session_admin_user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return str(self.name)


class SessionEntry(models.Model):
    estimate_session = models.ForeignKey(EstimateSession, on_delete=models.CASCADE)
    user_name = models.TextField(null=False, max_length=50)
    channel = models.TextField(null=False, max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    score = models.CharField(null=True, blank=True, max_length=5)
    description = models.CharField(default="", null=True, blank=True, max_length=200)

# https://freefrontend.com/css-checkboxes/
# https://readthedocs.org/projects/django-cryptography/downloads/pdf/latest/
