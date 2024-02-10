from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from .models import Event, Category, Location, TicketAvailability, Order
from .forms import EventForm, CustomUserCreationForm, BuyTicketsForm

def index(request):
    events = Event.objects.all()
    for event in events:
        category = Category.objects.get(pk=event.Category_id)
        location = Location.objects.get(pk=event.Location_id)
        event.category_name = category.Name
        event.location_name = location.Name
    return render(request, 'i_ticket_app/index.html', {'events': events})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('i_ticket_app:index')
    return render(request, 'i_ticket_app/login.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('i_ticket_app:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'i_ticket_app/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('i_ticket_app:index')

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            location = event.Location
            if event.AvailableTickets > location.Capacity:
                form.add_error('AvailableTickets', f'Ilość dostępnych miejsc nie może przekraczać {location.Capacity}')
            else:
                event.save()
                TicketAvailability.objects.create(Event=event, Location=location, AvailableTickets=event.AvailableTickets)
                return redirect('i_ticket_app:index')
    else:
        form = EventForm()
    return render(request, 'i_ticket_app/add_event.html', {'form': form})

def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            location = event.Location
            if event.AvailableTickets > location.Capacity:
                form.add_error('AvailableTickets', f'Ilość dostępnych miejsc nie może przekraczać {location.Capacity}')
            else:
                event.save()
                return redirect('i_ticket_app:index')
    else:
        form = EventForm(instance=event)
    return render(request, 'i_ticket_app/edit_event.html', {'form': form})

def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('i_ticket_app:index')
    return render(request, 'i_ticket_app/delete_event.html', {'event': event})

def buy_tickets(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    ticket_availability = get_object_or_404(TicketAvailability, Event=event)

    if request.method == 'POST':
        form = BuyTicketsForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['Quantity']
            if 0 < quantity <= ticket_availability.AvailableTickets:
                user = request.user
                order_date = timezone.now()
                Order.objects.create(User=user, Event=event, OrderDate=order_date, Quantity=quantity)
                
                ticket_availability.AvailableTickets -= quantity
                ticket_availability.save()

                event.AvailableTickets -= quantity
                event.save()

                return redirect('i_ticket_app:index')
    else:
        form = BuyTicketsForm()

    return render(request, 'i_ticket_app/buy_tickets.html', {'event': event, 'ticket_availability': ticket_availability, 'form': form})