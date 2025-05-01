from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f'{self.from_user} -> {self.to_user}'

    @classmethod
    def add(cls, from_user, to_user):
        cls.objects.create(from_user=from_user, to_user=to_user)


class Profile(models.Model):
    BOOLEAN_CHOICES = [
        (0, 'Female'),
        (1, 'Male'),

    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, default='')
    age = models.PositiveSmallIntegerField(blank=True, default=0)
    gender = models.PositiveSmallIntegerField(choices=BOOLEAN_CHOICES, default=0, blank=True)

    def __str__(self):
        return f'{self.user}'
