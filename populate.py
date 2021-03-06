import os
import logging
import django

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from django_seed import Seed
from market.models import Food
from django.contrib.auth.models import User

foodNames = set([
    "Cheese Pizza",
    "Hamburger",
    "Cheeseburger",
    "Bacon Burger",
    "Bacon Cheeseburger",
    "Little Hamburger",
    "Little Cheeseburger",
    "Little Bacon Burger",
    "Little Bacon Cheeseburger",
    "Veggie Sandwich",
    "Cheese Veggie Sandwich",
    "Grilled Cheese",
    "Cheese Dog",
    "Bacon Dog",
    "Bacon Cheese Dog",
    "Pasta",
    "Beer",
    "Bud Light",
    "Budweiser",
    "Miller Lite",
    "Milk Shake",
    "Tea",
    "Sweet Tea",
    "Coffee",
    "Hot Tea",
    "Champagne",
    "Wine",
    "Lemonade",
    "Coca-Cola",
    "Diet Coke",
    "Water",
    "Sprite",
    "Orange Juice",
    "Iced Coffee",
    "Butter",
    "Egg",
    "Cheese",
    "Sour cream",
    "Mozzarella",
    "Yogurt",
    "Cream",
    "Milk",
    "Custard",
])


def init_data():
    seeder = Seed.seeder()
    seeder.add_entity(
        Food, 20, {"name": lambda x: foodNames.pop()}
    )
    result = seeder.execute()
    log.info(f"Initialize db with Foods created: {len(result[Food])}")


def init_admin():
    if not User.objects.filter(username="admin").exists():
        args = ("admin", "admin@example.com", "admin")
        created = User.objects.create_superuser(*args)
        log.info(f"superuser created {created}")


if __name__ == "__main__":
    init_data()
    init_admin()
