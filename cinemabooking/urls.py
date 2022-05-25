
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

# easy admin modify method
admin.site.site_title = "Booking of tickets become easy"
admin.site.site_header = "Mega Cinema"
admin.site.index_title = "Welcome to Mega Cinema admin panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bookingapp.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
