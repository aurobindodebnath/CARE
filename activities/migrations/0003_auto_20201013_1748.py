# Generated by Django 3.1.1 on 2020-10-13 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_auto_20201013_1313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='id',
        ),
        migrations.AlterField(
            model_name='task',
            name='code',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]