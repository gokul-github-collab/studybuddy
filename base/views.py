from django.shortcuts import render, redirect
from .models import User, Room, Topic, Message
from .forms import UserForm, MyUserCreationForm, RoomForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
# Create your views here.



def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            HttpResponse("Hmm, there is no one with that email or password")
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'base/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')


def register(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('home')
        
    return render(request,  'base/sign_up.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' 
    rooms = Room.objects.filter(Q( topic__name__icontains=q ) |
                                Q(name__icontains=q) |
        Q(description__icontains=q))
    topics = Topic.objects.all()
    messages = Message.objects.all().order_by('-id')[:10]
    return render(request, 'base/home.html', {"rooms": rooms, 'topics': topics, 'messages': messages})


@login_required(login_url='/home')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    

    if request.method == 'POST':  
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        new_room = Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('room', pk=new_room.id)
    return render(request, 'base/create_room.html', {"form": form, "topics": topics})

@login_required(login_url='/home')
def update_room(request, pk):
    room = Room.objects.get(id=pk)

    form = RoomForm(instance=room)

    if request.user != room.host:
        HttpResponse("You aren't allowed to this page")

    if request.method == 'POST':
        form = RoomForm(request.POST ,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')


    return render(request, 'base/update_room.html', {"form": form})

@login_required(login_url='/home')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        HttpResponse("You aren't allowed to this page")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete_room.html', {'room': room})


def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message =  Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('message')
        )

        room.participants.add(request.user)

        return redirect('room', room.id)

    return render(request, 'base/room.html', {"messages": messages, 'room': room, 'participants': participants})


def user_profile(request, pk):
    topics = Topic.objects.all()

    ruser = User.objects.get(id=pk)

    messages = Message.objects.filter(user=ruser)

    rooms = Room.objects.filter(host=ruser)

    return render(request, 'base/user_profile.html', {'topics': topics, "ruser": ruser, "messages": messages, "rooms": rooms})


def edit_profile(request, pk):
    ruser = User.objects.get(id=pk)

    user_form = UserForm(instance=ruser)

    if request.method == "POST" and request.user == ruser:
        user_form = UserForm(request.POST, request.FILES, instance=ruser)

        if user_form.is_valid():
            user_form.save()

            return redirect('user_profile', pk=ruser.id)

    return render(request, "base/edit_profile.html", {"form": user_form})
