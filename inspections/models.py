from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class BaseUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
                                password=password,
                                first_name=first_name,
                                last_name=last_name,
                                )
        user.is_admin = True
        user.save(using=self._db)
        return user


class BaseUser(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(verbose_name='email address',
                              max_length=255,
                              unique=True,
                              )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

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

    class Meta:
        ordering = ('first_name', 'last_name', 'email')


class Seller(BaseUser):
    # TODO: a seller needs a rating
    pass


class Customer(BaseUser):
    pass


class Mechanic(BaseUser):
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=255)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']


class Inspection(models.Model):
    comments = models.TextField()
    date = models.DateField()
    mechanic = models.ForeignKey(Mechanic)
    # TODO: a video should be here... not sure how to handle
    # that just yet
    # video = ?


class Vehicle(models.Model):
    owner = models.ForeignKey(Seller)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    inspections = models.ForeignKey(Inspection, blank=True, null=True)
    vin = models.CharField(max_length=17, unique=True)

    def __str__(self):
        return self.year.__str__() + " " + self.make + " " + self.model

    class Meta:
        ordering = ('owner', 'year', 'make', 'model', 'vin', 'inspections')
