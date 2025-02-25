from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Expense
from .serializers import ExpenseSerializer
from django.utils import timezone
from datetime import timedelta, datetime

@method_decorator(csrf_exempt, name='dispatch')
class ExpenseListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Expense.objects.filter(user=user).order_by('-date')
        filter_param = self.request.query_params.get('filter', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        now = timezone.now().date()

        if filter_param:
            if filter_param == 'week':
                start = now - timedelta(days=7)
                queryset = queryset.filter(date__gte=start, date__lte=now)
            elif filter_param == 'month':
                start = now - timedelta(days=30)
                queryset = queryset.filter(date__gte=start, date__lte=now)
            elif filter_param == '3months':
                start = now - timedelta(days=90)
                queryset = queryset.filter(date__gte=start, date__lte=now)
        elif start_date and end_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=start, date__lte=end)
            except ValueError:
                pass  # If date format is invalid, ignore custom filtering.

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@method_decorator(csrf_exempt, name='dispatch')
class ExpenseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
