# Generated by Django 5.1.7 on 2025-03-28 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listedcompany',
            name='company_logo',
            field=models.ImageField(blank=True, null=True, upload_to='company_logos/'),
        ),
        migrations.AddField(
            model_name='listedcompany',
            name='industry',
            field=models.CharField(choices=[('Agriculture', 'Agriculture'), ('Automobiles & Accessories', 'Automobiles & Accessories'), ('Banking', 'Banking'), ('Commercial & Services', 'Commercial & Services'), ('Construction & Allied', 'Construction & Allied'), ('Energy & Petroleum', 'Energy & Petroleum'), ('Insurance', 'Insurance'), ('Investment', 'Investment'), ('Investment Services', 'Investment Services'), ('Manufacturing & Allied', 'Manufacturing & Allied'), ('Telecommunication & Technology', 'Telecommunication & Technology'), ('Real Estate Investment Trust', 'Real Estate Investment Trust'), ('Exchange Traded Fund', 'Exchange Traded Fund')], default='Banking', max_length=50),
        ),
        migrations.AlterField(
            model_name='listedcompany',
            name='trading_symbol',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
