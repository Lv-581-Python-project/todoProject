from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    objects = UserManager()

    first_name = models.CharField('First Name', max_length=55, null=False, blank=False)
    last_name = models.CharField('Last Name', max_length=55, null=False, blank=False)
    email = models.EmailField('Email', unique=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.first_name) + str(self.last_name)
