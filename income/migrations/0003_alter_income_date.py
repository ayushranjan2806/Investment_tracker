# Generated by Django 4.0 on 2025-01-21 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0002_alter_income_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='date',
            field=models.DateField(default=()),
        ),
    ]
