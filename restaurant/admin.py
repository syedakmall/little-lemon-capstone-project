from django.contrib import admin

from .models import Booking, Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'inventory']
    search_fields = ['title']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'number_of_guests', 'booking_date']
    list_filter = ['booking_date']
    search_fields = ['name']
    date_hierarchy = 'booking_date'
