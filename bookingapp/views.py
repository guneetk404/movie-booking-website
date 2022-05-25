from datetime import datetime
import re
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import JsonResponse
from bookingapp.models import BookedSeat, Booking, Cinema, Movie, Contact, Seat
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from bookingapp.serializer import SeatSerializer,BookedSeatSerializer
from bookingapp.utils import emailsending, send_password_reset_link
import jwt

# Create your views here.


# function to display recent released movies and homepage to user
def index(request):
    movies = Movie.objects.all()[:3]
    context = {'movies': movies}
    return render(request, 'bookingapp/index.html', context)

# function to fetch one movie at each time


def movie_detail(request, query):
    try:
        movie = Movie.objects.get(id=query)
        context = {'movie': movie}
        return render(request, 'bookingapp/movie_detail.html', context)
    except Exception as e:
        return redirect('/')

# function to handle about reqest and post form request for contact us


def about(request):
    if request.method == 'POST':
        try:
            contact = Contact(fname=request.POST['fname'], lname=request.POST['lname'], email=request.POST['email'],
                              phone=request.POST['phone'], query=request.POST['query'], desc=request.POST['desc'])
            contact.save()
            return render(request, 'bookingapp/about.html', {'success': 'Your query has been sent successfully'})
        except Exception as e:
            return redirect('/')
    return render(request, 'bookingapp/about.html')

# function to load all the movies and paginate them


def films(request):
    movies = Movie.objects.all().order_by('updated_at')
    paginator = Paginator(movies, 9)  # Show 10 movies per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'bookingapp/films.html', {'movies': page_obj})

# function to handle experince page requrest


def experience(request):
    return render(request, 'bookingapp/experience.html')

# function to handle all the cinema halls


def cinema_halls(request, query):
    movie = Movie.objects.get(id=query)
    cinemas = Cinema.objects.all()
    return render(request, 'bookingapp/cinemalist.html', {'movie': movie, 'cinemas': cinemas})

# function to handle login of user


