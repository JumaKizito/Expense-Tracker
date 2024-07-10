from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/<int:pk>/', views.expense_detail, name='expense_detail'),
    path('expenses/create/', views.expense_create, name='expense_create'),
    path(
        'expenses/<int:pk>/update/',
        views.expense_update, name='expense_update'
    ),
    path(
        'expenses/<int:pk>/delete/',
        views.expense_delete, name='expense_delete'
    ),
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:pk>',
         views.department_detail, name='department_detail'),
    path(
        'departments/create/',
        views.department_create, name='department_create'
    ),
    path(
        'departments/<int:pk>/update/',
        views.department_update,
        name='department_update'
    ),
    path(
        'departments/<int:pk>/delete/',
        views.department_delete,
        name='department_delete'
    ),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/',
         views.category_detail, name='category_detail'),
    path('categories/create/', views.category_create, name='category_create'),
    path(
        'categories/<int:pk>/update/',
        views.category_update,
        name='category_update'
    ),
    path(
        'categories/<int:pk>/delete/',
        views.category_delete,
        name='category_delete'
    ),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/<int:pk>/', views.budget_detail, name='budget_detail'),
    path('budgets/create/', views.budget_create, name='budget_create'),
    path('budgets/<int:pk>/update/',
         views.budget_update, name='budget_update'),
    path('budgets/<int:pk>/delete/',
         views.budget_delete, name='budget_delete'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/create/', views.project_create, name='project_create'),
    path(
        'projects/<int:pk>/update/',
        views.project_update,
        name='project_update'
    ),
    path(
        'projects/<int:pk>/delete/',
        views.project_delete,
        name='project_delete'
    ),
]
