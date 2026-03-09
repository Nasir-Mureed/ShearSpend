from django.urls import path 
from . import views

app_name = 'Expenses'

urlpatterns = [
    path('add/', views.add_expense, name='add_expense'),
    # path('list/', views.expense_list, name='expense_list'),
    path('edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    # path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('remove/<int:expense_id>/', views.remove_expense, name='remove_expense'),
]