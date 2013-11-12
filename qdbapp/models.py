from django.db import models

import secretballot

class Quote(models.Model):
    body = models.TextField()
    channel = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    ip = models.GenericIPAddressField(editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

secretballot.enable_voting_on(Quote)
