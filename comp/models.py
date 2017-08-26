from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _

COMP_STATUS = (('A', 'Active'), ('C', 'Closed'))
CRITERIA = (('D', 'Desc'), ('A', 'Asc'))
LANG = (('Python', 'Python'), ('C', 'C'), ('C++', 'C++'), ('R', 'R'), ('Python3', 'Python3'), ('Scala', 'Scala'))
ALGO = (('Reg', 'Regression'), ('LogReg', 'Logistic Regression'), ('RandF', 'Random Forest'),
        ('KNN', 'K - Nearest Neighbour'), ('NN', 'Neural Networks'), ('ACO', 'Ant Colony Optimization'),
        ('SVM', 'Support Vector Machines'), ('PSA', 'Particle Swarm Algorithm'), ('Oth', 'Other'))


class Team(models.Model):
    user = models.ForeignKey(User)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)


class Competition(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=1000)
    logo = models.FileField(default='')
    team_size = models.IntegerField(default=1)
    status = models.CharField(default="Active", max_length=1, choices=COMP_STATUS)
    start = models.DateTimeField(default=timezone.now, blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    sample = models.FileField(default='')
    train = models.FileField(default='')
    test = models.FileField(default='')
    train2 = models.FileField(default='', blank=True, null=True)
    test2 = models.FileField(default='', blank=True, null=True)
    valid = models.FileField(default='', blank=True, null=True)
    scoring_formula = models.Expression()
    gold = models.IntegerField(default=0)
    silver = models.IntegerField(default=0)
    bronze = models.IntegerField(default=0)
    prize4 = models.IntegerField(default=0)
    prize5 = models.IntegerField(default=0)
    prize6 = models.IntegerField(default=0)
    prize7 = models.IntegerField(default=0)
    prize8 = models.IntegerField(default=0)
    prize9 = models.IntegerField(default=0)
    prize10 = models.IntegerField(default=0)


class Submission(models.Model):
    file_submission = models.FileField(default='', blank=False, null=False)
    team = models.ForeignKey(Team)
    comp = models.ForeignKey(Competition)
    id = models.IntegerField(primary_key=True)
    time = models.DateTimeField(default=timezone.now, blank=True, null=True)
    score = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    language = models.CharField(default="Python", max_length=1, choices=LANG)
    algo = models.CharField(default="Reg", max_length=100, choices=ALGO)


class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset().filter(city='London')


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password
        """
        now = timezone.now()

        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        user = self.mode(email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now,
                         date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, password, True, True, **extra_fields)


class UserProfile(AbstractBaseUser):
    mail_id = models.EmailField(default='', max_length=100, blank=True)
    first_name = models.CharField(default='', max_length=100, blank=True)
    last_name = models.CharField(default='', max_length=100, blank=True)
    username = models.CharField(default='', max_length=50, blank=True)
    location = models.CharField(default='', max_length=50, blank=True)
    country = models.CharField(default='', max_length=50)
    avatar = models.ImageField(default='/media/propic.jpg', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'location', 'country']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _['user']
        verbose_name_plural = _['users']

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User
        """
        send_mail(subject, message, from_email, [self.email])


class Registration(models.Model):
    user = models.ForeignKey(User)
    comp = models.ForeignKey(Competition)
