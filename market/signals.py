from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .models import Cart, Order, CartRow


@receiver(post_save, sender=Cart)
def create_order(sender, **kwargs):
    is_created = kwargs.get("created")
    instance = kwargs.get("instance")
    if is_created:
        order = Order(cart=instance)
        order.save()


@receiver(pre_save, sender=Order)
def pre_save_order(sender, **kwargs):
    instance = kwargs.get("instance")
    instance.update_total()
    return instance


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
