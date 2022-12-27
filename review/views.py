from django.contrib import messages
from django.shortcuts import render
from django.views.generic.edit import FormMixin
from django.views.generic import TemplateView, CreateView, ListView, DetailView, FormView
from django.urls import reverse, reverse_lazy
from .models import Subject, Review
from .forms import ReviewForm, ContactForm
import math


class IndexView(TemplateView):
    template_name = 'review/index.html'

class TermsView(TemplateView):
    template_name = 'review/terms.html'

class PrivacyView(TemplateView):
    template_name = 'review/privacy.html'

class ContactsView(FormView):
    template_name = 'review/contacts.html'
    form_class = ContactForm

    def form_valid(self, form):
        return render(self.request, 'review/contacts.html', {'form': form})

class ContactsConfirmView(FormView):
    form_class = ContactForm

    def form_valid(self, form):
        return render(self.request, 'review/contacts_confirm.html', {'form': form})

    def form_invalid(self, form):
        return render(self.request, 'review/contacts.html', {'form': form})


class ContactCreateView(CreateView):
    form_class = ContactForm
    success_url = reverse_lazy('contacts_complete')

    def form_invalid(self, form):
        """基本的にはここに飛んでこないはずです。UserDataConfrimでバリデーションは済んでるため"""
        return render(self.request, 'review/contacts.html', {'form': form})


class ContactsCompleteView(TemplateView):
    template_name = 'review/contacts_complete.html'


class SearchView(ListView):
    model = Review
    template_name = 'review/search.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_list'] = self.model.objects.all().order_by('-created_at')[:5]
        return context

class NewReviewsView(ListView):
    model = Review
    template_name = 'review/new_reviews.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_list'] = self.model.objects.all().order_by('-created_at')[:30]
        return context

class LectureView(FormMixin, DetailView):
    model = Subject
    form_class = ReviewForm
    template_name = 'review/lecture.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.kwargs['pk']でurl中の変数pkを取得できる
        subject_data = Subject.objects.get(pk=self.kwargs['pk'])
        context['subject_data'] = subject_data
        context['review_datas'] = Review.objects.filter(lecture=self.kwargs['pk']).order_by('-created_at')
        context['rate_data1'] = DataRatingCalculation1(subject_data)
        context['rate_data2'] = DataRatingCalculation2(subject_data)
        context['review_count'] = CountCaluculation(subject_data)
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
        data['sender_name'] = self.request.user.username
        data['sender_college'] = self.request.user.college
        obj = Review(**data)
        obj.save()
        messages.success(self.request, 'この度はレビューしていただきありがとうございます。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'フォームの内容が不適切です。もう一度内容をご確認ください。')
        return super().form_invalid(form)


def DataRatingCalculation1(obj):
    """
    レビューの評価を計算する関数。入力はSubjectモデルのインスタンス。出力は小数点第一位までの評価。詳しくはstyle.cssを参照。
    """
    rate_dict = {1:0, 2:0, 3:0, 4:0, 5:0} # レビューの評価を格納する辞書 例) {1: 2, 2: 0, 3: 1, 4: 2, 5: 0}
    objs = obj.related_reviews.all()
    for obj in objs:
        rate_dict[obj.rating] += 1
    result = (rate_dict[1] + rate_dict[2] * 2 + rate_dict[3] * 3 + rate_dict[4] * 4 + rate_dict[5] * 5) / (rate_dict[1] + rate_dict[2] + rate_dict[3] + rate_dict[4] + rate_dict[5])
    result_round1 = round(result*100)/50
    result_floor = math.floor(result_round1)
    result_final = (result_floor*5)/10
    return result_final

def DataRatingCalculation2(obj):
    """
    レビューの評価を計算する関数。入力はSubjectモデルのインスタンス。出力は小数点第二位までの評価。
    """
    rate_dict = {1:0, 2:0, 3:0, 4:0, 5:0} # レビューの評価を格納する辞書 例) {1: 2, 2: 0, 3: 1, 4: 2, 5: 0}
    objs = obj.related_reviews.all()
    for obj in objs:
        rate_dict[obj.rating] += 1
    result = (rate_dict[1] + rate_dict[2] * 2 + rate_dict[3] * 3 + rate_dict[4] * 4 + rate_dict[5] * 5) / (rate_dict[1] + rate_dict[2] + rate_dict[3] + rate_dict[4] + rate_dict[5])
    result_round2 = round(result*100)/100
    return result_round2

def CountCaluculation(obj):
    """
    レビューの件数を計算する関数。入力はSubjectモデルのインスタンス。出力はレビューの件数。
    """
    count = obj.related_reviews.all().count()
    return count