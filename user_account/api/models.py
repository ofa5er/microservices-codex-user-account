# api/models.py
from django.db import models

class   UserAccount(models.Model):
    """This class represents the bucketlist model."""
    uid = models.CharField(max_length=255, blank=False, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    billing_address  = models.CharField(max_length=255, blank=True)
    shipping_address  = models.CharField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)