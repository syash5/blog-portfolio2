from rest_framework import generics
from blog.models import Article
from rest_framework import viewsets
from django.shortcuts import render
from .serializers import ArticleSerializer

class ArticleRUD(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    # def get_queryset(self):
    #     return Article.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return Article.objects.get(pk=pk)
    