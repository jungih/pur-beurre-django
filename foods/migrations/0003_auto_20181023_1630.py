# Generated by Django 2.1.2 on 2018-10-23 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0002_auto_20181023_1556'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foods',
            old_name='my_food',
            new_name='substitute',
        ),
        migrations.AlterField(
            model_name='foods',
            name='substitute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foods.Foods'),
        ),
    ]