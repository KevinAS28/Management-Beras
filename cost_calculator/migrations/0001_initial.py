# Generated by Django 4.2 on 2023-05-01 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CostDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CostItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_id', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('unit_count', models.IntegerField()),
                ('unit_type', models.CharField(max_length=25)),
                ('total_price', models.IntegerField()),
                ('sort_order', models.IntegerField(default=-1)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cost_calculator.costdate')),
            ],
        ),
    ]
