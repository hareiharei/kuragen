from django.urls import path
from . import views

app_name = 'kuragen_app'
urlpatterns = [
    path('schedule/', views.schedule, name='schedule'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('mypage/', views.MyPageView.as_view(), name='mypage'),
    path('ridenumbers/', views.RideNumbersView.as_view(), name='ridenumbers'),
    path('ensoushoku/', views.EnsoushokuView.as_view, name='ensoushoku'),
    path('ensoushoku/myschedule/', views.editmyschedule, name='editmyschedule'),
    path('ensoushoku/schedule/', views.editschedule, name='editschedule'),
    path('ensoushoku/ridenumbers/', views.editridenumbers, name='editridenumbers'),
    path('ensoushoku/members/', views.editmembers, name='editmembers'),
    path('ensoushoku/concerts/', views.editconcerts, name='editconcerts')
]