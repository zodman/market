from django.db import models
from django.core.validators import MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save
import logging

log = logging.getLogger(__name__)


class MixBase:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Food(MixBase, models.Model):
    FOOD_TYPES = (
        ('meat', 'Meat'),
        ('fruit', 'Fruit'),
        ('vegetable', 'Vegatable'),
        ('desert', 'Desert'),
        ('dairy', 'Dairy'),
        ('beverage', 'Beverage'),
        ('bread', 'Bread'),
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=11, choices=FOOD_TYPES)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class CartRow(MixBase, models.Model):
    food = models.ForeignKey("Food", related_name="cart_foods",
                             on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey("Cart", related_name="cart_rows",
                             on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1,
                                           validators=[MinValueValidator(limit_value=1)])
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0,
                                editable=False, verbose_name="Unit price")

    def __str__(self):
        return "CartRow {}".format(self.id)


@receiver(pre_save, sender=CartRow)
def pre_save_row(sender, **kwargs):
    instance = kwargs.get("instance")
    instance.price = instance.food.price
    return instance


class Cart(MixBase, models.Model):
    rows = models.ManyToManyField(Food, related_name="carts", through=CartRow,
                                  through_fields=("cart", "food"))

    def __str__(self):
        return "Cart {}".format(self.id)




class Order(MixBase, models.Model):
    STATUS = (
        ('n', 'New'),
        ('s', 'Send'),
        ('r', 'Received'),
        ('c', 'Cancelled'),
    )
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True)
    # owner
    status = models.CharField(max_length=1, choices=STATUS)
