# Generated by Django 4.2.15 on 2024-08-13 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('reference_no', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('ssn', models.CharField(max_length=11, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('reference_no', models.CharField(max_length=100, unique=True)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.agency')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('IN_COLLECTION', 'In Collection'), ('PAID_IN_FULL', 'Paid in Full'), ('INACTIVE', 'Inactive')], max_length=20)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.client')),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.consumer')),
            ],
        ),
    ]
