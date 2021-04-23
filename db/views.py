import json
from django.shortcuts import render
from rest_framework import viewsets, mixins, generics, views
from db.models import Person, VisitOccurrence
from .serializers import PracticeSerializer
from django.db.models import Count, Q
from django.http import JsonResponse


class PracticeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Person.objects.all()
    serializer_class = PracticeSerializer


class GetTotalPersonSum(generics.ListAPIView):
    # queryset = Person.objects.all()
    def get(self, request, *args, **kwargs):
        data = Person.objects.aggregate(Count('person_id'))
        return JsonResponse(data)


class GetEachGenderPerson(generics.ListAPIView):
    """
    8532 : F
    8507 : M
    """

    def get(self, request, *args, **kwargs):
        male = Person.objects.filter(gender_concept_id='8532').count()
        female = Person.objects.filter(gender_concept_id='8507').count()
        return JsonResponse({'male': male, 'female': female})


class GetEachRacePerson(generics.ListAPIView):
    """
    8527 : white
    8515 : asian
    8516 : black
    0 : native
    0 : other
    """

    def get(self, request, *args, **kwargs):
        white = Person.objects.filter(
            race_concept_id__in=['8527']).count()
        asian = Person.objects.filter(
            race_concept_id__in=['8515']).count()
        black = Person.objects.filter(
            race_concept_id__in=['8516']).count()
        native = Person.objects.filter(
            Q(race_concept_id__in=['0']) & Q(race_source_value='native')).count()
        other = Person.objects.filter(
            Q(race_concept_id__in=['0']) & Q(race_source_value='other')).count()
        data = {'white': white, 'asian': asian,
                'black': black, 'native': native, 'other': other}
        return JsonResponse(data)


class GetEachEthnicPerson(generics.ListAPIView):
    """
    0 : hispanic
    0 : nonhispanic
    """

    def get(self, request, *args, **kwargs):
        hispanic = Person.objects.filter(
            Q(ethnicity_concept_id__in=['0']) & Q(
                ethnicity_source_value='hispanic')).count()
        nonhispanic = Person.objects.filter(
            Q(ethnicity_concept_id__in=['0']) & Q(
                ethnicity_source_value='nonhispanic')).count()
        data = {'hispanic': hispanic, 'nonhispanic': nonhispanic}
        return JsonResponse(data)


class GetDeathPerson(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        data = Person.objects.extra(tables=['death'], where=[
            'person.person_id=death.person_id']).count()
        return JsonResponse({'death': data})


class GetTypeVisitOccurrence(generics.ListAPIView):
    """
    9201 : Inpatient Visit (입원)
    9202 : Outpatient Visit (외래)
    9203 : Emergency Room Visit (응급)
    """

    def get(self, request, *args, **kwargs):
        in_visit = VisitOccurrence.objects.filter(
            visit_concept_id__in=['9201']).count()
        out_visit = VisitOccurrence.objects.filter(
            visit_concept_id__in=['9202']).count()
        emg_visit = VisitOccurrence.objects.filter(
            visit_concept_id__in=['9203']).count()
        # data =
        return JsonResponse(data, safe=False)
