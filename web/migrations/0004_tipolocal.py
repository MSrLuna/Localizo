# Generated by Django 5.1.3 on 2024-11-15 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_ciudad'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoLocal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
    ]