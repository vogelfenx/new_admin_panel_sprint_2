# Generated by Django 3.2 on 2023-02-07 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(
            sql=('CREATE SCHEMA IF NOT EXISTS content;'),
            reverse_sql=('DROP SCHEMA IF EXISTS CONTENT;'),
        ),
    ]
