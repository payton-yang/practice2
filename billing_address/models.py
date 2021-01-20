from django.db import models

# Create your models here.
from users.models import Users


class BillingAddress(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    street_1 = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.CharField(max_length=20)
    country = models.CharField(max_length=200)
    country_iso2 = models.CharField(max_length=20)
    email = models.CharField(max_length=200)

    def __str__(self):
        return {
            'id': self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "street_1": self.street_1,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "country": self.country,
            "country_iso2": self.country_iso2,
            "email": self.email
        }

    class Meta:
        db_table = 'billing_address'
