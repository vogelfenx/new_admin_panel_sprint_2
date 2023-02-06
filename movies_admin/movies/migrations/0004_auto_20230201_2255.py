# Generated by Django 3.2 on 2023-02-01 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_person_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filmwork',
            name='certificate',
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='certificate_file_path',
            field=models.FileField(blank=True, null=True, upload_to='movies/',
                                   verbose_name='certificate'),
        ),
    ]