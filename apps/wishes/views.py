from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User,UserManager,Item,ItemManager

def index(request):
    return render(request, 'wishes/index.html')

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')


    hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    User.objects.create(first_name = request.POST['first_name'], username = request.POST['username'], password = hashed,hireDate=request.POST['hireddate'])
    request.session['username'] = request.POST['username']
    return redirect('/dashboard')

def login(request):
    if User.objects.filter(username = request.POST['username']):
        user = User.objects.get(username=request.POST['username'])
        request.session['username'] = request.POST['username']
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['username'] = request.POST['username']
            return redirect('/dashboard')



    messages.error(request, "Invalid User Name or Password")
    return redirect('/')




def dashboard (request):
    if 'username' not in request.session:
            return redirect('/')
    user = User.objects.get(username = request.session['username'])
    otheritems = Item.objects.exclude(liked_by=user)
    
    context = {
        'users': User.objects.all(),
        'items': Item.objects.all(),
        'user': user,
        'otheritems':otheritems,
    }




    return render(request, 'wishes/dashboard.html',context)


def logout(request):
    request.session.clear()
    return redirect('/') 

def additempage(request):
    if 'username' not in request.session:
        return redirect('/')
    return render(request, 'wishes/additem.html')

def createItem(request):
    if 'username' not in request.session:
        return redirect('/')
    errors = Item.objects.itemValidator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/additempage')
    else:
        user = User.objects.get(username = request.session['username'])
        Item.objects.create(name=request.POST['item_name'],created_by=user)
        return redirect('/dashboard')

def viewItem(request, id):
    if 'username' not in request.session:
        return redirect('/')
    context = {
        'item': Item.objects.get(id=id),
        'users': User.objects.all()
    }
    return render(request, 'wishes/viewitem.html', context)

def delete(request):
    Item.objects.get(id=request.POST['item_id']).delete()
    return redirect('/dashboard')

def like(request):
    user=User.objects.get(username=request.session['username'])
    item = Item.objects.get(id=request.POST['item_id'])
    item.liked_by.add(user)
    item.save()
    return redirect('/dashboard')

def remove(request):
    user = User.objects.get(username=request.session['username'])
    item = Item.objects.get(id=request.POST['item_id']) 
    item.liked_by.remove(user)
    item.save()
    return redirect('/dashboard')

    