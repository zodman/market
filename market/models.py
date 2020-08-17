from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
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


@receiver(pre_save, sender=CartRow)
def pre_save_row(sender, **kwargs):
    instance = kwargs.get("instance")
    # copy the price from the food
    if instance.price == 0:
        instance.price = instance.food.price


@receiver(post_save, sender=CartRow)
def post_save_row(sender, **kwargs):
    # update the total price of the order
    instance = kwargs.get("instance")
    instance.cart.order.update_total()
    instance.cart.order.save()


class Cart(MixBase, models.Model):
    rows = models.ManyToManyField(
        Food, related_name="carts", through=CartRow,
        through_fields=("cart", "food")
    )

    def __str__(self):
        return "Cart {}".format(self.id)


@receiver(post_save, sender=Cart)
def create_order(sender, **kwargs):
    is_created = kwargs.get("created")
    instance = kwargs.get("instance")
    if is_created:
        order = Order(cart=instance)
        order.save()


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


@receiver(pre_save, sender=Order)
def pre_save_order(sender, **kwargs):
    instance = kwargs.get("instance")
    instance.update_total()
    return instance
