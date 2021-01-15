from django.db import models

# Create your models here.
from users.models import Users


class Address(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200)
    state_or_province = models.CharField(max_length=200)
    country_code = models.CharField(max_length=200)
    company = models.CharField(max_length=20, null=True, blank=True)
    postal_code = models.CharField(max_length=200)
    user_id = models.ForeignKey(Users, on_delete=models.DO_NOTHING)

    def __str__(self):
        return {
            'id': self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address1": self.address1,
            "address2": self.address2,
            "city": self.city,
            "state_or_province": self.state_or_province,
            "country_code": self.country_code,
            "company": self.company,
            "postal_code": self.postal_code,
            "user_id": self.user_id
        }

    class Meta:
        db_table = 'address'
