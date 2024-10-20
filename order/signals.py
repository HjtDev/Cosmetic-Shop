from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order
from jdatetime import datetime


@receiver(pre_save, sender=Order)
def paid_signal(sender, instance: Order, **kwargs):
    if not instance.pk:
        return
    old_paid = Order.objects.get(pk=instance.pk).paid
    if not old_paid and instance.paid:
        if instance.status == Order.OrderStatus.PENDING:
            instance.status = Order.OrderStatus.CONFIRMED
        for item in instance.items.all():
            item.product.bought.add(instance.user)
            item.product.inventory -= item.quantity
            item.product.sold += item.quantity
            item.product.last_sell = datetime.now()
            item.product.save()
            
