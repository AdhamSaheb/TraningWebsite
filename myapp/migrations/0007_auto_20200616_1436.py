# Generated by Django 3.0.7 on 2020-06-16 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20200616_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='album',
            field=models.CharField(default='', max_length=100),
        ),
    ]