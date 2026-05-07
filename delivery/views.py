from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
import logging

logger = logging.getLogger(__name__)

from .models import Customer, Restaurant, Item, Cart, CartItem

import razorpay
from django.conf import settings
from django.db.models import Q
from django.db import models

# Create your views here.
def index(request):
    return render(request, 'delivery/index.html')

def open_signin(request):
    return render(request, 'delivery/signin.html')

def open_signup(request):
    return render(request, 'delivery/signup.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        try:
            Customer.objects.get(username = username)
            return HttpResponse("Duplicate username!")
        except:
            Customer.objects.create(
                username = username,
                password = password,
                email = email,
                mobile = mobile,
                address = address,
            )
        return redirect('open_signin')
    
    return render(request, 'delivery/signup.html')


def admin_home(request):
    return render(request, 'delivery/admin_home.html')

def customer_home(request, username):
    query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    
    if query:
        # Search for restaurants by name OR by items they contain
        restaurantList = Restaurant.objects.filter(
            models.Q(name__icontains=query) | 
            models.Q(cuisine__icontains=query) |
            models.Q(items__name__icontains=query)
        ).filter(status='Approved').distinct()
    elif category:
        # Filter by cuisine or item category
        restaurantList = Restaurant.objects.filter(
            models.Q(cuisine__icontains=category) | 
            models.Q(items__category__icontains=category)
        ).filter(status='Approved').distinct()
    else:
        restaurantList = Restaurant.objects.filter(status='Approved')
        
    return render(request, 'delivery/customer_home.html', {
        "restaurantList": restaurantList, 
        "username": username,
        "query": query,
        "category": category
    })

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        logger.error(f"DEBUG: Attempting login for '{username}' with password '{password}'")

        try:
            # Use __iexact for case-insensitive username check
            customer = Customer.objects.get(username__iexact = username, password = password)
            logger.error(f"DEBUG: Found customer: {customer.username}")
            if username == 'admin':
                return redirect('admin_home')
            else:
                return redirect('customer_home', username=username)

        except Customer.DoesNotExist:
            return render(request, 'delivery/fail.html')
    
    return redirect('open_signin')

def restaurant_apply(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        
        try:
            Restaurant.objects.get(name = name)
            return HttpResponse("Restaurant name already exists!")
        except:
            Restaurant.objects.create(
                name = name,
                picture = picture,
                cuisine = cuisine,
                rating = 0.0,
                status = 'Pending'
            )
        return render(request, 'delivery/apply_success.html')
    return render(request, 'delivery/restaurant_apply.html')

def pending_restaurants(request):
    restaurantList = Restaurant.objects.filter(status='Pending')
    return render(request, 'delivery/pending_restaurants.html', {"restaurantList": restaurantList})

def accept_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    restaurant.status = 'Approved'
    restaurant.save()
    return redirect('pending_restaurants')

def reject_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    restaurant.delete()
    return redirect('pending_restaurants')
    
def open_add_restaurant(request):
    return render(request, 'delivery/add_restaurant.html')

def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        
        try:
            Restaurant.objects.get(name = name)
            return HttpResponse("Duplicate restaurant!")
        except:
            Restaurant.objects.create(
                name = name,
                picture = picture,
                cuisine = cuisine,
                rating = rating,
                status = 'Approved'
            )
    return redirect('admin_home')

def open_show_restaurant(request):
    restaurantList = Restaurant.objects.filter(status='Approved')
    return render(request, 'delivery/show_restaurants.html',{"restaurantList" : restaurantList})

def open_update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    return render(request, 'delivery/update_restaurant.html', {"restaurant" : restaurant})

def update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        
        restaurant.name = name
        restaurant.picture = picture
        restaurant.cuisine = cuisine
        restaurant.rating = rating

        restaurant.save()

    return redirect('open_show_restaurant')


def delete_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    restaurant.delete()

    return redirect('open_show_restaurant')


def open_update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    return render(request, 'delivery/update_menu.html',{"itemList" : itemList, "restaurant" : restaurant})
    
def update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegeterian = request.POST.get('vegeterian') == 'on'
        picture = request.POST.get('picture')
        
        try:
            Item.objects.get(name = name, restaurant = restaurant)
            return HttpResponse("Duplicate item in this restaurant!")
        except:
            Item.objects.create(
                restaurant = restaurant,
                name = name,
                description = description,
                price = price,
                vegeterian = vegeterian,
                picture = picture,
                category = request.POST.get('category', 'General')
            )
    return redirect('admin_home')

def view_menu(request, restaurant_id, username):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    
    # We also want to pass current quantities to the template
    customer = Customer.objects.get(username__iexact=username)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    cart_items = cart.cart_items.all()
    
    quantities = {ci.item.id: ci.quantity for ci in cart_items}
    for item in itemList:
        item.current_quantity = quantities.get(item.id, 0)
        
    # Group items by category
    categories = {}
    for item in itemList:
        cat = item.category if item.category else "Other"
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    return render(request, 'delivery/customer_menu.html', {
        "categories": categories,
        "restaurant": restaurant, 
        "username": username
    })

def add_to_cart(request, item_id, username):
    item = Item.objects.get(id = item_id)
    customer = Customer.objects.get(username = username)
    cart, created = Cart.objects.get_or_create(customer = customer)

    action = request.GET.get('action', 'add')
    
    if action == 'add':
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return JsonResponse({"status": "ok", "quantity": cart_item.quantity})
    elif action == 'remove':
        try:
            cart_item = CartItem.objects.get(cart=cart, item=item)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                return JsonResponse({"status": "ok", "quantity": cart_item.quantity})
            else:
                cart_item.delete()
                return JsonResponse({"status": "ok", "quantity": 0})
        except CartItem.DoesNotExist:
            return JsonResponse({"status": "ok", "quantity": 0})

def show_cart(request, username):
    customer = Customer.objects.get(username = username)
    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.cart_items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    return render(request, 'delivery/cart.html', {
        "cart_items": cart_items, 
        "total_price": total_price, 
        "username": username
    })

# Checkout View
def checkout(request, username):
    # Fetch customer and their cart
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.cart_items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'delivery/checkout.html', {
            'error': 'Your cart is empty!',
        })

    # Group totals by restaurant
    restaurant_totals = {}
    for ci in cart_items:
        r_id = ci.item.restaurant.id
        if r_id not in restaurant_totals:
            restaurant_totals[r_id] = {'restaurant': ci.item.restaurant, 'total': 0}
        restaurant_totals[r_id]['total'] += (ci.item.price * ci.quantity)

    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create transfers array for Razorpay Route
    transfers = []
    for r_id, data in restaurant_totals.items():
        rest = data['restaurant']
        amount = data['total']
        
        # Admin gets 20%, restaurant gets 80%
        transfer_amount = int(amount * 0.8 * 100)
        
        if rest.razorpay_account_id:
            transfers.append({
                'account': rest.razorpay_account_id,
                'amount': transfer_amount,
                'currency': 'INR',
                'notes': {
                    'branch': rest.name,
                    'name': 'Restaurant Payout'
                },
                'linked_account_notes': ['branch'],
                'on_hold': 0
            })

    # Create Razorpay order
    order_data = {
        'amount': int(total_price * 100),  # Amount in paisa
        'currency': 'INR',
        'payment_capture': '1',  # Automatically capture payment
    }
    
    if transfers:
        order_data['transfers'] = transfers

    try:
        order = client.order.create(data=order_data)
    except Exception as e:
        # If Razorpay fails (e.g. because of dummy connected accounts), 
        # fallback to standard payment so it doesn't crash the flow.
        order_data.pop('transfers', None)
        order = client.order.create(data=order_data)

    # Pass the order details to the frontend
    return render(request, 'delivery/checkout.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],  # Razorpay order ID
        'amount': total_price,
        'amount_in_paise': int(total_price * 100),
    })


