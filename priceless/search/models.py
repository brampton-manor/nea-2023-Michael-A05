from django.db import models


# Create your models here.
class Supermarkets(models.Model):
    supermarket_name = models.CharField(max_length=100)
    supermarket_logo = models.CharField(max_length=100)
    supermarket_base_url = models.CharField(max_length=100)

    class Meta:
        db_table = 'supermarkets'


class SupermarketCategories(models.Model):
    supermarket = models.ForeignKey(Supermarkets, on_delete=models.CASCADE)
    supermarket_category_name = models.CharField(max_length=100)
    supermarket_category_part_url = models.CharField(max_length=100)

    class Meta:
        db_table = 'supermarket_categories'


class SupermarketProducts(models.Model):
    supermarket_category = models.ForeignKey(SupermarketCategories, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField()
    product_image = models.CharField(max_length=100)
    product_part_url = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField()

    class Meta:
        db_table = 'supermarket_products'


class SupermarketProductDetails(models.Model):
    supermarket_product = models.OneToOneField(SupermarketProducts, on_delete=models.CASCADE)
    energy_kj = models.FloatField()
    energy_kcal = models.FloatField()
    fat = models.FloatField()
    of_which_saturates = models.FloatField()
    carbohydrates = models.FloatField()
    of_which_sugars = models.FloatField()
    fibre = models.FloatField()
    protein = models.FloatField()
    salt = models.FloatField()

    class Meta:
        db_table = 'supermarket_product_details'


class SupermarketProductAllergens(models.Model):
    supermarket_product = models.ForeignKey(SupermarketProducts, on_delete=models.CASCADE)
    allergen = models.CharField(max_length=100)

    class Meta:
        db_table = 'supermarket_product_allergens'
