# Generated by Django 2.1.5 on 2019-01-18 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
