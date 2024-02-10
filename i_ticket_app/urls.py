from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

app_name = "i_ticket_app"

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_event, name='add_event'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('buy/<int:event_id>/', views.buy_tickets, name='buy_tickets'),
    path('register/', views.register_view, name='register'),
    path("logout/", views.custom_logout, name="logout"),
    path("login/",LoginView.as_view(
            template_name="i_ticket_app/login.html",
            next_page="i_ticket_app:index",
            redirect_authenticated_user=True
        ),
        name="login",
    ),   
]
