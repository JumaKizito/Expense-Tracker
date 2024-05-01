from django.contrib import admin
from .models import Budget_Management, Category, Expense_Management, Project, Department

# Register your models here.
admin.site.register(Budget_Management)
admin.site.register(Category)
admin.site.register(Expense_Management)
admin.site.register(Project)
admin.site.register(Department)