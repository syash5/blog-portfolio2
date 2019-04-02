from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Article
from .models import Query
from blog.forms import Query_form
from django.contrib.auth.decorators import login_required
from blog.forms import CreateArticle
from django.core.mail import EmailMessage, send_mail
import smtplib
from django.conf import settings






def article_list(request):
    articles = Article.objects.all().order_by('date');
    return render(request, 'blog/article_list.html', { 'articles': articles })

def article_detail(request, slug):
    # return HttpResponse(slug)
    article = Article.objects.get(slug=slug)
    return render(request, 'blog/article_detail.html', { 'article': article })


@login_required(login_url="/users/login/")
def article_create(request):
    title = "Create an Article"
    if request.method == 'POST':
        form = CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return HttpResponseRedirect(reverse('article_list'))
    else:
        form = CreateArticle()

    context = {"title": title, "form": form}
    return render(request, 'blog/article_create.html', context)



def query_create(request):
    title= "Query"
    if request.method == 'POST':
        form = Query_form(request.POST, request.FILES)
        if form.is_valid():
            # gmail smtp
            # subject= 'Query'
            # from_email= settings.EMAIL_HOST_USER
            # to_email=['']
            # contact_message = "Your Query is sent to our office and we will reply soon"
            # send_mail(subject, contact_message, from_email, [to_email], fail_silently=True)


            #aws ses
            # s = smtplib.SMTP()
            # s.connect('email-smtp.us-east-1.amazonaws.com', 587)
            # s.starttls()
            # s.login('', '')
            # msg = ' From: abc@gmail.com\nFrom: cde@gmail.com\nSubject: test\n\nTest Email'
            # s.sendmail('from', 'to', msg)



            # only saves a model from the modelform.
            # instance = form.save(commit=False)
            # user = request.user
            # instance.save()


            Query.objects.create(**form.cleaned_data) #creates a new instance (saves the data) and can be called anywhere, **is for passing the arguements
            return HttpResponseRedirect(reverse('home_page'))
    else:
        form = Query()
    context = {"title": title, "form": form}
    return render(request, 'blog/query_create.html', context )




def contact_us(request):
    return render(request, 'blog/contact_us.html')

def abcd(request):
    return render(request, 'blog/abcd.html')


def home_page(request):
    return render(request, 'blog/homepage.html')

def about(request):
    return render(request, 'about.html')
