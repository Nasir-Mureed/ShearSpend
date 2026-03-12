from django.shortcuts import render , redirect
from .models import Expenses
from Partners.models import Partner
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='Authentication:login')
def add_expense(request):
    if request.method == 'POST':
        expense=request.POST
        description=expense.get('description')
        amount=expense.get('amount')
        partner_id=expense.get('partner')

        partner=Partner.objects.get(id=partner_id)
        
        Expenses.objects.create(user=request.user, description=description, amount=amount,partner=partner)
        return redirect( 'Dashboard:dashboard')     

    return render(request, 'Expenses/addExpense.html' , {'partners': Partner.objects.filter(user_id=request.user.id) })

# def expense_list(request):
#     return render(request, 'Expenses/expense_list.html')

@login_required(login_url='Authentication:login')
def edit_expense(request, expense_id):
    if request.method == 'POST':
        expense=request.POST
        description=expense.get('description')
        amount=expense.get('amount')
        partner_id=expense.get('partner')

        partner=Partner.objects.get(id=partner_id)
        
        Expenses.objects.filter(id=expense_id).update(user=request.user, description=description, amount=amount,partner=partner)
        return redirect( 'Dashboard:dashboard')
    
    expense = Expenses.objects.get(id=expense_id)
    partners = Partner.objects.filter(user_id=request.user.id)
    return render(request, 'Expenses/editExpense.html', {'expense': expense, 'partners': partners})


@login_required(login_url='Authentication:login')
def remove_expense(request, expense_id):
    Expenses.objects.filter(id=expense_id).delete()
    return redirect( 'Dashboard:dashboard')