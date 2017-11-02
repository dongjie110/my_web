# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from embed_video.fields import EmbedVideoField

# Create your models here.

from django.contrib.auth.models import User

class MyUser(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=16)
    permission = models.IntegerField(default=1)

    def __unicode__(self):
        return self.user.username

class Catagory(models.Model):
    """
    博客分类
    """
    name = models.CharField('名称',max_length=30)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    """
    博客标签
    """
    name = models.CharField('名称',max_length=16)
    code = models.IntegerField('编码',null=True)

    def __unicode__(self):
        return self.name

class Blog(models.Model):
    """
    博客
    """
    title = models.CharField('标题',max_length=32)
    author = models.CharField('作者',max_length=16)
    content = models.TextField('博客正文')
    created = models.DateTimeField('发布时间',auto_now_add=True)
    catagory = models.ForeignKey(Catagory,verbose_name='分类')
    tags = models.ManyToManyField(Tag,verbose_name='标签')

    class META:
        ordering = ['author']

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    """
    评论
    """
    blog = models.ForeignKey(Blog,verbose_name='博客')
    name = models.CharField('称呼',max_length=16)
    email = models.EmailField('邮箱')
    content = models.CharField('内容',max_length=240)
    created = models.DateTimeField('发布时间',auto_now_add=True)

    def __unicode__(self):
        return self.content

class Book(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    author = models.CharField(max_length=128)
    publish_date = models.DateField()
    category = models.CharField(max_length=128)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Img(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    img = models.ImageField(upload_to='image/%Y/%m/%d/')
    book = models.ForeignKey(Book)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Movie(models.Model):
    video = EmbedVideoField()  # same like models.URLField()