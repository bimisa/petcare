# Generated by Django 4.2.6 on 2023-10-25 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_appointment_service_provider"),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name="appointment",
            name="status",
            field=models.CharField(
                choices=[("approved", "approved"), ("pending", "pending")],
                default="pending",
                max_length=200,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="license_no",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="vaccination",
            name="next_vaccination_date",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="vaccination",
            name="vaccination_no",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="service_provider",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.company",
            ),
        ),
    ]
