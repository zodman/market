from test_plus.test import TestCase
from rest_framework.test import APIClient
from django_seed import Seed
from .models import Food, Order, Cart, CartRow


class ModelTest(TestCase):
    def setUp(self):
        seed = Seed.seeder()
        seed.add_entity(Food, 10)
        seed.execute()

    def test_cart_signals(self):
        food = Food.objects.all().order_by("?")[0]
        cart = Cart.objects.create()
        CartRow.objects.create(quantity=1, cart=cart, food=food)
        self.assertTrue(cart.order is not None)


class OrderTestApi(TestCase):
    client_class = APIClient

    def setUp(self):
        seed = Seed.seeder()
        seed.add_entity(Cart, 10)
        seed.add_entity(Food, 10)
        seed.execute()
        self.user = self.make_user()

    def test_check_orders(self):
        """ check if the index works with inertia"""
        r = Order.objects.all()
        self.assertTrue(r.exists())
        self.get_check_200("market:index")
        self.assertInContext("page")

    def test_not_update_order_fields(self):
        """ We only can update the status"""
        order = Order.objects.all()[0]
        order.total = 1
        order.save()
        user = self.make_user(username="temp1")
        data = {
            "user": user.id,
            "total": 0.01,
        }
        self.put("market:order_detail", pk=order.id, data=data)
        newobj = self.last_response.json()
        self.assertTrue(float(newobj["total"]) != 1.0, newobj)
        self.assertTrue(newobj["user"] != user.id)

    def test_update_status_order(self):
        """ update the status of the order"""
        order = Order.objects.all()[0]
        data = {"status": "c"}
        self.put("market:order_detail", pk=order.id, data=data)
        self.assert_http_200_ok()
        sameorder = Order.objects.get(id=order.id)
        self.assertTrue(sameorder.status == "c")

    def test_list_orders(self):
        """ list orders by status and user """
        self.get_check_200("market:order_list")
        self.assertTrue(len(self.last_response.json()) > 10)

        order = Order.objects.all()[0]
        order.status = "s"
        order.user = self.user
        order.save()
        url = self.reverse("market:order_list")
        self.get_check_200(f"{url}?status=s")
        self.assertTrue(len(self.last_response.json()) == 1)

        self.get_check_200(f"{url}?user={self.user.username}")
        self.assertTrue(len(self.last_response.json()) == 1)

    def test_detail_destroy_order(self):
        """ We can delete orders"""
        qs = Order.objects.all()
        count = qs.count()
        order = qs[0]
        self.get("market:order_detail", pk=order.id)
        self.assert_http_200_ok()
        self.delete("market:order_detail", pk=order.id)
        self.response_204()
        newcount = Order.objects.all().count()
        self.assertTrue(count != newcount, (count, newcount))
