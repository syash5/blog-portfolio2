from graphene_django import DjangoObjectType
import graphene
from blog.models import Article




class User(DjangoObjectType):
    class Meta:
        model = Article

class Query(graphene.ObjectType):
    users = graphene.List(User)

    def resolve_users(self, info):
        return Article.objects.all()

schema = graphene.Schema(query=Query)