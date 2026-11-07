import uuid
from django.conf import settings
from django.db import models

class Flight(models.Model):
 origin=models.CharField(max_length=3,db_index=True)
 destination=models.CharField(max_length=3,db_index=True)
 airline=models.CharField(max_length=120)
 flight_number=models.CharField(max_length=20)
 departure=models.DateTimeField(db_index=True)
 arrival=models.DateTimeField()
 price=models.DecimalField(max_digits=10,decimal_places=2)
 currency=models.CharField(max_length=3,default='USD')
 seats_available=models.PositiveIntegerField(default=0)
 active=models.BooleanField(default=True)
 def __str__(self):return f'{self.flight_number}: {self.origin} → {self.destination}'

class Booking(models.Model):
 class Status(models.TextChoices):
  PENDING='pending','Pending';CONFIRMED='confirmed','Confirmed';CANCELLED='cancelled','Cancelled'
 reference=models.CharField(max_length=12,unique=True,editable=False,default='')
 flight=models.ForeignKey(Flight,on_delete=models.PROTECT,related_name='bookings')
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
 passenger_name=models.CharField(max_length=150)
 passenger_email=models.EmailField()
 passenger_count=models.PositiveSmallIntegerField(default=1)
 total=models.DecimalField(max_digits=12,decimal_places=2)
 currency=models.CharField(max_length=3,default='USD')
 status=models.CharField(max_length=12,choices=Status.choices,default=Status.PENDING)
 created_at=models.DateTimeField(auto_now_add=True)
 def save(self,*args,**kwargs):
  if not self.reference:self.reference=uuid.uuid4().hex[:12].upper()
  super().save(*args,**kwargs)
 def __str__(self):return self.reference

class Payment(models.Model):
 class Status(models.TextChoices):
  UNPAID='unpaid','Unpaid';PENDING='pending','Pending';PAID='paid','Paid';FAILED='failed','Failed';REFUNDED='refunded','Refunded'
 booking=models.OneToOneField(Booking,on_delete=models.PROTECT,related_name='payment')
 provider=models.CharField(max_length=32,default='sandbox')
 status=models.CharField(max_length=12,choices=Status.choices,default=Status.UNPAID)
 provider_reference=models.CharField(max_length=200,blank=True)
 updated_at=models.DateTimeField(auto_now=True)
