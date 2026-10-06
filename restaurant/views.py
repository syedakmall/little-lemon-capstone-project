from datetime import datetime, time, timedelta

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_date
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from .forms import BookingForm
from .models import Booking, Menu
from .permissions import IsStaffOrReadOnly
from .serializers import BookingSerializer, MenuSerializer


class MenuItemsView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    search_fields = ['title']
    ordering_fields = ['title', 'price', 'inventory']


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    search_fields = ['name']
    ordering_fields = ['booking_date', 'number_of_guests']


def home(request):
    return render(request, 'restaurant/index.html')


def about(request):
    return render(request, 'restaurant/about.html')


def menu(request):
    return render(request, 'restaurant/menu.html', {'menu': Menu.objects.all()})


def menu_item(request, pk):
    return render(request, 'restaurant/menu_item.html', {'item': get_object_or_404(Menu, pk=pk)})


def book(request):
    form = BookingForm(request.POST or None)
    if form.is_valid():
        booking = form.save()
        messages.success(
            request,
            f'Thanks {booking.name}, your table for {booking.number_of_guests} is booked.',
        )
        return redirect('book')
    return render(request, 'restaurant/book.html', {'form': form})


@staff_member_required
def reservations(request):
    day = parse_date(request.GET.get('date', '')) or timezone.localdate()
    start = timezone.make_aware(datetime.combine(day, time.min))
    bookings = Booking.objects.filter(booking_date__gte=start, booking_date__lt=start + timedelta(days=1))
    return render(request, 'restaurant/reservations.html', {'bookings': bookings, 'day': day})
