# Generated by Django 4.2.6 on 2023-11-15 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_details_campus'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='is_sold',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='details',
            name='is_wishlist',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='details',
            name='recently_viewed',
            field=models.BooleanField(default=False),
        ),
    ]
