# Generated by Django 4.0.4 on 2024-03-18 22:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('national_id', models.CharField(max_length=12, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('^\\d{11}$')])),
                ('account_id', models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator('^\\d{4,10}$')])),
                ('client_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('^\\d{10}$')])),
                ('mother_firstname', models.CharField(max_length=50)),
                ('mother_lastname', models.CharField(max_length=50)),
                ('address', models.TextField(blank=True, null=True)),
                ('working', models.BooleanField()),
                ('client_status', models.CharField(blank=True, max_length=50, null=True)),
                ('working_field', models.TextField(blank=True, null=True)),
                ('company_name', models.CharField(blank=True, max_length=50, null=True)),
                ('salary', models.PositiveBigIntegerField(blank=True, null=True)),
                ('housing', models.BooleanField()),
                ('married', models.BooleanField()),
                ('spouse_firstname', models.CharField(blank=True, max_length=50, null=True)),
                ('spouse_lastname', models.CharField(blank=True, max_length=50, null=True)),
                ('num_children', models.PositiveBigIntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=50)),
                ('amount', models.IntegerField()),
                ('source', models.TextField(blank=True, null=True)),
                ('cause', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='services', to='Service.client')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]
