from rest_framework import serializers
from .models import Subject, Review

class SearchSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('name', 'code', 'unit', 'semester', 'grade', 'teachers', 'schools', 'colleges', 'star1', 'star2', 'star3', 'star4', 'star5')

class GetSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
 