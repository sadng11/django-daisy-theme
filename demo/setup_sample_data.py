#!/usr/bin/env python
import os
import sys

# Setup django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
import django
django.setup()

from django.contrib.auth.models import User
from shop.models import Category, Product, Order, OrderItem
from decimal import Decimal

def seed():
    print("-> Setting up demo data...")

    # 1. Superuser
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin1234")
        print("✔ Superuser created: admin / admin1234")
    else:
        print("✔ Superuser admin already exists.")

    # 2. Categories
    cat_tech, _ = Category.objects.get_or_create(
        slug="electronics",
        defaults={"name": "کالای دیجیتال و الکترونیک", "description": "گوشی‌های هوشمند، لپ‌تاپ و تجهیزات کامپیوتری", "is_active": True}
    )
    cat_cloth, _ = Category.objects.get_or_create(
        slug="clothing",
        defaults={"name": "مد و پوشاک", "description": "لباس، کفش و اکسسوری‌های مردانه و زنانه", "is_active": True}
    )
    cat_books, _ = Category.objects.get_or_create(
        slug="books",
        defaults={"name": "کتاب و لوازم تحریر", "description": "کتاب‌های تخصصی، رمان و نوشت‌افزار", "is_active": True}
    )
    print("✔ Sample categories ready.")

    # 3. Products
    products_data = [
        {"category": cat_tech, "title": "مک‌بوک پرو M3 Max", "slug": "macbook-pro-m3-max", "price": Decimal("2450.00"), "stock": 15, "is_featured": True, "description": "لپ‌تاپ قدرتمند اپل با تراشه M3 Max و ۳۶ گیگابایت رم."},
        {"category": cat_tech, "title": "آیفون ۱۵ پرو مکس", "slug": "iphone-15-pro-max", "price": Decimal("1199.00"), "stock": 25, "is_featured": True, "description": "پرچمدار اپل با بدنه تیتانیومی و دوربین ۵ برابری پریسکوپ."},
        {"category": cat_tech, "title": "کیبورد مکانیکی بیسیم کی‌کرون", "slug": "keychron-k2-keyboard", "price": Decimal("95.00"), "stock": 40, "is_featured": False, "description": "کیبورد ارگونومیک مکانیکی مناسب برنامه‌نویسی."},
        {"category": cat_cloth, "title": "هودی اسپرت کتان ارگانیک", "slug": "organic-cotton-hoodie", "price": Decimal("49.90"), "stock": 80, "is_featured": False, "description": "هودی نرم و باکیفیت ساخته شده از الیاف ۱۰۰٪ طبیعی."},
        {"category": cat_cloth, "title": "کفش رانینگ آدیداس اولترابوست", "slug": "ultraboost-running-shoes", "price": Decimal("180.00"), "stock": 20, "is_featured": True, "description": "کفش ورزشی سبک و راحت مناسب دویدن طولانی."},
        {"category": cat_books, "title": "کتاب معماری تمیز (Clean Architecture)", "slug": "clean-architecture-book", "price": Decimal("28.50"), "stock": 50, "is_featured": True, "description": "راهنمای جامع ساختاردهی نرم‌افزارهای حرفه‌ای از رابرت سی مارتین."},
    ]

    for p in products_data:
        Product.objects.get_or_create(
            slug=p["slug"],
            defaults=p
        )
    print("✔ Sample products created.")

    # 4. Sample Orders
    order1, created = Order.objects.get_or_create(
        customer_name="علی محمدی",
        defaults={
            "customer_email": "ali@example.com",
            "status": "completed",
            "total_amount": Decimal("1294.00"),
            "notes": "ارسال سریع با پست پیشتاز انجام شود.",
        }
    )
    if created:
        p1 = Product.objects.get(slug="iphone-15-pro-max")
        p2 = Product.objects.get(slug="keychron-k2-keyboard")
        OrderItem.objects.create(order=order1, product=p1, quantity=1, unit_price=p1.price)
        OrderItem.objects.create(order=order1, product=p2, quantity=1, unit_price=p2.price)

    order2, created = Order.objects.get_or_create(
        customer_name="سارا احمدی",
        defaults={
            "customer_email": "sara@example.com",
            "status": "processing",
            "total_amount": Decimal("78.40"),
            "notes": "کادویی بسته‌بندی شود.",
        }
    )
    if created:
        p3 = Product.objects.get(slug="organic-cotton-hoodie")
        p4 = Product.objects.get(slug="clean-architecture-book")
        OrderItem.objects.create(order=order2, product=p3, quantity=1, unit_price=p3.price)
        OrderItem.objects.create(order=order2, product=p4, quantity=1, unit_price=p4.price)

    print("✔ Sample orders and inlines created.")
    print("🎉 All demo data successfully seeded!")

if __name__ == "__main__":
    seed()
