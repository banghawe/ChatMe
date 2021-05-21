from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User


class TrackableDataModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Session(TrackableDataModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    code = models.UUIDField(default=uuid4)

    def __str__(self):
        return str(self.code)


class Message(TrackableDataModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    message = models.TextField(max_length=2000)


class Member(TrackableDataModel):
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.user.username} - {str(self.session.code)}"
