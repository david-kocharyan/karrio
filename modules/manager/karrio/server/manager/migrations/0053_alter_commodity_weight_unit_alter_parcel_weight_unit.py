# Generated by Django 4.2.7 on 2023-11-11 11:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0052_auto_20230520_0811"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commodity",
            name="weight_unit",
            field=models.CharField(
                blank=True,
                choices=[("KG", "KG"), ("LB", "LB"), ("OZ", "OZ"), ("G", "G")],
                max_length=2,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="parcel",
            name="weight_unit",
            field=models.CharField(
                blank=True,
                choices=[("KG", "KG"), ("LB", "LB"), ("OZ", "OZ"), ("G", "G")],
                max_length=2,
                null=True,
            ),
        ),
    ]
