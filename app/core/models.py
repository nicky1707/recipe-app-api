from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):

        # raise error if email address is not provided
        if not email:
            raise ValueError("User must have an email address")

        #  **extrafields gives flexibilty of creating additinal fields of needed.
        user = self.model(
            email=self.normalize_email(email), **extra_fields
        )  # calling self.User(email=email), normalize the email.
        user.set_password(password)  # encrypt and save the password
        user.save(using=self._db)  # saves the user to database.

        return user

    def create_superuser(self, email, password):
        """Create and return a superuser"""
        user = self.create_user(email=email, password=password)
        user.is_staff = True  # makes the user a admin
        user.is_superuser = True
        user.save(using=self._db)

        return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=225, unique=True)
    name = models.CharField(max_length=225)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # assign user manager

    USERNAME_FIELD = "email"