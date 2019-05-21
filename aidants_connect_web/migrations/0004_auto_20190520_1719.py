# Generated by Django 2.2 on 2019-05-20 15:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aidants_connect_web', '0003_auto_20190507_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('given_name', models.TextField()),
                ('family_name', models.TextField()),
                ('preferred_username', models.TextField(blank=True)),
                ('birthdate', models.DateField()),
                ('gender', models.CharField(choices=[('F', 'Femme'), ('H', 'Homme')], default='F', max_length=1)),
                ('birthplace', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(9999), django.core.validators.MaxValueValidator(100000)])),
                ('birthcountry', models.IntegerField(default=99100, validators=[django.core.validators.MinValueValidator(99100), django.core.validators.MaxValueValidator(99500)])),
                ('sub', models.TextField(default='No Sub yet')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='connection',
            name='access_token',
            field=models.TextField(default='No token Provided'),
        ),
        migrations.AddField(
            model_name='connection',
            name='sub_usager',
            field=models.TextField(default='No sub Provided'),
        ),
    ]
