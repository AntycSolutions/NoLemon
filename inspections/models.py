# http://michalcodes4life.wordpress.com/2014/02/08
# /multiple-user-types-in-django-1-6/
import datetime

from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager as DjangoBaseUserManager
from django.db import models


YEAR_CHOICES = []
for r in range(1980, (datetime.datetime.now().year + 1)):
    YEAR_CHOICES.append((r, r))


class BaseUserManager(DjangoBaseUserManager):

    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = BaseUser(
            email=BaseUserManager.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_admin=False
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=BaseUserManager.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class SellerManager(DjangoBaseUserManager):

    def create_user(self, email, first_name, last_name, city,
                    password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = Seller(
            email=SellerManager.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            city=city
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class MechanicManager(DjangoBaseUserManager):

    def create_user(self, email, first_name, last_name,
                    phone_number, address, city, province,
                    password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = Mechanic(
            email=MechanicManager.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
            city=city,
            province=province
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class BaseUser(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(
        "email address",
        max_length=255,
        unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = BaseUserManager()

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

    # class Meta:
    #     ordering = ('first_name', 'last_name', 'email')


class Seller(BaseUser):
    city = models.CharField(max_length=255)

    objects = SellerManager()


class Mechanic(BaseUser):
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = MechanicManager()

    def full_address(self):
        return self.address \
            + " " + self.city \
            + " " + self.province
    full_address.allow_tags = True


class Vehicle(models.Model):
    owner = models.ForeignKey(Seller)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField(max_length=4, choices=YEAR_CHOICES,
                               default=datetime.datetime.now().year)
    vin = models.CharField(
        "vehicle identification number", max_length=17, unique=True)
    odometer = models.IntegerField()
    photo = models.ImageField(upload_to='inspections/vehicles/%Y/%m/%d',
                              null=True, blank=True)

    def __str__(self):
        return self.vin \
            + " " + str(self.year) \
            + " " + self.make \
            + " " + self.model

    class Meta:
        ordering = ('owner', 'year', 'make', 'model', 'vin')


class Inspection(models.Model):
    comments = models.TextField(blank=True)
    date = models.DateTimeField(null=True, blank=True)
    views = models.IntegerField(default=0, blank=True)
    mechanic = models.ForeignKey(Mechanic)
    vehicle = models.ForeignKey(Vehicle)
    video = models.FileField(upload_to='inspections/videos/%Y/%m/%d',
                             null=True, blank=True)
    report = models.FileField(upload_to='inspections/reports/%Y/%m/%d',
                              null=True, blank=True)
    vehicle_history = models.FileField(
        upload_to='inspections/history/%Y/%m/%d',
        null=True, blank=True)

    def __str__(self):
        return self.comments \
            + " " + str(self.date) \
            + " " + str(self.mechanic) \
            + " " + str(self.vehicle)


class InspectionRequest(models.Model):
    vehicle = models.ForeignKey(Vehicle)
    seller = models.ForeignKey(Seller)
    request_date = models.DateTimeField()

    def __str__(self):
        return str(self.vehicle) + " " + str(self.seller)


class Receipt(models.Model):
    # TODO: Pick better choice names
    INSPECTION_CHOICES = [(29.99, 'level1'),
                          (37.00, 'level2'),
                          (56.00, 'level3')]

    number = models.CharField(max_length=64, primary_key=True,
                              verbose_name="Receipt Number")
    inspection = models.ForeignKey(Inspection)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    payment_level = models.FloatField(choices=INSPECTION_CHOICES)


class SiteStatistics(models.Model):
    home_page_views = models.IntegerField(default=0)
