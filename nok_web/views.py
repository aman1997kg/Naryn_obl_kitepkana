import os
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import path, reverse_lazy
from django.views import generic, View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.db.models import Q
from .models import *
from django.template import Context, Template
from .forms import *
from django.db import models



class HomeListView(generic.ListView):
    model = Post

    template_name = 'nok_web/index.html'


    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.filter(active=True)[:3]
        context['news'] = News.objects.filter(active=True)[:3]
        context['books'] = Books.objects.all()
        context['book_category'] = Book_category.objects.all()

        return context


class HomeBookCategoryListView(generic.ListView):
    model = Books
    context_object_name = 'books'
    template_name = 'nok_web/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeBookCategoryListView, self).get_context_data(**kwargs)
        context['books'] = Books.objects.filter(book_category__slug=self.kwargs['slug'])
        context['title'] = 'Китептердин каталогу'

        return context

    def get_queryset(self):
        return Book_category.objects.filter(slug=self.kwargs['slug'])


#---------------------video-palayer----------------------
from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
from .services import *

def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response



def get_news_video(request, pk: int):
    file, status_code, content_length, content_range = open_file_news(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')
    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response







#---------------------------News------------------------------------

def search_news(request):
    search_news = request.GET.get('search_news')

    if search_news:
        news = News.objects.filter(Q(title__iregex=search_news) | Q(text__iregex=search_news))
        paginator = Paginator(news, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        news = News.objects.filter(active=True)
        paginator = Paginator(news, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    title = 'Сайт боюнча издөө'
    return render(request, 'nok_web/news/search_news_list.html', {'page_obj': page_obj, 'title': title})

from django.shortcuts import render
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import *

@login_required
def post(request):

    Image_NewsForm = modelformset_factory(Images_News,
                                        form=Image_NewsForm, extra=3)
    #'extra' means the number of photos that you can upload   ^
    if request.method == 'POST':

        newsForm = NewsForm(request.POST)
        formset = Image_NewsForm(request.POST, request.FILES,
                               queryset=Images_News.objects.none())


        if NewsForm.is_valid() and formset.is_valid():
            news_form = NewsForm.save(commit=False)
            news_form.author_news.user = request.user
            news_form.save()

            for form in formset.cleaned_data:
                #this helps to not crash if the user
                #do not upload all the photos
                if form:
                    image = form['image']
                    photo = Images_News(news=news_form, image=image)
                    photo.save()
            messages.success(request,
                             "Yeeew, check it out on the home page!")
            return HttpResponseRedirect("/")
        else:
            print(newsForm.errors, formset.errors)
    else:
        newsForm = NewsForm()
        formset = Image_NewsFormSet(queryset=Images_News.objects.none())
    return render(request, 'nok_web/news/news_detail_view.html',
                  {'newsForm': newsForm, 'formset': formset})


class NewsListView(generic.ListView):
    model = News
    paginate_by = 2
    context_object_name = 'news'
    template_name = 'nok_web/news/news_list_view.html'

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['news_cats'] = News_cat.objects.all()
        context['title'] = 'Жаңылыктар'

        return context


class NewsDetailView(generic.DetailView):
    model = News
    context_object_name = 'news_detail'
    template_name = 'nok_web/news/news_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Жаңылыктардын мазмуну'
        context['news_cats'] = News_cat.objects.all()

        return context

    def get_object(self):
        obj = super().get_object()
        obj.count_views += 1
        obj.save()
        return obj



class NewsByCategoryListView(generic.ListView):
    model = News
    paginate_by = 2
    context_object_name = 'news'
    allow_empty = False
    template_name = 'nok_web/news/news_list_view.html'

    def get_context_data(self, **kwargs):
        context = super(NewsByCategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Категориясы:  ' + str(News_cat.objects.get(slug=self.kwargs['slug']))
        context['news'] = News.objects.filter(cat__slug=self.kwargs['slug'])
        context['news_count'] = News.objects.all().count()

        return context

    def get_queryset(self):
        return News_cat.objects.filter(slug=self.kwargs['slug'])

class NewsByTagsListView(generic.ListView):
    model = News
    paginate_by = 2
    context_object_name = 'news'
    allow_empty = False
    template_name = 'nok_web/news/news_list_view.html'

    def get_context_data(self, **kwargs):
        context = super(NewsByTagsListView, self).get_context_data(**kwargs)
        context['title'] = 'Жаңылыктын теги: ' + str(Tags_News.objects.get(slug=self.kwargs['slug']))
        context['news'] = News.objects.filter(tags__slug=self.kwargs['slug'])
        context['news_count'] = News.objects.all().count()

        return context

    def get_queryset(self):
        return Tags_News.objects.filter(slug=self.kwargs['slug'])




#----------------------------books-views-----------------------
def search_books(request):
    search_books = request.GET.get('search_books')

    if search_books:
        books = Books.objects.filter(Q(title__iregex=search_books) | Q(summary__iregex=search_books) | Q(isbn__iregex=search_books) | Q(author__full_name__iregex=search_books))
        paginator = Paginator(books, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        books = Books.objects.all()
        paginator = Paginator(books, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


    return render(request, 'nok_web/books/search_books_list.html', {'page_obj': page_obj, 'title': 'Сайт боюнча табылган китептер'})


class BooksListView(LoginRequiredMixin, generic.ListView):
    model = Books
    paginate_by = 3
    context_object_name = 'books'
    template_name = 'nok_web/books/books_list_view.html'


    def get_context_data(self, **kwargs):
        context = super(BooksListView, self).get_context_data(**kwargs)
        context['author_count'] = Author.objects.all().count()
        context['books_count'] = Books.objects.all().count()
        context['title'] = 'Китептердин тизмеси'
        return context

    def get_queryset(self):
        return Books.objects.all()


class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return '%s?slug=%s' % (self.success_url, self.object.slug)



class BooksGridListView(generic.ListView):
    model = Books
    paginate_by = 3
    context_object_name = 'books'
    template_name = 'nok_web/books/books_grid_view.html'

    def get_queryset(self):
        return Books.objects.all()


    def get_context_data(self, **kwargs):
        context = super(BooksGridListView, self).get_context_data(**kwargs)
        context['author_count'] = Author.objects.all().count()
        context['books_count'] = Books.objects.all().count()
        context['title'] = 'Китептердин тизмеси'
        return context



class BookDetailView(LoginRequiredMixin, CustomSuccessMessageMixin, FormMixin, generic.DetailView):

    model = Books
    form_class = CommentForm
    success_msg = 'Коментарий ийгиликтүү жазылды, админ текшерүүдө'
    context_object_name = 'book_detail'
    template_name = 'nok_web/books/book_detail_view.html'

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'slug': self.get_object().slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        #context["middle_star"] = Books.objects.filter(active=True).annotate(rating_star=models.Sum(models.F('rating_books__star'))/models.Count(models.F('rating_books')))
        return context



    def post(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        comment_form = self.get_form()
        if comment_form.is_valid():
            return self.form_valid(comment_form)
        else:
            return self.form_invalid(comment_form)

    def form_valid(self, comment_form):
        self.object = comment_form.save(commit=False)
        self.object.article = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(comment_form)



    def get_object(self):
        obj = super().get_object()
        obj.books_view += 1
        obj.save()
        return obj



class AddStarRating(View):
    """Добавление рейтинга"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                book_id=int(request.POST.get("book")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)






class BookbyCategoryListView(generic.ListView):
    model = Books
    paginate_by = 2
    context_object_name = 'books'
    allow_empty = False
    template_name = 'nok_web/books/books_list_view.html'

    def get_context_data(self, **kwargs):
        context = super(BookbyCategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Китептердин каталогу:' + str(Books.objects.get(book_category__slug=self.kwargs['slug']))
        context['books'] = Books.objects.filter(book_category__slug=self.kwargs['slug'])
        context['books_count'] = Books.objects.all().count()
        context['author_count'] = Author.objects.all().count()

        return context

    def get_queryset(self):
        return Book_category.objects.filter(slug=self.kwargs['slug'])



class BookbyTagsListView(generic.ListView):
    model = Books
    paginate_by = 2
    allow_empty = False
    template_name = 'nok_web/books/books_list_view.html'

    def get_context_data(self, **kwargs):
        context = super(BookbyTagsListView, self).get_context_data(**kwargs)
        context['title'] = 'Китептерди теги боюнча издөө:  ' + str(Tags_Books.objects.get(slug=self.kwargs['slug']))
        context['books'] = Books.objects.filter(tags__slug=self.kwargs['slug'])
        context['books_count'] = Books.objects.all().count()
        context['author_count'] = Author.objects.all().count()

        return context

    def get_queryset(self):
        return Tags_Books.objects.filter(slug=self.kwargs['slug'])



'''
def addlike(request, slug):
    try:
        books = Books.objects.get(slug=slug)
        books.like += 1
        books.save()
    except ObjectDoesNotExist:
        raise Http404
    return redirect('books_list')
'''


class Favourite_bookListView(generic.ListView):
    model = Books
    paginate_by = 3
    context_object_name = 'favourite_books'
    template_name = 'nok_web/books/user_favourite_books_list.html'


    def get_context_data(self, **kwargs):
        context = super(Favourite_bookListView, self).get_context_data(**kwargs)
        context['favourite_books'] = Books.objects.filter(favourite=self.request.user)
        context['favourite_books_count'] = Books.objects.filter(favourite=self.request.user).all().count()
        context['title'] = 'Тандалган китептердин тизмеси'
        return context



def like_or_unlike(request, slug):
    books = Books.objects.get(slug=slug)
    if request.user in books.like.all():
        books.like.remove(request.user)
    else:
        books.like.add(request.user)

    return redirect(reverse('book_detail', kwargs={'slug': books.slug}))


def user_favourites(request):
    user_likes = Books.objects.filter(like=request.user)
    user_likes_count = Books.objects.filter(like=request.user).all().count()
    paginator = Paginator(user_likes, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'Сиз жакшы көргөн китептер'

    return render(request, 'nok_web/books/likes_books_list.html', {'page_obj': page_obj, 'user_likes_count': user_likes_count, 'title': title})


def favourite(request, slug):
    books = get_object_or_404(Books, slug=slug)
    if books.favourite.filter(id=request.user.id).exists():
        books.favourite.remove(request.user)
    else:
        books.favourite.add(request.user)
    return HttpResponseRedirect(books.get_absolute_url())


def update_comment_status(request, pk, type):
    comment = Comments.object.get(pk=pk)
    if type == 'public':
        import operator
        comment.status = operator.not_(comment.status)
        comment.save()
        template = 'nok_web/books/comments_books.html'
        context = {'comment': comment, 'status_comment_public': 'Комментарий опубликован'}
        return render(request, template, context)

    elif type == 'delete':
        comment.delete()
        template = 'nok_web/books/comments_books.html'
        context = {'comment': comment, 'status_comment_delete': 'Комментарий удален!'}
        return render(request, template, context)

    return HttpResponse('1')





#---------------------------post-list------------------------------
def search_posts(request):
    search_posts = request.GET.get('search_posts')

    if search_posts:
        posts = Post.objects.filter(Q(title__iregex=search_posts) | Q(text__iregex=search_posts))
        paginator = Paginator(posts, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        posts = Post.objects.filter(active=True)
        paginator = Paginator(posts, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    title = 'Сайт боюнча издөө'
    return render(request, 'nok_web/posts/search_posts_list.html', {'page_obj': page_obj, 'title': title})




class PostListView(generic.ListView):
    model = Post
    paginate_by = 3
    context_object_name = 'post_list'
    queryset = Post.objects.all()
    template_name = 'nok_web/posts/post_list_view.html'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['title'] = 'Иш чаралар'

        return context




class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'nok_web/posts/post_detail_view.html'
    queryset = Post.objects.all()
    context_object_name = 'post_detail'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Иш чаранын мазмуну'

        return context

    def get_object(self):
        obj = super().get_object()
        obj.count_views += 1
        obj.save()
        return obj




class PostByCategorytListView(generic.ListView):
    model = Post
    paginate_by = 2
    context_object_name = 'post'
    allow_empty = False
    template_name = 'nok_web/posts/post_list_view.html'

    def get_context_data(self, **kwargs):
        context = super(PostByCategorytListView, self).get_context_data(**kwargs)
        context['title'] = 'Категория: ' + str(Post_cat.objects.get(slug=self.kwargs['slug']))
        context['post_list'] = Post.objects.filter(post_cat__slug=self.kwargs['slug'])
        context['post_count'] = Post.objects.all().count()

        return context

    def get_queryset(self):
        return Post_cat.objects.filter(slug=self.kwargs['slug'])



class PostByTagsListView(generic.ListView):
    model = Post
    paginate_by = 2
    context_object_name = 'post'
    allow_empty = False
    template_name = 'nok_web/posts/post_list_view.html'

    def get_context_data(self, **kwargs):
        context = super(PostByTagsListView, self).get_context_data(**kwargs)
        context['title'] = 'Иш чаралардын теги:  ' + str(Tags_Posts.objects.get(slug=self.kwargs['slug']))
        context['post_list'] = Post.objects.filter(tags__slug=self.kwargs['slug'])
        context['post_count'] = Post.objects.all().count()

        return context

    def get_queryset(self):
        return Tags_Posts.objects.filter(slug=self.kwargs['slug'])


    #-------------------------------------------------User------------------


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'registration/register.html'




    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} - Сиз ийгиликтүү катталдыңыз')
            return redirect(to='login')
        else:
            messages.error(request, 'Катталууда ката кетти туура жазыңыз!')

        return render(request, self.template_name, {'form': form})



class LoginView(TemplateView):
    template_name = 'registration/login.html'





    def dispatch(self, request, *args, **kwargs):
        context = {}

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в систему')
                return redirect("/")
            else:
                messages.error(request, 'Аккаунтка кирүүдө ката бар')
                context['error'] = "Аккаунтка кирүүдө ката бар"
        return render(request, self.template_name, context)







#----------------------------------book-manager-----------------------


from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from datetime import date
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "book_manager/index.html")


@login_required(login_url='/admin_login')
def add_book(request):
    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category = request.POST['category']

        books = Book.objects.create(name=name, author=author, isbn=isbn, category=category)
        books.save()
        alert = True
        return render(request, "book_manager/add_book.html", {'alert': alert})
    return render(request, "book_manager/add_book.html")


@login_required(login_url='/admin_login')
def view_books(request):
    books = Book.objects.all()
    return render(request, "book_manager/view_books.html", {'books': books})


@login_required(login_url='/admin_login')
def view_students(request):
    students = User_reader.objects.all()
    return render(request, "book_manager/view_students.html", {'students': students})


@login_required(login_url='/admin_login')
def issue_book(request):
    form = forms.IssueBookForm()
    if request.method == "POST":
        form = forms.IssueBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.student_id = request.POST['name2']
            obj.isbn = request.POST['isbn2']
            obj.save()
            alert = True
            return render(request, "book_manager/issue_book.html", {'obj': obj, 'alert': alert})
    return render(request, "book_manager/issue_book.html", {'form': form})


@login_required(login_url='/admin_login')
def view_issued_book(request):
    issuedBooks = IssuedBook.objects.all()
    details = []
    for i in issuedBooks:
        days = (date.today() - i.issued_date)
        d = days.days
        fine = 0
        if d > 14:
            day = d - 14
            fine = day * 5
        books = list(models.Book.objects.filter(isbn=i.isbn))
        students = list(models.User_reader.objects.filter(user=i.student_id))
        i = 0
        for l in books:
            t = (students[i].user, students[i].user_id, books[i].name, books[i].isbn, issuedBooks[0].issued_date,
                 issuedBooks[0].expiry_date, fine)
            i = i + 1
            details.append(t)
    return render(request, "book_manager/view_issued_book.html", {'issuedBooks': issuedBooks, 'details': details})


@login_required(login_url='/student_login')
def student_issued_books(request):
    student = User_reader.objects.filter(user_id=request.user.id)
    issuedBooks = IssuedBook.objects.filter(student_id=student[0].user_id)
    li1 = []
    li2 = []

    for i in issuedBooks:
        books = Book.objects.filter(isbn=i.isbn)
        for book in books:
            t = (request.user.id, request.user.get_full_name, book.name, book.author)
            li1.append(t)

        days = (date.today() - i.issued_date)
        d = days.days
        fine = 0
        if d > 15:
            day = d - 14
            fine = day * 5
        t = (issuedBooks[0].issued_date, issuedBooks[0].expiry_date, fine)
        li2.append(t)
    return render(request, 'book_manager/student_issued_books.html', {'li1': li1, 'li2': li2})


@login_required(login_url='/student_login')
def profile(request):
    return render(request, "book_manager/profile.html")


@login_required(login_url='/student_login')
def edit_profile(request):
    student = User_reader.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']

        student.user.email = email
        student.phone = phone
        student.branch = branch
        student.classroom = classroom
        student.roll_no = roll_no
        student.user.save()
        student.save()
        alert = True
        return render(request, "book_manager/edit_profile.html", {'alert': alert})
    return render(request, "book_manager/edit_profile.html")


def delete_book(request, myid):
    books = Book.objects.filter(id=myid)
    books.delete()
    return redirect("view_books")


def delete_student(request, myid):
    students = User_reader.objects.filter(id=myid)
    students.delete()
    return redirect("view_students")


def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "book_manager/change_password.html", {'alert': alert})
            else:
                currpasswrong = True
                return render(request, "book_manager/change_password.html", {'currpasswrong': currpasswrong})
        except:
            pass
    return render(request, "book_manager/change_password.html")


def student_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']
        image = request.FILES['image']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            passnotmatch = True
            return render(request, "book_manager/student_registration.html", {'passnotmatch': passnotmatch})

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                        last_name=last_name)
        student = User_reader.objects.create(user=user, phone=phone, branch=branch, classroom=classroom, roll_no=roll_no,
                                         image=image)
        user.save()
        student.save()
        alert = True
        return render(request, "book_manager/student_registration.html", {'alert': alert})
    return render(request, "book_manager/student_registration.html")


def student_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a student!!")
            else:
                return redirect("/profile")
        else:
            alert = True
            return render(request, "book_manager/student_login.html", {'alert': alert})
    return render(request, "book_manager/student_login.html")


def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("add_book")
            else:
                return HttpResponse("You are not an admin.")
        else:
            alert = True
            return render(request, "book_manager/admin_login.html", {'alert': alert})
    return render(request, "book_manager/admin_login.html")


def Logout(request):
    logout(request)
    return redirect("book_manager")