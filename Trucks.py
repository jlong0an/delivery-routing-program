# Creates Trucks class
class Trucks:
    def __init__(self, id, mileage, speed, packages, load, address, capacity, depart_time):
        self.id = id
        self.mileage = mileage
        self.speed = speed
        self.packages = packages
        self.load = load
        self.capacity = capacity
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time

    # Returns a string value for Trucks' attributes
    def __str__(self):
        return f"{self.id}, {self.capacity}, {self.speed}, {self.load}, {self.packages}, {self.mileage}, {self.address}, {self.depart_time}"
