from rest_framework.generics import ListAPIView
from .serializers import *
from .models import Subject
from django.db.models import Q

class SearchSubjectAPI(ListAPIView):
    serializer_class = SearchSubjectSerializer

    # クエリに対し、科目名・教員名検索なら大文字小文字区別なしのLIKE検索、科目番号なら前方一致検索を行う
    def get_queryset(self):
        q :str = self.request.query_params.get("q", "")
        return Subject.objects.filter(Q(name__icontains = q)|Q(code__startswith = q)|Q(teachers__icontains = q)).order_by('code')[:200]
