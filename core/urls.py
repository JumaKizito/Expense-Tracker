from django.urls import path
from core.views import expense_list

urlpatterns = [
    path('', expense_list, name='expense_list'),
]