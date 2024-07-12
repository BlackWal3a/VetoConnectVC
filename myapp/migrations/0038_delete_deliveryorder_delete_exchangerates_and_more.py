# Generated by Django 4.2.7 on 2024-04-27 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0037_account_dark_mode'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DeliveryOrder',
        ),
        migrations.DeleteModel(
            name='ExchangeRates',
        ),
        migrations.DeleteModel(
            name='Invoice',
        ),
        migrations.DeleteModel(
            name='UnitConversion',
        ),
        migrations.RenameField(
            model_name='account',
            old_name='provider1',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='account',
            old_name='provider2',
            new_name='surname',
        ),
        migrations.RemoveField(
            model_name='account',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='account',
            name='geography_filter_id',
        ),
        migrations.RemoveField(
            model_name='account',
            name='geography_global_selection',
        ),
        migrations.RemoveField(
            model_name='account',
            name='is_selected',
        ),
        migrations.RemoveField(
            model_name='account',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='account',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='account',
            name='suppliers_global_selection',
        ),
    ]
