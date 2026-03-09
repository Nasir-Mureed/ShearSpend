from django.db import models

# Create your models here.

class Partner(models.Model):
    user_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name