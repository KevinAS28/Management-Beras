# Generated by Django 4.2 on 2023-05-08 04:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cost_calculator', '0017_rename_costdate_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='costitem',
            old_name='cost_date',
            new_name='the_date',
        ),
    ]
