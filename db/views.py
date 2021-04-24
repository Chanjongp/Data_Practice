import json
from rest_framework import generics
from db.models import Death, DrugExposure, Person, VisitOccurrence, Concept, ConditionOccurrence
from .serializers import ConceptIdInfoSerializer, ConditionOccurrenceSerializer, DeathSerializer, DrugExposureSerializer, PersonSerializer, VisitOccurrenceSerializer
from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework import status
from .pagination import CustomPagination


class GetTotalPersonSum(generics.ListAPIView):
    # queryset = Person.objects.all()
    def get(self, request, *args, **kwargs):
        data = Person.objects.aggregate(Count('person_id'))
        return Response(data)


class GetEachGenderPerson(generics.ListAPIView):
    """
    8532 : F
    8507 : M
    """

    def get(self, request, *args, **kwargs):
        male = Person.objects.filter(gender_concept_id='8532').count()
        female = Person.objects.filter(gender_concept_id='8507').count()
        return Response({'male': male, 'female': female})


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
        return Response(data)


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
        return Response(data)


class GetDeathPerson(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        data = Person.objects.extra(tables=['death'], where=[
            'person.person_id=death.person_id']).count()
        return Response({'death': data})


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
        return Response(data)


class GetGenderVisitOccurrence(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        basic = VisitOccurrence.objects.extra(tables=['person'], where=[
            'visit_occurrence.person_id=person.person_id'])
        female_visit = basic.extra(
            where=['person.gender_concept_id=8532']).count()
        male_visit = basic.extra(
            where=['person.gender_concept_id=8507']).count()

        data = {'female_visit': female_visit, 'male_visit': male_visit}
        return Response(data)


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
        return Response(data)


class GetEthnicVisitOccurrence(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        basic = VisitOccurrence.objects.extra(tables=['person'], where=[
            "visit_occurrence.person_id=person.person_id"])
        his_visit = basic.extra(where=[
                                "person.ethnicity_concept_id=0", "person.ethnicity_source_value='hispanic'"]).count()
        nonhis_visit = basic.extra(
            where=["person.ethnicity_concept_id=0", "person.ethnicity_source_value='nonhispanic'"]).count()
        data = {'hispanic_visit': his_visit, 'nonhispanic_visit': nonhis_visit}
        return Response(data)


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
        return Response(data)


class GetConecptIdInformation(generics.ListAPIView):
    serializer_class = ConceptIdInfoSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        1. domain_id, concept_name이 모두 request에 있을 때
        2. domain만 request에 있을 때
        3. concept_name만 request에 있을 때
        4. 둘다 없으면 전체 값 Response
        """
        req_json = json.loads(self.request.body)
        if "domain_id" in req_json and "concept_name" in req_json:
            domain_id = req_json['domain_id']
            concept_name = req_json['concept_name']
            return Concept.objects.filter(domain_id=domain_id, concept_name__contains=concept_name)
        elif "domain_id" in req_json:
            domain_id = req_json['domain_id']
            return Concept.objects.filter(domain_id=domain_id)
        elif "concept_name" in req_json:
            concept_name = req_json['concept_name']
            return Concept.objects.filter(concept_name__contains=concept_name)
        return Concept.objects.all()


class GetPersonRowInformation(generics.ListAPIView):
    """
    gender
    8532 : F
    8507 : M
    race
    8527 : white
    8515 : asian
    8516 : black
    0 : native
    0 : other

    0 : hispanic
    0 : nonhispanic
    """
    queryset = Person.objects.all()
    pagination_class = CustomPagination
    serializer_class = PersonSerializer

    def get_queryset(self):
        # req_json = json.loads(self.request.body)
        # if "column_name" in req_json:
        #     column_name = req_json['column_name']
        #     check_field = VisitOccurrence.field_exists(column_name)
        #     if check_field:
        #         return VisitOccurrence.objects.only(column_name)
        return VisitOccurrence.objects.all()


class GetVisitRowInformation(generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = VisitOccurrenceSerializer

    def get_queryset(self):
        # req_json = json.loads(self.request.body)
        # if "column_name" in req_json:
        #     column_name = req_json['column_name']
        #     check_field = VisitOccurrence.field_exists(column_name)
        #     if check_field:
        #         return VisitOccurrence.objects.only('person_id')
        return VisitOccurrence.objects.all()


class GetConditionRowInformation(generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = ConditionOccurrenceSerializer

    def get_queryset(self):
        # req_json = json.loads(self.request.body)
        # if "column_name" in req_json:
        #     column_name = req_json['column_name']
        #     check_field = VisitOccurrence.field_exists(column_name)
        #     if check_field:
        #         return VisitOccurrence.objects.only(column_name)
        return VisitOccurrence.objects.all()


class GetDrugRowInformation(generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = DrugExposureSerializer

    def get_queryset(self):
        # req_json = json.loads(self.request.body)
        # if "column_name" in req_json:
        #     column_name = req_json['column_name']
        #     check_field = VisitOccurrence.field_exists(column_name)
        #     if check_field:
        #         return VisitOccurrence.objects.only(column_name)
        return VisitOccurrence.objects.all()


class GetDeathRowInformation(generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = DeathSerializer

    def get_queryset(self):
        # req_json = json.loads(self.request.body)
        # if "column_name" in req_json:
        #     column_name = req_json['column_name']
        #     check_field = VisitOccurrence.field_exists(column_name)
        #     if check_field:
        #         return VisitOccurrence.objects.only(column_name)
        return VisitOccurrence.objects.all()
