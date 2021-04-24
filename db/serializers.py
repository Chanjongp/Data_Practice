from os import set_inheritable
from rest_framework import serializers
from db.models import Death, DrugExposure, Person, Concept, VisitOccurrence


class PersonSerializer(serializers.ModelSerializer):
    gender_concept_name = serializers.SerializerMethodField()
    race_concept_name = serializers.SerializerMethodField()
    ethnicity_concept_name = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = '__all__'

    def get_gender_concept_name(self, person):
        concept_name = Concept.objects.filter(
            concept_id=person.gender_concept_id).values_list('concept_name')
        name_tuple = concept_name[0]
        name_str = ''.join(name_tuple)
        return name_str

    def get_race_concept_name(self, person):
        concept_name = Concept.objects.filter(
            concept_id=person.race_concept_id).values_list('concept_name')
        name_tuple = concept_name[0]
        name_str = ''.join(name_tuple)
        return name_str

    def get_ethnicity_concept_name(self, person):
        if person.ethnicity_source_value == "hispanic":
            return "hispanic"
        if person.ethnicity_source_value == "nonhispanic":
            return "nonhispanic"


class VisitOccurrenceSerializer(serializers.ModelSerializer):
    visit_concept_name = serializers.SerializerMethodField()

    class Meta:
        model = VisitOccurrence
        fields = '__all__'

    def get_visit_concept_name(self, visit):
        concept_name = Concept.objects.filter(
            concept_id=visit.visit_concept_id).values_list('concept_name')
        name_tuple = concept_name[0]
        name_str = ''.join(name_tuple)
        return name_str


class ConditionOccurrenceSerializer(serializers.ModelSerializer):
    condition_concept_name = serializers.SerializerMethodField()

    class Meta:
        model = VisitOccurrence
        fields = '__all__'

    def get_condition_concept_name(slef, condition):
        concept_name = Concept.objects.filter(
            concept_id=condition.condition_concept_id).values_list('concept_name')
        name_tuple = concept_name[0]
        name_str = ''.join(name_tuple)
        return name_str


class DrugExposureSerializer(serializers.ModelSerializer):
    drug_concept_name = serializers.SerializerMethodField()

    class Meta:
        model = DrugExposure
        fields = '__all__'

    def get_drug_concept_name(self, drug):
        concept_name = Concept.objects.filter(
            concept_id=drug.drug_concept_id).values_list('concept_name')
        name_tuple = concept_name[0]
        name_str = ''.join(name_tuple)
        return name_str


class DeathSerializer(serializers.ModelSerializer):
    death_concept_name = serializers.SerializerMethodField()

    class Meta:
        model = Death
        fields = '__all__'

    def get_death_concept_name(self, death):
        concept_name = Concept.objects.filter(
            concept_id=death.death_type_concept_id).values_list('concept_name')
        name_tuple = concept_name[0]
        name_str = ''.join(name_tuple)
        return name_str


class ConceptIdInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = ['concept_id', 'concept_name', 'domain_id', 'vocabulary_id',
                  'concept_class_id', 'concept_code', 'valid_start_date', 'valid_end_date']
    # def
