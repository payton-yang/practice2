from django.db import models


# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=25)
    token = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return {
            'name': self.name,
            'email': self.email,
        }

    class Meta:
        db_table = 'users'
