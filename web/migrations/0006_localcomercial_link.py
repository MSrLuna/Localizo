# Generated by Django 5.1.3 on 2024-11-15 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_localcomercial'),
    ]

    operations = [
        migrations.AddField(
            model_name='localcomercial',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]