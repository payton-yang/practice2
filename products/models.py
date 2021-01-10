from django.db import models


# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20)
    image = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField()
    color = models.CharField(max_length=5)

    def __str__(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'quantity': self.quantity,
            'color': self.color
        }

    class Meta:
        db_table = 'products'
