from django.contrib import admin
from .models import Department, Project, Category, Budget_Management, Expense_Management

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'date_created')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(Budget_Management)
class BudgetManagementAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'project', 'amount', 'category', 'date_created')
    list_filter = ('department', 'project', 'category')
    search_fields = ('name', 'remarks')

@admin.register(Expense_Management)
class ExpenseManagementAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'project', 'amount', 'date_created')
    list_filter = ('department', 'project')
    search_fields = ('name', 'remarks')
