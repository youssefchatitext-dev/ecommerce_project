import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name="product",
            name="stock",
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="products/images",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(max_length=255),
        ),
        migrations.RemoveField(
            model_name="product",
            name="updated_at",
        ),
        migrations.AlterModelOptions(
            name="category",
            options={},
        ),
        migrations.AlterModelOptions(
            name="product",
            options={},
        ),
    ]
