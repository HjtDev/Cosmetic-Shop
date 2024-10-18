from django.db import models
from django.core.handlers.wsgi import WSGIRequest
from product.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        # Initialize cart if it doesn't exist
        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

        # Ensure 'products' is initialized
        if 'products' not in self.cart:
            self.cart['products'] = {}

    def save(self):
        """Mark the session as modified to save changes."""
        self.session.modified = True

    def add(self, product_id, quantity):
        try:
            product = Product.visible_products.get(id=product_id)

            if self.cart['products'].get(str(product_id), None):
                self.cart['products'][str(product_id)]['quantity'] = int(self.cart['products'][str(product_id)]['quantity']) + int(quantity)
                self.cart['products'][str(product_id)]['price'] = product.price
                existed = True
            else:
                self.cart['products'][str(product_id)] = {'quantity': quantity, 'price': str(product.get_price())}
                existed = False

            self.save()
            return existed
        except Product.DoesNotExist:
            print('Tried to add a non-existing object to the cart')

    def remove(self, product_id):
        try:
            del self.cart['products'][str(product_id)]
            self.save()
        except KeyError:
            print('Failed to remove product from cart: Product does not exist in cart')

    def get_total_cost(self):
        total_cost = 0
        for item in self.cart.get('products', {}).values():
            try:
                price = int(item['price'])
                quantity = int(item['quantity'])
                total_cost += price * quantity
            except (ValueError, TypeError) as e:
                print(f"Error calculating total cost for item {item}: {e}")
        return total_cost

    def __iter__(self):
        # Fetch all products at once
        product_ids = list(self.cart.get('products', {}).keys())
        products = {product.id: product for product in Product.objects.filter(id__in=product_ids)}

        for product_id, item in self.cart.get('products', {}).items():
            product = products.get(int(product_id))  # Use int() for safety
            if product:  # Check if the product exists
                yield {
                    'product': product,
                    'quantity': item['quantity'],
                    'price': item['price'],
                }
            else:
                print(f'Product with id {product_id} does not exist.')

    def __len__(self):
        """Return the total number of items in the cart."""
        return sum(int(item['quantity']) for item in self.cart.get('products', {}).values())

    def clear(self):
        """Clear the cart."""
        del self.session['cart']