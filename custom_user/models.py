from django.contrib.auth.models import AbstractBaseUser
from django.db import models, DatabaseError
from utils.abstract_model import AbstractModel


class CustomUser(AbstractBaseUser, AbstractModel):
    objects = models.Manager()

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
        if not email:
            raise ValueError('User must have an email address')
        user = CustomUser(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        try:
            user.save()
            return user
        except (ValueError, TypeError, DatabaseError):
            return False

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
        except (TypeError, ValueError, DatabaseError):
            return None
