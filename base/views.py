from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from . models import Room,Topic,User,Message
from . forms import RoomForm,MyUserCreationForm,UserUpdateForm
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def loginPage(request):
    user = ''
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
    
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
            # print('user not exist')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')
    
    context = {'user': user, 'page': page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    
    form = MyUserCreationForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        login(request,user)
        return redirect('home')
    else:
        messages.error(request,"Please Check The Spelling!")
    context = {'form':form}
    return render(request,'base/login_register.html',context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''

    rooms = Room.objects.filter(Q(topic__name__icontains = q)|
                                Q(name__icontains = q)|
                                Q(description__icontains = q)|
                                Q(host__username__icontains = q))
    # roomUser = Room.objects.filter()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains =q)|
                                           Q(room__name__icontains = q)|
                                           Q(room__host__username__icontains = q))
    room_count = Room.objects.all().count()
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html', context)


# @login_required(login_url = '/login')
def userProfile(request,pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all() 
    room_count = Room.objects.all().count()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages,'room_count':room_count, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url = 'login')
def updateProfile(request, pk):
    user = request.user

    form = UserUpdateForm(instance=user)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile',pk=user.id)

    context = {'user': user,'form': form}
    return render (request, 'base/settings.html',context)


@login_required(login_url = '/login')
def createRoom(request):
    topics = Topic.objects.all()

    if request.method == 'POST':

        topic_name = request.POST.get('topic')
        topic , c = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create (
            host=request.user,
            topic=topic,
            name=request.POST.get('room_name'),
            description = request.POST.get('room_about')
        )
        return redirect('home')
    
    context = {'topics':topics}
    return render(request, 'base/createRoom.html', context)

def viewRoom(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()


    if request.method == 'POST':
        messages = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('message'),
        )
        room.participants.add(request.user)

        return redirect('view-room',pk=room.id)
    

    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/viewRoom.html', context)


@login_required(login_url = '/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,c = Topic.objects.get_or_create(name=topic_name)

        room.topic=topic
        room.name=request.POST.get('room_name')
        room.description = request.POST.get('room_about')
        room.save()
        return redirect('home')
    
    context = {'topics':topics, 'room':room}
    return render(request, 'base/createRoom.html', context)


@login_required(login_url = '/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context={'room': room}
    return render(request, 'base/delete.html', context)


@login_required(login_url = '/login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('view-room',message.room.id)
    context={'room': message}
    return render(request, 'base/delete.html', context)


def topicPage(request):
    topics = Topic.objects.all()
    context={'topics':topics}
    return render(request, 'base/topics.html',context)


def activityPage(request):
    room_messages = Message.objects.all()
    context={'room_messages':room_messages}
    return render(request, 'base/activity.html',context)