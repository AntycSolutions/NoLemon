# http://michalcodes4life.wordpress.com/2014/02/08
# /multiple-user-types-in-django-1-6/

from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager as DjangoBaseUserManager
from django.db import models


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

    def create_user(self, email, first_name, last_name,
                    password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = Seller(
            email=SellerManager.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomerManager(DjangoBaseUserManager):

    def create_user(self, email, first_name, last_name,
                    password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = Customer(
            email=CustomerManager.normalize_email(email),
            first_name=first_name,
            last_name=last_name
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
    objects = SellerManager()

    def rating(self):
        ratings = Rating.objects.filter(seller=self)
        number = 0
        for rating in ratings:
            number += rating.rating
        if ratings.count() is not 0:
            return number / ratings.count()
        return None
    rating.allow_tags = True


class Customer(BaseUser):
    objects = CustomerManager()


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


class Rating(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SELLER_RATING = ((ONE, 'ONE'),
                     (TWO, 'TWO'),
                     (THREE, 'THREE'),
                     (FOUR, 'FOUR'),
                     (FIVE, 'FIVE')
                     )
    rating = models.IntegerField(choices=SELLER_RATING)
    seller = models.ForeignKey(Seller)
    customer = models.ForeignKey(Customer)

    def __str__(self):
        return str(self.rating) \
            + " " + str(self.seller) \
            + " " + str(self.customer)

    class Meta:
        unique_together = (('seller', 'customer'),)


class Vehicle(models.Model):
    owner = models.ForeignKey(Seller)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vin = models.CharField(
        "vehicle identification number", max_length=17, unique=True)

    def __str__(self):
        return self.vin \
            + " " + str(self.year) \
            + " " + self.make \
            + " " + self.model

    class Meta:
        ordering = ('owner', 'year', 'make', 'model', 'vin')


class Inspection(models.Model):
    comments = models.TextField()
    date = models.DateTimeField()
    views = models.IntegerField()
    mechanic = models.ForeignKey(Mechanic)
    vehicle = models.ForeignKey(Vehicle)
    video = models.FileField(upload_to='inspections/%Y/%m/%d',
                             null=True, blank=True)

    def __str__(self):
        return self.comments \
            + " " + str(self.date) \
            + " " + str(self.mechanic) \
            + " " + str(self.vehicle)


class RequestInspection(models.Model):
    vehicle = models.ForeignKey(Vehicle)
    seller = models.ForeignKey(Seller)
    mechanic = models.ForeignKey(Mechanic)
    request_date = models.DateTimeField()

    def __str__(self):
        return str(self.vehicle) + " " + str(self.seller)
