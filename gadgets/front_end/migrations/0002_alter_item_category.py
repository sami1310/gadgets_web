# Generated by Django 4.1.1 on 2022-10-20 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('D', 'Desktop'), ('L', 'Laptop'), ('M', 'Mobile'), ('C', 'Camera'), ('K', 'Keyboard')], max_length=2),
        ),
    ]
