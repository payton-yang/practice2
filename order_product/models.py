from django.db import models

# Create your models here.
from orders.models import Orders
from products.models import Products


class OrderProduct(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.DO_NOTHING)
    product_id = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product_id

    class Meta:
        db_table = 'order_product'
