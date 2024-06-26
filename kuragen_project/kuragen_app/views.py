from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView as BaseLoginView
from django.db.models import Prefetch, Count, Q
from django.utils import timezone
from datetime import timedelta, datetime, date
from calendar import monthrange
from collections import defaultdict
from . import forms
from . import models
#from .forms import AddScheduleForm, AddRideNumberForm, AddConcertForm, AddSongForm, AddMemberForm, LoginForm #, SelectConcertForm
#from .models import Concert, Song, Member, RideNumber, Schedule, Participant, Note


# Create your views here.

class LoginView(BaseLoginView, TemplateView):
    form_class = forms.LoginForm
    template_name = 'login.html'
    form_name = 'login_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.form_name] = self.get_form(self.form_class)
        return context 

    def get_success_url(self):
        return reverse_lazy('mypage')

class Schedule(TemplateView):
    template_name = 'schedule.html'

class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'mypage.html'

class RideNumbersView(LoginRequiredMixin, TemplateView):
    template_name = 'ridenumber.html'

class EnsoushokuView(LoginRequiredMixin, TemplateView):
    template_name = 'ensoushoku,html'

class EditMyScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'editmyschedule.html'

class EditScheduleView(LoginRequiredMixin, TemplateView, FormView):
    template_name = 'editschedule.html'
    form_class = forms.AddScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year_month = self.kwargs.get('year_month', datetime.now().strftime("%Y%m"))
        context['year_month'] = year_month
        context['schedule_data'] = self.get_current_data(year_month)

    def get_current_data(self, year_month):
        year = int(year_month[:4])
        month = int(year_month[4:])
        start_of_month = date(year, month, 1)
        end_of_month = date(year, month, monthrange(year, month)[1])

        notes_prefetch = Prefetch('note_set', queryset=models.Note.select_related('member'))
        get_schedules = models.Schedule.objects.all(
            ).select_related('period').prefetch_related(
                notes_prefetch
            ).annotate(
                absent_count=Count('participants', filter=Q(participants__attendance='absent')),
                participants=Count('song__ridenumbers')
            ).filter(
                 date__gte=start_of_month,
                 date__lte=end_of_month
            )
        
        weekdays = ["月", "火", "水", "木", "金", "土", "日"]
        
        schedules_by_month = []
        for s in get_schedules:
            notes=""
            for note in s.note_set.all():
                notes += f"{note.note} ({note.member.name})\n"

            schedules_by_month.append({

                'date': s.date.strftime("%m/%d") + f"({weekdays[s.date.weekday()]})",
                'period': s.period,
                'room': f"{s.room_name} ({s.get_room_type_display()})",
                'practice': f"{s.song.song_name} ({s.get_practice_type_display()})",
                'participants': s.participants - s.absent_count,
                'notes': notes,
            })

        current_data = {
                        'schedules_by_month': dict(schedules_by_month),
                        'year_month': year_month
                       }

        return current_data


    def get(self, request, *args, **kwargs):
        add_schedule_form = self.form_class()
        current_data = self.get_current_data()

        return render(request, self.template_name, {
            'add_schedule_form': add_schedule_form,
            'schedules': current_data['schedules']
        })
    
    def post(self, request, *args, **kwargs):
        add_schedule_form = self.form_class(request.POST)

        if 'add_schedule' in request.POST:
            if add_schedule_form.is_valid():
                add_schedule_form.save()

        return render(request, self.template_name, {
            'add_schedule_form': add_schedule_form
        })
    

