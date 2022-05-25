from django.urls import path
from bookingapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movie_detail/<str:query>', views.movie_detail, name='movie_detail'),
    path('about/', views.about, name='about'),
    path('films/', views.films, name='films'),
    path('experience/', views.experience, name='experience'),
    path('cinema_halls/<str:query>', views.cinema_halls, name='cinema_halls'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('checkout/', views.checkout, name='checkout'),
    path('logout/', views.logout, name='logout'),
    path('bookings/', views.booking, name='booking'),
    path('confirm_booking/', views.confirm_booking, name='confirm_booking'),
    path('seat_availability/', views.seat_availability, name='seat_availability'),
    path('passwordreset/', views.passwordreset, name='passwordreset'),
    path('changepassword/', views.verify_email_link, name='verify_email_link'),
]
