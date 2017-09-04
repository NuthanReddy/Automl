from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

User._meta.get_field('email')._unique = True


class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset()


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=100, default='')
    location = models.CharField(default='', max_length=100, null=True, blank=True)
    phone = models.IntegerField(default=0, null=True, blank=True)
    image = models.ImageField(default='profile_image/propic.jpg', upload_to='profile_image', blank=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'user'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.user.username


def create_profile(**kwargs):
    if kwargs['created']:
        UserProfile.objects.get_or_create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
