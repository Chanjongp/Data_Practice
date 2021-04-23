from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('person/total/', views.GetTotalPersonSum.as_view(), name='total'),
    path('person/gender/', views.GetEachGenderPerson.as_view(), name='gender'),
    path('person/race/', views.GetEachRacePerson.as_view(), name='race'),
]
