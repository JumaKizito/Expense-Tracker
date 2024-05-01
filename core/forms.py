from django import forms
from .models import Department, Project, Category, Budget_Management, Expense_Management

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class BudgetManagementForm(forms.ModelForm):
    class Meta:
        model = Budget_Management
        fields = '__all__'

class ExpenseManagementForm(forms.ModelForm):
    class Meta:
        model = Expense_Management
        fields = '__all__'
