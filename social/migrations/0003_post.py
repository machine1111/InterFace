# Generated by Django 3.2.7 on 2022-11-05 11:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_rename_pofile_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('post_img', models.ImageField(upload_to='posts_images')),
                ('caption', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
    ]
