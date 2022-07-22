from django.shortcuts import render
from django.template.defaulttags import url
from django.urls import path
from .views import *

urlpatterns = [

    path('', HomeListView.as_view(), name='home'),

    path('search_books/', search_books, name='search_books'),
    path('search_news/', search_news, name='search_news'),
    path('search_posts/', search_posts, name='search_posts'),

    path('register/', RegisterView.as_view(), name='users_register'),

    path('post/', PostListView.as_view(), name='post_list_view'),
    path('post_list/category/<slug:slug>/', PostByCategorytListView.as_view(), name='post_list_category'),
    path('post_list/tags/<slug:slug>/', PostByTagsListView.as_view(), name='tags_post'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail_url'),

    path('news/', NewsListView.as_view(), name='news_list'),
    path('news_list/category/<slug:slug>/', NewsByCategoryListView.as_view(), name='news_category'),
    path('news_list/tags/<slug:slug>/', NewsByTagsListView.as_view(), name='tags_news'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),

    path('category/<slug:slug>/', HomeBookCategoryListView.as_view(), name='home_book_category'),
    path('books_list/', BooksListView.as_view(), name='books_list'),
    path('books_grid/', BooksGridListView.as_view(), name='books_grid'),
    #path('books_list/addlike/<slug:slug>/', addlike, name='addlike'),

    path('user/favourits', user_favourites, name='user_favourites'),
    path('favourite/<slug:slug>/', favourite, name='favourite'),
    path('user_favourite_books_list/', Favourite_bookListView.as_view(), name='user_favourite_books_list'),
    path('book/<slug:slug>/like_or_unlike', like_or_unlike, name=('like')),
    path('update_comment_status/<int:pk>/<slug:type>', update_comment_status, name='update_comment_status'),
    path("add-rating/", AddStarRating.as_view(), name='add_rating'),

    path('book/<slug:slug>/', BookDetailView.as_view(), name='book_detail'),
    path('books_list/category/<slug:slug>/', BookbyCategoryListView.as_view(), name='book_cat'),
    path('books_list/tags/<slug:slug>/', BookbyTagsListView.as_view(), name='tag_books'),


    # -------------------------book-m   anager----------------------

    path("book_manager/", index, name="book_manager"),
    path("add_book/", add_book, name="add_book"),
    path("view_books/", view_books, name="view_books"),
    path("view_students/", view_students, name="view_students"),
    path("issue_book/", issue_book, name="issue_book"),
    path("view_issued_book/", view_issued_book, name="view_issued_book"),
    path("student_issued_books/", student_issued_books, name="student_issued_books"),
    path("profile/", profile, name="profile"),
    path("edit_profile/", edit_profile, name="edit_profile"),

    path("student_registration/", student_registration, name="student_registration"),
    path("change_password/", change_password, name="change_password"),
    path("student_login/", student_login, name="student_login"),
    path("admin_login/", admin_login, name="admin_login"),
    path("logout/", Logout, name="logout"),

    path("delete_book/<int:myid>/", delete_book, name="delete_book"),
    path("delete_student/<int:myid>/", delete_student, name="delete_student"),

]
