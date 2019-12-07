# A python client library for UCL API

What this does is allows easier access to the UCL API, without having to manually deal with HTTP requests yourself. This makes start-up time for developing applications quicker meaning hackathon and prototype projects can be constructed quickly. To install this you can do:
```bash
pip install -e git+git://github.com/uclapi/uclapyi@master#egg=uclapyi
```

# But how do i use it?

Using this package is designed to be simple. The first step is to initialise a client. You can do this by first importing it:
```python
from uclapyi.uclapyi import Client
```
You can then initialise it:
```python
client = Client(token="YOUR-TOKEN-HERE")
```
Now we can make requests by accessing endpoints like functions. For example to get bookings for a room with id 443 and site_id 086 we would do:
```python
bookings = client.roombookings.bookings(roomid="433",siteid="086",results_per_page=10)
```
All pagination is handled for you as a generator and supports indexing. This allows you to do things like:
```python
for booking in bookings:
  print(booking.contact)
  print(booking.get_room().capacity)
  for equipment in booking.get_equipment():
    print(equipment.description)
```
This prints out who booked the room, what the capacity is and the equipment available for each booking in the result of the query. This shows the power of a native client library and how much easier it is to use than raw requests.

# Is there an dis-advantage of this over raw HTTP requests?

This is a good question and yes there is. Since this wrapper makes everything into an object there is a time cost to converting the data into this form. For example when you get bookings we give you a list of Booking objects, which you can query to get the Room object associated with it. This is apposed to just a dictionary of strings and such that the normal endpoint would return in JSON format.
