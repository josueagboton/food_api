from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class FoodCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.name
    
class Food(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    foodCategory = models.ForeignKey(FoodCategory, on_delete =models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"Order #{self.pk} - Date: {self.date_ordered}, Total: {self.total_price}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='item', on_delete=models.CASCADE )
    food = models.ForeignKey(Food, on_delete= models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"Order #{self.order.pk} - {self.food.name} ({self.quantity})"
    
    def save(self, *args, **kwargs):
        # Calcul du prix en fonction de la quantité
        self.price = self.food.price * self.quantity
        super().save(*args, **kwargs)
