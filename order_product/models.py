from django.db import models

# Create your models here.
from orders.models import Orders
from products.models import Products
from billing_address.models import BillingAddress


class OrderProduct(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.DO_NOTHING)
    product_id = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    billing_address_id = models.ForeignKey(BillingAddress, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'billing_address': self.billing_address_id,
            'quantity': self.quantity
        }

    class Meta:
        db_table = 'order_product'
