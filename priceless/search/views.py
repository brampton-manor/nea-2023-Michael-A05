from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import Choice
from .models import Supermarkets, SupermarketCategories, SupermarketProducts, SupermarketProductAllergens

from urllib.parse import urljoin
import itertools


# Create your views here.

def search_view(request):
    if request.method == 'GET':
        query = request.GET.get('query')

        if query:
            # Query the database for products matching the search query
            all_results = SupermarketProducts.objects.filter(product_name__icontains=query).order_by('product_price')

            # Remove duplicates that are caused by products being in multiple distinct categories
            unique_results = []
            seen_pairs = set()

            for result in all_results:
                # Product name and image together are unique as the image contains identifying supermarket link
                pair = (result.product_name, result.product_image)
                if pair not in seen_pairs:
                    unique_results.append(result)
                    seen_pairs.add(pair)

            # Retrieve the user's selected allergen information
            user_allergens = Choice.objects.filter(user=request.user,
                                                   chosen=True).values_list('allergen__name', flat=True)

            # Filter search results based on the user's allergens
            results_without_allergens = []
            results_with_allergens = []

            for result in unique_results:
                supermarket_category = result.supermarket_category

                if supermarket_category:
                    supermarket = supermarket_category.supermarket

                    if supermarket:
                        result.logo_url = supermarket.supermarket_logo

                contains_allergen = SupermarketProductAllergens.objects.filter(
                    supermarket_product_id=result.id,
                    allergen__in=user_allergens
                ).exists()

                if contains_allergen:
                    results_with_allergens.append(result)
                else:
                    results_without_allergens.append(result)

            # Group and compare prices of search results
            grouped_results_without_allergens = compare_prices(results_without_allergens)
            grouped_results_with_allergens = compare_prices(results_with_allergens)

            # Calculate product URL for each result without allergens
            for grouped_result in grouped_results_without_allergens:
                for product in grouped_result[1]:  # Accessing the list of products in each grouped result
                    supermarket_category = SupermarketCategories.objects.get(id=product.supermarket_category_id)
                    if supermarket_category:
                        supermarket = Supermarkets.objects.get(id=supermarket_category.supermarket_id)
                        if supermarket:
                            product.product_url = urljoin(supermarket.supermarket_base_url, product.product_part_url)

            # Calculate product URL for each result with allergens
            for grouped_result in grouped_results_with_allergens:
                for product in grouped_result[1]:  # Accessing the list of products in each grouped result
                    supermarket_category = SupermarketCategories.objects.get(id=product.supermarket_category_id)
                    if supermarket_category:
                        supermarket = Supermarkets.objects.get(id=supermarket_category.supermarket_id)
                        if supermarket:
                            product.product_url = urljoin(supermarket.supermarket_base_url, product.product_part_url)

            return render(request, 'search_results.html',
                          {'grouped_results_with_allergens': grouped_results_with_allergens,
                           'grouped_results_without_allergens': grouped_results_without_allergens,
                           'query': query})


def compare_prices(results):
    grouped_results = []
    for name, group in itertools.groupby(results, key=lambda x: (x.product_name, x.product_image)):
        products = list(group)
        if len(products) > 1:
            cheapest_product = min(products, key=lambda x: x.product_price)
            for product in products:
                product.is_cheaper = product == cheapest_product
        else:
            products[0].is_cheaper = True
        grouped_results.append((name[0], products))  # Using name[0] to extract product name
    return grouped_results
