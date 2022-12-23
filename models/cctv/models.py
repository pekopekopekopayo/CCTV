from django.db import models
from models.user.models import User


class Cctv(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    users = models.ManyToManyField(User, related_name="cctvs")
    road_name = models.CharField(max_length=255, unique=True)
