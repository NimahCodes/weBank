from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """creates and saves a new user """
        if not email:
            raise ValueError('User must have an Email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """creates and saves a new superuser"""
        if password is None:
            raise TypeError('Password should not been None')
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=255, null=True, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp = models.CharField(max_length=200)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class AccountDetails(models.Model):
    ACCOUNT_TYPE = (
        ('Savings Account', 'Savings Account'),
        ('Current Account', 'Current Account'),
        )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    account_type = models.CharField(max_length=200, null=True, choices=ACCOUNT_TYPE)
    account_number = models.IntegerField(null=True, unique=True)
    age = models.IntegerField(null=True)
    fullname = models.CharField(max_length=200, null=True)
    employment_status = models.CharField(max_length=200, null=True)


class UserBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_account = models.ForeignKey(AccountDetails, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=15, decimal_places=2)
