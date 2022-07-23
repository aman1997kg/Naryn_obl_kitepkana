# Generated by Django 4.0.5 on 2022-07-21 03:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import nok_web.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('author_img', models.ImageField(blank=True, null=True, upload_to='author_book_img/')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('date_of_death', models.DateField(blank=True, null=True, verbose_name='Умер')),
            ],
            options={
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('isbn', models.PositiveIntegerField()),
                ('category', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=False, verbose_name='Опубликовать')),
            ],
        ),
        migrations.CreateModel(
            name='Book_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_cat', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, db_index=True, max_length=120, verbose_name='Китептин аталышы')),
                ('slug', models.SlugField(max_length=120, unique=True)),
                ('img_book', models.ImageField(blank=True, upload_to='book_image/%Y/%m/%d/')),
                ('book_file', models.FileField(blank=True, upload_to='book_file/')),
                ('isbn', models.CharField(blank=True, db_index=True, max_length=30, unique=True)),
                ('edition', models.CharField(blank=True, max_length=100, null=True, verbose_name='китептин чыгарылган жылы')),
                ('publication_date', models.DateField(auto_now_add=True)),
                ('summary', models.TextField(blank=True, help_text='Китеп тууралуу кыскача: ', verbose_name='Китеп тууралуу')),
                ('length_page', models.IntegerField(blank=True, null=True, verbose_name='Китептин барагынын саны')),
                ('topics', models.CharField(blank=True, max_length=300, null=True)),
                ('total_copies', models.IntegerField(default=0, verbose_name='Китептин жалпы саны')),
                ('available_copies', models.IntegerField(default=0, verbose_name='Окурмандарга берилген китептин саны')),
                ('books_view', models.IntegerField(default=0, verbose_name='Китепти онлайн окугандарын саны')),
                ('active', models.BooleanField(default=False, verbose_name='Опубликовать')),
                ('author', models.ManyToManyField(related_name='author_book', to='nok_web.author', verbose_name='Китептин автору')),
                ('author_pub', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_books', to=settings.AUTH_USER_MODEL, verbose_name='Автор публикации')),
                ('book_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nok_web.book_category', verbose_name='Китептин категориясы')),
                ('favourite', models.ManyToManyField(blank=True, related_name='favourite', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Китеп',
                'verbose_name_plural': 'Китептер',
                'ordering': ['-books_view'],
            },
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Китептин жанры: ', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='IssuedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(blank=True, max_length=100)),
                ('isbn', models.CharField(max_length=13)),
                ('issued_date', models.DateField(auto_now=True)),
                ('expiry_date', models.DateField(default=nok_web.models.expiry)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Китептин тили:  ', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100, verbose_name='Местоположение')),
            ],
        ),
        migrations.CreateModel(
            name='News_cat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=300, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post_cat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Басмакананын аты')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Адресс')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='Шаар')),
                ('country', models.CharField(blank=True, max_length=100, null=True, verbose_name='Мамлекет')),
            ],
        ),
        migrations.CreateModel(
            name='RatingStar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(default=0, verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Звезда рейтинга',
                'verbose_name_plural': 'Звезды рейтинга',
                'ordering': ['-value'],
            },
        ),
        migrations.CreateModel(
            name='Tags_Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Тег')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
            ],
        ),
        migrations.CreateModel(
            name='Tags_News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Тег')),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='slug')),
            ],
        ),
        migrations.CreateModel(
            name='Tags_Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Тег')),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='slug')),
            ],
        ),
        migrations.CreateModel(
            name='User_reader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classroom', models.CharField(max_length=10)),
                ('branch', models.CharField(max_length=10)),
                ('roll_no', models.CharField(blank=True, max_length=3, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('image', models.ImageField(blank=True, upload_to='user_reader/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=15, verbose_name='IP адрес')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_books', to='nok_web.books', verbose_name='Китеп')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_books_star', to='nok_web.ratingstar', verbose_name='звезда')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='default.jpg', upload_to='profile_images/')),
                ('bio', models.TextField()),
                ('instance', models.ManyToManyField(to='nok_web.books')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профиль пользователей',
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('img', models.ImageField(upload_to='post_images/%Y/%m/%d/')),
                ('description', models.CharField(blank=True, db_index=True, max_length=500)),
                ('count_views', models.IntegerField(default=0)),
                ('text', models.TextField(blank=True)),
                ('date_pub', models.DateField(auto_now_add=True)),
                ('active', models.BooleanField(default=False, verbose_name='Опубликовать')),
                ('favourite', models.ManyToManyField(blank=True, related_name='favourite_posts', to=settings.AUTH_USER_MODEL)),
                ('like', models.ManyToManyField(blank=True, related_name='likes_posts', to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nok_web.location', verbose_name='Локация')),
                ('post_cat', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='nok_web.post_cat')),
                ('tags', models.ManyToManyField(related_name='tags_posts', to='nok_web.tags_posts', verbose_name='Теги постов')),
            ],
            options={
                'ordering': ['-date_pub'],
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=300)),
                ('img', models.ImageField(upload_to='news_images/%Y/%m/%d/')),
                ('slug', models.SlugField(max_length=300, unique=True)),
                ('description', models.CharField(blank=True, db_index=True, max_length=200)),
                ('count_views', models.IntegerField(default=0)),
                ('text', models.TextField(blank=True)),
                ('date_pub', models.DateField(auto_now_add=True)),
                ('active', models.BooleanField(default=False, verbose_name='Опубликовать')),
                ('cat', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='nok_web.news_cat')),
                ('favourite', models.ManyToManyField(blank=True, related_name='favourite_news', to=settings.AUTH_USER_MODEL)),
                ('like', models.ManyToManyField(blank=True, related_name='likes_news', to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nok_web.location', verbose_name='Локация')),
                ('tags', models.ManyToManyField(related_name='tags_news', to='nok_web.tags_news', verbose_name='Теги новостей')),
            ],
            options={
                'ordering': ['-date_pub'],
            },
        ),
        migrations.CreateModel(
            name='Comments_posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(verbose_name='150 символ')),
                ('status', models.BooleanField(default=False, verbose_name='Статус')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_posts', to='nok_web.post', verbose_name='Иш чаралар')),
            ],
        ),
        migrations.CreateModel(
            name='Comments_news',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(verbose_name='')),
                ('status', models.BooleanField(default=False, verbose_name='Статус')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
                ('news', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_news', to='nok_web.news', verbose_name='Жаңылык')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(verbose_name='150 символ')),
                ('status', models.BooleanField(default=False, verbose_name='Видимость')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_article', to='nok_web.books', verbose_name='Китеп')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
            ],
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='books',
            name='format',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nok_web.format', verbose_name='Китептин форматы'),
        ),
        migrations.AddField(
            model_name='books',
            name='genre',
            field=models.ManyToManyField(help_text='Китептин жанры ', related_name='book_cat', to='nok_web.genre', verbose_name='Китептин жанры'),
        ),
        migrations.AddField(
            model_name='books',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nok_web.language', verbose_name=' Китеп жазылган тили'),
        ),
        migrations.AddField(
            model_name='books',
            name='like',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='books',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='nok_web.publisher', verbose_name='Китепти чыгарган басмакана'),
        ),
        migrations.AddField(
            model_name='books',
            name='rating',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nok_web.rating', verbose_name='Рейтинг книги'),
        ),
        migrations.AddField(
            model_name='books',
            name='tags',
            field=models.ManyToManyField(help_text='Китептин теги ', related_name='books_tags', to='nok_web.tags_books', verbose_name='Китептин теги'),
        ),
    ]