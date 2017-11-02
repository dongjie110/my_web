# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render,render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from myweb.utils import permission_check

# Create your views here.
from blog.models import *
from blog.forms import CommentForm
from django.http import Http404

def index(request):
    user = request.user if request.user.is_authenticated() else None
    content = {
        'active_menu': 'homepage',
        'user': user,
    }
    return render(request, 'index.html', content)

def movie(request):
    # user = request.user if request.user.is_authenticated() else None
    content = {
        'active_menu': 'movie',

        }
    return render(request, 'movie.html', content)

def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if password == '' or repeat_password == '':
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            username = request.POST.get('username', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create_user(username=username, password=password,
                                                    email=request.POST.get('email', ''))
                new_user.save()
                new_my_user = MyUser(user=new_user, nickname=request.POST.get('nickname', ''))
                new_my_user.save()
                state = 'success'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None,
    }
    return render(request, 'signup.html', content)

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            state = 'not_exist_or_password_error'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None
    }
    return render(request, 'login.html', content)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage'))

@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'
        else:
            state = 'password_error'
    content = {
        'user': user,
        'active_menu': 'homepage',
        'state': state,
    }
    return render(request, 'set_password.html', content)

@user_passes_test(permission_check)
def add_book(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_book = Book(
                name=request.POST.get('name', ''),
                author=request.POST.get('author', ''),
                category=request.POST.get('category', ''),
                price=request.POST.get('price', 0),
                publish_date=request.POST.get('publish_date', '')
        )
        new_book.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_book',
        'state': state,
    }
    return render(request, 'add_book.html', content)

def detail(request):
    user = request.user if request.user.is_authenticated() else None
    book_id = request.GET.get('id', '')
    if book_id == '':
        return HttpResponseRedirect(reverse('view_book_list'))
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return HttpResponseRedirect(reverse('view_book_list'))
    content = {
        'user': user,
        'active_menu': 'view_book',
        'book': book,
    }
    return render(request, 'detail.html', content)

@user_passes_test(permission_check)
def add_img(request):
    user = request.user
    state = None
    if request.method == 'POST':
        try:
            new_img = Img(
                    name=request.POST.get('name', ''),
                    description=request.POST.get('description', ''),
                    img=request.FILES.get('img', ''),
                    book=Book.objects.get(pk=request.POST.get('book', ''))
            )
            new_img.save()
        except Book.DoesNotExist as e:
            state = 'error'
            print(e)
        else:
            state = 'success'
    content = {
        'user': user,
        'state': state,
        'book_list': Book.objects.all(),
        'active_menu': 'add_img',
    }
    return render(request, 'add_img.html', content)

def get_blogs(request):
    blogs = Blog.objects.all().order_by('-created')
    return render_to_response('blog_list.html',{'blogs':blogs})

def get_details(request,blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        raise Http404
    if request.method == 'GET':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['blog'] = blog
            Comment.objects.create(**cleaned_data)
    ctx = {
        'blog':blog,
        'comments':blog.comment_set.all().order_by('-created'),
        'form':form
    }
    return render(request,'blog_details.html',ctx)

def view_blog_list(request):
    user = request.user if request.user.is_authenticated() else None
    author_list = Blog.objects.values_list('author', flat=True).distinct()
    query_author = request.GET.get('author', 'all')
    if (not query_author) or Blog.objects.filter(author=query_author).count() is 0:
        query_author = 'all'
        blog_list = Blog.objects.all()
    else:
        blog_list = Blog.objects.filter(author=query_author)

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        blog_list = Blog.objects.filter(name__contains=keyword)
        query_author = 'all'

    paginator = Paginator(blog_list, 5)
    page = request.GET.get('page')
    try:
        blog_list = paginator.page(page)
    except PageNotAnInteger:
        blog_list = paginator.page(1)
    except EmptyPage:
        blog_list = paginator.page(paginator.num_pages)
    ctx = {
        'user': user,
        'active_menu': 'view_book',
        'author_list': author_list,
        'query_author': query_author,
        'blog_list': blog_list,
    }
    return render(request, 'blist_detail.html', ctx)

def view_book_list(request):
    user = request.user if request.user.is_authenticated() else None
    category_list = Book.objects.values_list('category', flat=True).distinct()
    query_category = request.GET.get('category', 'all')
    if (not query_category) or Book.objects.filter(category=query_category).count() is 0:
        query_category = 'all'
        book_list = Book.objects.all()
    else:
        book_list = Book.objects.filter(category=query_category)

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        book_list = Book.objects.filter(name__contains=keyword)
        query_category = 'all'

    paginator = Paginator(book_list, 5)
    page = request.GET.get('page')
    try:
        book_list = paginator.page(page)
    except PageNotAnInteger:
        book_list = paginator.page(1)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages)
    content = {
        'user': user,
        'active_menu': 'view_book',
        'category_list': category_list,
        'query_category': query_category,
        'book_list': book_list,
    }
    return render(request, 'view_book_list.html', content)

def get_catagory_detail(request,catagory_id):
    try:
        catagory = Catagory.objects.get(id=catagory_id)
    except Tag.DoesNotExist:
        raise Http404
    if request.method == 'GET':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['catagory'] = catagory
            Comment.objects.create(**cleaned_data)
    ctx = {
        'catagory': catagory,
        # 'comments': catagory.comment_set.all().order_by('-created'),
        'form': form
    }
    return render(request, 'catagory_detail.html', ctx)