from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db.models import Q, Avg
from django.core.validators import FileExtensionValidator

from nok_web.middleware import get_current_user

User = get_user_model()
from django.db import models
from django.urls import reverse
from datetime import date, datetime, timedelta



#-----------------------Posts-models-----------------------------

class Location(models.Model):
    location = models.CharField(max_length=100, verbose_name='Местоположение')

    def __str__(self):
        return self.location


class Post_cat(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post_list_category', kwargs={'slug': self.slug})


class Tags_Posts(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True,  verbose_name='Тег')
    slug = models.SlugField(max_length=100, unique=True, db_index=True,  blank=True, null=True,  verbose_name='slug')

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('tags_post', kwargs={'slug': self.slug})



class Post(models.Model):
    post_cat = models.ForeignKey(Post_cat,  blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    img = models.ImageField(upload_to='post_images/%Y/%m/%d/')
    post_video_file = models.FileField(upload_to='video_posts/%Y/%m/%d/', blank=True, null=True, verbose_name='Иш чаранын видеосу', validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    youtube_links = models.CharField(max_length=200, verbose_name='Иш чаранын ютуб каналдагы шилтемеси', blank=True, null=True)
    facebook_links = models.CharField(max_length=200, verbose_name='Иш чаранын фейсбук каналдагы шилтемеси', blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, db_index=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Локация')
    count_views = models.IntegerField(default=0)
    text = models.TextField(blank=True)
    author_posts = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор публикации', blank=True,
                                    null=True)
    date_pub = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField('Tags_Posts', related_name='tags_posts', verbose_name='Теги постов')
    like = models.ManyToManyField(User, blank=True, related_name='likes_posts')
    favourite = models.ManyToManyField(User, blank=True, related_name='favourite_posts')
    active = models.BooleanField(verbose_name='Опубликовать', default=False)

    class Meta:
        ordering = ['-date_pub']

    def __str__(self):
        return '{}'.format(self.title)


    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})



def get_image_filename(instance, filename):
    title = instance.posts.title
    slug = slugify(title)
    return "posts_images/%s-%s" % (slug, filename)


class Images_Posts(models.Model):
    posts = models.ForeignKey(Post, default=None, on_delete=models.CASCADE, related_name='posts_slides_img')
    title = models.CharField(max_length=100, verbose_name='Слайдга кыскача тема', blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image')



class Comments_posts(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, verbose_name='Иш чаралар', blank = True, null = True, related_name='comments_posts' )
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Автор комментария', blank = True, null = True )
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name='150 символ')
    status = models.BooleanField(verbose_name='Статус', default=False)


#--------------------------------News-models--------------------------------------
class News_cat(models.Model):
    name = models.CharField(max_length=300, unique=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('news_category', kwargs={'slug': self.slug})


class Tags_News(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True,  verbose_name='Тег')
    slug = models.SlugField(max_length=100, unique=True, db_index=True,  blank=True, null=True,  verbose_name='slug')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tags_news', kwargs={'slug': self.slug})



class News(models.Model):
    cat = models.ForeignKey(News_cat, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, db_index=True)
    img = models.ImageField(upload_to='news_images/%Y/%m/%d/')
    slug = models.SlugField(max_length=300, unique=True)
    description = models.CharField(max_length=200, blank=True, db_index=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Локация')
    count_views = models.IntegerField(default=0)
    text = models.TextField(blank=True)
    news_video_file = models.FileField(upload_to='video_news/%Y/%m/%d/', blank=True, null=True,
                                       verbose_name='Иш чаранын видеосу',
                                       validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    youtube_links = models.CharField(max_length=200, verbose_name='Иш чаранын ютуб каналдагы шилтемеси', blank=True,
                                     null=True)
    facebook_links = models.CharField(max_length=200, verbose_name='Иш чаранын фейсбук каналдагы шилтемеси', blank=True,
                                      null=True)
    date_pub = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField('Tags_News', related_name='tags_news', verbose_name='Теги новостей')
    like = models.ManyToManyField(User, blank=True, related_name='likes_news')
    favourite = models.ManyToManyField(User, blank=True, related_name='favourite_news')
    author_news = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор публикации', blank=True, null=True)
    active = models.BooleanField(verbose_name='Опубликовать', default=False)

    class Meta:
        ordering = ['-date_pub']

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})


def get_image_filename(instance, filename):
    title = instance.news.title
    slug = slugify(title)
    return "news_images/%s-%s" % (slug, filename)


class Images_News(models.Model):
    news = models.ForeignKey(News, default=None, on_delete=models.CASCADE, related_name='news_slides_img')
    title = models.CharField(max_length=200, default=' ', verbose_name='Слайдга кыскача тема', blank=True, null=True)
    description = models.CharField(max_length=500, default=' ', blank=True, null=True)
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image')



class Comments_news(models.Model):
    news = models.ForeignKey(News, on_delete = models.CASCADE, verbose_name='Жаңылык', blank = True, null = True, related_name='comments_news' )
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Автор комментария', blank = True, null = True )
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name='')
    status = models.BooleanField(verbose_name='Статус', default=False)




#------------------------------book models----------------------------------
class Author(models.Model):
    full_name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    author_img = models.ImageField(upload_to='author_book_img/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Умер', null=True, blank=True)


    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        ordering = ['full_name',]

    def get_absolute_url(self):
        return reverse('author_book_detail', kwargs={'slug': self.slug})



class Publisher(models.Model):
    name = models.CharField(max_length=100, verbose_name='Басмакананын аты')
    address = models.CharField(max_length=100, verbose_name='Адресс', blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name='Шаар', blank=True, null=True)
    country = models.CharField(max_length=100, verbose_name='Мамлекет', blank=True, null=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Китептин жанры: ")

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Китептин тили:  ")
    def __str__(self):
        return self.name


class Format(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Tags_Books(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тег')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='slug')

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('tag_books', kwargs={'slug': self.slug})



class Book_category(models.Model):
    book_cat = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.book_cat

    def get_absolute_url(self):
        return reverse('book_cat', kwargs={'slug': self.slug})






class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда", related_name='rating_books_star')
    book = models.ForeignKey('Books', on_delete=models.CASCADE, verbose_name="Китеп", related_name='rating_books')


    def __str__(self):
        return f"{self.star}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"





class Books(models.Model):
    book_category = models.ForeignKey(Book_category, on_delete=models.PROTECT, verbose_name='Китептин категориясы')
    title = models.CharField(max_length=120, db_index=True, blank=True, verbose_name='Китептин аталышы')
    slug = models.SlugField(max_length=120, unique=True)
    author_pub = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор публикации', blank=True, null=True, related_name='author_books')
    author = models.ManyToManyField(Author, verbose_name='Китептин автору', related_name='author_book')
    img_book = models.ImageField(upload_to='book_image/%Y/%m/%d/', blank=True)
    book_file = models.FileField(upload_to='book_file/', blank=True)
    google_docs_file = models.CharField(max_length=200, verbose_name='Гугл документ же китеп', blank=True, null=True)
    isbn = models.CharField(max_length=30, db_index=True, unique=True, blank=True)
    edition = models.CharField(max_length=100, blank=True, null=True, verbose_name='китептин чыгарылган жылы')
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Китепти чыгарган басмакана')
    publication_date = models.DateField(auto_now_add=True)
    summary = models.TextField(help_text="Китеп тууралуу кыскача: ", blank=True, verbose_name='Китеп тууралуу')
    length_page = models.IntegerField(blank=True, null=True, verbose_name='Китептин барагынын саны')
    format = models.ForeignKey(Format, on_delete=models.PROTECT,  verbose_name='Китептин форматы')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=' Китеп жазылган тили')
    genre = models.ManyToManyField(Genre, help_text="Китептин жанры ", related_name='book_cat', verbose_name='Китептин жанры')
    tags = models.ManyToManyField('Tags_Books', help_text="Китептин теги ", related_name='books_tags', verbose_name='Китептин теги')
    topics = models.CharField(max_length=300, blank=True, null=True)
    total_copies = models.IntegerField(default=0, verbose_name='Китептин жалпы саны')
    available_copies = models.IntegerField(default=0, verbose_name='Окурмандарга берилген китептин саны')
    books_view = models.IntegerField(default=0, verbose_name='Китепти онлайн окугандарын саны')
    #like = models.IntegerField(default=0)
    like = models.ManyToManyField(User, blank=True)
    favourite = models.ManyToManyField(User, blank=True, related_name='favourite')
    active = models.BooleanField(verbose_name='Опубликовать', default=False)

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.slug})

    def get_avg_rating(self):
        #avg_rating = Books.objects.filter(id=self.id).aggregate(f=models.Sum(models.F('rating_books__star'))/models.Count(models.F('rating_books')))
        avg_rating = Books.objects.filter(id=self.id).aggregate(f=Avg('rating_books__star'))
        return avg_rating.get('f', 0)


    def __str__(self):
        return str(self.title) + " ["+str(self.isbn)+']'


    class Meta:
        verbose_name = 'Китеп'
        verbose_name_plural = 'Китептер'
        ordering = ['-books_view']


class StatusFilterComments(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(status=False, author = get_current_user()) | Q(status=False, article__author_pub=get_current_user()) | Q(status=True))


class Comments(models.Model):
    article = models.ForeignKey('Books', on_delete = models.CASCADE, verbose_name='Китеп', related_name='comments_article' )
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Автор комментария' )
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name='150 символ')
    status = models.BooleanField(verbose_name='Видимость', default=False)
    object = StatusFilterComments()



#------------------------------Book-manager--------------------------------------------
class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.PositiveIntegerField()
    category = models.CharField(max_length=50)
    active = models.BooleanField(verbose_name='Опубликовать', default=False)

    def __str__(self):
        return str(self.name) + " ["+str(self.isbn)+']'


class User_reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=10)
    branch = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=3, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to="user_reader/", blank=True)

    def __str__(self):
        return str(self.user) + " [" + str(self.branch) + ']' + " [" + str(self.classroom) + ']' + " [" + str(
            self.roll_no) + ']'



def expiry():
    return datetime.today() + timedelta(days=14)

class IssuedBook(models.Model):
    student_id = models.CharField(max_length=100, blank=True)
    isbn = models.CharField(max_length=13)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)







#--------------------------User-reader-profile-------------------------------

class Profile(models.Model):
    class Meta:
        ordering = ['user']
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профиль пользователей'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    instance = models.ManyToManyField(Books)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images/')
    bio = models.TextField()


    def __str__(self):
        return str(self.user)


