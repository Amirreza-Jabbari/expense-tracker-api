from django.urls import path
from .views import ExpenseListCreateAPIView, ExpenseDetailAPIView

app_name = 'expenses'

urlpatterns = [
    path('', ExpenseListCreateAPIView.as_view(), name='list_create'),
    path('<int:pk>/', ExpenseDetailAPIView.as_view(), name='detail'),
]
