from django import forms

from .models import Comment, User, Post


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class Commentform(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ( 'body',)

class RoleForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ( 'role',)


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ( 'title','category', 'body',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Categoría'}),
        }

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ( 'title','category', 'body', 'active')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Categoría'}),
        }


class ActivePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ( 'fecha_activacion',)
        widgets ={
            'fecha1': forms.DateTimeInput(attrs={'type':'datetime-local'})
        }

class DeactivePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ( 'fecha_desactivacion',)
        widgets ={
            'fecha1': forms.DateTimeInput(attrs={'type':'datetime-local'})
        }