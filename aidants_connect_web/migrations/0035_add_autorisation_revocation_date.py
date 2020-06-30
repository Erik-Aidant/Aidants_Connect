# Generated by Django 3.0.4 on 2020-06-05 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aidants_connect_web", "0034_add_related_names"),
    ]

    operations = [
        migrations.AddField(
            model_name="autorisation",
            name="revocation_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(name="autorisation", unique_together=set(),),
    ]
