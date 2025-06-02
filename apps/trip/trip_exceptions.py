from excption import Exception

class NotFoundError(Exception):
    pass

class TripDestinationError(Exception):
    """ Raised when multiple trips with the same destination are found """

    def __init__(self, destination):
        super().__init__(f"Error. Found multiple trips with same destination '{destination}'")
        self.destination = destination
    
class DuplicateTripCreationError(Exception):
        """ Raised when attempting to create a trip with same id as an existing one """

    def __init__(self, trip_id):
        super().__init__(f"Trip with id '{trip_id}' already exists!")
        self.trip_id = trip_id
