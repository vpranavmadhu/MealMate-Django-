# Generated by Django 5.2.3 on 2025-07-07 16:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('is_available', models.BooleanField(default=True)),
                ('category', models.CharField(max_length=50)),
                ('img', models.URLField(default='https://www.citypng.com/public/uploads/preview/loading-load-icon-transparent-png-701751695033022vy5stltzj3.png')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res_name', models.CharField(max_length=100)),
                ('food_cat', models.CharField(max_length=200)),
                ('rating', models.FloatField()),
                ('img', models.URLField(default='https://www.citypng.com/public/uploads/preview/loading-load-icon-transparent-png-701751695033022vy5stltzj3.png')),
                ('address', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customer')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.cart')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.menu')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(through='delivery.CartItem', to='delivery.menu'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razorpay_order_id', models.CharField(max_length=100, null=True)),
                ('total_price', models.FloatField(null=True)),
                ('order_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=100, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customer')),
                ('items', models.ManyToManyField(to='delivery.menu')),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='res',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.restaurant'),
        ),
    ]
