# Generated by Django 4.0.5 on 2022-07-26 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nok_web', '0010_news_author_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='images_news',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='images_news',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Слайдга кыскача тема'),
        ),
        migrations.AlterField(
            model_name='images_news',
            name='news',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='news_slides_img', to='nok_web.news'),
        ),
    ]
