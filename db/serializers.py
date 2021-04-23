from rest_framework import serializers
from db.models import Person


class PracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        # fields = ['person_id', ]
        fields = '__all__'
