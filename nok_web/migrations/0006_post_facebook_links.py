# Generated by Django 4.0.5 on 2022-07-24 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nok_web', '0005_post_youtube_links'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='facebook_links',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Иш чаранын фейсбук каналдагы шилтемеси'),
        ),
    ]
