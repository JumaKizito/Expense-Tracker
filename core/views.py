from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from .models import Department, Project, Category, Budget_Management, Expense_Management
from .forms import DepartmentForm, ProjectForm, CategoryForm, BudgetManagementForm, ExpenseManagementForm

# Create your views here.
def dashboard_view(request):
    # Retrieve data for the dashboard
    budget_data = Budget_Management.objects.all()
    expense_data = Expense_Management.objects.all()
    departments = Department.objects.count()
    projects = Project.objects.count()
    
    # Calculate total budget and total expenses
    total_budget = budget_data.aggregate(total_budget=models.Sum('amount'))['total_budget']
    total_expenses = expense_data.aggregate(total_expenses=models.Sum('amount'))['total_expenses']

    
    # Calculate remaining budget
    remaining_budget = total_budget - total_expenses if total_budget is not None and total_expenses is not None else None
    
    # Prepare the context dictionary
    context = {
        'total_budget': total_budget,
        'total_expenses': total_expenses,
        'remaining_budget': remaining_budget,
        'departments': departments,
        'projects': projects,
        # Pass any other data you want to display on the dashboard
    }
    
    # Render the dashboard template with the data
    return render(request, 'core/dashboard.html', context)

def expense_list(request):
    """List expense"""
    expenses = Expense_Management.objects.all()
    context = {'expenses': expenses}
    return render(request, 'core/expense_list.html', context)

def expense_detail(request, pk):
    expense = get_object_or_404(Expense_Management, pk=pk)
    context = {'expense': expense}
    return render(request, 'core/expense_detail.html', context)

def expense_create(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Create a form instance with the POST data
        form = ExpenseManagementForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Redirect to the expense list page
            return redirect('expense_list')
    else:
        # If the request method is not POST, create an empty form instance
        form = ExpenseManagementForm()
    # Render the expense creation form template with the form instance
    return render(request, 'core/expense_form.html', {'form': form})


def expense_update(request, pk):
    # Retrieve the expense object with the given primary key or return a 404 error
    expense = get_object_or_404(Expense_Management, pk=pk)
    # Check if the request method is POST
    if request.method == 'POST':
        # Create a form instance with the POST data and the retrieved expense object
        form = ExpenseManagementForm(request.POST, instance=expense)
        # Check if the form is valid
        if form.is_valid():
            # Save the updated form data to the database
            form.save()
            # Redirect to the expense list page
            return redirect('expense_list')
    else:
        # If the request method is not POST, create a form instance with the retrieved expense object
        form = ExpenseManagementForm(instance=expense)
    # Render the expense update form template with the form instance
    return render(request, 'core/expense_form.html', {'form': form})

def expense_delete(request, pk):
    # Retrieve the expense object with the given primary key or return a 404 error
    expense = get_object_or_404(Expense_Management, pk=pk)
    # Check if the request method is POST
    if request.method == 'POST':
        # Delete the expense object
        expense.delete()
        # Redirect to the expense list page
        return redirect('expense_list')
    # Render the expense delete confirmation template with the expense object
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
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'core/department_form.html', {'form': form})

def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('department-list')
    return render(request, 'core/department_confirm_delete.html', {'department': department})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'core/category_list.html', {'categories': categories})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'core/category_detail.html', {'category': category})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'core/category_form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'core/category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'core/category_confirm_delete.html', {'category': category})

def budget_list(request):
    budgets = Budget_Management.objects.all()
    return render(request, 'core/budget_list.html', {'budgets': budgets})

def budget_detail(request, pk):
    budget = get_object_or_404(Budget_Management, pk=pk)
    return render(request, 'core/budget_detail.html', {'budget': budget})

def budget_create(request):
    if request.method == 'POST':
        form = BudgetManagementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetManagementForm()
    return render(request, 'core/budget_create.html', {'form': form})

def budget_update(request, pk):
    budget = get_object_or_404(Budget_Management, pk=pk)
    if request.method == 'POST':
        form = BudgetManagementForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetManagementForm(instance=budget)
    return render(request, 'core/budget_update.html', {'form': form})

def budget_delete(request, pk):
    budget = get_object_or_404(Budget_Management, pk=pk)
    budget.delete()
    return redirect('budget_list')