def login(request):
    if request.method == 'POST':
        try:
            email = request.POST['email'].lower()
            password = request.POST['password']
            username = User.objects.filter(email=email).first()
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/')
            return render(request, 'bookingapp/login.html', {'error': 'Invalid credentials'})
        except Exception as e:
            print(e)
            return render(request, 'bookingapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'bookingapp/login.html')


# function to handle login of user
def signup(request):
    if request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']
        password2 = request.POST['password2']
        if not password == password2:
            return render(request, 'bookingapp/signup.html', {'error': 'Passwords do not match'})
        check = User.objects.filter(email=email).first()
        if check is not None:
            return render(request, 'bookingapp/signup.html', {'error': 'Email already exists'})
        user = User.objects.create_user(
            username=email, email=email, password=password)
        user.save()
        return redirect('/login')
    return render(request, 'bookingapp/signup.html')

# function to handle login of user


def checkout(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('/login')
        cinema = Cinema.objects.get(id=request.POST['cinema'])
        movie = Movie.objects.get(id=request.POST['movie'])
        now = datetime.now()
        context = {
            'cinema': request.POST['cinema'],
            'cname': cinema.name,
            'caddress': cinema.address,
            'cfare': cinema.fare,
            'totalfare': cinema.fare * int(len(request.POST.getlist('seats'))),
            'totalseats': len(request.POST.getlist('seats')),
            'movie': movie.id,
            'title': movie.title,
            'date': now.strftime("%Y-%m-%d"),
            'time': now.strftime("%H:%M:%S"),
            'seats': request.POST.getlist('seats'),
        }
        return render(request, 'bookingapp/checkout.html', {'checkout': context})
    return redirect('/')

# function to handle logout


def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('/')

# function to display booking page


def booking(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    bookings = Booking.objects.filter(user=request.user).order_by('updated_at')
    seats = BookedSeat.objects.filter(booking__in=bookings)
    paginator = Paginator(bookings, 5)  # Show 10 movies per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'bookingapp/booking.html', {'bookings': page_obj, 'seats': seats})

# function to handle ajax request for confirm the booking of seats


def confirm_booking(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                bookingno = random_with_n_digits()
                title = request.POST['title']
                cname = request.POST['cname']
                caddress = request.POST['caddress']
                date = request.POST['date']
                time = request.POST['time']
                cfare = request.POST['cfare']
                totalseats = request.POST['totalseats']
                totalfare = request.POST['totalfare']
                seats = request.POST.getlist('seats')
                movie = request.POST['movie']
                cinema = request.POST['cinema']
                cinema = Cinema.objects.get(id=cinema)
                movie = Movie.objects.get(id=movie)
                a = seats[0].replace('\'', '')
                a = a.replace('[', '')
                a = a.replace(']', '')
                a = a.replace(' ', '')
                a = a.split(',')
                create_booking = Booking(user=request.user, title=title, cname=cname, caddress=caddress, date=date, time=time,cfare=cfare, totalseats=totalseats, totalfare=totalfare, seats=seats, movie=movie, cinema=cinema, bookingno=bookingno)
                create_booking.save()
                for item in a:
                    seat = Seat.objects.get(seatno=item,cinema=cinema)
                    book = BookedSeat(booking=create_booking,seat=seat,date=date,cinema=cinema,movie=movie)
                    book.save()
                return JsonResponse({'message': True})
            except Exception as e:
                print(e)
                return JsonResponse({'message': False})
    return redirect('/')


# function to generate random numbers for booking refernce
def random_with_n_digits():
    import random
    range_start = 10**(10-1)
    range_end = (10**10)-1
    return random.randint(range_start, range_end)

def seat_availability(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            movie = Movie.objects.get(id=request.POST['movie'])
            cinema = Cinema.objects.get(id=request.POST['cinema'])
            now = datetime.now()
            bookedseats = BookedSeat.objects.filter(date=now.strftime("%Y-%m-%d"),movie=movie,cinema=cinema)
            seats = Seat.objects.filter(cinema=cinema)
            seats = SeatSerializer(seats, many=True)
            bookedseats = BookedSeatSerializer(bookedseats, many=True)
            return JsonResponse({'seats': seats.data, 'bookedseats': bookedseats.data})
        

def passwordreset(request):
    if request.method =='POST':
        try:
            email = request.POST['email'].lower()
            user = User.objects.get(email=email)
            if user is not None:
                send_password_reset_link(request, user)
                return render(request, 'bookingapp/passwordreset.html', {'message': 'Password reset link has been sent to your email'})
        except Exception as identifier:
            print(identifier)
            return render(request, 'bookingapp/passwordreset.html', {'message': 'Password reset link has been sent to your email'})
    return render(request, 'bookingapp/passwordreset.html')

def verify_email_link(request):
    if request.method == 'GET':
        return render(request, 'bookingapp/changepassword.html')
    
    if request.method == 'POST':
        try:
            token = request.POST['token']
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'], issuer=None, audience=None, verify=True)
            user = User.objects.get(id=payload['user_id'])
            if user is not None:
                password = request.POST['password']
                password2 = request.POST['password2']
                if len(password)<8:
                    return render(request, 'bookingapp/changepassword.html', {'error': 'Password must be atleast 8 characters long'})
                if password != password2:
                    return render(request, 'bookingapp/changepassword.html', {'error': 'Passwords do not match'})
                user.set_password(password)
                user.save()
                return redirect('/login')
            return render(request, 'bookingapp/changepassword.html', {'error': 'Link Expired'})
        except jwt.ExpiredSignatureError as identifier:
            return render(request, 'bookingapp/changepassword.html', {'error': 'Link Expired'})
        except jwt.exceptions.DecodeError as identifier:
            return render(request, 'bookingapp/changepassword.html', {'error': 'Link Expired'})
        except Exception as identifier:
            print(identifier)
            return render(request, 'bookingapp/changepassword.html', {'error': 'Link Expired'})