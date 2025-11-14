from django.urls import path
from . import views

urlpatterns = [
    path('auth/login/', views.LoginAPIView.as_view(), name='login'),
    path('transactions/', views.TransactionListCreateAPIView.as_view(), name='transactions'),
    path('budget/', views.BudgetRetrieveUpdateAPIView.as_view(), name='budget'),
    path('summary/', views.FinancialSummaryAPIView.as_view(), name='summary'),
]
