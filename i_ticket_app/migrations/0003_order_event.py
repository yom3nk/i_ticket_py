# Generated by Django 5.0.1 on 2024-02-09 14:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('i_ticket_app', '0002_alter_order_user_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='i_ticket_app.event'),
            preserve_default=False,
        ),
    ]
