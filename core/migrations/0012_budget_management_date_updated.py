# Generated by Django 5.0.4 on 2024-07-31 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_expense_management_budget'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget_management',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]