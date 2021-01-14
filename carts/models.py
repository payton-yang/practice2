from django.db import models
from users.models import Users


# Create your models here.
class Carts(models.Model):
    create_time = models.DateTimeField(null=True, blank=True)
    user_id = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20, default='')
    bc_cart_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return {
            'id': self.id,
            'create_time': self.create_time,
            'user_id': self.user_id,
            'status': self.status,
            'bc_cart_id': self.bc_cart_id
        }

    class Meta:
        db_table = 'carts'
