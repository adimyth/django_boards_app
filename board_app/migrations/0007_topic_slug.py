# Generated by Django 2.1.5 on 2019-02-02 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board_app', '0006_board_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]