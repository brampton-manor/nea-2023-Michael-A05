from search.models import Supermarkets, SupermarketCategories, SupermarketProducts

def create_test_database():
    # Create 3 supermarkets
    supermarket1 = Supermarkets.objects.create(supermarket_name="Supermarket 1", supermarket_logo="logo1.png", supermarket_base_url="https://supermarket1.com")
    supermarket2 = Supermarkets.objects.create(supermarket_name="Supermarket 2", supermarket_logo="logo2.png", supermarket_base_url="https://supermarket2.com")
    supermarket3 = Supermarkets.objects.create(supermarket_name="Supermarket 3", supermarket_logo="logo3.png", supermarket_base_url="https://supermarket3.com")

    # Create category for each supermarket (assuming bakery category)
    bakery_category1 = SupermarketCategories.objects.create(supermarket=supermarket1, supermarket_category_name="Bakery", supermarket_category_part_url="bakery")
    bakery_category2 = SupermarketCategories.objects.create(supermarket=supermarket2, supermarket_category_name="Bakery", supermarket_category_part_url="bakery")
    bakery_category3 = SupermarketCategories.objects.create(supermarket=supermarket3, supermarket_category_name="Bakery", supermarket_category_part_url="bakery")

    # Create 5 products with the same name but different prices for each supermarket
    product_names = ["Bread", "Cake", "Pastry", "Muffin", "Croissant"]
    for i in range(5):
        # Assuming different prices for each product in each supermarket
        SupermarketProducts.objects.create(supermarket_category=bakery_category1, product_name=product_names[i], product_price=1.99 + i, product_image="bread.jpg", product_part_url="bread", is_available=True)
        SupermarketProducts.objects.create(supermarket_category=bakery_category2, product_name=product_names[i], product_price=2.49 + i, product_image="cake.jpg", product_part_url="cake", is_available=True)
        SupermarketProducts.objects.create(supermarket_category=bakery_category3, product_name=product_names[i], product_price=2.99 + i, product_image="pastry.jpg", product_part_url="pastry", is_available=True)

# Run the function to create the test database
create_test_database()