from rest_framework import serializers
from db.models import Person, Concept


class PracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        # fields = ['person_id', ]
        fields = '__all__'


class ConceptIdInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = ['concept_id', 'concept_name', 'domain_id', 'vocabulary_id',
                  'concept_class_id', 'concept_code', 'valid_start_date', 'valid_end_date']
    # def
