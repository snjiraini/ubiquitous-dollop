# Generated by Django 5.1.7 on 2025-03-28 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonds', '0003_rename_investor_investorbondbid_investor_wallet'),
    ]

    operations = [
        migrations.RenameField(
            model_name='investorbondbid',
            old_name='investor_wallet',
            new_name='investor',
        ),
        migrations.RemoveField(
            model_name='listedcompany',
            name='company_logo',
        ),
        migrations.RemoveField(
            model_name='listedcompany',
            name='industry',
        ),
        migrations.AlterField(
            model_name='listedcompany',
            name='trading_symbol',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
