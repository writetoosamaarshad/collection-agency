from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Account, Agency, Client, Consumer
from .serializers import AccountSerializer
import csv
from drf_yasg.utils import swagger_auto_schema  # Utility for Swagger documentation
from drf_yasg import openapi  # Module for OpenAPI specifications
import django_filters
from django_filters.rest_framework import DjangoFilterBackend


class AccountFilter(django_filters.FilterSet):
    """
    FilterSet class for filtering accounts based on various criteria.

    Filters:
    - min_balance: Filters accounts with a balance greater than or equal to a specified amount.
    - max_balance: Filters accounts with a balance less than or equal to a specified amount.
    - consumer_name: Filters accounts by consumer name (case-insensitive, partial matches allowed).
    - status: Filters accounts by their status, according to the choices defined in Account.STATUS_CHOICES.
    """

    min_balance = django_filters.NumberFilter(field_name='balance', lookup_expr='gte')
    max_balance = django_filters.NumberFilter(field_name='balance', lookup_expr='lte')
    consumer_name = django_filters.CharFilter(field_name='consumer__name', lookup_expr='icontains')
    status = django_filters.ChoiceFilter(field_name='status', choices=Account.STATUS_CHOICES)

    class Meta:
        model = Account
        fields = ['min_balance', 'max_balance', 'consumer_name', 'status']  # Fields available for filtering


class AccountListView(generics.ListAPIView):
    """
    API endpoint that allows querying of accounts based on various filters.

    Filters:
    - min_balance: Minimum balance to filter accounts by.
    - max_balance: Maximum balance to filter accounts by.
    - consumer_name: Part or full name of the consumer to filter accounts by.
    - status: Status of the account (e.g., 'IN_COLLECTION', 'PAID_IN_FULL', 'INACTIVE').

    Supports ordering by balance, consumer name, and status.
    """

    queryset = Account.objects.all()  # Queryset containing all accounts
    serializer_class = AccountSerializer  # Serializer class used for accounts
    filter_backends = (DjangoFilterBackend,)  # Specifies that filtering is supported
    filterset_class = AccountFilter  # FilterSet class used for filtering accounts


class CSVUploadView(APIView):
    """
    API endpoint to upload a CSV file and ingest the account data.
    The CSV file should have columns: client reference no, balance, status, consumer name,
    consumer address, ssn.
    """

    parser_classes = [MultiPartParser, FormParser]  # Parsers to handle file uploads

    @swagger_auto_schema(
        operation_description="Upload a CSV file containing account data.",
        manual_parameters=[
            openapi.Parameter(
                'file', openapi.IN_FORM, description="CSV file", type=openapi.TYPE_FILE, required=True),
            openapi.Parameter(
                'agency_name', openapi.IN_FORM, description="Name of the agency", type=openapi.TYPE_STRING,
                required=True),
            openapi.Parameter(
                'agency_reference_no', openapi.IN_FORM, description="Reference number of the agency",
                type=openapi.TYPE_STRING, required=True),
        ],
        responses={201: 'CSV data ingested successfully'},  # Response description for successful upload
    )
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to upload and process a CSV file.
        """

        # Extract agency details and file object from the request
        agency_name = request.data.get('agency_name')
        agency_ref_no = request.data.get('agency_reference_no')
        file_obj = request.FILES['file']

        # Get or create an Agency instance based on the provided name and reference number
        agency, _ = Agency.objects.get_or_create(name=agency_name, reference_no=agency_ref_no)

        # Decode the uploaded file and parse it as a CSV
        decoded_file = file_obj.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        # Process each row in the CSV file
        for row in reader:
            client_ref_no = row['client reference no']
            client, _ = Client.objects.get_or_create(agency=agency, reference_no=client_ref_no)

            # Get or create a Consumer instance based on the provided details
            consumer_name = row['consumer name']
            consumer, _ = Consumer.objects.get_or_create(
                name=consumer_name,
                address=row['consumer address'],
                ssn=row['ssn']
            )

            # Create a new Account instance with the parsed data
            Account.objects.create(
                client=client,
                consumer=consumer,
                balance=row['balance'],
                status=row['status']
            )

        # Return a success response after processing the CSV data
        return Response({'status': 'success', 'message': 'CSV data ingested successfully'},
                        status=status.HTTP_201_CREATED)
