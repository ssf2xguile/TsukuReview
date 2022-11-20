from django.contrib import messages
from django.shortcuts import render
from django.views.generic.edit import FormMixin
from django.views.generic import TemplateView, CreateView, ListView, DetailView, FormView
from django.urls import reverse, reverse_lazy
from .models import Subject, Review
from .forms import ReviewForm, ContactForm


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

class ContactsCompleteView(CreateView):
    form_class = ContactForm
    success_url = reverse_lazy('contacts_complete')

    def form_invalid(self, form):
        """基本的にはここに飛んでこないはずです。UserDataConfrimでバリデーションは済んでるため"""
        return render(self.request, 'review/contacts_complete.html', {'form': form})

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
        # レビューの件数を取得
        # context['review_count'] = subject_data.star1 + subject_data.star2 + subject_data.star3 + subject_data.star4 + subject_data.star5
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
        subject_data = Subject.objects.get(pk=self.kwargs['pk'])
        data = form.cleaned_data
        data['lecture'] = Subject.objects.get(pk=self.kwargs['pk'])
        data['sender_name'] = self.request.user.username
        data['sender_college'] = self.request.user.college
        obj = Review(**data)
        obj.save()
        if data['rating'] == 1:
            Subject.objects.filter(pk=self.kwargs['pk']).update(star1=subject_data.star1+1)
        elif data['rating'] == 2:
            Subject.objects.filter(pk=self.kwargs['pk']).update(star2=subject_data.star2+1)
        elif data['rating'] == 3:
            Subject.objects.filter(pk=self.kwargs['pk']).update(star3=subject_data.star3+1)
        elif data['rating'] == 4:
            Subject.objects.filter(pk=self.kwargs['pk']).update(star4=subject_data.star4+1)
        elif data['rating'] == 5:
            Subject.objects.filter(pk=self.kwargs['pk']).update(star5=subject_data.star5+1)
        messages.success(self.request, 'この度はレビューしていただきありがとうございます。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'フォームの内容が不適切です。もう一度内容をご確認ください。')
        return super().form_invalid(form)