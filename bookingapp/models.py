from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Cinema(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    fare = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    year = models.IntegerField()
    duration = models.CharField(max_length=255, default='1h')
    image = models.ImageField(upload_to='images/')
    type = models.CharField(max_length=255, default='Drama')
    release = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Contact(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.IntegerField()
    query = models.TextField()
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Booking(models.Model):
    bookingno = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    cname = models.CharField(max_length=255)
    caddress = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    cfare = models.IntegerField()
    totalseats = models.IntegerField()
    totalfare = models.IntegerField()
    seats = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Seat(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    seatno = models.CharField(max_length=255) 

class BookedSeat(models.Model):
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat,on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField()