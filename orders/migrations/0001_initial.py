# Generated by Django 3.1.5 on 2021-01-17 05:52

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
                ('total_ex_tax', models.IntegerField()),
                ('total_inc_tax', models.IntegerField()),
                ('bc_order_id', models.IntegerField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.users')),
            ],
            options={
                'db_table': 'orders',
            },
        ),
    ]
