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

    def __str__(self):
        return self.name


class CartRow(MixBase, models.Model):
    food = models.ForeignKey(Food, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "CartRow {}".format(self.id)


class Cart(MixBase, models.Model):
    rows = models.ManyToManyField(CartRow, through=CartRow)

    def __str__(self):
        return "Cart {}".format(self.id)


class Order(MixBase, models.Model):
    STATUS = (
        ('n', 'New'),
        ('s', 'Send'),
        ('r', 'Received'),
        ('c', 'Cancelled'),
    )
    cart = models.OneToOneField(Cart)
    # owner
    status = models.CharField(max_length=1, choices=STATUS)

