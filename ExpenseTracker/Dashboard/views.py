from django.shortcuts import render , redirect
from django.contrib.auth import login
from operator import attrgetter # to sort expenses by date
from Expenses.models import Expenses
from Partners.models import Partner

# Create your views here.
def home_view(request):
    return render(request, 'Dashboard/home.html')


#@login_required

def dashboard_view(request):
    expenses_list=Expenses.objects.filter(user_id=request.user.id)
    sorted_expenses = sorted(expenses_list,  key=attrgetter('created_at'), reverse=True)
    partners_list=Partner.objects.filter(user_id=request.user.id)
    total_expenses = 0
    budget_list={}
    for expense in sorted_expenses:
        total_expenses += expense.amount
        if expense.partner.name in budget_list:
            budget_list[expense.partner.name] += expense.amount
        else:
            budget_list[expense.partner.name] = expense.amount
    
    return render(request, 'Dashboard/dashboard.html' , {'Expenses_list': sorted_expenses , 'Partners_list': partners_list ,'total_budget' : total_expenses , 'budget_list' : budget_list })