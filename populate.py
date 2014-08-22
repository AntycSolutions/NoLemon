# Populate the database with showcase and testing data
import datetime
import os
import random


def populate():
    password = "nolemon"

    admin = add_seller('admin@nolemon.ca', 'Admin', 'Man', password)
    admin.is_admin = True
    admin.save()

    print("Creating Sellers...")
    bobSeller = add_seller("bob@seller.ca", "Bob", "Bobson", password)
    samSeller = add_seller("sam@seller.ca", "Sam", "Samson", password)
    timSeller = add_seller("tim@seller.ca", "Tim", "Timson", password)
    tomSeller = add_seller("tom@seller.ca", "Tom", "Tomson", password)
    patSeller = add_seller("pat@seller.ca", "Pat", "Patson", password)
    print("... Sellers added.")

    print("Creating Mechanics...")
    sarahMechanic = add_mechanic(
        "sarah@mechanic.ca", "Sarah", "Sarahson", password, "7801234567",
        "123 st nw", "edmonton", "ab")
    andreMechanic = add_mechanic(
        "andre@mechanic.ca", "Andre", "Andreson", password, "7802345678",
        "23 st nw", "edmonton", "ab")
    barryMechanic = add_mechanic(
        "barry@mechanic.ca", "Barry", "Barryson", password, "7803456789",
        "83 st nw", "edmonton", "ab")
    susanMechanic = add_mechanic(
        "susan@mechanic.ca", "Susan", "Susanson", password, "7804567890",
        "123 ave nw", "edmonton", "ab")
    wendyMechanic = add_mechanic(
        "wendy@mechanic.ca", "Wendy", "Wendyson", password, "7805678901",
        "23 ave nw", "edmonton", "ab")
    print("... Mechanics added.")

    print("Creating Vehicles...")
    make_model_choices = {'Oldsmobile': ['Cutlass',
                                         '442',
                                         '88',
                                         'Alero',
                                         'Bravada'],
                          'Chrysler': ['Airflow',
                                       'Alpine',
                                       '300',
                                       'Aspen',
                                       'Royal'],
                          'Ford': ['Del Rey',
                                   'Escort',
                                   'Fiesta',
                                   'Crown Victoria',
                                   'Tempo'],
                          'Dodge': ['Royal',
                                    'Shadow',
                                    'Lancer',
                                    'Spirit',
                                    'Ram'],
                          'Jeep': ['Commander',
                                   'Liberty',
                                   'Grand Cherokee',
                                   'Cherokee',
                                   'Wrangler'],
                          'Chevrolet': ['Lanos',
                                        'Lumina',
                                        'Cavalier',
                                        'Impala',
                                        'Malibu'],
                          'Mercedes-Benz': ['E-Class',
                                            'SLS AMG',
                                            'R230',
                                            'CLA-Class',
                                            'W166'],
                          'Lincoln': ['Continental',
                                      'Navigator',
                                      'Mark LT',
                                      'MKC',
                                      'MKS']}
    for x in range(15):
        vin = random.randint(100, 999)
        owner = random.choice(Seller.objects.all())
        keys = [key for key in make_model_choices.keys()]
        make = random.choice(keys)
        model = random.choice(make_model_choices[make])
        years = [year for year in range(1950, 2014)]
        year = random.choice(years)

        vehicle = add_vehicle(vin, owner, make, model, year)
    print("... Vehicles added.")

    print("Creating Inspections...")
    now = datetime.datetime.now()
    comment_choices = ['Good',
                       'Bad',
                       'Everything is broken',
                       'Best vehicle ever.',
                       'Something is broken.',
                       'Incredible.',
                       'Kill this car with fire.',
                       'Alright']
    for x in range(15):
        mechanics = Mechanic.objects.all()
        mech = random.choice(mechanics)
        vehicles = Vehicle.objects.all()
        vehicle = random.choice(vehicles)
        comment = random.choice(comment_choices)
        inspection = add_inspection(x-1, mech, vehicle, comment, now, 0)
    print("... Inspections added.\n")

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
    try:
        vehicle = Vehicle.objects.get(vin=vin)
        print("Already exists, vehicle:", vehicle)
        return vehicle
    except:
        pass

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
        print(vehicle.__str__() + ' ' + vehicle.owner.__str__())


if __name__ == '__main__':
    print("Starting NoLemon database population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'no_lemon.settings')
    from inspections.models import Seller, Mechanic, \
        Inspection, Vehicle
    populate()
    print("Finished populate script.")
