# Generated by Django 3.1.6 on 2021-02-12 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0004_delete_leaderboard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='rank',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
