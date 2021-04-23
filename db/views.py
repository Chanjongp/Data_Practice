from django.shortcuts import render
from rest_framework import viewsets, mixins, generics, views
from db.models import Person
from .serializers import PracticeSerializer
from django.db.models import Count, Q
from django.http import JsonResponse


class PracticeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Person.objects.all()
    serializer_class = PracticeSerializer


class GetTotalPersonSum(generics.ListAPIView):
    # queryset = Person.objects.all()
    def get(self, request, *args, **kwargs):
        sum = Person.objects.aggregate(Count('person_id'))
        return JsonResponse(sum)


class GetEachGenderPerson(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        male = Person.objects.filter(gender_concept_id='8532').count()
        female = Person.objects.filter(gender_concept_id='8507').count()
        return JsonResponse({'male': male, 'female': female})
# 8532 : F
# 8507 : M


class GetEachRacePerson(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        white = Person.objects.filter(
            race_concept_id__in=['8527']).count()
        asian = Person.objects.filter(
            race_concept_id__in=['8515']).count()
        black = Person.objects.filter(
            race_concept_id__in=['8516']).count()
        native = Person.objects.filter(
            race_concept_id__in=['0']).count()
        data = {'white': white, 'asian': asian,
                'black': black, 'native': native}
        return JsonResponse(data)
# 8527 : white
# 8515 : asian
# 8516 : black
# 0 : native
