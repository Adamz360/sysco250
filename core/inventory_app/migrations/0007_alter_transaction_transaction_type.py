# Generated by Django 5.1.3 on 2024-12-05 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_app', '0006_alter_transaction_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('ADD', 'Add Stock'), ('REMOVE', 'Remove Stock'), ('UPDATE', 'Update Stock')], max_length=10),
        ),
    ]
