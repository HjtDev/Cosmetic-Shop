from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Product
from shop.sms import send_sms, NOTIFY_ME


@receiver(pre_save, sender=Product)
def notify(sender, instance, **kwargs):
    if not instance.pk:
        return

    if instance.inventory != 0 and Product.objects.get(pk=instance.pk).inventory == 0 and instance.notify_me.all().exists():
        for user in instance.notify_me.all():
            send_sms(NOTIFY_ME, user.phone, message='محصول رزرو شده شما')
            instance.notify_me.remove(user)
