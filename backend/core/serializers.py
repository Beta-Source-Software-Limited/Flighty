from rest_framework import serializers
from .models import Flight,Booking
class FlightSerializer(serializers.ModelSerializer):
 class Meta:
  model=Flight;fields=['id','origin','destination','airline','flight_number','departure','arrival','price','currency','seats_available']
class BookingSerializer(serializers.ModelSerializer):
 flight_detail=FlightSerializer(source='flight',read_only=True)
 class Meta:
  model=Booking;fields=['reference','flight','flight_detail','passenger_name','passenger_email','passenger_count','total','currency','status','created_at']
  read_only_fields=['reference','total','currency','status','created_at']
 def validate_passenger_count(self,value):
  if not 1<=value<=9:raise serializers.ValidationError('Select 1 to 9 passengers.')
  return value
