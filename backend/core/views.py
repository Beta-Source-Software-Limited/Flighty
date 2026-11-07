from datetime import datetime,time,timedelta
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from rest_framework import generics,status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Flight,Booking,Payment
from .serializers import FlightSerializer,BookingSerializer

@api_view(['GET'])
def health(request):return Response({'status':'ok','mode':'sandbox'})
class FlightList(generics.ListAPIView):
 serializer_class=FlightSerializer
 def get_queryset(self):
  qs=Flight.objects.filter(active=True,seats_available__gt=0,departure__gte=timezone.now()).order_by('departure')
  for key in ['origin','destination']:
   value=self.request.query_params.get(key,'').strip().upper()
   if value:qs=qs.filter(**{key:value})
  date=self.request.query_params.get('date')
  if date:
   try:day=datetime.strptime(date,'%Y-%m-%d').date()
   except ValueError:raise ValidationError({'date':'Use YYYY-MM-DD.'})
   qs=qs.filter(departure__date=day)
  return qs[:100]
class BookingCreate(generics.CreateAPIView):
 serializer_class=BookingSerializer
 def perform_create(self,serializer):
  flight_id=serializer.validated_data['flight'].pk
  count=serializer.validated_data['passenger_count']
  with transaction.atomic():
   flight=Flight.objects.select_for_update().get(pk=flight_id)
   if not flight.active or flight.departure<=timezone.now() or flight.seats_available<count:
    raise ValidationError({'flight':'Flight is no longer available.'})
   booking=serializer.save(total=flight.price*count,currency=flight.currency,user=self.request.user if self.request.user.is_authenticated else None)
   Flight.objects.filter(pk=flight.pk).update(seats_available=F('seats_available')-count)
   Payment.objects.create(booking=booking)

@api_view(['GET'])
def booking_lookup(request,reference):
 email=request.query_params.get('email','').strip()
 if not email:return Response({'detail':'Email is required.'},status=400)
 booking=Booking.objects.filter(reference=reference.upper(),passenger_email__iexact=email).first()
 if not booking:return Response({'detail':'Booking not found.'},status=404)
 return Response(BookingSerializer(booking).data)
