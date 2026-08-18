from django.db import models
from django.utils import timezone

class Item(models.Model):
    STATUS_CHOICES = [
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
        ('RESOLVED', 'Resolved'),
    ]
    
    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Jewelry', 'Jewelry'),
        ('Documents', 'Documents'),
        ('Clothing', 'Clothing'),
        ('Keys', 'Keys'),
        ('Accessories', 'Accessories'),
        ('Other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='LOST')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    location = models.CharField(max_length=300)
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=100)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lost & Found Item'
        verbose_name_plural = 'Lost & Found Items'
    
    def __str__(self):
        return f"{self.title} - {self.status}"
