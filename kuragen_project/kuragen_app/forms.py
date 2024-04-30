from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .models import Schedule, Member, Position, Concert, Song, RideNumber

# ログイン 

class LoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '名前（全角カナ）'
        self.fields['password'].label = 'パスワード'

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['username'] = cleaned_data.get('name')
        return cleaned_data

    
    


# 練習日程調整

class AddScheduleForm(forms.ModelForm):
    # SQLの勉強したらデータベースから現在練習中の曲の抽出　実装する
    # JavaScriptの勉強したらその他欄の実装する
    # アンサンブル、パート練、その他の場合の代表者、参加人数の追加？

    class Meta:
        model = Schedule
        fields = ['date', 'period', 'room_name', 'room_type', 'song', 'practice_type']
        labels = {
            'date': '日にち',
            'period': '時限',
            'room_name': '部屋の名前',
            'room_type': '部屋の種類・予約方法',
            'song': '曲名',
            'practice_type': '練習内容',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddScheduleForm, self).__init__(*args, **kwargs)
        
        today = timezone.now().date()
        songs = Song.objects.filter(
            concert__date_start__lte = today,
            concert__date_end__gte = today
        )
        song_choices = [(song.id, f"{song.song_name}/{song.author}") for song in songs]
        self.fields['song'].choices = song_choices

        PERIOD_CHOICES = [
            ('1', '早朝'),
            ('2', '1限'),
            ('3', '2限'),
            ('4', '昼限'),
            ('5', '3限'),
            ('6', '4限'),
            ('7', '5限'),
            ('8', '6限'),
            ('9', '夜限')
        ]
        self.fields['period'].choices = PERIOD_CHOICES
    
    def save(self, *args, **kwargs):
        return super(AddScheduleForm, self).save(*args, **kwargs)
        

# 乗り番調整

#class SelectConcertForm(forms.Form):
#    today = timezone.now().date()
#    current_concert = Concert.objects.filter(
#        concert__date_start__lte=today,
#        concert__date_end__gte = today
#    )
#    year = timezone.now().year()
#    initial_concert = str(year) + '年' + current_concert.season
#    concert = forms.ChoiceField(choices=CONCERT_CHOICES, initial=initial_concert)


class AddRideNumberForm(forms.ModelForm):
    name = forms.CharField(max_length=30, label='名前')
    class Meta:
        model = RideNumber
        fields = '__all__'
        labels = {
            'leader': '演奏職'
        }
        widgets = {
            'song': forms.HiddenInput(),
            'member': forms.HiddenInput(),
            'part': forms.HiddenInput(),
        }
    
    def save(self, *args, **kwargs):
        ride = super(AddRideNumberForm, self).save(commit=False)
        try:
            ride.member = Member.objects.get(name=ride.name)
        except ObjectDoesNotExist:
            raise ValueError("指定された団員が存在しません。")
        
        ride.save()
        return ride


# 団員情報

class AddMemberForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ['name', 'generation', 'position', 'email', 'password1', 'password2']
        labels = {
            'name': '名前(全角カナ)',
            'generation': '期',
            'position': '役職',
            'email': 'メールアドレス(任意)',
            'password1': '初期パスワード',
            'password2': '初期パスワード(確認)'
        }
        widgets = {
            'password1': forms.PasswordInput,
            'password2': forms.PasswordInput
        }

    def __init__(self, *args, **kwargs):
        super(AddMemberForm, self).__init__(*args, **kwargs)
        self.fields['position'].queryset = Position.objects.all()

    def save(self, *args, **kwargs):
        return super(AddMemberForm, self).save(*args, **kwargs)


# 演奏会情報

class AddConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = '__all__'
        labels = {
            'date_start': '練習開始日',
            'date_end': '練習終了日',
            'season': '',
        }
        widgets = {
            'date_start': forms.DateInput(attrs={'type': 'date'}),
            'date_end': forms.DateInput(attrs={'type': 'date'}),
            'season': forms.RadioSelect,
        }
    
    def save(self, *args, **kwargs):
        return super(AddConcertForm, self).save(*args, **kwargs)


class AddSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['concert', 'song_name', 'author']
        labels = {
            'song_name': '曲名',
            'author': '作曲者'
        }
        widgets = {
            'concert': forms.HiddenInput()
        }
    
    def save(self, *args, **kwargs):
        return super(AddSongForm, self).save(*args, **kwargs)