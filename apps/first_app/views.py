# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

import bcrypt

# Create your views here.

def index(request):
    return render(request,'first_app/index.html')

def register(request):
    name = request.POST['name']
    alias = request.POST['alias']
    email = request.POST['email']
    password = request.POST['password']
    confirm = request.POST['confirm']
    x = {'name': name,'alias': alias, 'email': email, 'password': password, 'confirm': confirm}
    errors = User.objects.validate(x)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(name = name, alias = alias, email = email, password = hashed_password )
        request.session['id'] = User.objects.filter(email=request.POST['email'])[0].id
        return redirect('/books')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        user = User.objects.filter(email = email)[0]
        hash1 = user.password
    except:
        hash1 = request.POST['email']


    x = { 'email': email, 'password': password, 'hash1' : hash1}
    errors = User.objects.validateLogin(x)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        request.session['id'] = User.objects.filter(email=request.POST['email'])[0].id
        return redirect('/books')

def books(request):
    context = {}
    context['stuff'] = Review.objects.all()
    print Book.objects.all()
    return render(request,'first_app/books.html',context)


def logout(request):
    request.session['id'] = ""
    return redirect('/')