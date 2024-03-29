import requests
import pytz
import datetime
from collections import namedtuple


class BadResponseError(Exception):
    pass

class Client:

    def __init__(self, token, client_secret=None, client_id=None):
        self.token = token
        self.secret = client_secret
        self.id = client_id
        self.roombookings = self.roombookings(self)
        self.search = self.search(self)
        self.resources = self.resources(self)
        self.workspaces = self.workspaces(self)

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

        def freerooms(self, start_datetime, end_datetime):
            start = start_datetime.astimezone(pytz.utc)
            end = end_datetime.astimezone(pytz.utc)
            params = {}
            params["token"] = self.client.token
            params["start_datetime"] = start.isoformat()
            params["end_datetime"] = end.isoformat()

            result = requests.get("https://uclapi.com/roombookings/freerooms", params=params).json()
            if not result["ok"]:
                raise BadResponseError
            free_rooms = []
            for room in result["free_rooms"]:
                free_rooms.append(Room(room))
            return free_rooms

    class search:

        def __init__(self, client):
            self.client = client

        def people(self, query):
            params = {"query":query}
            params["token"] = self.client.token
            result = requests.get("https://uclapi.com/search/people", params=params).json()
            if not result["ok"]:
                raise BadResponseError
            people = []
            for person in result["people"]:
                people.append(Person(person))
            return people

    class resources:

        def __init__(self, client):
            self.client = client

        def desktops(self):
            params = {}
            params["token"] = self.client.token
            result = requests.get("https://uclapi.com/resources/desktops", params=params).json()
            if not result["ok"]:
                raise BadResponseError
            desktops = []
            for desktop in result["data"]:
                desktops.append(Desktop(desktop))
            return desktops

    class workspaces:

        def __init__(self, client):
            self.client = client
            self.sensors = self.sensors(client)

        def surveys(self, survey_filter="student"):
            params = {}
            params["token"] = self.client.token
            params["survey_filter"] = survey_filter
            result = requests.get("https://uclapi.com/workspaces/surveys", params=params).json()
            if not result["ok"]:
                raise BadResponseError
            surveys = []
            for survey in result["data"]:
                surveys.append(Survey(survey))
            return surveys

        class sensors:

            def __init__(self, client):
                self.client = client

                Averages = namedtuple('Averages', 'time')
                self.averages = Averages(self.averages_time)

            def __call__(self, survey_id, return_states="false"):
                params = {}
                params["token"] = self.client.token
                params["survey_id"] = survey_id
                params["return_states"] = return_states
                result = requests.get("https://uclapi.com/workspaces/sensors", params=params).json()
                if not result["ok"]:
                    raise BadResponseError
                maps = []
                for map in result["maps"]:
                    maps.append(Map(map))
                return maps

            def averages_time(self, days, **kwargs):
                params = kwargs
                params["days"] = days
                params["token"] = self.client.token
                result = requests.get("https://uclapi.com/workspaces/sensors/averages/time", params=params).json()
                if not result["ok"]:
                    raise BadResponseError
                surveys = []
                for survey in result["surveys"]:
                    surveys.append(Averages(survey))
                return surveys

            def lastupdated(self, survey_id):
                params = {
                    "survey_id": survey_id,
                    "token": self.client.token
                }
                result = requests.get("https://uclapi.com/workspaces/sensors/lastupdated")
                if not result["ok"]:
                    raise BadResponseError
                Result = namedtuple("Result", "last_updated survey_id")
                return Result(result["last_updated"], result["survey_id"])

            

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
        self.contact = booking["contact"]
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

class Person:
    def __init__(self, person):
        self.name = person["name"]
        self.status = person["status"]
        self.department = person["department"]
        self.email = person["email"]

class Desktop:
    def __init__(self, desktop):
        self.room_status = desktop["room_status"]
        self.total_seats = desktop["total_seats"]
        self.free_seats = desktop["free_seats"]
        self.roomname = desktop["location"]["roomname"]
        self.room_id = desktop["location"]["room_id"]
        self.building_name = desktop["location"]["building_name"]
        location = {}
        location["coordinates"] = {"lat": desktop["location"]["latitude"], "lng": desktop["location"]["longitude"]}
        location["address"] = desktop["location"]["address"].split(", ") + [desktop["location"]["postcode"]]
        self.location = Location(location)

class Survey:
    def __init__(self, survey):
        self.id = survey["id"]
        self.name = survey["name"]
        self.active = survey["active"]
        self.start_time = survey["start_time"]
        self.end_time = survey["end_time"]
        self.staff_survey = survey["staff_survey"]
        self.location = Location(survey["location"])
        self.maps = []
        for map in survey["maps"]:
            self.maps.append(Maps(map))

class Map:
    def __init__(self, map):
        self.id = map["id"]
        self.name = map["name"]
        self.image_id = map["image_id"]
        self.sensors = {}
        if "sensors" in map:
            for sensor_id in map["sensors"]:
                self.sensors[sensor_id] = Sensor(sensor_id, map["sensors"][sensor_id])

class Sensor:
    def __init__(self, id, sensor):
        self.id = id
        self.description_2 = sensor["description_2"]
        self.floor = sensor["floor"]
        self.y_pos = sensor["y_pos"]
        self.description_3 = sensor["description_3"]
        self.device_type = sensor["device_type"]
        self.host_address = sensor["host_address"]
        self.building_name = sensor["building_name"]
        self.room_description = sensor["room_description"]
        self.last_trigger_type = sensor["last_trigger_type"]
        self.survey_id = sensor["survey_id"]
        self.room_type = sensor["room_type"]
        self.room_name = sensor["room_name"]
        self.room_id = sensor["room_id"]
        self.location = sensor["location"]
        self.survey_device_id = sensor["survey_device_id"]
        self.share_id = sensor["share_id"]
        self.x_pos = sensor["x_pos"]
        self.description_1 = sensor["description_1"]
        self.hardware_id = sensor["hardware_id"]
        self.pir_address = sensor["pir_address"]
        self.last_trigger_timestamp = sensor["last_trigger_timestamp"]
        self.occupied = sensor["occupied"]

class Averages:
    def __init__(self, averages):
        self.survey_id = averages["survey_id"]
        self.name = averages["name"]
        self.averages = {}
        Sensor_status = namedtuple("Sensor_status", "sensors_absent sensors_total sensors_occupied")
        for average in averages["averages"]:
            self.averages[average] = Sensor_status(averages["averages"][average]["sensors_absent"], averages["averages"][average]["sensors_total"], averages["averages"][average]["sensors_occupied"])
