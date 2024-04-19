from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView as BaseLoginView
from django.db.models import Prefetch
from .forms import AddScheduleForm, AddRideNumberForm, AddConcertForm, AddSongForm, AddMemberForm, LoginForm #, SelectConcertForm
from .models import Concert, Song, Member, RideNumber, Schedule, Participant, Note


# Create your views here.

class LoginView(BaseLoginView):
    form_class = LoginForm
    template_name = "login.html"
    form_name = 'login_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.form_name] = self.get_form(self.form_class)
        return context



def schedule(request):
    return render(request, 'schedule.html')

'''
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            name = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            member = authenticate(name=name, password=password)
            if member is not None:
                login(request, member)
                return redirect('mypage')
            else:
                login_form.add_error(None, '名前またはパスワードが間違っています')
    else:
        login_form = LoginForm()

    return render(request, 'login.html', context={'login_form': login_form})
'''

def mypage(request):
    return render(request, 'mypage.html')

def ridenumbers(request):
    return render(request, 'ridenumbers.html')

def ensoushoku(request):
    return render(request, 'ensoushoku.html')

def editmyschedule(request):
    return render(request, 'editmyschedule.html')

def editschedule(request):
    if request.method == 'POST':
        add_schedule_form = AddScheduleForm(request.POST)
        if add_schedule_form.is_valid():
            add_schedule_form.save()
    else:
        add_schedule_form = AddScheduleForm()
    return render(request, 'editschedule.html', 
                  context={
                      'add_schedule_form': add_schedule_form
                  })

def editridenumbers(request):
    concerts = Concert.objects.all()
    member_prefetch = Prefetch('member')
    ride_numbers = RideNumber.objects.all().prefetch_related(member_prefetch)
    songs_in_concerts = Concert.objects.prefetch_related(
        Prefetch('song_set', queryset=Song.objects.prefetch_related(
            Prefetch('ridenumber_set', queryset=ride_numbers, to_attr='rides')
        ))
    )
    songs = {}
    song_rides = {}
    for concert in songs_in_concerts:
        songs[concert.id] = concert.song_set.all()
        for song in songs[concert.id]:
            song_rides[song.id] = {}
            for ride in song.rides:
                if ride.part not in song_rides[song.id]:
                    song_rides[song.id][ride.part] = []
                song_rides[song.id][ride.part].append(f"{ride.member.last_name} {ride.member.first_name}")


    if request.method == 'POST':
        if 'select_concert' in request.POST:
            #select_concert_form = SelectConcertForm(request.POST)
            add_ride_number_form = AddRideNumberForm()
            #if select_concert_form.is_valid:
            #    pass
        elif 'add_ride_number' in request.POST:
            #select_concert_form = SelectConcertForm()
            add_ride_number_form = AddRideNumberForm(request.POST)
            if add_ride_number_form.is_valid:
                add_ride_number_form.save()
    else:
        #select_concert_form = SelectConcertForm()
        add_ride_number_form = AddRideNumberForm()

    return render(request, 'editridenumbers.html', 
                  context={
                      #'select_concert_form': select_concert_form,
                      'add_ride_number_form': add_ride_number_form,
                      'concerts': concerts,
                      'songs': songs,
                      'song_rides': song_rides,
                  })


def editmembers(request):
    members = Member.objects.all()

    if request.method == 'POST':
        if 'add_member' in request.POST:
            add_member_form = AddMemberForm(request.POST)
            if add_member_form.is_valid:
                add_member_form.save()
    else:
        add_member_form = AddMemberForm()

    return render(request, 'editmembers.html',
                  context ={
                      'add_member_form': add_member_form,
                      'members': members
                  })


def editconcerts(request):
    concerts = Concert.objects.all()
    member_prefetch = Prefetch('member')
    ride_numbers = RideNumber.objects.filter(leader='1').prefetch_related(member_prefetch)
    songs_in_concerts = Concert.objects.prefetch_related(
        Prefetch('song_set', queryset=Song.objects.prefetch_related(
            Prefetch('ridenumber_set', queryset=ride_numbers, to_attr='leaders')
        ))
    )
    songs = {}
    leaders = {}
    for concert in songs_in_concerts:
        songs[concert.id] = concert.song_set.all()
        for song in songs[concert.id]:
            leaders[song.id] = {leaders.part: f"{leader.member.last_name} {leader.member.first_name}" for leader in song.leaders}

    if request.method == 'POST':
        if 'add_concert' in request.POST:
            add_concert_form = AddConcertForm(request.POST)
            add_song_form = AddSongForm()
            if add_concert_form.is_valid():
                add_concert_form.save()

        elif 'add_song' in request.POST:
            add_concert_form = AddConcertForm()
            add_song_form = AddSongForm(request.POST)
            if add_song_form.is_valid():
                add_song_form.save()
    else:
        add_concert_form = AddConcertForm()
        add_song_form = AddSongForm()

    return render(request, 'editconcerts.html', 
                  context={
                      'add_concert_form': add_concert_form,
                      'add_song_form': add_song_form,
                      'concerts': concerts,
                      'songs': songs,
                      'leaders': leaders
                    })


