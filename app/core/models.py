""" Database models for the core app. """
import os
import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


def origin_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    # ext = filename.split('.')[-1]
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('predicate', 'recognition', filename)


def update_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    # ext = filename.split('.')[-1]
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('update', 'recognition', filename)


class UserManager(BaseUserManager):
    """
    Manager for user profiles.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a new user.
        """
        if not email:
            raise ValueError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Create and save a new superuser.
        """
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User in the system.
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Recognition(models.Model):
    """
    Recognition model.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    description = models.CharField(max_length=255, null=True)
    qualified = models.BooleanField(default=True)
    origin_image = models.ImageField(
        null=True, upload_to=origin_image_file_path)
    origin_pos = models.CharField(max_length=255, null=True)
    update_image = models.ImageField(
        null=True, upload_to=update_image_file_path)
    update_pos = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of our user."""
        return self.date
