from test_plus.test import TestCase
from rest_framework.test import APIClient
from django_seed import Seed
from .models import Food, Order, Cart, CartRow


class OrderTestApi(TestCase):
    client_class = APIClient

    def setUp(self):
        seed = Seed.seeder()
        seed.add_entity(Cart, 10)
        seed.execute()
        self.user = self.make_user()

    def test_check_orders(self):
        r = Order.objects.all()
        self.assertTrue(r.exists())

    def test_list_orders(self):
        self.get_check_200('market:order_list')
        self.assertTrue(len(self.last_response.json()) > 10)

    def __test_create_orders(self):
        cart = Cart.objects.all()[0]
        data = {
            'cart': cart.id,
        }
        self.post('market:order_list', data=data)
        print(self.last_response.json())
        self.assert_http_200_ok()


