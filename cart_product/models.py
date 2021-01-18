from django.db import models

# Create your models here.
from carts.models import Carts
from products.models import Products


class CartProduct(models.Model):
    cart_id = models.ForeignKey(Carts, on_delete=models.DO_NOTHING)
    product_id = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=0)
    bc_item_id = models.CharField(max_length=200, default='')

    def __str__(self):
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'bc_item_id': self.bc_item_id
        }

    class Meta:
        db_table = 'cart_product'
