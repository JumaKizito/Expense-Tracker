from django.urls import path
from core.views import *

urlpatterns = [
    path('', expense_list, name='expense_list'),
    path('<int:pk>/', expense_detail, name='expense_detail'),
    path('create/', expense_create, name='expense_create'),
    path('<int:pk>/', expense_detail, name='expense_detail'),
    path('<int:pk>/update/', expense_update, name='expense_update'),
    path('<int:pk>/delete/', expense_delete, name='expense_delete'),
    path('deparments/', department_list, name='department_list'),
    path('departments/<int:pk>', department_detail, name='department_detail'),
    path('department', department_create, name='department_create'),
    path('<int:pk>/update/', department_update, name='department_update'),
    path('<int:pk>/delete/', department_delete, name='department_delete'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('categories/', category_list, name='category_list'),
    path('category/<int:pk>/', category_detail, name='category_detail'),
    path('category/create/', category_create, name='category_create'),
    path('category/<int:pk>/update/', category_update, name='category_update'),
    path('category/<int:pk>/delete/', category_delete, name='category_delete'),
    path('budgets/', budget_list, name='budget_list'),
    path('budgets/<int:pk>/', budget_detail, name='budget_detail'),
    path('budgets/create/', budget_create, name='budget_create'),
    path('budgets/<int:pk>/update/', budget_update, name='budget_update'),
    path('budgets/<int:pk>/delete/', budget_delete, name='budget_delete'),
]
