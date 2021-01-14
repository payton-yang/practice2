from django.db import models


# Create your models here.
class Users(models.Model):
    first_name = models.CharField(max_length=20, default='')
    last_name = models.CharField(max_length=20, default='')
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=25)
    token = models.CharField(null=True, blank=True, max_length=200)
    company = models.CharField(max_length=200, default='', null=True, blank=True)
    customer_group_id = models.IntegerField(default=0, null=True, blank=True)
    phone = models.CharField(max_length=200, default='', null=True, blank=True)
    bc_id = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'token': self.token,
            'company': self.company,
            'customer_group_id': self.customer_group_id,
            'bc_id': self.bc_id
        }

    class Meta:
        db_table = 'users'
