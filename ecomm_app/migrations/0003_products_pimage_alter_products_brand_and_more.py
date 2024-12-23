# Generated by Django 5.0.4 on 2024-07-11 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm_app', '0002_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='pimage',
            field=models.ImageField(default=0, upload_to='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='products',
            name='brand',
            field=models.CharField(max_length=100, verbose_name='Brand'),
        ),
        migrations.AlterField(
            model_name='products',
            name='cat',
            field=models.IntegerField(choices=[(1, 'dairy'), (2, 'fruits'), (3, 'vegetables'), (4, 'Pasta_rice_cereals'), (5, 'Meat_alternatives'), (6, 'Cans_jars'), (7, 'Bread_baked'), (8, 'Frozen_food'), (9, 'sauces'), (10, 'Nuts_snacks'), (11, 'beverages'), (12, 'herbs_spices')], verbose_name='Categgory'),
        ),
        migrations.AlterField(
            model_name='products',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Availabel'),
        ),
        migrations.AlterField(
            model_name='products',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='products',
            name='pdetails',
            field=models.CharField(max_length=100, verbose_name='Product Details'),
        ),
    ]
