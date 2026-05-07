from django.db import models

# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    email = models.CharField(max_length = 20)
    mobile = models.CharField(max_length = 10)
    address = models.CharField(max_length = 50)
    # Banking Info
    bank_account_no = models.CharField(max_length=20, blank=True, null=True)
    ifsc_code = models.CharField(max_length=15, blank=True, null=True)
    bank_name = models.CharField(max_length=50, blank=True, null=True)

class Restaurant(models.Model):
    name = models.CharField(max_length = 50)
    picture = models.URLField(max_length = 400, default='https://www.indiafilings.com/learn/wp-content/uploads/2024/08/How-to-Start-Food-Business.jpg')
    cuisine = models.CharField(max_length = 50)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    status = models.CharField(max_length=20, default='Approved')
    razorpay_account_id = models.CharField(max_length=100, blank=True, null=True)
    
class Item(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, related_name = "items")
    name = models.CharField(max_length = 20)
    description = models.CharField(max_length = 200)
    price = models.FloatField()
    vegeterian = models.BooleanField(default=False)
    picture = models.URLField(max_length = 400, default='https://www.indiafilings.com/learn/wp-content/uploads/2024/08/How-to-Start-Food-Business.jpg')
    category = models.CharField(max_length=50, default='General')

class CartItem(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE, related_name="cart_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, related_name = "cart")

    def total_price(self):
        return sum(cart_item.item.price * cart_item.quantity for cart_item in self.cart_items.all())

class DeliveryPartner(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    status = models.CharField(max_length=20, default='Available') # Available, Busy
    latitude = models.FloatField(default=12.9716) # Default to Bangalore
    longitude = models.FloatField(default=77.5946)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('Placed', 'Order Placed'),
        ('Preparing', 'Preparing Food'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    delivery_partner = models.ForeignKey(DeliveryPartner, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200)
    pincode = models.CharField(max_length=10, default='')
    phone = models.CharField(max_length=15, default='')
    total_amount = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Placed')
    estimated_time = models.IntegerField(default=30) # in minutes
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Split Amounts
    restaurant_share = models.FloatField(default=0)
    delivery_share = models.FloatField(default=0)
    platform_fee = models.FloatField(default=0)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    