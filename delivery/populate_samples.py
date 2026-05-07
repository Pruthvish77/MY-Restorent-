import os
import django
import sys

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meal_buddy.settings')
django.setup()

from delivery.models import Restaurant, Item

def add_sample_items():
    # Truffles (Burgers & Desserts)
    truffles = Restaurant.objects.filter(name__iexact='truffles').first()
    if truffles:
        Item.objects.get_or_create(
            restaurant=truffles, name='Classic Beef Burger',
            defaults={'description': 'Juicy beef patty with cheese', 'price': 250, 'category': 'Burgers', 'picture': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400'}
        )
        Item.objects.get_or_create(
            restaurant=truffles, name='Death by Chocolate',
            defaults={'description': 'Rich chocolate cake with fudge', 'price': 180, 'category': 'Desserts', 'picture': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400'}
        )
        Item.objects.get_or_create(
            restaurant=truffles, name='Ferrero Rocher Shake',
            defaults={'description': 'Creamy chocolate hazelnut shake', 'price': 220, 'category': 'Beverages', 'picture': 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400'}
        )

    # Dominos (Pizzas)
    dominos = Restaurant.objects.filter(name__iexact='dominos').first()
    if dominos:
        Item.objects.get_or_create(
            restaurant=dominos, name='Margherita Pizza',
            defaults={'description': 'Classic cheese pizza', 'price': 350, 'category': 'Pizza', 'picture': 'https://images.unsplash.com/photo-1574071318508-1cdbad80ad38?w=400'}
        )
        Item.objects.get_or_create(
            restaurant=dominos, name='Peppy Paneer',
            defaults={'description': 'Paneer, capsicum, red paprika', 'price': 450, 'category': 'Pizza', 'picture': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400'}
        )
        Item.objects.get_or_create(
            restaurant=dominos, name='Choco Lava Cake',
            defaults={'description': 'Hot chocolate filled cake', 'price': 99, 'category': 'Desserts', 'picture': 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=400'}
        )

    # Pruthvi (Biryani)
    pruthvi = Restaurant.objects.filter(name__iexact='pruthvi').first()
    if pruthvi:
        Item.objects.get_or_create(
            restaurant=pruthvi, name='Hyderabadi Biryani',
            defaults={'description': 'Spicy authentic dum biryani', 'price': 320, 'category': 'Biryani', 'picture': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400'}
        )
        Item.objects.get_or_create(
            restaurant=pruthvi, name='Paneer Tikka',
            defaults={'description': 'Grilled spiced paneer cubes', 'price': 240, 'category': 'Starters', 'picture': 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=400'}
        )
        Item.objects.get_or_create(
            restaurant=pruthvi, name='Butter Chicken',
            defaults={'description': 'Creamy tomato gravy with chicken', 'price': 380, 'category': 'Main Course', 'picture': 'https://images.unsplash.com/photo-1603894584202-933259bb499a?w=400'}
        )
        Item.objects.get_or_create(
            restaurant=pruthvi, name='Gulab Jamun',
            defaults={'description': 'Sweet milk balls in syrup', 'price': 80, 'category': 'Desserts', 'picture': 'https://images.unsplash.com/photo-1589119908995-c6837fa14848?w=400'}
        )

    print("Sample items added successfully!")

if __name__ == '__main__':
    add_sample_items()