# Orders Page
def orders(request, username):
    customer = get_object_or_404(Customer, username=username)
    payment_id = request.GET.get('payment_id')
    
    if payment_id:
        # Create a new Order from current cart
        cart = Cart.objects.filter(customer=customer).first()
        if cart and cart.cart_items.exists():
            address = request.GET.get('address', customer.address)
            pincode = request.GET.get('pincode', '')
            phone = request.GET.get('phone', customer.mobile)
            
            # Group items by restaurant
            restaurant_items = {}
            for ci in cart.cart_items.all():
                r = ci.item.restaurant
                if r not in restaurant_items:
                    restaurant_items[r] = []
                restaurant_items[r].append(ci)
            
            for restaurant, items in restaurant_items.items():
                # Assign a random available delivery partner
                partner = DeliveryPartner.objects.filter(status='Available').order_by('?').first()
                if partner:
                    partner.status = 'Busy'
                    partner.save()
                
                total = sum(i.item.price * i.quantity for i in items)
                
                # Split Logic (20% platform, 10% delivery, 70% restaurant)
                p_fee = total * 0.20
                d_share = total * 0.10
                r_share = total * 0.70
                
                import random
                new_order = Order.objects.create(
                    customer=customer,
                    restaurant=restaurant,
                    delivery_partner=partner,
                    address=address,
                    pincode=pincode,
                    phone=phone,
                    total_amount=total,
                    status='Placed',
                    estimated_time=random.randint(25, 45),
                    platform_fee=p_fee,
                    delivery_share=d_share,
                    restaurant_share=r_share
                )
                
                for ci in items:
                    OrderItem.objects.create(
                        order=new_order,
                        item=ci.item,
                        quantity=ci.quantity,
                        price=ci.item.price
                    )
            
            # Clear cart
            cart.cart_items.all().delete()
            
    # Fetch all orders for this customer
    user_orders = Order.objects.filter(customer=customer).order_by('-created_at')
    
    return render(request, 'delivery/orders.html', {
        'username': username,
        'customer': customer,
        'orders': user_orders,
    })


def profile(request, username):
    customer = get_object_or_404(Customer, username=username)
    if request.method == 'POST':
        customer.email = request.POST.get('email')
        customer.mobile = request.POST.get('mobile')
        customer.address = request.POST.get('address')
        customer.bank_name = request.POST.get('bank_name')
        customer.ifsc_code = request.POST.get('ifsc_code')
        customer.bank_account_no = request.POST.get('bank_account_no')
        customer.save()
        return redirect('profile', username=username)
        
    return render(request, 'delivery/profile.html', {
        'customer': customer,
        'username': username
    })

def show_users(request):
    users = Customer.objects.all()
    return render(request, 'delivery/show_users.html', {'users': users})
