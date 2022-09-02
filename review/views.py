from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

class IndexView(TemplateView):
    template_name = 'review/index.html'

class LectureView(TemplateView):
    http_method_names = ['get', 'post']
    template_name = 'review/lecture.html'

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['overall'] = request.POST['overall']
        context['difficulty'] = request.POST['difficulty']
        context['kadai'] = request.POST['kadai']
        context['evaluation'] = request.POST['evaluation']
        return render(request, 'review/lecture.html', context=context) 