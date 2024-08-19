import os

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import Agency, Client, Consumer, Account


class AccountModelTest(TestCase):
    """
    Test case for the Account model.
    Ensures that Account instances are correctly created and linked to the appropriate Client and Consumer.
    """

    def setUp(self):
        """
        Set up initial data for the Account model test.
        Creates an Agency, Client, Consumer, and Account instance for testing.
        """
        self.agency = Agency.objects.create(name="Test Agency", reference_no="AGENCY001")
        self.client = Client.objects.create(name="Test Client", reference_no="CLIENT001", agency=self.agency)
        self.consumer = Consumer.objects.create(name="Test Consumer", address="123 Main St", ssn="123-45-6789")
        self.account = Account.objects.create(
            client=self.client,
            consumer=self.consumer,
            balance=100.00,
            status="IN_COLLECTION"
        )

    def test_account_creation(self):
        """
        Test that an account is correctly created and linked to a client and consumer.
        Asserts that the client, consumer, balance, and status are set correctly.
        """
        self.assertEqual(self.account.client.name, "Test Client")
        self.assertEqual(self.account.consumer.name, "Test Consumer")
        self.assertEqual(float(self.account.balance), 100.00)
        self.assertEqual(self.account.status, "IN_COLLECTION")


class CSVUploadAPITest(TestCase):
    """
    Test case for the CSV upload API.
    Ensures that CSV data is correctly ingested via the API endpoint.
    """

    def setUp(self):
        """
        Set up the API client and a sample CSV file for testing the upload.
        """
        self.client = APIClient()
        self.agency_data = {
            "agency_name": "Test Agency",
            "agency_reference_no": "AGENCY001",
        }
        self.csv_file_path = os.path.join(os.path.dirname(__file__), 'test_data.csv')
        with open(self.csv_file_path, 'w') as f:
            f.write("client reference no,balance,status,consumer name,consumer address,ssn\n")
            f.write("CLIENT001,100.00,IN_COLLECTION,Test Consumer,123 Main St,123-45-6789\n")

    def tearDown(self):
        """
        Clean up the test CSV file after the test is complete.
        """
        os.remove(self.csv_file_path)

    def test_csv_upload(self):
        """
        Test the CSV ingestion via the API endpoint.
        Ensures that the CSV file is correctly processed and an Account is created.
        """
        with open(self.csv_file_path, 'rb') as csv_file:
            response = self.client.post(reverse('upload-csv'), {
                **self.agency_data,
                'file': csv_file
            })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Account.objects.exists())
        account = Account.objects.first()
        self.assertEqual(account.consumer.name, "Test Consumer")


class AccountListViewTest(TestCase):
    """
    Test case for the Account list view API.
    Ensures that the account listing and filtering functionalities work as expected.
    """

    def setUp(self):
        """
        Set up the API client and initial data for testing the account list view.
        Creates multiple Account instances for testing list and filter views.
        """
        self.client = APIClient()
        self.agency = Agency.objects.create(name="Test Agency", reference_no="AGENCY001")
        self.client_obj = Client.objects.create(name="Test Client", reference_no="CLIENT001", agency=self.agency)
        self.consumer1 = Consumer.objects.create(name="John Doe", address="123 Main St", ssn="123-45-6789")
        self.consumer2 = Consumer.objects.create(name="Jane Smith", address="456 Elm St", ssn="987-65-4321")
        Account.objects.create(client=self.client_obj, consumer=self.consumer1, balance=200.00, status="IN_COLLECTION")
        Account.objects.create(client=self.client_obj, consumer=self.consumer2, balance=500.00, status="PAID_IN_FULL")

    def test_account_list_view(self):
        """
        Test the account list view without filters.
        Ensures that all accounts are returned in the response.
        """
        response = self.client.get(reverse('account-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_account_list_view_with_filters(self):
        """
        Test the account list view with filters.
        Ensures that the correct accounts are returned based on balance and status filters.
        """
        response = self.client.get(reverse('account-list'), {
            'min_balance': 100,
            'max_balance': 300,
            'status': 'IN_COLLECTION'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['consumer']['name'], 'John Doe')
