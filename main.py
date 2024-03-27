# James Long - Student ID: 011476223
from Trucks import Trucks
from HashTable import HashTable
from Package import Package
import csv
import datetime

# Reads the contents of the csv files into a list
with open("csv/Addresses.csv") as csvfile:
    csv_addresses = list(csv.reader(csvfile))

with open("csv/Packages.csv") as csvfile:
    csv_packages = list(csv.reader(csvfile))

with open("csv/Distance.csv") as csvfile:
    csv_distance = list(csv.reader(csvfile))

# Creates package objects using the packages csv file
def load_package_data(filename, package_hash_table):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        for package in package_data:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pStatus = "At Hub"

            p = Package(pID, pAddress, pCity, pState, pZipcode, pDeadline, pWeight, pStatus)

            package_hash_table.insert(pID, p)

# Finds the distance between addresses
def address_distances(x, y):
    distance = csv_distance[x][y] or csv_distance[y][x]
    return float(distance)

# Creates dictionary to store addresses
address_dict = {}

# Populates the address dictionary
for row in csv_addresses:
    address_dict[row[2]] = int(row[0])

# Gets an address id from the address dictionary
def get_address_id(address):
    return address_dict.get(address, None)

# Defines the default truck attributes
default_truck_attributes = {
    "capacity": 16,
    "speed": 18,
    "load": None,
    "mileage": 0.0,
    "address": "4001 South 700 East"
}

# Defines attributes that are specific to each truck
truck_data = [
    {"packages": [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40], "depart_time": datetime.timedelta(hours=8)}, # Truck 1
    {"packages": [3, 6, 12, 17, 18, 21, 22, 23, 24, 25, 26, 27, 35, 36, 38, 39], "depart_time": datetime.timedelta(hours=9, minutes=5)}, # Truck 2
    {"packages": [2, 4, 5, 7, 8, 9, 10, 11, 28, 32, 33], "depart_time": datetime.timedelta(hours=10, minutes=20)} # Truck 3
]

# Creates a hash table
package_hash_table = HashTable()

# Loads packages into the hash table
load_package_data("csv/Packages.csv", package_hash_table)

target_time = datetime.timedelta(10,20)

# Prompt user to enter a specific time
user_time = input("Enter a time to check the status of packages. Use the format: HH:MM ")


# Parse the user input time
try:
    user_hour, user_minute = map(int, user_time.split(":"))
    user_input_time = datetime.timedelta(user_hour, user_minute)

    # Check if user's input time is greater than or equal to 10:20
    if user_input_time >= target_time:
        # Update package 9's address and zipcode
        package_9 = package_hash_table.lookup(9)
        package_38 = package_hash_table.lookup(38)
        package_9.address = package_38.address
        package_9.zipcode = package_38.zipcode

except ValueError:
    print("Invalid time format. Please enter the time in HH:MM format.")

