# models.py
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
import logging
from smtplib import SMTPException



class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('cashier', 'Cashier'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cashier')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name} "


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural='Categories'


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit
    quantity = models.PositiveIntegerField(default=0)  # Total number of items in stock
    low_stock_threshold = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.category})"

class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    transaction_type = models.CharField(
        max_length=10, 
        choices=[('ADD', 'Add Stock'), ('REMOVE', 'Remove Stock'), ('UPDATE', 'Update Stock')]
    )
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.transaction_type} - {self.product.name} by {self.employee.username}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # Quantity sold
    timestamp = models.DateTimeField(default=now)  # When the item was sold

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity} sold"

# models Table to store to selling Items By Revenue and By Quantity


class ReceiverEmail(models.Model):
    admin_email = models.EmailField()

    def __str__(self):
        return self.admin_email



class LowStockNotification(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)  # Allows marking alerts as resolved

    def __str__(self):
        return f"Low Stock Alert for {self.product.name} - Created: {self.created_at}"
