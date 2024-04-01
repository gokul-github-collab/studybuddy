from django.shortcuts import render, redirect
from .models import User, Room, Topic, Message
from .forms import UserForm, MyUserCreationForm, RoomForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
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
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

       
        if password1 != password2:

            return render(request, 'base/sign_up.html', {'error': 'Passwords do not match!'})

        User = get_user_model()
        user = User.objects.create(username=username, email=email, name=name)
        user.password = make_password(password1)
        user.save()

        user = authenticate(request, email=email, password = password1)
        login(request, user)

        return redirect('home')

    context = {}
    return render(request, 'base/sign_up.html', context)



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' 
    rooms = Room.objects.filter(Q( topic__name__icontains=q ) |
                                Q(name__icontains=q) |
        Q(description__icontains=q))
    topics = Topic.objects.all()
    messages = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-id')[:10]
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

@login_required(login_url='/home')
def edit_profile(request, pk):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        avatar = request.FILES.get('avatar') 
        

        user.name = name
        user.username = username
        user.email = email
        user.bio = bio
        if avatar:
            user.avatar = avatar
        user.save()
        
        return redirect('home')  
    else:

        form = UserForm(instance=user)
    

    return render(request, "base/edit_profile.html", {"form": form})
