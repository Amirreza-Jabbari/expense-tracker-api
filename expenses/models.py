from django.db import models
from django.conf import settings

class Expense(models.Model):
    CATEGORY_CHOICES = (
        ('Groceries', 'Groceries'),
        ('Leisure', 'Leisure'),
        ('Electronics', 'Electronics'),
        ('Utilities', 'Utilities'),
        ('Clothing', 'Clothing'),
        ('Health', 'Health'),
        ('Others', 'Others'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='Others'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.category})"
