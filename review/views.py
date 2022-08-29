from django.views.generic import TemplateView, DetailView

class IndexView(TemplateView):
    template_name = 'review/index.html'

class LectureView(TemplateView):
    template_name = 'review/lecture.html'