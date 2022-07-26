from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Textarea
from .models import *
from django.contrib.auth.models import User
from .models import Profile



#-----------------book-form---------------------------------

class IssueBookForm(forms.Form):
    isbn2 = forms.ModelChoiceField(queryset=Book.objects.all(), empty_label="Китептин аты - [ISBN]",
                                   to_field_name="isbn", label="Китеп (китептин аты жана ISBN номери)")
    name2 = forms.ModelChoiceField(queryset=User_reader.objects.all(), empty_label="Аты [Окуу жайдын аты жана курсу] [Мектептин аты жана классы] [Окурмандын №_]",
                                   to_field_name="user", label="Окурмандын жөнүндө маалымат")

    isbn2.widget.attrs.update({'class': 'form-control'})
    name2.widget.attrs.update({'class': 'form-control'})


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('avatar',)



class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'tm-form-control'}))
    first_name = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'tm-form-control'}))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'tm-form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'tm-form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'tm-form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'tm-form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']




class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Атыңыз: ',
                                                               'class': 'input-text',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Фамилияңыз: ',
                                                              'class': 'input-text',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Логин: ',
                                                             'class': 'input-text',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Почтаңызды жазыңыз: ',
                                                           'class': 'input-text',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Сыр сөздү жазыңыз: ',
                                                                  'class': 'input-text',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password1',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Сыр сөздү кайталап жазыңыз: ',
                                                                  'class': 'input-text',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password2',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']




class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(
                               attrs={'class': 'form-control', 'placeholder': 'Сөз жазып издеңиз'}),)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'comment-form-comment'
        self.fields['text'].widget = Textarea(attrs={'class': 'comment-form-comment', 'placeholder': 'Ой-пикирлерди жазуу:'})





from .models import Rating, RatingStar

class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)


#------------------------News-multi-img-form------------------------------
class NewsForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    text = forms.Textarea()

    class Meta:
        model = News
        fields = ('title', 'text', )


class Image_NewsForm(forms.ModelForm):
    image = forms.ImageField(label='Image', widget=forms.FileInput(attrs={'multiple': 'multiple'}))
    class Meta:
        model = Images_News
        fields = ('image', )