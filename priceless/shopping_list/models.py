from django.db import models
from accounts.models import CustomUser
from search.models import SupermarketProducts


# Create your models here.

class ShoppingListItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(SupermarketProducts, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    supermarket_name = models.CharField(max_length=100, default="")
    product_price = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username}'s {self.product.product_name} ({self.quantity})"
