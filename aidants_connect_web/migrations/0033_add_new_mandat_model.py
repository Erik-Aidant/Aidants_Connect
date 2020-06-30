# Generated by Django 3.0.5 on 2020-06-01 15:30

import aidants_connect_web.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("aidants_connect_web", "0032_allow_indexes_with_autorisation"),
    ]

    operations = [
        migrations.CreateModel(
            name="Mandat",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "organisation",
                    models.ForeignKey(
                        default=aidants_connect_web.models.get_staff_organisation_name_id,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="aidants_connect_web.Organisation",
                    ),
                ),
                (
                    "usager",
                    models.ForeignKey(
                        default=0,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="aidants_connect_web.Usager",
                    ),
                ),
                (
                    "creation_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "expiration_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "duree_keyword",
                    models.CharField(
                        choices=[
                            ("SHORT", "pour une durée de 1 jour"),
                            ("LONG", "pour une durée de 1 an"),
                            (
                                "EUS_03_20",
                                "jusqu’à la fin de l’état d’urgence sanitaire ",
                            ),
                        ],
                        max_length=16,
                        null=True,
                    ),
                ),
                ("is_remote", models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name="autorisation",
            name="mandat",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="autorisations",
                to="aidants_connect_web.Mandat",
            ),
        ),
    ]
