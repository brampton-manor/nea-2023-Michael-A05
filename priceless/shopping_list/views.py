from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum

from search.models import SupermarketProducts, Supermarkets
from .models import ShoppingListItem

from collections import defaultdict


# Create your views here.
@login_required
def shopping_list(request):
    user = request.user
    shopping_items = ShoppingListItem.objects.filter(user=user)

    # Calculate current_supermarket_id
    if shopping_items.exists():
        first_item = shopping_items.first()
        current_supermarket_id = first_item.product.supermarket_category.supermarket.id
    else:
        # Handle case when shopping list is empty
        current_supermarket_id = None

    # Call compare_supermarkets to get comparison results
    comparison_results = compare_supermarkets(shopping_items, current_supermarket_id)

    return render(request, 'shopping_list.html',
                  {'shopping_items': shopping_items, 'comparison_results': comparison_results})


@login_required
def add_to_shopping_list(request, product_id):
    user = request.user
    product = get_object_or_404(SupermarketProducts, id=product_id)

    # Fetch the associated supermarket name
    supermarket_name = product.supermarket_category.supermarket.supermarket_name
    product_price = product.product_price

    # Check if the product is already in the shopping list
    existing_item = ShoppingListItem.objects.filter(user=user, product=product).first()
    if existing_item:
        existing_item.quantity += 1
        existing_item.save()
    else:
        ShoppingListItem.objects.create(user=user, product=product, product_price=product_price,
                                        supermarket_name=supermarket_name)

    return redirect('shopping_list')


@login_required
def remove_from_shopping_list(request, item_id):
    user = request.user
    item = get_object_or_404(ShoppingListItem, id=item_id, user=user)
    item.delete()
    return redirect('shopping_list')


def find_matching_products(product_name, current_supermarket_id):
    # Query for products from other supermarkets with the same name
    matching_products = SupermarketProducts.objects.filter(
        product_name=product_name
    ).exclude(
        supermarket_category__supermarket_id=current_supermarket_id
    ).distinct()

    return matching_products


def compare_supermarkets(shopping_list, current_supermarket_id):
    comparison_results = defaultdict(dict)
    supermarket_names = {}

    # Get the names of all supermarkets
    all_supermarkets = Supermarkets.objects.all()
    for supermarket in all_supermarkets:
        supermarket_names[supermarket.id] = supermarket.supermarket_name

    for item in shopping_list:
        # Create separate shopping lists for each supermarket
        shopping_lists = defaultdict(list)
        shopping_lists[current_supermarket_id].append(item)

        # Query for alternative versions of the product from other supermarkets
        matching_products = find_matching_products(item.product.product_name, current_supermarket_id)
        for product in matching_products:
            shopping_lists[product.supermarket_category.supermarket.id].append(product)

        # Calculate total value for each supermarket's shopping list
        for supermarket_id, products in shopping_lists.items():
            total = sum(product.product_price for product in products)
            comparison_results[item.product.product_name][supermarket_id] = total

    return comparison_results, supermarket_names


"""
Old version

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum

from search.models import SupermarketProducts
from .models import ShoppingListItem


# Create your views here.
@login_required
def shopping_list(request):
    user = request.user
    shopping_items = ShoppingListItem.objects.filter(user=user)

    # Calculate current_supermarket_id
    if shopping_items.exists():
        first_item = shopping_items.first()
        current_supermarket_id = first_item.product.supermarket_category.supermarket.id
    else:
        # Handle case when shopping list is empty
        current_supermarket_id = None

    # Call compare_supermarkets to get comparison results
    comparison_results = compare_supermarkets(shopping_items, current_supermarket_id)

    return render(request, 'shopping_list.html',
                  {'shopping_items': shopping_items, 'comparison_results': comparison_results})


@login_required
def add_to_shopping_list(request, product_id):
    user = request.user
    product = get_object_or_404(SupermarketProducts, id=product_id)

    # Fetch the associated supermarket name
    supermarket_name = product.supermarket_category.supermarket.supermarket_name
    product_price = product.product_price
    print(product_price)

    # Check if the product is already in the shopping list
    existing_item = ShoppingListItem.objects.filter(user=user, product=product).first()
    if existing_item:
        existing_item.quantity += 1
        existing_item.save()
    else:
        ShoppingListItem.objects.create(user=user, product=product, product_price=product_price,
                                        supermarket_name=supermarket_name)

    return redirect('shopping_list')


@login_required
def remove_from_shopping_list(request, item_id):
    user = request.user
    item = get_object_or_404(ShoppingListItem, id=item_id, user=user)
    item.delete()
    return redirect('shopping_list')


def find_matching_products(product_name, current_supermarket_id):
    # Exclude products from the current supermarket
    matching_products = SupermarketProducts.objects.filter(
        product_name=product_name
    ).exclude(
        supermarket_category__supermarket_id=current_supermarket_id
    ).distinct()

    return matching_products


def compare_supermarkets(shopping_list, current_supermarket_id):
    comparison_results = {}

    for item in shopping_list:
        matching_products = find_matching_products(item.product.product_name, current_supermarket_id)

        # Calculate total value for current supermarket
        total_current_supermarket = \
            shopping_list.filter(product__supermarket_category__supermarket_id=current_supermarket_id).aggregate(
                total=Sum('product_price'))['total']

        # Calculate total value for other supermarkets
        total_other_supermarkets = matching_products.aggregate(total=Sum('product_price'))[
            'total'] if matching_products.exists() else 0

        # Compare totals and store result
        cheaper_supermarket = 'Current Supermarket' if total_current_supermarket < total_other_supermarkets else 'Other Supermarkets'
        comparison_results[item.product.product_name] = {'current_supermarket': total_current_supermarket,
                                                         'other_supermarkets': total_other_supermarkets,
                                                         'cheaper_supermarket': cheaper_supermarket}

    return comparison_results


Corresponding shopping_list.html


{% extends "base.html" %}
{% load static %}

{% block title %}Shopping List{% endblock %}
{% block content %}
    <h1>Shopping List</h1>

    <h2>Your Shopping List</h2>
    <ul>
        {% for item in shopping_items %}
            <li>
                {{ item.product.product_name }} - Quantity: {{ item.quantity }}
                <form action="{% url 'remove_from_shopping_list' item.id %}" method="post">
                    {% csrf_token %}
                    <button type="submit">Remove</button>
                </form>
            </li>
        {% endfor %}
    </ul>

    <h2>Comparison Results</h2>
    {% for product_name, result in comparison_results.items %}
        <h3>{{ product_name }}</h3>
        <p>Total in Current Supermarket: £{{ result.current_supermarket }}</p>
        <p>Total in Other Supermarkets: £{{ result.other_supermarkets }}</p>
        <p>Cheaper Supermarket: {{ result.cheaper_supermarket }}</p>
    {% empty %}
        <p>No comparison results available.</p>
    {% endfor %}
{% endblock %}


Comparison logic

We need to fix the comparison logic

If a user adds supermarket 1's version of product X
we create a shopping list for supermarket 1 containing product X and any further products from supermarket 1 that the user may add

For every product in supermarket 1's shopping list, we query our database for products from supermarket 2 and supermarket 3 that have the same name

We then create alternative shopping lists for supermarket 2 and 3 if alternative version's of product X that may have different prices are found

Finally, we get display totals of all the shopping least and say which supermarket has the cheapest shopping list

A user shouldn't be able to add a product Y from supermarket 2
"""