from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Flight
class Command(BaseCommand):
 help='Create sample sandbox flights'
 def handle(self,*args,**kwargs):
  routes=[('DAC','DXB','Emirates','EK585','399'),('DAC','LHR','Biman Bangladesh','BG201','549'),('DAC','JFK','Qatar Airways','QR641','799'),('DAC','SIN','Singapore Airlines','SQ447','329'),('DXB','DAC','Emirates','EK584','385')]
  for day in range(1,31):
   for i,(origin,destination,airline,number,price) in enumerate(routes):
    departure=timezone.now().replace(hour=8,minute=0,second=0,microsecond=0)+timedelta(days=day,hours=i*2)
    Flight.objects.get_or_create(flight_number=number,departure=departure,defaults={'origin':origin,'destination':destination,'airline':airline,'arrival':departure+timedelta(hours=5+i),'price':Decimal(price),'seats_available':35})
  self.stdout.write(self.style.SUCCESS('Sandbox flights seeded.'))
