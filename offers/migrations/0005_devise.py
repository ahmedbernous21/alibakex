# Generated by Django 4.1.4 on 2023-01-08 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0004_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Devise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
