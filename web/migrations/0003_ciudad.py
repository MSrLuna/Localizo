# Generated by Django 5.1.3 on 2024-11-15 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_remove_producto_categoria_delete_categoriaproducto_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
    ]
