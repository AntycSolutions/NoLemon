# Populate the database with showcase and testing data
import datetime
import os


def populate():
    password = "nolemon"

    admin = add_seller('admin@nolemon.ca', 'Admin', 'Man', password)
    admin.is_admin = True
    admin.save()

    bobSeller = add_seller("bob@seller.ca", "Bob", "Bobson", password)
    samSeller = add_seller("sam@seller.ca", "Sam", "Samson", password)
    timSeller = add_seller("tim@seller.ca", "Tim", "Timson", password)
    tomSeller = add_seller("tom@seller.ca", "Tom", "Tomson", password)
    patSeller = add_seller("pat@seller.ca", "Pat", "Patson", password)

    sarahMechanic = add_mechanic(
        "sarah@mechanic.ca", "Sarah", "Sarahson", password, "7801",
        "123 st nw", "edmonton", "ab")
    andreMechanic = add_mechanic(
        "andre@mechanic.ca", "Andre", "Andreson", password, "7802",
        "23 st nw", "edmonton", "ab")
    barryMechanic = add_mechanic(
        "barry@mechanic.ca", "Barry", "Barryson", password, "7803",
        "83 st nw", "edmonton", "ab")
    susanMechanic = add_mechanic(
        "susan@mechanic.ca", "Susan", "Susanson", password, "7804",
        "123 ave nw", "edmonton", "ab")
    wendyMechanic = add_mechanic(
        "wendy@mechanic.ca", "Wendy", "Wendyson", password, "7805",
        "23 ave nw", "edmonton", "ab")

    aleroVehicle = add_vehicle(
        "123", bobSeller, "Oldsmobile", "Alero", 2004)
    lebaronVehicle = add_vehicle(
        "456", bobSeller, "Chrysler", "Le Baron", 1989)
    grandcherokeeVehicle = add_vehicle(
        "789", bobSeller, "Jeep", "Grand Cherokee", 2011)

    now = datetime.datetime.now()
    goodInspection = add_inspection(
        0, sarahMechanic, aleroVehicle, "Good", now, 0)
    duplicateInspection = add_inspection(
        1, sarahMechanic, aleroVehicle, "Good", now, 0)
    alrightInspection = add_inspection(
        2, sarahMechanic, lebaronVehicle, "Alright", now, 0)
    badInspection = add_inspection(
        3, sarahMechanic, grandcherokeeVehicle, "Bad", now, 0)

    print_all_sellers()
    print_all_mechanics()
    print_all_inspections()
    print_all_vehicles()


def add_seller(email, firstName, lastName, password):
    seller = None
    try:
        seller = Seller.objects.get(email=email)
        print("Already exists, seller:", seller)
        return seller
    except:
        pass
    seller = Seller.objects.create_user(
        email=email, first_name=firstName, last_name=lastName,
        password=password
    )
    if not seller:
        print("Did not create seller:", seller)
    return seller


def add_mechanic(email, firstName, lastName, password,
                 phoneNumber, address, city, province):
    mechanic = None
    try:
        mechanic = Mechanic.objects.get(email=email)
        print("Already exists, mechanic:", mechanic)
        return mechanic
    except:
        pass
    mechanic = Mechanic.objects.create_user(
        email=email, first_name=firstName, last_name=lastName,
        password=password, phone_number=phoneNumber, address=address,
        city=city, province=province
    )
    if not mechanic:
        print("Did not create mechanic:", mechanic)
    return mechanic


def add_inspection(pk, mechanic, vehicle, comments, date, views):
    inspection, created = Inspection.objects.get_or_create(
        pk=pk, mechanic=mechanic, comments=comments, date=date,
        vehicle=vehicle, views=views
    )
    if created:
        inspection.save()
    else:
        print("Did not create inspection:", comments)
    return inspection


def add_vehicle(vin, owner, make, model, year):
    vehicle, created = Vehicle.objects.get_or_create(
        vin=vin, owner=owner,
        make=make, model=model, year=year
    )
    if created:
        vehicle.save()
    else:
        print("Did not create vehicle:", vin)
    return vehicle


def print_all_sellers():
    print("Sellers:")
    for seller in Seller.objects.all():
        print(seller)


def print_all_mechanics():
    print("Mechanics:")
    for mechanic in Mechanic.objects.all():
        print(mechanic)


def print_all_inspections():
    print("Inspections:")
    for inspection in Inspection.objects.all():
        print(inspection)


def print_all_vehicles():
    print("Vehicles:")
    for vehicle in Vehicle.objects.all():
        print(vehicle)


if __name__ == '__main__':
    print("Starting NoLemon database population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'no_lemon.settings')
    from inspections.models import Seller, Mechanic, \
        Inspection, Vehicle
    populate()
    print("Finished populate script.")
