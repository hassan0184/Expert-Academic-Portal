# Generated by Django 3.2.9 on 2021-12-13 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0030_auto_20211213_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
