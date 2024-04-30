from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import time

# Create your models here.

class Concert(models.Model):
    date_start = models.DateField()
    date_end = models.DateField()
    SEASON_CHOICES = [
        ('1', '夏定'),
        ('2', '冬定')
    ]
    season = models.CharField(max_length=1, choices=SEASON_CHOICES)

class Song(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.PROTECT)
    song_name = models.CharField(max_length=30)
    author = models.CharField(max_length=30)

class Position(models.Model):
    POSITION_CHOICES = [
        ('1', 'その他/なし'),
        ('2', '指揮者'),
        ('3', 'コンサートマスター'),
        ('4', 'パートリーダー'),
        ('5', '幹事長'),
        ('6', '副幹事長'),
        ('7', '会計')
    ]
    position_name = models.CharField(max_length=20, choices=POSITION_CHOICES)
    is_staff = models.BooleanField()



class MemberManager(BaseUserManager):
    def create_user(self, name, generation, position, password=None, **extra_fields):
        if not name:
            raise ValueError('名前を入力してください')
        if not generation:
            raise ValueError('期を入力してください')
        if not position:
            raise ValueError('役職を入力してください')
        if not password:
            raise ValueError('パスワードを入力してください')
        
        position_temp = Position.objects.get(pk=position)

        member = self.model(
            name=name,
            generation=generation,
            position=position_temp
            **extra_fields
        )

        member.set_password(password)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        member.save(using=self._db)
        return member

    def create_superuser(self, name, generation, position, password, **extra_fields):
        position_temp = Position.objects.get(pk=position)

        member = self.model(
            name=name,
            generation=generation,
            position=position_temp
            **extra_fields
        )
        member.set_password(password)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        member.save(using=self._db)
        return member

class Member(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, unique=True)
    generation = models.IntegerField()
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(max_length=50, unique=True, blank=True, null=True)
    info1 = models.CharField(max_length=50, blank=True, null=True)
    info2 = models.CharField(max_length=50, blank=True, null=True)
    
    objects = MemberManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['generation', 'position']

    @property
    def is_staff(self):
        return self.position.is_staff if self.position else False
    

class RideNumber(models.Model):
    song = models.ForeignKey(Song, on_delete=models.PROTECT)
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    part = models.CharField(max_length=10)
    LEADER_CHOICES = [('1', '〇'), ('2', '×')]
    leader = models.CharField(choices=LEADER_CHOICES, max_length=1)


class Period(models.Model):
    PERIOD_CHOICES = [
        ('1', '早朝'), ('2', '1限'), ('3', '2限'), 
        ('4', '昼限'), ('5', '3限'), ('6', '4限'), 
        ('7', '5限'), ('8', '6限'), ('9', '夜限')
    ]
    period_name = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    time_start = models.TimeField()
    time_end = models.TimeField()


class Schedule(models.Model):
    date = models.DateField()
    period = models.ForeignKey(Period, on_delete=models.PROTECT)
    room_name = models.CharField(max_length=10)
    ROOM_TYPE_CHOICES = [
        ('1', '音楽練習室(月予約)'),
        ('2', '音楽練習室(週予約)'),
        ('3', '音楽練習室(当日予約)'),
        ('4', '個人ブース'),
        ('5', '部室'),
        ('6', 'その他')
    ]
    room_type = models.CharField(choices=ROOM_TYPE_CHOICES, max_length=1)
    song = models.ForeignKey(Song, on_delete=models.PROTECT)
    PRACTICE_TYPE_CHOICES = [
        ('1', '合奏練'),
        ('2', 'パート練'),
        ('3', 'アンサンブル練'),
        ('4', 'その他')
    ]
    practice_type = models.CharField(choices=PRACTICE_TYPE_CHOICES ,max_length=1)
    member = models.ForeignKey(Member, on_delete=models.PROTECT, blank=True, null=True)
   

class Participant(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT)
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    attendance = models.CharField(max_length=10)
    time = models.TimeField()
    updated_time = models.DateTimeField()


class Note(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT)
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    note = models.TextField()

def set_default_data(sender, **kwargs):
    periods = [
        {'period_name': '早朝', 'time_start': time(8,10,0), 'time_end': time(8,40,0)},
        {'period_name': '1限', 'time_start': time(8,50,0), 'time_end': time(10,30,0)},
        {'period_name': '2限', 'time_start': time(10,40,0), 'time_end': time(12,20,0)},
        {'period_name': '昼限', 'time_start': time(12,30,0), 'time_end': time(13,0,0)},
        {'period_name': '3限', 'time_start': time(13,10,0), 'time_end': time(14,50,0)},
        {'period_name': '4限', 'time_start': time(15,5,0), 'time_end': time(16,45,0)},
        {'period_name': '5限', 'time_start': time(17,0,0), 'time_end': time(18,40,0)},
        {'period_name': '6限', 'time_start': time(18,55,0), 'time_end': time(20,35,0)},
        {'period_name': '夜限', 'time_start': time(20,45,0), 'time_end': time(21,35,0)}
    ]

    positions = [
        {'position_name': 'その他/なし', 'is_staff': False},
        {'position_name': '指揮者', 'is_staff': True},
        {'position_name': 'コンサートマスター', 'is_staff': True},
        {'position_name': 'パートリーダー', 'is_staff': True},
        {'position_name': '幹事長', 'is_staff': True},
        {'position_name': '副幹事長', 'is_staff': True},
        {'position_name': '会計', 'is_staff': True}
    ]

    if Period.objects.count() == 0:
        for period in periods:
            default_periods = Period(period_name = period['period_name'], time_start = period['time_start'], time_end = period['time_end'])
            default_periods.save()

    if Position.objects.count() == 0:
        for position in positions:
            default_positions = Position(position_name = position['position_name'], is_staff = position['is_staff'])
            default_positions.save()

    return