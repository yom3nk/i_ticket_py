from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Event, Order

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['Name', 'Date', 'Location', 'Category', 'AvailableTickets']
        labels = {
            'Name': 'Nazwa wydarzenia',
            'Date': 'Data',
            'Location': 'Lokalizacja',
            'Category': 'Kategoria',
            'AvailableTickets': 'Dostępne bilety',
        }
        widgets = {
            'Date': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
        }

class BuyTicketsForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['Quantity']
        labels = {
            'Quantity': 'Liczba biletów',
        }


class CustomUserCreationForm(UserCreationForm):   
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None 
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        self.fields['username'].label = 'Nazwa użytkownika'
        self.fields['password1'].label = 'Hasło'
        self.fields['password2'].label = 'Potwierdź hasło'