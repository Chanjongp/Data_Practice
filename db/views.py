import json
from django.db.models.fields import DateField
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
        data = {'Inpatient_Visit': in_visit,
                'OutPatient_Visit': out_visit, 'Emergency_Room_Visit': emg_visit}
        return JsonResponse(data)


class GetGenderVisitOccurrence(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        basic = VisitOccurrence.objects.extra(tables=['person'], where=[
            'visit_occurrence.person_id=person.person_id'])
        female_visit = basic.extra(
            where=['person.gender_concept_id=8532']).count()
        male_visit = basic.extra(
            where=['person.gender_concept_id=8507']).count()

        data = {'female_visit': female_visit, 'male_visit': male_visit}
        return JsonResponse(data)


class GetRaceVisitOccurrence(generics.ListAPIView):
    """
    8527 : white
    8515 : asian
    8516 : black
    0 : native
    0 : other
    """

    def get(self, request, *args, **kwargs):
        basic = VisitOccurrence.objects.extra(tables=['person'], where=[
            "visit_occurrence.person_id=person.person_id"])
        white_visit = basic.extra(
            where=["person.race_concept_id=8527"]).count()
        asian_visit = basic.extra(
            where=["person.race_concept_id=8515"]).count()
        black_visit = basic.extra(
            where=["person.race_concept_id=8516"]).count()
        native_visit = basic.extra(
            where=["person.race_concept_id=0", "person.race_source_value='native'"]).count()
        other_visit = basic.extra(
            where=["person.race_concept_id=0", "person.race_source_value='other'"]).count()
        data = {"white_visit": white_visit, "asian_visit": asian_visit,
                "black_visit": black_visit, "native_visit": native_visit, "other_visit": other_visit}
        return JsonResponse(data)


class GetEthnicVisitOccurrence(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        basic = VisitOccurrence.objects.extra(tables=['person'], where=[
            "visit_occurrence.person_id=person.person_id"])
        his_visit = basic.extra(where=[
                                "person.ethnicity_concept_id=0", "person.ethnicity_source_value='hispanic'"]).count()
        nonhis_visit = basic.extra(
            where=["person.ethnicity_concept_id=0", "person.ethnicity_source_value='nonhispanic'"]).count()
        data = {'hispanic_visit': his_visit, 'nonhispanic_visit': nonhis_visit}
        return JsonResponse(data)


class GetAgeVisitOccurrence(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        basic = VisitOccurrence.objects.extra(tables=['person'], where=[
            "visit_occurrence.person_id=person.person_id"])
        visit_0_to_10 = basic.extra(
            where=["visit_occurrence.visit_start_datetime - person.birth_datetime <= '10 YEAR'"]).count()
        visit_11_to_20 = basic.extra(where=["visit_occurrence.visit_start_datetime - person.birth_datetime > '10 YEAR'",
                                     "visit_occurrence.visit_start_datetime - person.birth_datetime <= '20 YEAR'"]).count()
        visit_21_to_30 = basic.extra(where=["visit_occurrence.visit_start_datetime - person.birth_datetime > '20 YEAR'",
                                     "visit_occurrence.visit_start_datetime - person.birth_datetime <= '30 YEAR'"]).count()
        visit_31_to_40 = basic.extra(where=["visit_occurrence.visit_start_datetime - person.birth_datetime > '30 YEAR'",
                                     "visit_occurrence.visit_start_datetime - person.birth_datetime <= '40 YEAR'"]).count()
        visit_41_to_50 = basic.extra(where=["visit_occurrence.visit_start_datetime - person.birth_datetime > '40 YEAR'",
                                     "visit_occurrence.visit_start_datetime - person.birth_datetime <= '50 YEAR'"]).count()
        visit_51_to_60 = basic.extra(where=["visit_occurrence.visit_start_datetime - person.birth_datetime > '50 YEAR'",
                                     "visit_occurrence.visit_start_datetime - person.birth_datetime <= '60 YEAR'"]).count()
        visit_61_to_70 = basic.extra(where=["visit_occurrence.visit_start_datetime - person.birth_datetime > '60 YEAR'",
                                     "visit_occurrence.visit_start_datetime - person.birth_datetime <= '70 YEAR'"]).count()
        visit_71_to_80 = basic.extra(where=["visit_occurrence.visit_start_datetime - person.birth_datetime > '70 YEAR'",
                                     "visit_occurrence.visit_start_datetime - person.birth_datetime <= '80 YEAR'"]).count()
        visit_81_to_90 = basic.extra(where=["visit_occurrence.visit_start_datetime - person.birth_datetime > '80 YEAR'",
                                     "visit_occurrence.visit_start_datetime - person.birth_datetime <= '90 YEAR'"]).count()
        visit_91_to_100 = basic.extra(where=["visit_occurrence.visit_start_datetime - person.birth_datetime > '90 YEAR'",
                                             "visit_occurrence.visit_start_datetime - person.birth_datetime <= '100 YEAR'"]).count()
        visit_101_to_110 = basic.extra(where=["visit_occurrence.visit_start_datetime - person.birth_datetime > '100 YEAR'",
                                              "visit_occurrence.visit_start_datetime - person.birth_datetime <= '110 YEAR'"]).count()
        visit_111_to_120 = basic.extra(where=["visit_occurrence.visit_start_datetime - person.birth_datetime > '110 YEAR'",
                                              "visit_occurrence.visit_start_datetime - person.birth_datetime <= '120 YEAR'"]).count()
        data = {'visit_0_to_10': visit_0_to_10, 'visit_11_to_20': visit_11_to_20,
                'visit_21_to_30': visit_21_to_30, 'visit_31_to_40': visit_31_to_40,
                'visit_41_to_50': visit_41_to_50, 'visit_51_to_60': visit_51_to_60, 'visit_61_to_70': visit_61_to_70, 'visit_71_to_80': visit_71_to_80, 'visit_81_to_90': visit_81_to_90, 'visit_91_to_100': visit_91_to_100,
                'visit_101_to_110': visit_101_to_110, 'visit_111_to_120': visit_111_to_120
                }
        # print(visit_0_to_10 + visit_11_to_20 + visit_21_to_30 + visit_31_to_40 + visit_41_to_50 + visit_51_to_60 +
        #       visit_61_to_70 + visit_71_to_80 + visit_81_to_90 + visit_91_to_100 + visit_101_to_110 + visit_111_to_120)
        return JsonResponse(data)
