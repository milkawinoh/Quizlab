# Generated by Django 5.0.6 on 2024-06-30 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='share_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
