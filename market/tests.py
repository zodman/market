from test_plus.test import TestCase
from rest_framework.test import APIClient
from django_seed import Seed
from .models import Food, Order, Cart, CartRow
from .serializers import FoodSerializer
from decimal import Decimal


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
        self.seed = seed
        self.user = self.make_user()
        self.admin = self.make_user(username="admin")
        self.admin.is_superuser = True
        self.admin.save()

    def test_create_cart(self):
        foods = Food.objects.all()
        data_list = []
        for f in foods:
            data_list.append(dict(food=f.id, 
                    quantity=self.seed.faker.random_digit_not_null()))
        data = data_list
        total = sum(map(
            lambda x: 
                x["quantity"]*Food.objects.get(id=x["food"]).price,
            data))
        with self.login(username=self.user.username):
            self.post("market:create_cart", data=data, 
                        extra={'format':'json'})
            self.response_302()
        # response = self.last_response.json()
        # self.assertTrue(response["user"]== self.user.id)
        # self.assertTrue(Decimal(response["total"])==total)

    def test_check_orders(self):
        """ check if the index works with inertia"""
        r = Order.objects.all()
        self.assertTrue(r.exists())
        self.get_check_200("market:index")
        self.assertInContext("page")

    def test_not_update_order_fields(self):
        """ We only can update the status"""
        user = self.make_user(username="temp1")
        order = Order.objects.all()[0]
        order.total = 1
        order.user = user
        order.save()
        data = {
            "user": self.user.id,
            "total": 0.01,
        }
        with self.login(username=user.username):
            self.put("market:order_detail", pk=order.id, data=data)
        newobj = self.last_response.json()
        self.assertTrue(float(newobj["total"]) != 1.0, newobj)
        self.assertTrue(newobj["user"] == user.id)

    def test_update_status_order(self):
        """ update the status of the order"""
        order = Order.objects.all()[0]
        order.user = self.user
        order.save()
        data = {"status": "c"}
        with self.login(username=self.user.username):
            self.put("market:order_detail", pk=order.id, data=data)
        self.assert_http_200_ok()
        sameorder = Order.objects.get(id=order.id)
        self.assertTrue(sameorder.status == "c")

    def test_list_orders(self):
        """ list orders by status and user """
        with self.login(username=self.admin.username):
            self.get_check_200("market:order_list")
        self.assertTrue(len(self.last_response.json()) > 10)
        order = Order.objects.all()[0]
        order.status = "s"
        order.user = self.user
        order.save()
        with self.login(username=self.admin.username): 
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
        order.user = self.admin
        order.save()
        with self.login(username=self.admin.username):
            self.get("market:order_detail", pk=order.id)
            self.assert_http_200_ok()
            self.delete("market:order_detail", pk=order.id)
            self.response_204()
        newcount = Order.objects.all().count()
        self.assertTrue(count != newcount, (count, newcount))
