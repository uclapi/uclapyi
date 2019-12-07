# A python client library for UCL API

What this does is allows easier access to the UCL API, without having to manually deal with HTTP requests yourself. This makes start-up time for developing applications quicker meaning hackathon and prototype projects can be constructed quickly.

# Is there an dis-advantage of this over raw HTTP requests?

This is a good question and yes there is. Since this wrapper makes everything into an object there is a time cost to converting the data into this form. For example when you get bookings we give you a list of Booking objects, which you can query to get the Room object associated with it. This is apposed to just a dictionary of strings and such that the normal endpoint would return in JSON format.
