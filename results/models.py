from django.db import models
from django.contrib.auth.models import User


class Results(models.Model):
    owner = models.ForeignKey(User)


