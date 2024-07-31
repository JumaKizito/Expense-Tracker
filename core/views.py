import csv
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db import models
from .decorators import admin_required


from .models import (
    Department, Project, Category,
    Budget_Management, Expense_Management
)
from .forms import (
    DepartmentForm, ProjectForm,
    CategoryForm, BudgetManagementForm,
    ExpenseManagementForm
)


# Create your views here.
@login_required
def dashboard_view(request):
    # Retrieve data for the dashboard
    budget_data = Budget_Management.objects.all()
    expense_data = Expense_Management.objects.all()
    departments = Department.objects.count()
    projects = Project.objects.count()

    # Calculate total budget and total expenses
    total_budget = budget_data.aggregate(
        total_budget=models.Sum('amount')
        )['total_budget']
    total_expenses = expense_data.aggregate(
        total_expenses=models.Sum('amount')
        )['total_expenses']

    # Calculate remaining budget
    if total_budget is not None and total_expenses is not None:
        remaining_budget = total_budget - total_expenses
    else:
        remaining_budget = None

    # Prepare data for the pie chart (Budget Allocation by Category)
    budget_by_category = budget_data.values(
        'category__name'
        ).annotate(total_amount=models.Sum('amount'))
    pie_chart_data = [
        {
            'category': item['category__name'],
            'total_amount': float(item['total_amount'])
        } for item in budget_by_category]

    # Prepare data for the bar chart (Department-wise Expenses)
    expenses_by_department = expense_data.values(
        'department__name').annotate(total_expenses=models.Sum('amount'))
    bar_chart_data = [
        {
            'department': item['department__name'],
            'total_expenses': float(item['total_expenses'])
        } for item in expenses_by_department]

    # Prepare the context dictionary
    context = {
        'total_budget': total_budget,
        'total_expenses': total_expenses,
        'remaining_budget': remaining_budget,
        'departments': departments,
        'projects': projects,
        # Convert to JSON for passing to template
        'pie_chart_data': json.dumps(pie_chart_data),
        # Convert to JSON for passing to template
        'bar_chart_data': json.dumps(bar_chart_data),
        # Pass any other data you want to display on the dashboard
    }

    # Render the dashboard template with the data
    return render(request, 'core/dashboard.html', context)


@login_required
def expense_list(request):
    """List expense"""
    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

        expenses = Expense_Management.objects.all()

        writer = csv.writer(response)
        writer.writerow(
            [
                'Name', 'Date Created',
                'Department', 'Project',
                'Amount', 'Remarks'
            ]
        )

        for expense in expenses:
            writer.writerow(
                [
                    expense.name,
                    expense.date_created,
                    expense.department.name if expense.department else '',
                    expense.project.name if expense.project else '',
                    expense.amount, expense.remarks
                ]
            )

        return response

    query = request.GET.get('q')
    if query:
        expenses = Expense_Management.objects.filter(
            models.Q(name__icontains=query) |
            models.Q(department__name__icontains=query) |
            models.Q(project__name__icontains=query) |
            models.Q(remarks__icontains=query)
        )
    else:
        expenses = Expense_Management.objects.all()

    paginator = Paginator(expenses, 15)  # Show 15 expenses per page
    page = request.GET.get('page')

    try:
        expenses = paginator.page(page)
    except PageNotAnInteger:
        expenses = paginator.page(1)
    except EmptyPage:
        expenses = paginator.page(paginator.num_pages)

    context = {
        'expenses': expenses,
        'query': query,
    }
    return render(request, 'core/expense_list.html', context)


@login_required
def expense_detail(request, pk):
    expense = get_object_or_404(Expense_Management, pk=pk)
    data = {
        'name': expense.name,
        'date_created': expense.date_created,
        'department': {
            'name': expense.department.name if expense.department else None,
        },
        'project': {
            'name': expense.project.name if expense.project else None,
        },
        'amount': expense.amount,
        'remarks': expense.remarks,
    }
    return JsonResponse(data)

@login_required
@admin_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            budget = get_object_or_404(
                Budget_Management, project=expense.project, department=expense.department
            )

            if budget.amount >= expense.amount:
                budget.amount -= expense.amount
                budget.save()
                expense.save()
                messages.success(
                    request, 'Expense created and budget updated successfully.'
                )
                return redirect('dashboard')
            else:
                messages.error(
                    request, 'Not enough budget available for this expense.'
                )
    else:
        form = ExpenseForm()
    
    return render(request, 'core/expense_form.html', {'form': form})

@login_required
@admin_required
def expense_update(request, pk):
    # Retrieve the expense object with the given
    # primary key or return a 404 error
    expense = get_object_or_404(Expense_Management, pk=pk)
    # Check if the request method is POST
    if request.method == 'POST':
        # Create a form instance with the POST data
        # and the retrieved expense object
        form = ExpenseManagementForm(request.POST, instance=expense)
        # Check if the form is valid
        if form.is_valid():
            # Save the updated form data to the database
            form.save()
            # Redirect to the expense list page
            return redirect('expense_list')
    else:
        # If the request method is not POST, create a form instance
        # with the retrieved expense object
        form = ExpenseManagementForm(instance=expense)
    # Render the expense update form template with the form instance
    return render(request, 'core/expense_form.html', {'form': form})


