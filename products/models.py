from django.db import models


# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    image = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField()
    price = models.IntegerField()
    sku = models.CharField(max_length=200, default='')
    description = models.CharField(max_length=5000, default='')
    date_created = models.CharField(max_length=200, default='')
    date_modified = models.CharField(max_length=200, default='')
    option_set_id = models.IntegerField(null=True, blank=True, default=0, verbose_name='variant_id')
    bc_product_id = models.IntegerField(default=0)

    def __str__(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'quantity': self.quantity,
            'price': self.price,
            'sku': self.sku,
            'description': self.description,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'option_set_id': self.option_set_id,
            'bc_product_id': self.bc_product_id
        }

    class Meta:
        db_table = 'products'
