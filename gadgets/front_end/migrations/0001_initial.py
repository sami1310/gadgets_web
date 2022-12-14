# Generated by Django 4.1.1 on 2022-10-20 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('price', models.FloatField()),
                ('category', models.CharField(choices=[('D', 'Desktop'), ('L', 'Laptop'), ('M', 'Mobile'), ('C', 'Camera')], max_length=2)),
                ('label', models.CharField(choices=[('N', 'New'), ('S', 'SecondHand')], max_length=2)),
                ('discount', models.FloatField()),
                ('description', models.TextField()),
                ('slug', models.SlugField()),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
    ]
