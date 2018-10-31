from django.db import models


class TimeStampedModel(models.Model):
    """A class representing the timestamp of when the model was created"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
