from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import logging

log = logging.getLogger(__name__)


class MixBase:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Food(MixBase, models.Model):
    FOOD_TYPES = (
        ("meat", "Meat"),
        ("fruit", "Fruit"),
        ("vegetable", "Vegatable"),
        ("desert", "Desert"),
        ("dairy", "Dairy"),
        ("beverage", "Beverage"),
        ("bread", "Bread"),
    )
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=11, choices=FOOD_TYPES)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class CartRow(MixBase, models.Model):
    food = models.ForeignKey("Food", related_name="cart_foods",
                             on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey("Cart", related_name="cart_rows",
                             on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(
                                default=1,
                                validators=[MinValueValidator(limit_value=1)])
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0,
                                verbose_name="Unit price")

    def __str__(self):
        return "CartRow {}".format(self.id)



class Cart(MixBase, models.Model):
    rows = models.ManyToManyField(
        Food, related_name="carts", through=CartRow,
        through_fields=("cart", "food")
    )

    def __str__(self):
        return "Cart {}".format(self.id)


class Order(MixBase, models.Model):
    NEW = "n"
    SEND = "s"
    RECEIVED = "r"
    CANCELLED = "c"
    STATUS = (
        (NEW, "New"),
        (SEND, "Send"),
        (RECEIVED, "Received"),
        (CANCELLED, "Cancelled"),
    )
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=1, choices=STATUS, default=NEW)
    total = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def update_total(self):
        total = Decimal(0)
        for row in self.cart.cart_rows.all():
            total += row.quantity * row.price
        self.total = total
        return total

    def __str__(self):
        return "Order {}".format(self.id)



