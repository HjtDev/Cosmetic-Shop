from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order, Transaction
from jdatetime import datetime


@receiver(pre_save, sender=Order)
def paid_signal(sender, instance: Order, **kwargs):
    if not instance.pk:
        return
    old_paid = Order.objects.get(pk=instance.pk).paid
    if not old_paid and instance.paid:
        if instance.status == Order.OrderStatus.PENDING:
            instance.status = Order.OrderStatus.CONFIRMED
        transaction_text = f'Order: {instance.order_id}'
        for item in instance.items.all():
            item.product.bought.add(instance.user)
            item.product.inventory -= item.quantity
            item.product.sold += item.quantity
            item.product.last_sell = datetime.now()
            item.product.save()
            transaction_text += f'\n {item.product.title} x {item.quantity} -- {item.get_cost()}'

        Transaction.objects.create(
            user=instance.user,
            reason=Transaction.ReasonChoice.ORDER,
            status=Transaction.TransactionStatusChoice.PAID,
            description=transaction_text,
            price=instance.get_items_cost()
        )
