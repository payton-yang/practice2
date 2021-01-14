from django.db import models

# Create your models here.
from carts.models import Carts
from products.models import Products


class CartProduct(models.Model):
    cart_id = models.ForeignKey(Carts, on_delete=models.DO_NOTHING)
    product_id = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return {
            'id': self.id,
            'cart_id': self.product_id,
            'user_id': self.user_id,
            'quantity': self.quantity
        }

    class Meta:
        db_table = 'cart_product'
