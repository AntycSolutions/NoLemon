from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    class Meta:
        ordering = ('first_name', 'last_name', 'email')
        
    def __str__(self):
        return self.first_name + " " + self.last_name
    

class Seller(User):
    #TODO: a seller needs a rating
    pass
    
    
class Mechanic(User):
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    
    
class Customer(User):
    pass


class Inspection(models.Model):
    comments = models.TextField()
    date = models.DateField()
    mechanic = models.ForeignKey(Mechanic)
    #TODO: a video should be here... not sure how to handle
    # that just yet


class Vehicle(models.Model):
    owner = models.ForeignKey(Seller)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    inspections = models.ForeignKey(Inspection, blank=True)
    vin = models.CharField(max_length=17, unique=True)
    
    def __str__(self):
        return self.year + " " + self.make + " " + self.model
    
    class Meta:
        ordering = ('owner', 'year', 'make', 'model', 'vin', 'inspections')