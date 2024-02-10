from django.db import models
from django.contrib.auth.models import User as DjangoUser

class Location(models.Model):
    Name = models.CharField(max_length=100)
    Capacity = models.IntegerField()

    def __str__(self):
        return self.Name

class Category(models.Model):
    Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Name

class Event(models.Model):
    Name = models.CharField(max_length=100)
    Date = models.DateField()
    Location = models.ForeignKey(Location, on_delete=models.CASCADE)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    AvailableTickets = models.IntegerField()


class TicketAvailability(models.Model):
    Event = models.ForeignKey(Event, on_delete=models.CASCADE)
    Location = models.ForeignKey(Location, on_delete=models.CASCADE)
    AvailableTickets = models.IntegerField()

class Order(models.Model):
    User = models.ForeignKey(DjangoUser, on_delete=models.CASCADE)
    Event = models.ForeignKey(Event, on_delete=models.CASCADE)
    OrderDate = models.DateField()
    Quantity = models.IntegerField()