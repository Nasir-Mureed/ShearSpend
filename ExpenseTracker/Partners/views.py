from django.shortcuts import render , redirect
from .models import Partner

# Create your views here.
def add_partner(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Partner.objects.create(name=name, user_id=request.user.id)
        return redirect('Dashboard:dashboard') 
    
    return render(request, 'Partners/addPartner.html')

def remove_partner(request,partner_id):
        Partner.objects.filter(id=partner_id, user_id=request.user.id).delete()
        return redirect('Dashboard:dashboard')