# Generated by Django 3.2.15 on 2024-01-09 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_userbookrelation_rate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['-id'], 'verbose_name': 'Книга'},
        ),
    ]
