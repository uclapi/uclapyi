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
            return Bookings(result, self.client.token)

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
    def __init__(self, result, token):
        self._bookings = []
        self.token = token
        for booking in result["bookings"]:
            self._bookings.append(Booking(booking))
        self._count = result["count"]
        self._current = 0
        self._next_page = result["next_page_exists"]
        if self._next_page:
            self._page_token = result["page_token"]

    def __iter__(self):
        return self

    def __next__(self):
        if self._current == self._count:
            raise StopIteration
        if self._current < len(self._bookings):
            self._current += 1
            return self._bookings[self._current-1]
        else:
            params = {}
            params["token"] = self.token
            params["page_token"] = self._page_token
            result = requests.get("https://uclapi.com/roombookings/bookings", params=params).json()
            self._next_page = result["next_page_exists"]
            if self._next_page:
                self._page_token = result["page_token"]
            for booking in result["bookings"]:
                self._bookings.append(Booking(booking))
            self._current += 1
            return self._bookings[self._current-1]

    def __getitem__(self, index):
        try:
            max_idx = index.stop
        except AttributeError:
            max_idx = index
        n = max_idx - len(self._bookings) + 1
        if n > 0:
            self._bookings.extend(itertools.islice(self, n))
        return self._bookings[index]

    def __len__():
        return self._count

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
