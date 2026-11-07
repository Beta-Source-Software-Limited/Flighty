from django.contrib import admin
from .models import Flight,Booking,Payment
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
 list_display=('flight_number','airline','origin','destination','departure','price','seats_available','active')
 list_filter=('active','airline','origin','destination')
 search_fields=('flight_number','airline')
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
 list_display=('reference','flight','passenger_name','passenger_email','passenger_count','total','status','created_at')
 list_filter=('status',);search_fields=('reference','passenger_email')
 readonly_fields=('reference','total','currency','created_at')
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
 list_display=('booking','provider','status','updated_at')
 list_filter=('status','provider')
