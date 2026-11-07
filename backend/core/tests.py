from datetime import timedelta
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from .models import Flight,Booking
class BookingTests(TestCase):
 def setUp(self):
  self.client=APIClient()
  self.flight=Flight.objects.create(origin='DAC',destination='DXB',airline='Test Air',flight_number='TA100',departure=timezone.now()+timedelta(days=2),arrival=timezone.now()+timedelta(days=2,hours=5),price=Decimal('120.00'),seats_available=2)
 def test_booking_and_inventory(self):
  payload={'flight':self.flight.id,'passenger_name':'Test Passenger','passenger_email':'test@example.com','passenger_count':2}
  response=self.client.post('/api/bookings/',payload,format='json')
  self.assertEqual(response.status_code,201)
  self.assertEqual(Booking.objects.get().total,Decimal('240.00'))
  self.flight.refresh_from_db();self.assertEqual(self.flight.seats_available,0)
  self.assertEqual(self.client.post('/api/bookings/',payload,format='json').status_code,400)
