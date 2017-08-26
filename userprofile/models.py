from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    location = models.CharField(default='', max_length=50, blank=True)
    country = models.CharField(default='', max_length=50)
    avatar = models.ImageField(default='/media/propic.jpg', blank=True)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
