from uclapyi import Client
import datetime


if __name__ == "__main__":
    client = Client("uclapi-14e9d20943c96b2-7902ccba4ad90f9-c89ccdbb676f08b-ca7829bf6eb21d7", "d5c75f7c34490ad28669161186876848ea556de71a6bbb4567142a53bf81d47e", "6046604012478137.4049789112059384")
    # bookings = client.roombookings.bookings(roomid="433",siteid="086",results_per_page=10)
    # for booking in bookings:
    #     print(booking.description)
    
    # start = datetime.datetime.now()
    # end = datetime.datetime.now() + datetime.timedelta(days=2)
    # freerooms = client.roombookings.freerooms(start,end)
    # print(freerooms[0].roomname)
