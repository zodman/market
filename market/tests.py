from test_plus.test   import TestCase
from django_seed import Seed
from .models import Food, Order, Cart, CartRow


class OrderTestApi(TestCase):

    def setUp(self):
        seed = Seed.seeder()
        seed.add_entity(Food, 10)
        seed.execute()
        seed.add_entity(Cart, 10)
        seed.execute()

    def test_create_orders(self):
        r = Order.objects.all()
        self.assertTrue(r.exists())

    def test_list_orders(self):
        self.get_check_200('market:order_list')
    
