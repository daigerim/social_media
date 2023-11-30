from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from .managers import CustomUserManager

username_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9_.]{1,30}$',
    message='Username can be up to 30 characters and should contain numbers, letters, periods, and underscores only.',
)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=30, validators=[username_validator])
    bio = models.CharField(max_length=150)
    profile_picture = models.ImageField(upload_to='profilepic', blank=True, null=True)
    data_joined = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'





