from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('person/total/', views.GetTotalPersonSum.as_view(), name='person_total'),
    path('person/gender/', views.GetEachGenderPerson.as_view(), name='person_gender'),
    path('person/race/', views.GetEachRacePerson.as_view(), name='person_race'),
    path('person/ethnic', views.GetEachEthnicPerson.as_view(), name='person_ehnic'),
    path('person/death', views.GetDeathPerson.as_view(), name='person_death'),
    path('visit/type', views.GetTypeVisitOccurrence.as_view(), name='visit_type'),
]
