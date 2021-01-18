# Generated by Django 2.2 on 2021-01-18 02:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(max_length=20)),
                ('total_ex_tax', models.IntegerField(blank=True, null=True)),
                ('total_inc_tax', models.IntegerField(blank=True, null=True)),
                ('bc_order_id', models.IntegerField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.Users')),
            ],
            options={
                'db_table': 'orders',
            },
        ),
    ]
