from django.urls import path
from .views import health,FlightList,BookingCreate,booking_lookup
urlpatterns=[path('health/',health),path('flights/',FlightList.as_view()),path('bookings/',BookingCreate.as_view()),path('bookings/<str:reference>/',booking_lookup)]
