# Generated by Django 3.2 on 2021-04-23 14:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('website', models.CharField(max_length=127)),
                ('email_domain', models.CharField(max_length=127)),
                ('membership', models.BooleanField(default=False)),
                ('membership_start_date', models.DateTimeField(default=datetime.date.today)),
                ('membership_end_date', models.DateField()),
            ],
        ),
    ]
