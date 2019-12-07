import requests

class BadResponseError(Exception):
    pass

class Client:

    def __init__(self, token, client_secret, client_id):
        self.token = token
        self.secret = client_secret
        self.id = client_id
        self.roombookings = self.roombookings(self)

    class roombookings:

        def __init__(self, client):
            self.client = client

        def rooms(self, **kwargs):
            params = kwargs
            params["token"] = self.client.token

            result = requests.get("https://uclapi.com/roombookings/rooms", params=params)
            rooms = []
            result = result.json()
            if not result["ok"]:
                raise BadResponseError
            for room in result["rooms"]:
                rooms.append(Room(room))
            return rooms

        def bookings(self, **kwargs):
            params = kwargs
            params["token"] = self.client.token

            result = requests.get("https://uclapi.com/roombookings/bookings", params=params).json()
            bookings = []
            if not result["ok"]:
                raise BadResponseError
            return Bookings(result["bookings"])

        def equipment(self, **kwargs):
            params = kwargs
            params["token"] = self.client.token

            result = requests.get("https://uclapi.com/roombookings/equipment", params=params).json()
            equipments = []
            if not result["ok"]:
                raise BadResponseError
            for equipment in result["equipment"]:
                equipments.append(Equipment(equipment))
            return equipments

class Bookings:
    def __init__(self, bookings):
        self.bookings = []
        for booking in bookings:
            self.bookings.append(Booking(booking))

    def __iter__():
        pass

class Room:
    def __init__(self, room):
        self.roomname = room["roomname"]
        self.roomid = room["roomid"]
        self.siteid = room["siteid"]
        self.sitename = room["sitename"]
        self.capacity = room["capacity"]
        self.classification = room["classification"]
        self.classification_name = room["classification_name"]
        self.automated = room["automated"]
        self.location = Location(room["location"])

    def get_bookings(self, client, **kwargs):
        return client.roombookings.bookings(siteid=self.siteid, roomid=self.roomid, **kwargs)

    def get_equipment(self, client, **kwargs):
        return client.roombookings.equipment(siteid=self.siteid, roomid=self.roomid, **kwargs)

class Location:
    def __init__(self,location):
        if "coordinates" in location:
            self.coordinates = location["coordinates"]
        else:
            self.coordinates = None
        if "address" in location:
            self.address = location["address"]
        else:
            self.address = None

class Booking:
    def __init__(self, booking):
        self.slotid = booking["slotid"]
        self.end_time = booking["end_time"]
        self.description = booking["description"]
        self.roomname = booking["roomname"]
        self.siteid = booking["siteid"]
        self.contant = booking["contact"]
        self.weeknumber = booking["weeknumber"]
        self.roomid = booking["roomid"]
        self.start_time = booking["start_time"]
        self.phone = booking["phone"]

    def get_room(self, client):
        return client.roombookings.rooms(siteid=self.siteid,roomid=self.roomid)[0]

    def get_equipment(self, client, **kwargs):
        return client.roombookings.equipment(siteid=self.siteid, roomid=self.roomid, **kwargs)

class Equipment:
    def __init__(self, equipment):
        self.type = equipment["type"]
        self.description = equipment["description"]
        self.units = equipment["units"]
