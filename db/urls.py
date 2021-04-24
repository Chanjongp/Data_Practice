from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('person/total/', views.GetTotalPersonSum.as_view(), name='person_total'),
    path('person/gender/', views.GetEachGenderPerson.as_view(), name='person_gender'),
    path('person/race/', views.GetEachRacePerson.as_view(), name='person_race'),
    path('person/ethnic/', views.GetEachEthnicPerson.as_view(), name='person_ehnic'),
    path('person/death/', views.GetDeathPerson.as_view(), name='person_death'),
    path('visit/type/', views.GetTypeVisitOccurrence.as_view(), name='visit_type'),
    path('visit/gender/', views.GetGenderVisitOccurrence.as_view(),
         name='visit_gender'),
    path('visit/race/', views.GetRaceVisitOccurrence.as_view(), name='visit_race'),
    path('visit/ethnic/', views.GetEthnicVisitOccurrence.as_view(),
         name='visit_ethnic'),
    path('visit/age/', views.GetAgeVisitOccurrence.as_view(), name='visit_age'),
    path('conceptinfo/', views.GetConecptIdInformation.as_view(), name='concept_info'),

    path('personinfo/', views.GetPersonRowInformation.as_view(), name='person_info'),
    path('visitinfo/', views.GetVisitRowInformation.as_view(), name='visit_info'),
    path('conditioninfo/', views.GetConditionRowInformation.as_view(),
         name='condition_info'),
    path('druginfo/', views.GetDrugRowInformation.as_view(), name='drug_info'),
    path('deathinfo/', views.GetDeathRowInformation.as_view(), name='death_info'),
]
