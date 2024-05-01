from django.shortcuts import render, get_object_or_404, redirect
from .models import Department, Project, Category, Budget_Management, Expense_Management
from .forms import DepartmentForm, ProjectForm, CategoryForm, BudgetManagementForm, ExpenseManagementForm

# Create your views here.
def expense_list(request):
    """List expense"""
    expenses = Expense_Management.objects.all()
    context = {'expenses': expenses}
    return render(request, 'core/expense_list.html', context)

def expense_detail(request, pk):
    expense = get_object_or_404(Expense_Management, pk=pk)
    return render(request, 'core/expense_detail.html', {'expense': expense})

def expense_create(request):
    if request.method == 'POST':
        form = ExpenseManagementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense-list')
    else:
        form = ExpenseManagementForm()
    return render(request, 'core/expense_form.html', {'form': form})

def expense_update(request, pk):
    expense = get_object_or_404(Expense_Management, pk=pk)
    if request.method == 'POST':
        form = ExpenseManagementForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense-list')
    else:
        form = ExpenseManagementForm(instance=expense)
    return render(request, 'core/expense_form.html', {'form': form})

def expense_delete(request, pk):
    expense = get_object_or_404(Expense_Management, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense-list')
    return render(request, 'core/expense_confirm_delete.html', {'expense': expense})

# Department Views
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'core/department_list.html', {'departments': departments})

def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    return render(request, 'core/department_detail.html', {'department': department})

def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department-list')
    else:
        form = DepartmentForm()
    return render(request, 'core/department_form.html', {'form': form})

def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department-list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'core/department_form.html', {'form': form})

def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('department-list')
    return render(request, 'core/department_confirm_delete.html', {'department': department})
