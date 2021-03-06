# Generated by Django 3.1.6 on 2021-02-12 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0002_auto_20210212_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaderboard',
            name='rank',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='rank',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='leaderboard',
            name='user_id',
            field=models.UUIDField(),
        ),
    ]
