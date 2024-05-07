from django import forms
from .models import Department, Project, Category, Budget_Management, Expense_Management

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class BudgetManagementForm(forms.ModelForm):
    class Meta:
        model = Budget_Management
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ExpenseManagementForm(forms.ModelForm):
    class Meta:
        model = Expense_Management
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control'}),
        }
