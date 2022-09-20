from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'sender_name', 'sender_college','year', 'rating', 'grade', 'overall', 'difficulty', 'kadai', 'evaluation']
    
    # バリデーションエラーがある場合は、エラーを表示する
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 3:
            raise forms.ValidationError('タイトルが短すぎます')
        return title
    
    def clean_overall(self):
        overall = self.cleaned_data['overall']
        if len(overall) < 10:
            raise forms.ValidationError('総評が短すぎます')
        return overall

    def clean_difficulty(self):
        difficulty = self.cleaned_data['difficulty']
        if len(difficulty) < 10:
            raise forms.ValidationError('課題の難易度についての言及が短すぎます')
        return difficulty

    def clean_kadai(self):
        kadai = self.cleaned_data['kadai']
        if len(kadai) < 10:
            raise forms.ValidationError('課題や試験についての言及が短すぎます')
        return kadai

    def clean_evaluation(self):
        evaluation = self.cleaned_data['evaluation']
        if len(evaluation) < 5:
            raise forms.ValidationError('課題の評価についての言及が短すぎます')
        return evaluation