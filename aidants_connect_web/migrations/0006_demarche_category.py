# Generated by Django 2.2 on 2019-06-27 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aidants_connect_web', '0005_demarchecategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='demarche',
            name='category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='aidants_connect_web.DemarcheCategory'),
        ),
    ]
