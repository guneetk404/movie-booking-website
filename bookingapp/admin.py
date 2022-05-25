from django.contrib import admin
from bookingapp.models import Movie,Contact,Cinema,Booking,BookedSeat,Seat

# Register your models here.
admin.site.register(Movie)
admin.site.register(Contact)
admin.site.register(Cinema)
admin.site.register(Booking)
admin.site.register(BookedSeat)
admin.site.register(Seat)