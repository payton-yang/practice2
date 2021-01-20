from django.db import models

# Create your models here.
from carts.models import Carts
from users.models import Users
from billing_address.models import BillingAddress


class Orders(models.Model):
    create_time = models.DateTimeField(null=True, blank=True)
    user_id = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20)
    total_ex_tax = models.IntegerField(null=True, blank=True)
    total_inc_tax = models.IntegerField(null=True, blank=True)
    bc_order_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return {
            'id': self.id,
            'create_time': self.create_time,
            'user_id': self.user_id,
            'bc_order_id': self.bc_order_id,
            'total_ex_tax': self.total_ex_tax,
            'total_inc_tax': self.total_inc_tax,
            'status': self.status
        }

    class Meta:
        db_table = 'orders'
