# Creates Package class
class Package:
    def __init__(self, id, address, city, state, zipcode, deadline, weight, special_notes):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes
        self.departure_time = None
        self.delivery_time = None

    # Returns a string value of the Packages' attributes
    def __str__(self):
        return f"{self.id}, {self.address}, {self.city}, {self.state}, {self.zipcode}, {self.deadline}, {self.weight}, {self.delivery_time}, {self.status}"

    # Updates the time status of packages
    def package_status(self, convert_time):
        if self.delivery_time < convert_time:
            self.status = f"left the hub at {self.departure_time} and was delivered"
        elif self.departure_time < convert_time:
            self.status = f"left the hub at {self.departure_time} is en route"
        else:
            self.status = f"is at the hub. It will depart at {self.departure_time} and is estimated to be delivered"