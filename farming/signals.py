# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tsrdetail, Order
from datetime import timedelta

@receiver(post_save, sender=Tsrdetail)
def create_order(sender, instance, created, **kwargs):
    if created:
        order_date = instance.created_date
        delivery_date = order_date + timedelta(days=3)

        Order.objects.create(
            order_id=instance.order_id,
            order_date=order_date,
            delivery_date=delivery_date,
            delivery_status='Order Placed'
        )