from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from review.models import Subject

class IndexView(TemplateView):
    template_name = 'review/index.html'

class LectureView(DetailView):
    model = Subject
    # context_object_nameはテンプレートで表示する際のモデルの参照名。
    context_object_name = 'subject_data'
    http_method_names = ['get', 'post']
    template_name = 'review/lecture.html'

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['overall'] = request.POST['overall']
        context['difficulty'] = request.POST['difficulty']
        context['kadai'] = request.POST['kadai']
        context['evaluation'] = request.POST['evaluation']
        return render(request, 'review/lecture.html', context=context) 