import csv

from django.core.management.base import BaseCommand
from accounts.models import Account, Client, Consumer, Agency


class Command(BaseCommand):
    """
    Django management command to ingest accounts data from a CSV file.

    This command reads a CSV file and creates or updates Account, Client, Consumer,
    and Agency objects in the database based on the data provided in the file.
    """
    help = 'Ingest a CSV file of accounts'

    def add_arguments(self, parser):
        """
        Define the command-line arguments that can be passed to the command.

        :param parser: ArgumentParser object to which arguments can be added.
        """
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        parser.add_argument('agency_name', type=str, help='Name of the agency')
        parser.add_argument('agency_reference_no', type=str, help='Reference number of the agency')

    def handle(self, *args, **kwargs):
        """
        The main logic of the command. This method is called when the command is run.

        :param args: Additional positional arguments.
        :param kwargs: Keyword arguments containing the command-line options.
        """
        file_path = kwargs['file_path']
        agency_name = kwargs['agency_name']
        agency_reference_no = kwargs['agency_reference_no']

        # Get or create the agency based on the provided name and reference number.
        agency, _ = Agency.objects.get_or_create(name=agency_name, reference_no=agency_reference_no)

        # Open the CSV file and start reading its contents.
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)

            # Iterate through each row in the CSV file.
            for row in reader:
                # Get or create the client associated with the agency.
                client_ref_no = row['client reference no']
                client, _ = Client.objects.get_or_create(
                    agency=agency,
                    reference_no=client_ref_no,
                    name=row['consumer name']
                )

                # Get or create the consumer associated with the client.
                consumer_name = row['consumer name']
                consumer, _ = Consumer.objects.get_or_create(
                    name=consumer_name,
                    address=row['consumer address'],
                    ssn=row['ssn']
                )

                # Create a new account for the client and consumer.
                Account.objects.create(
                    client=client,
                    consumer=consumer,
                    balance=row['balance'],
                    status=row['status']
                )

        # Output a success message upon completion.
        self.stdout.write(self.style.SUCCESS('CSV data ingested successfully'))
