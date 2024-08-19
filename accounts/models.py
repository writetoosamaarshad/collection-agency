from django.db import models


class Agency(models.Model):
    """
    Represents a collection agency that works with multiple clients.
    Each agency has a name and a unique reference number.
    """
    name = models.CharField(max_length=255)
    reference_no = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    """
    Represents a client that hires a collection agency to collect debts on their behalf.
    Each client is identified by a unique reference number.
    A client is associated with one agency.
    """
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    reference_no = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Consumer(models.Model):
    """
    Represents a consumer who owes debt.
    Each consumer is identified by their unique SSN (Social Security Number).
    """
    name = models.CharField(max_length=255)
    address = models.TextField()
    ssn = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    """
    Represents an account associated with a consumer, containing the balance and status of the debt.
    An account is linked to a specific client and consumer.

    Attributes:
        client: The client for whom the account was created.
        consumer: The consumer associated with the account.
        balance: The current balance of the account.
        status: The current status of the account (e.g., 'In Collection', 'Paid in Full', 'Inactive').
    """
    STATUS_CHOICES = [
        ('IN_COLLECTION', 'In Collection'),
        ('PAID_IN_FULL', 'Paid in Full'),
        ('INACTIVE', 'Inactive'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.client.reference_no} - {self.consumer.name}"