# Delivers packages
def package_delivery(truck):
    # Creates a list of packages that need to be delivered
    not_delivered = [package_hash_table.lookup(packageID) for packageID in truck.packages]
    truck.packages.clear()

    # Checks if there are undelivered packages
    while not_delivered:
        next_address = 2000
        next_package = None
        current_address_id = get_address_id(truck.address)

        # Finds the next package to deliver
        for package in not_delivered:
            package_address_id = get_address_id(package.address)
            distance = address_distances(current_address_id, package_address_id)
            if distance <= next_address:
                next_address = distance
                next_package = package

        # Assign the truck ID to the delivered package
        next_package.truck_id = truck.id

        # Adds nearest package to the truck package list
        truck.packages.append(next_package.id)
        # Removes the package from the not_delivered list
        not_delivered.remove(next_package)
        # Adds miles driven to truck.mileage
        truck.mileage += next_address
        # Updates truck's current address
        truck.address = next_package.address
        # Updates time to the nearest package address
        truck.time += datetime.timedelta(hours=next_address / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time


# List to store truck instances
trucks = []

# Initialize a counter for truck IDs
truck_id_counter = 1

# Creates truck instances to deliver packages
for data in truck_data:
    # Combine default and specific attributes for trucks
    truck_attributes = {**default_truck_attributes, **data, 'id': truck_id_counter}
    # Create truck instance with combined attributes
    truck = Trucks(**truck_attributes)
    # Delivers packages using the truck instance
    package_delivery(truck)
    # Append truck instance to the list
    trucks.append(truck)


class Main:
    while True:
        try:
            # Initialize total mileage
            total_mileage = 0

            # Calculate and print total mileage for all trucks
            for truck in trucks:
                total_mileage += truck.mileage

            # user_time = input("Enter a time to check the status of packages. Use the format: HH:MM ")
            (h, m) = user_time.split(":")

            convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m))

            # Prompt user to choose between solo or all packages
            second_input = input(
                "To view the status of an individual package type 'S'. For all packages type 'A':")

            # If user chooses solo
            if second_input.lower() == "s":
                solo_input = input("Enter the package ID: ")
                package = package_hash_table.lookup(int(solo_input))
                package.package_status(convert_timedelta)
                truck_id = '1 (Driver 1)' if package.departure_time == datetime.timedelta(hours=8) else ('2 (Driver 2)' if package.departure_time == datetime.timedelta(hours=9,minutes=5) else '3 (Driver 1)')
                print(f"Truck {truck_id}: Package {package.id} ({package.weight}) has a deadline of {package.deadline} and {package.status} to {package.address}, {package.city}, {package.state}, {package.zipcode} at {package.delivery_time}")

                # Returns truck to the hub
                if package.id in [30, 12, 8]:
                    return_time = package.delivery_time + datetime.timedelta(minutes=25.2)
                    print(f"Truck {truck_id} returns to the hub at {return_time}")

            # If user chooses all
            elif second_input.lower() == "a":
                # Prompt user to choose sorting option
                sorting_option = input(
                    "You can sort by package ID or estimated delivery time. Enter sorting option: 'id', or 'time': ")

                # Validate sorting option
                if sorting_option.lower() not in ['id', 'time']:
                    print("Invalid sorting option. Closing program.")
                    exit()

                # Get list of all packages
                all_packages = [package_hash_table.lookup(packageID) for packageID in range(1, 41)]

                # Sort packages based on sorting option
                if sorting_option.lower() == 'id':
                    all_packages.sort(key=lambda x: x.id)
                elif sorting_option.lower() == 'time':
                    all_packages.sort(key=lambda x: x.delivery_time)

                # Print sorted packages
                for package in all_packages:
                    package.package_status(convert_timedelta)
                    truck_id = '1 (Driver 1)' if package.departure_time == datetime.timedelta(hours=8) else ('2 (Driver 2)' if package.departure_time == datetime.timedelta(hours=9,minutes=5) else '3 (Driver 1)')
                    print(f"Truck {truck_id}: Package {package.id} ({package.weight}) has a deadline of {package.deadline} and {package.status} to {package.address}, {package.city}, {package.state}, {package.zipcode} at {package.delivery_time}")

                    # If user input time is before 10:20
                    if user_input_time < target_time:
                        if package.id in [30, 12, 9]:
                            return_time = package.delivery_time + datetime.timedelta(minutes=25.2)
                            print(f"Truck {truck_id} returns to the hub at {return_time}")

                    # If user input time is after 10:20
                    if user_input_time > target_time:
                        if package.id in [30, 12, 8]:
                            return_time = package.delivery_time + datetime.timedelta(minutes=25.2)
                            print(f"Truck {truck_id} returns to the hub at {return_time}")

            else:
                print("Invalid option. Shutting program down")
                break

            # Calculate distance back to hub for individual trucks. 30, 12, and 8 are the final packages with each with 7.6 miles to the hub
            for package.id in [30, 12, 8]:
                total_mileage += 7.6

            # Print the final total mileage for all trucks
            print(f"Final mileage for all trucks: {total_mileage:.2f}")

            # Ask user if they want to continue or quit
            option = input("Do you want to continue (C) or quit (Q)? ")

            # If user chooses to quit, exit the loop
            if option.lower() != 'c':
                print("Shutting down.")
                break

        except Exception as e:
            print(f"An error occurred: {e}")
            exit()
