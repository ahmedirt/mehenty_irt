# Generated by Django 3.0.5 on 2024-05-11 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_auto_20240511_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='category',
            field=models.CharField(choices=[('plumbing', 'Plumbing'), ('electricity', 'Electricity'), ('painting', 'Painting'), ('carpentry', 'Carpentry')], max_length=50),
        ),
    ]