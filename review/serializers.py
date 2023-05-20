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

class ValidateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('title', 'overall', 'difficulty', 'kadai', 'evaluation')

    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("タイトルが短すぎます")
        return value
    
    def validate_overall(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("総評が短すぎます")
        return value
    
    def validate_difficulty(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("課題の難易度についての言及が短すぎます")
        return value

    def validate_kadai(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("課題や試験についての言及が短すぎます")
        return value
    
    def validate_evaluation(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("課題の評価についての言及が短すぎます")
        return value