# Generated by Django 2.2.3 on 2019-07-22 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aidants_connect_web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usager',
            name='sub',
            field=models.TextField(unique=True),
        ),
    ]
