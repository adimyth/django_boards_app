# Generated by Django 2.1.5 on 2019-02-01 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board_app', '0004_topic_views'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ['-views']},
        ),
        migrations.AlterField(
            model_name='post',
            name='message',
            field=models.TextField(max_length=100),
        ),
    ]
