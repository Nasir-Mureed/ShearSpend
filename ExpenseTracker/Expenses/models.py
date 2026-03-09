from django.db import models
from django.utils import timezone
from Partners.models import Partner
from django.contrib.auth.models import User

# Create your models here.

class Expenses(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    partner= models.ForeignKey(Partner, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    description=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.description
