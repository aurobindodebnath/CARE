# Generated by Django 3.1.1 on 2020-11-19 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0007_auto_20201118_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulkactivity',
            name='category',
            field=models.CharField(choices=[(None, '----------------'), ('app_sec', 'Penetration Testing'), ('vapt', 'Vulnerability Assessment'), ('config_review', 'Configuration Audit'), ('multiple', 'Multiple Activities')], default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='bulkactivity',
            name='task',
            field=models.ForeignKey(default=25, on_delete=django.db.models.deletion.CASCADE, to='activities.task'),
            preserve_default=False,
        ),
    ]
