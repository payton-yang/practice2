# Generated by Django 2.2 on 2021-01-13 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=20)),
                ('last_name', models.CharField(default='', max_length=20)),
                ('email', models.CharField(max_length=200, unique=True)),
                ('password', models.CharField(max_length=25)),
                ('token', models.CharField(blank=True, max_length=200, null=True)),
                ('company', models.CharField(default='', max_length=200)),
                ('customer_group_id', models.IntegerField(default=0)),
                ('phone', models.CharField(default='', max_length=200)),
                ('bc_id', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
