from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields) -> "User":
        """Creates and saves a new user"""
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)  # encrypts the password
        user.save(using=self._db)  # standard procedure to save objects in django
        return user

    def create_superuser(self, email, password) -> "User":
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        # no need to pass extra_fields since they are already included in the create_user function
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of username.
    PermissionsMixin adds the necessary fields and methods to support the Django"s Group and Permission model
    """

    email = models.EmailField(max_length=255, unique=True)
    # max_length is required for all CharFields
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    # is_active is required for all users
    is_staff = models.BooleanField(default=False)
    # is_staff is required for all users, will determine if user is allowed to access the admin site

    objects = UserManager()
    # UserManager is a class that comes with BaseUserManager

    USERNAME_FIELD = "email"
    # tells django to use email as the username field
