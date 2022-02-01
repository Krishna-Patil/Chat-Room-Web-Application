from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RoomCreateForm, RoomUpdateForm, UserUpdateForm, CustomUserCreationForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import *
# Create your views here.


def login_view(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('Email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "user does not exist.")

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(
                request, "wrong Password.")
    return render(request, 'base/login_register.html', {'page': page})


def logout_view(request):
    logout(request)
    return redirect('home')


def signup_view(request):
    if request.method == 'POST':
        data = CustomUserCreationForm(request.POST)
        if data.is_valid():
            user = data.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            HttpResponse("issues during signing up.")
    form = CustomUserCreationForm()
    return render(request, 'base/login_register.html', {'form': form})


def home_view(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(name__icontains=q) |
        Q(topic__name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(discription__icontains=q)
    )
    rooms_count = rooms.count()
    topics = Topic.objects.all()[:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics,
               'rooms_count': rooms_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room_view(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        text = request.POST.get('text')
        msg = Message.objects.create(text=text, room=room, user=request.user)
        msg.save()
        room.participants.add(request.user)
        return redirect('room', pk)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
    }
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def create_room_view(request):
    form = RoomCreateForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            discription=request.POST.get('discription')
        )
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room_view(request, pk):
    room = get_object_or_404(Room, pk=pk)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse(" What are you doing here? ")
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.discription = request.POST.get('discription')
        room.save()
        return redirect('room', pk)
    else:
        form = RoomUpdateForm(instance=room)
        context = {'form': form, 'topics': topics, 'room': room}
        return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_room_view(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.user != room.host:
        return HttpResponse(" What are you doing here? ")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    else:
        context = {'obj': room}
        return render(request, 'base/delete.html', context)


def delete_message_view(request, pk):
    msg = Message.objects.get(pk=pk)
    if request.user != msg.user:
        return HttpResponse("What are you doing here?")
    if request.method == 'POST':
        msg.delete()
        return redirect('home')
    context = {'obj': msg}
    return render(request, 'base/delete.html', context)


def user_profile_view(request, pk):
    user = User.objects.get(pk=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    rooms_count = rooms.count()
    context = {'user': user, 'rooms': rooms, 'rooms_count': rooms_count,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/user_profile.html', context)


@login_required(login_url='login')
def user_update_view(request):
    form = UserUpdateForm(instance=request.user)
    if request.method == 'POST':
        data = UserUpdateForm(request.POST, request.FILES,
                              instance=request.user)
        if data.is_valid():
            data.save()
            return redirect('user_profile', request.user.id)
    context = {'form': form}
    return render(request, 'base/update_user.html', context)


def topics_view(request):
    q = request.POST.get('q') if request.POST.get('q') is not None else ''
    topics = Topic.objects.filter(name__icontains=q)
    topics_count = topics.count()
    context = {
        'topics': topics,
        'topics_count': topics_count,
    }
    return render(request, 'base/topics.html', context)
