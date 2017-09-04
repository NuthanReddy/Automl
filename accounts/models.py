from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset()


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=100, default='')
    phone = models.IntegerField(default=0)
    image = models.ImageField(default='profile_image/propic.jpg', upload_to='profile_image', blank=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'user'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
