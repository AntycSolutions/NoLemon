# Populate the database with showcase and testing data
import os
import datetime


def populate():
    password = "nolemon"

    bobSeller = add_seller("bob@seller.ca", "Bob", "Bobson", 5, password)
    samSeller = add_seller("sam@seller.ca", "Sam", "Samson", 4, password)
    timSeller = add_seller("tim@seller.ca", "Tim", "Timson", 3, password)
    tomSeller = add_seller("tom@seller.ca", "Tom", "Tomson", 2, password)
    patSeller = add_seller("pat@seller.ca", "Pat", "Patson", 1, password)

    johnCustomer = add_customer(
        "john@customer.ca", "John", "Johnson", password)
    janeCustomer = add_customer(
        "jane@customer.ca", "Jane", "Johnson", password)
    judyCustomer = add_customer(
        "judy@customer.ca", "Judy", "Johnson", password)
    jackCustomer = add_customer(
        "jack@customer.ca", "Jack", "Johnson", password)
    jillCustomer = add_customer(
        "jill@customer.ca", "Jill", "Johnson", password)

    sarahMechanic = add_mechanic(
        "sarah@mechanic.ca", "Sarah", "Sarahson", password, "7801", "123 st")
    andreMechanic = add_mechanic(
        "andre@mechanic.ca", "Andre", "Andreson", password, "7802", "456 st")
    barryMechanic = add_mechanic(
        "barry@mechanic.ca", "Barry", "Barryson", password, "7803", "789 st")
    susanMechanic = add_mechanic(
        "susan@mechanic.ca", "Susan", "Susanson", password, "7804", "123 ave")
    wendyMechanic = add_mechanic(
        "wendy@mechanic.ca", "Wendy", "Wendyson", password, "7805", "456 ave")

    now = datetime.datetime.now()
    goodInspection = add_inspection(sarahMechanic, "Good", now)
    alrightInspection = add_inspection(sarahMechanic, "Alright", now)
    badInspection = add_inspection(sarahMechanic, "Bad", now)

    #goodInspection.Vehicle

    aleroVehicle = add_vehicle(
        "123", bobSeller, goodInspection, "Oldsmobile", "Alero", 2004)
    lebaronVehicle = add_vehicle(
        "456", bobSeller, alrightInspection, "Chrysler", "Le Baron", 1989)
    grandcherokeeVehicle = add_vehicle(
        "789", bobSeller, badInspection, "Jeep", "Grand Cherokee", 2011)

    print_all_sellers()
    print_all_customers()
    print_all_mechanics()
    print_all_inspections()
    print_all_vehicles()


def add_seller(email, firstName, lastName, rating, password):
    seller = None
    try:
        seller = Seller.objects.get(email=email)
        return seller
    except:
        pass
    seller = Seller.objects.create_user(
        email=email, first_name=firstName, last_name=lastName,
        password=password, rating=rating)
    if not seller:
        print ("Did not create seller: ", seller)
    return seller


def add_customer(email, firstName, lastName, password):
    customer = None
    try:
        customer = customer.objects.get(email=email)
        return customer
    except:
        pass
    customer = Customer.objects.create_user(
        email=email, first_name=firstName, last_name=lastName,
        password=password)
    if not customer:
        print ("Did not create customer: ", customer)
    return customer


def add_mechanic(email, firstName, lastName, phoneNumber, address,
                 password):
    mechanic = None
    try:
        mechanic = mechanic.objects.get(email=email)
        return mechanic
    except:
        pass
    mechanic = Mechanic.objects.create_user(
        email=email, first_name=firstName, last_name=lastName,
        password=password, phone_number=phoneNumber, address=address)
    if not mechanic:
        print ("Did not create mechanic: ", mechanic)
    return mechanic


def add_inspection(mechanic, comments, date):
    inspection, created = Inspection.objects.get_or_create(
        mechanic=mechanic, comments=comments, date=date)
    if created:
        inspection.save()
    else:
        print ("Did not create inspection: ", comments)
    return inspection


def add_vehicle(vin, owner, inspections, make, model, year):
    vehicle, created = Vehicle.objects.get_or_create(
        vin=vin, owner=owner, inspections=inspections,
        make=make, model=model, year=year)
    if created:
        vehicle.save()
    else:
        print ("Did not create vehicle: ", vin)
    return vehicle


def print_all_sellers():
    print ("Sellers:")
    for seller in Seller.objects.all():
        print (seller)


def print_all_customers():
    print("Customers:")
    for customer in Customer.objects.all():
        print (customer)


def print_all_mechanics():
    print("Mechanics:")
    for mechanic in Mechanic.objects.all():
        print (mechanic)


def print_all_inspections():
    print("Inspections:")
    for inspection in Inspection.objects.all():
        print (inspection)


def print_all_vehicles():
    print("Vehicles:")
    for vehicle in Vehicle.objects.all():
        print (vehicle)


if __name__ == '__main__':
    print("Starting NoLemon database population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'no_lemon.settings')
    from inspections.models import Seller, Customer, Mechanic, \
        Inspection, Vehicle
    populate()
    print("Finished populate script.")
