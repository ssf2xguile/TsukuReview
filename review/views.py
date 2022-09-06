from django.contrib import messages
from django.shortcuts import render
from django.views.generic.edit import FormMixin
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.urls import reverse
from .models import Subject, Review
from .forms import ReviewForm


class IndexView(TemplateView):
    template_name = 'review/index.html'

class LectureView(FormMixin, DetailView):
    model = Subject
    form_class = ReviewForm
    template_name = 'review/lecture.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.kwargs['pk']でurl中の変数pkを取得できる
        subject_data = Subject.objects.get(pk=self.kwargs['pk'])
        context['subject_data'] = subject_data
        context['review_datas'] = Review.objects.filter(lecture=self.kwargs['pk']).order_by('created_at')
        # レビューの件数を取得
        context['review_count'] = subject_data.star1 + subject_data.star2 + subject_data.star3 + subject_data.star4 + subject_data.star5
        context['form'] = ReviewForm()
        return context

    def get_success_url(self):
        return reverse('lecture', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        # Detailview限定のget_object()を使う
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        #1 cleaned_dataでバリデートしたformの値を取得できる
        #2 lectureにインスタンスを渡す
        #3 オブジェクトを作成し、値を代入する(今回は辞書ごと)
        #4 オブジェクトを保存する
        data = form.cleaned_data
        data['lecture'] = Subject.objects.get(pk=self.kwargs['pk'])
        obj = Review(**data)
        obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '入力内容をご確認ください。')
        return super().form_invalid(form)