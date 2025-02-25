from datetime import date, timedelta, datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Expense

User = get_user_model()

class ExpenseAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user and force authentication
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword123",
            f_name="Test",
            l_name="User"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url_list_create = reverse("expenses:list_create")

    def test_create_expense(self):
        """Test that a user can create an expense."""
        data = {
            "title": "Grocery Shopping",
            "description": "Bought vegetables and fruits",
            "amount": "45.67",
            "date": "2025-02-20",
            "category": "Groceries"
        }
        response = self.client.post(self.url_list_create, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["description"], data["description"])
        self.assertEqual(response.data["amount"], data["amount"])
        self.assertEqual(response.data["date"], data["date"])
        self.assertEqual(response.data["category"], data["category"])
        # Verify that the expense is linked to the authenticated user
        expense = Expense.objects.get(id=response.data["id"])
        self.assertEqual(expense.user, self.user)

    def test_list_expenses(self):
        """Test that listing returns only the expenses of the authenticated user."""
        # Create two expenses for our test user
        Expense.objects.create(
            user=self.user, title="Expense 1", description="Test 1",
            amount="10.00", date=date(2025, 2, 20), category="Others"
        )
        Expense.objects.create(
            user=self.user, title="Expense 2", description="Test 2",
            amount="20.00", date=date(2025, 2, 21), category="Leisure"
        )
        response = self.client.get(self.url_list_create)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_expense(self):
        """Test retrieving a single expense."""
        expense = Expense.objects.create(
            user=self.user, title="Expense Retrieve", description="Test retrieve",
            amount="15.00", date=date(2025, 2, 22), category="Health"
        )
        url_detail = reverse("expenses:detail", args=[expense.id])
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], expense.title)

    def test_update_expense(self):
        """Test that a user can update their expense."""
        expense = Expense.objects.create(
            user=self.user, title="Expense Update", description="Test update",
            amount="10.00", date=date(2025, 2, 23), category="Others"
        )
        url_detail = reverse("expenses:detail", args=[expense.id])
        update_data = {"title": "Updated Expense", "amount": "15.50"}
        response = self.client.patch(url_detail, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expense.refresh_from_db()
        self.assertEqual(expense.title, update_data["title"])
        # Ensure the decimal field is updated correctly.
        self.assertEqual(str(expense.amount), update_data["amount"])

    def test_delete_expense(self):
        """Test that a user can delete an expense."""
        expense = Expense.objects.create(
            user=self.user, title="Expense Delete", description="Test delete",
            amount="10.00", date=date(2025, 2, 24), category="Others"
        )
        url_detail = reverse("expenses:detail", args=[expense.id])
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Expense.objects.filter(id=expense.id).exists())

    def test_filter_expenses_by_week(self):
        """Test filtering expenses by past week."""
        today = date.today()
        # Expense within the past week
        expense_recent = Expense.objects.create(
            user=self.user, title="Recent Expense", description="Within week",
            amount="20.00", date=today, category="Health"
        )
        # Expense older than a week
        expense_old = Expense.objects.create(
            user=self.user, title="Old Expense", description="Older than week",
            amount="30.00", date=today - timedelta(days=10), category="Utilities"
        )
        response = self.client.get(self.url_list_create, {"filter": "week"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Only the recent expense should be returned
        returned_ids = [expense["id"] for expense in response.data]
        self.assertIn(expense_recent.id, returned_ids)
        self.assertNotIn(expense_old.id, returned_ids)

    def test_filter_expenses_by_custom_date_range(self):
        """Test filtering expenses with a custom start and end date."""
        # Expense within the custom date range
        expense_in_range = Expense.objects.create(
            user=self.user, title="Expense in Range", description="Within date range",
            amount="50.00", date=date(2025, 1, 15), category="Electronics"
        )
        # Expense outside the custom date range
        Expense.objects.create(
            user=self.user, title="Expense out of Range", description="Outside date range",
            amount="60.00", date=date(2025, 2, 15), category="Electronics"
        )
        response = self.client.get(self.url_list_create, {"start_date": "2025-01-01", "end_date": "2025-01-31"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Only one expense should match the custom date range
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Expense in Range")
