# Generated by Django 4.1.5 on 2023-01-26 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_api', '0003_alter_comment_added_at_alter_post_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='img_thumbnail',
            field=models.ImageField(upload_to='Blog_Project\\media'),
        ),
    ]