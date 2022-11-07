# Generated by Django 3.2.7 on 2022-11-07 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0010_postcomments_commented_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postcomments',
            name='user',
        ),
        migrations.AddField(
            model_name='postcomments',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='social.profile'),
            preserve_default=False,
        ),
    ]