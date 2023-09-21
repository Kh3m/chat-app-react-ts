# Generated by Django 4.2.5 on 2023-09-21 04:07

from django.db import migrations
import django_ulid.models
import ulid.api.api


class Migration(migrations.Migration):

    dependencies = [
        ("api_v1", "0003_alter_category_id_alter_image_id_alter_option_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="id",
            field=django_ulid.models.ULIDField(
                default=ulid.api.api.Api.new, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="id",
            field=django_ulid.models.ULIDField(
                default=ulid.api.api.Api.new, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="option",
            name="id",
            field=django_ulid.models.ULIDField(
                default=ulid.api.api.Api.new, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="id",
            field=django_ulid.models.ULIDField(
                default=ulid.api.api.Api.new, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="id",
            field=django_ulid.models.ULIDField(
                default=ulid.api.api.Api.new, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="variant",
            name="id",
            field=django_ulid.models.ULIDField(
                default=ulid.api.api.Api.new, primary_key=True, serialize=False
            ),
        ),
    ]
