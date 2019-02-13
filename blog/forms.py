from django import forms
from blog.models import Article
from .models import Query
from blog.models import Query


class CreateArticle(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'thumb',]


class Query_form(forms.Form):
    full_name= forms.CharField()
    contact_no = forms.IntegerField()
    detail = forms.CharField()
