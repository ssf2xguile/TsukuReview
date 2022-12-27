from rest_framework import serializers
from .models import Subject, Review
from .views import DataRatingCalculation1, DataRatingCalculation2, CountCaluculation

class SearchSubjectSerializer(serializers.ModelSerializer):
    rating_datas = serializers.SerializerMethodField()
    class Meta:
        model = Subject
        fields = ('name', 'code', 'unit', 'semester', 'grade', 'teachers', 'schools', 'rating_datas')
    
    def get_rating_datas(self, obj):
        context = {}
        context['rating_data1'] = DataRatingCalculation1(obj)
        context['rating_data2'] = DataRatingCalculation2(obj)
        context['rating_count'] = CountCaluculation(obj)
        return context


class GetSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
 