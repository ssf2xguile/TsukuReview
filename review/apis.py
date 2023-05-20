from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import Subject
from django.db.models import Q

class SearchSubjectAPI(ListAPIView):
    serializer_class = SearchSubjectSerializer

    # クエリに対し、科目名・教員名検索なら大文字小文字区別なしのLIKE検索、科目番号なら前方一致検索を行う
    def get_queryset(self):
        q :str = self.request.query_params.get("q", "")
        return Subject.objects.filter(Q(name__icontains = q)|Q(code__startswith = q)|Q(teachers__icontains = q)).order_by('code')[:200]

class GetSubjectAPI(ListAPIView):
    serializer_class = GetSubjectSerializer

    # 科目番号で前方一致検索を行う
    def get_queryset(self):
        q :str = self.request.query_params.get("q", "")
        return Subject.objects.filter(Q(code__startswith = q)).order_by('code')[:1]

class CreateReviewAPI(APIView):

    def post(self, request):
        serializer = ValidateReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)