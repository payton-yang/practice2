# Generated by Django 2.2 on 2021-01-14 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20210114_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.CharField(default='', max_length=5000),
        ),
    ]