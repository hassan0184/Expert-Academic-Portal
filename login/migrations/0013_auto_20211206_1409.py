# Generated by Django 3.2.9 on 2021-12-06 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0012_auto_20211206_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='sno',
        ),
        migrations.AddField(
            model_name='comment',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
