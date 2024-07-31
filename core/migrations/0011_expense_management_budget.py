# Generated by Django 5.0.4 on 2024-07-31 19:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_budget_management_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense_management',
            name='budget',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.budget_management'),
        ),
    ]
