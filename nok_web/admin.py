from django.contrib import admin
from .models import *


# ---------------Posts-slider-----------------

class Images_PostsAdmin(admin.ModelAdmin):
    pass


class Images_PostsInline(admin.StackedInline):
    model = Images_Posts
    max_num = 10
    extra = 0

#-----------------post-admin------------------
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    save_as = True
    inlines = [Images_PostsInline, ]


class Post_catAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    save_as = True


admin.site.register(Post, PostAdmin)
admin.site.register(Images_Posts, Images_PostsAdmin)
admin.site.register(Post_cat, Post_catAdmin)


#------------------News----------------------

class Images_NewsAdmin(admin.ModelAdmin):
    pass


class Images_NewsInline(admin.StackedInline):
  model = Images_News
  max_num = 10
  extra = 0


class News_catAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    save_as = True

class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    list_display = ('title', 'cat', 'count_views', 'date_pub', 'active')
    save_as = True
    inlines = [Images_NewsInline, ]




admin.site.register(News, NewsAdmin)
admin.site.register(Images_News, Images_NewsAdmin)
admin.site.register(News_cat, News_catAdmin)


#---------------------------------------

class BooksAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',), }
    save_as = True



class Book_categoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('book_cat',), }
    save_as = True

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'slug', 'date_of_birth', 'date_of_death')
    fields = ['full_name', 'slug',('date_of_birth', 'date_of_death')]
    prepopulated_fields = {'slug': ('full_name',), }
    save_as = True


class Tags_BooksAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    save_as = True

class Tags_PostsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    save_as = True

class Tags_NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    save_as = True


class RatingAdmin(admin.ModelAdmin):
    list_display = ("star", "book", "ip")






admin.site.register(Books, BooksAdmin)
admin.site.register(Book_category, Book_categoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Format)
admin.site.register(Comments)
admin.site.register(Profile)
admin.site.register(Location)
admin.site.register(Comments_posts)
admin.site.register(Comments_news)
admin.site.register(Rating, RatingAdmin)
admin.site.register(RatingStar)
admin.site.register(Tags_Books, Tags_BooksAdmin)
admin.site.register(Tags_Posts, Tags_PostsAdmin)
admin.site.register(Tags_News, Tags_NewsAdmin)


