from .views import ArticleRUD
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register('articles',ArticleRUD)

urlpatterns = [
    path('', include(router.urls), name='articlerud'),

]