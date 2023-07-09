# Generated by Django 4.2.3 on 2023-07-09 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_productselection_selected_at_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='productselection',
            constraint=models.UniqueConstraint(fields=('user', 'product'), name='unique_user_product'),
        ),
    ]