class EditRideNumbersView(LoginRequiredMixin, View):
    template_name = 'editridenumbers.html'

    def get_current_data(self):
        concerts = models.Concert.objects.all()
        member_prefetch = Prefetch('member')
        ride_numbers = models.RideNumber.objects.all().prefetch_related(member_prefetch)
        songs_in_concerts = models.Concert.objects.prefetch_related(
            Prefetch('song_set', queryset=models.Song.objects.prefetch_related(
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
                    song_rides[song.id][ride.part].append(
                        f"{ride.member.name}"
                        )
        
        current_data = {
            'concerts': concerts,
            'songs': songs,
            'song_rides': song_rides,
        }

        return current_data
    
    def get(self, request, *args, **kwargs):
        add_ride_number_form = forms.AddRideNumberForm
        current_data = self.get_current_data()

        return render(request, self.template_name, {
            'add_ride_number_form': add_ride_number_form,
            'concerts': current_data['concerts'],
            'songs': current_data['songs'],
            'song_rides': current_data['song_rides'],
        })
    
    def post(self, request, *args, **kwargs):
        add_ride_number_form = forms.AddRideNumberForm(request.POST)
        current_data = self.get_current_data()

        if request.method == 'POST':
            if 'select_concert' in request.POST:
                #select_concert_form = SelectConcertForm(request.POST)
                add_ride_number_form = forms.AddRideNumberForm()
                #if select_concert_form.is_valid:
                #    pass
            elif 'add_ride_number' in request.POST:
                #select_concert_form = SelectConcertForm()
                add_ride_number_form = forms.AddRideNumberForm(request.POST)
                if add_ride_number_form.is_valid:
                    add_ride_number_form.save()
        else:
            #select_concert_form = SelectConcertForm()
            add_ride_number_form = forms.AddRideNumberForm()
        
        return render(request, self.template_name, {
                        #'select_concert_form': select_concert_form,
                        'add_ride_number_form': add_ride_number_form,
                        'concerts': current_data['concerts'],
                        'songs': current_data['songs'],
                        'song_rides': current_data['song_rides'],
                    })


class EditMembersView(LoginRequiredMixin, View):
    template_name = 'editmembers.html'
    form_class = forms.AddMemberForm

    def get(self, request, *args, **kwargs):
        add_member_form = self.form_class()
        members = models.Member.objects.all().order_by('name', 'generation')
        return render(request, self.template_name, {
            'add_member_form': add_member_form,
            'members': members
        })

    def post(self, request, *args, **kwargs):
        add_member_form = self.form_class(request.POST)
        members = models.Member.objects.all()

        if 'add_member' in request.POST:
            if add_member_form.is_valid():
                add_member_form.save()
        
        return render(request, self.template_name, {
            'add_member_form': add_member_form,
            'members': members
        })
    

class EditConcertsView(LoginRequiredMixin, TemplateView, View):
    template_name = 'editconcerts.html'

    def get_current_data(self):
        concerts = models.Concert.objects.all()
        member_prefetch = Prefetch('member')
        ride_numbers = models.RideNumber.objects.filter(leader='1').prefetch_related(member_prefetch)
        songs_in_concerts = models.Concert.objects.prefetch_related(
            Prefetch('song_set', queryset=models.Song.objects.prefetch_related(
                Prefetch('ridenumber_set', queryset=ride_numbers, to_attr='leaders')
            ))
        )
        songs = {}
        leaders = {}
        for concert in songs_in_concerts:
            songs[concert.id] = concert.song_set.all()
            for song in songs[concert.id]:
                leaders[song.id] = {leaders.part: f"{leader.member.last_name} {leader.member.first_name}" for leader in song.leaders}

        current_data = {
            'concerts': concerts,
            'songs': songs,
            'leaders': leaders,
        }
        return current_data
    
    def get(self, request, *args, **kwargs):
        add_concert_form = forms.AddConcertForm()
        add_song_form = forms.AddSongForm()
        current_data = self.get_current_data()

        return render(request, self.template_name, {
            'add_concert_form': add_concert_form,
            'add_song_form': add_song_form,
            'concerts': current_data['concerts'],
            'songs': current_data['songs'],
            'leaders': current_data['leaders']
        })

    def post(self, request, *args, **kwargs):
        current_data = self.get_current_data()

        if request.method == 'POST':
            if 'add_concert' in request.POST:
                add_concert_form = forms.AddConcertForm(request.POST)
                add_song_form = forms.AddSongForm()
                if add_concert_form.is_valid():
                    add_concert_form.save()

            elif 'add_song' in request.POST:
                add_concert_form = forms.AddConcertForm()
                add_song_form = forms.AddSongForm(request.POST)
                if add_song_form.is_valid():
                    add_song_form.save()
        else:
            add_concert_form = forms.AddConcertForm()
            add_song_form = forms.AddSongForm()

        return render(request, 'editconcerts.html', 
                    context={
                        'add_concert_form': add_concert_form,
                        'add_song_form': add_song_form,
                        'concerts': current_data['concerts'],
                        'songs': current_data['songs'],
                        'leaders': current_data['leaders']
                        })


