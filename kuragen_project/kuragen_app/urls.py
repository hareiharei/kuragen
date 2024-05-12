from django.urls import path
from . import views

app_name = 'kuragen_app'
urlpatterns = [
    path('schedule/', views.schedule, name='schedule'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('mypage/', views.MyPageView.as_view(), name='mypage'),
    path('ridenumbers/', views.RideNumbersView.as_view(), name='ridenumbers'),
    path('ensoushoku/', views.EnsoushokuView.as_view(), name='ensoushoku'),
    path('ensoushoku/myschedule/', views.EditMyScheduleView.as_view(), name='editmyschedule'),
    path('ensoushoku/schedule/', views.EditScheduleView.as_view(), name='editschedule'),
    path('ensoushoku/ridenumbers/', views.EditRideNumbersView.as_view(), name='editridenumbers'),
    path('ensoushoku/members/', views.EditMembersView.as_view(), name='editmembers'),
    path('ensoushoku/concerts/', views.EditConcertsView.as_view(), name='editconcerts')
]