@login_required
@admin_required
def expense_delete(request, pk):
    # Retrieve the expense object with the given primary key
    # or return a 404 error
    expense = get_object_or_404(Expense_Management, pk=pk)
    # Check if the request method is POST
    if request.method == 'POST':
        expense.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': True})


# Department Views
@login_required
def department_list(request):
    """List departments"""
    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response[
            'Content-Disposition'] = 'attachment; filename="departments.csv"'

        departments = Department.objects.all()

        writer = csv.writer(response)
        writer.writerow(['Name'])

        for department in departments:
            writer.writerow([department.name])

        return response

    query = request.GET.get('q')
    if query:
        departments = Department.objects.filter(name__icontains=query)
    else:
        departments = Department.objects.all()

    paginator = Paginator(departments, 15)  # Show 15 departments per page
    page = request.GET.get('page')

    try:
        departments = paginator.page(page)
    except PageNotAnInteger:
        departments = paginator.page(1)
    except EmptyPage:
        departments = paginator.page(paginator.num_pages)

    context = {
        'departments': departments,
        'query': query,
    }
    return render(request, 'core/department_list.html', context)


@login_required
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    context = {'department': department}
    return render(request, 'core/department_detail.html', context)


@login_required
@admin_required
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'core/department_form.html', {'form': form})


@login_required
@admin_required
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


@login_required
@admin_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def category_list(request):
    query = request.GET.get('q')
    if query:
        categories = Category.objects.filter(name__icontains=query)
    else:
        categories = Category.objects.all()

    paginator = Paginator(categories, 15)
    page = request.GET.get('page')

    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'query': query,
    }
    return render(request, 'core/category_list.html', context)


@login_required
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'core/category_detail.html', {'category': category})


@login_required
@admin_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'core/category_form.html', {'form': form})


@login_required
@admin_required
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


@login_required
@admin_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def budget_list(request):
    """List budgets"""
    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="budgets.csv"'

        budgets = Budget_Management.objects.all()

        writer = csv.writer(response)
        writer.writerow(
            [
                'Name', 'Date Created',
                'Department', 'Project',
                'Amount', 'Category', 'Remarks'
            ]
        )

        for budget in budgets:
            writer.writerow(
                [
                    budget.name,
                    budget.date_created,
                    budget.department.name if budget.department else '',
                    budget.project.name if budget.project else '',
                    budget.amount,
                    budget.category.name if budget.category else '',
                    budget.remarks
                ]
            )

        return response

    query = request.GET.get('q')
    if query:
        budgets = Budget_Management.objects.filter(name__icontains=query)
    else:
        budgets = Budget_Management.objects.all()

    paginator = Paginator(budgets, 15)  # Show 15 budgets per page
    page = request.GET.get('page')

    try:
        budgets = paginator.page(page)
    except PageNotAnInteger:
        budgets = paginator.page(1)
    except EmptyPage:
        budgets = paginator.page(paginator.num_pages)

    context = {
        'budgets': budgets,
        'query': query,
    }
    return render(request, 'core/budget_list.html', context)


@login_required
def budget_detail(request, pk):
    budget = get_object_or_404(Budget_Management, pk=pk)
    data = {
        'date_created': budget.date_created,
        'name': budget.name,
        'project': {
            'name': budget.project.name if budget.project else None,
        },
        'amount': budget.amount,
        'category': {
            'name': budget.category.name if budget.category else None,
        }
    }
    return JsonResponse(data)


@login_required
@admin_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetManagementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetManagementForm()
    return render(request, 'core/budget_create.html', {'form': form})


@login_required
@admin_required
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


@login_required
@admin_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget_Management, pk=pk)
    if request.method == 'POST':
        budget.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def project_list(request):
    """List projects"""
    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="projects.csv"'

        projects = Project.objects.all()

        writer = csv.writer(response)
        writer.writerow(['Name', 'Department'])

        for project in projects:
            writer.writerow([project.name, project.department.name])

        return response

    query = request.GET.get('q')
    if query:
        projects = Project.objects.filter(name__icontains=query)
    else:
        projects = Project.objects.all()

    paginator = Paginator(projects, 15)  # Show 15 projects per page
    page = request.GET.get('page')

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    context = {
        'projects': projects,
        'query': query,
    }
    return render(request, 'core/project_list.html', context)


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    data = {
        'name': project.name,
    }
    return JsonResponse(data)


@login_required
@admin_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'core/project_form.html', {'form': form})


@login_required
@admin_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'core/project_form.html', {'form': form})


@login_required
@admin_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
