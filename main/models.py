from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class MyUserManager(BaseUserManager):
    def create_user(self, meter_id, first_name, last_name, email, phone_number, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not meter_id:
            raise ValueError('Users must have an meter_id')

        user = self.model(
            meter_id=meter_id,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=self.normalize_email(email)

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, meter_id, email, first_name, last_name, phone_number, password=None, ):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            meter_id=meter_id,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    meter_id = models.CharField(max_length=16, primary_key=True, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=12, null=True)
    billing = models.ForeignKey('Billing', default=None,null=True, on_delete=models.CASCADE)
    objects = MyUserManager()

    USERNAME_FIELD = 'meter_id'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.meter_id

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Billing(models.Model):
    tariff = models.CharField(max_length=10)

    class Meta:
        db_table = 'billing'


class Active(models.Model):
    meter_id = models.ForeignKey('MyUser', primary_key=True, on_delete=models.CASCADE, related_name='active')
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'active'
