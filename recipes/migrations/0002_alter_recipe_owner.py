# Generated by Django 5.1 on 2024-08-23 08:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="owner_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
