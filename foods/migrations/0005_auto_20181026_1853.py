# Generated by Django 2.1.2 on 2018-10-26 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0004_auto_20181026_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foods',
            name='code',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='substitute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foods.Foods'),
        ),
    ]