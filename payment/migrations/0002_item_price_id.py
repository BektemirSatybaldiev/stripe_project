# Generated by Django 3.2 on 2023-02-13 11:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='price_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
