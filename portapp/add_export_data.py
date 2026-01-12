import uuid
import random
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from .models import Export, Login, Ship  # Replace 'yourapp' with your app name

def run():
    login = Login.objects.first()
    ships = list(Ship.objects.all())

    if not login or not ships:
        print("⚠️ Login or Ship records are missing.")
        return

    categories = ["Electronics", "Pharma", "Textile", "Furniture", "Automobile"]
    products = {
        "Electronics": ["LED TV", "Smartphone", "Laptop"],
        "Pharma": ["Painkillers", "Vitamin D", "Syringes"],
        "Textile": ["Cotton Shirt", "Silk Saree", "Woolen Blanket"],
        "Furniture": ["Office Chair", "Dining Table", "Wardrobe"],
        "Automobile": ["Brake Pads", "Clutch Kit", "Steering Wheel"]
    }
    companies = ["TechCorp", "MediPlus", "WeaveIndia", "WoodCraft", "AutoPro"]
    destinations = ["USA", "UK", "Germany", "Australia", "UAE", "Singapore"]

    def random_date():
        start_date = datetime(2023, 1, 1)
        end_date = datetime.now()
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        return make_aware(start_date + timedelta(days=random_days))

    for i in range(150):
        category = random.choice(categories)
        product = random.choice(products[category])
        company = random.choice(companies)
        destination = random.choice(destinations)
        quantity = random.randint(10, 100)
        price = random.randint(5000, 25000)
        tax_percent = random.uniform(10, 20)
        tax_amount = round(price * (tax_percent / 100), 2)
        date = random_date()

        Export.objects.create(
            user_login=login,
            ship=random.choice(ships),
            product_category=category,
            product_name=product,
            company_name=company,
            exporting_price=price,
            tax=tax_amount,
            quantity=quantity,
            product_description=f"{product} exported by {company}",
            recipient_name=f"Client {i+1}",
            recipient_address=f"{i+1} Export Street, {destination}",
            recipient_contact_number=f"98{random.randint(10000000, 99999999)}",
            source="India",
            destination=destination,
            cancel_status=0,
            refund_status=0,
            payment_status=random.choice([0, 1]),
            unique_id=str(uuid.uuid4()),
            current_date=date.date(),
            month=date.month,
            year=date.year
        )

    print("✅ 50 export records added successfully.")
