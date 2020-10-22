# Generated by Django 3.1.2 on 2020-10-21 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval_engine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvalpending',
            name='hiring_manager',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='approvalpending',
            name='status',
            field=models.CharField(choices=[('approved', 'Approved'), ('rejected', 'Rejected'), ('pending', 'Pending')], default='pending', max_length=100),
        ),
    ]