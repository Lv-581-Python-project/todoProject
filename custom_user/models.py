from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from abstract.abstract_model import AbstractModel


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
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


class CustomUser(AbstractBaseUser, AbstractModel):
    objects = UserManager()

    first_name = models.CharField('First Name', max_length=55, null=False, blank=False)
    last_name = models.CharField('Last Name', max_length=55, null=False, blank=False)
    email = models.EmailField('Email', unique=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)

    def to_dict(self):
        return {'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email}

    @classmethod
    def create(cls, email, password, **extra_fields):
        manager = UserManager()
        return manager.create_user(email, password, **extra_fields)

    def update(self, first_name=None, last_name=None, email=None):
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if email:
            self.email = email
        try:
            self.save()
            return self
        except (TypeError, ValueError):
            return None
