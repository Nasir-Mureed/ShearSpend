from django.urls import path 
from . import views

app_name = 'Partners'

urlpatterns = [
    path('add/', views.add_partner, name='add_partner'),
    path('remove/<int:partner_id>/', views.remove_partner, name='remove_partner'),
]