# Generated by Django 5.1.4 on 2025-01-15 15:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "expensetracker",
            "0002_alter_category_options_alter_expense_options_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="date",
            field=models.DateField(
                default=datetime.datetime(
                    2025, 1, 15, 15, 24, 57, 414663, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
