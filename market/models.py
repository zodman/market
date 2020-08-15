from django.db import models


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
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "CartRow {}".format(self.id)


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
