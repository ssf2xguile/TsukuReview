from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'sender_name', 'sender_college','year', 'rating', 'grade', 'overall', 'difficulty', 'kadai', 'evaluation']
    
    # バリデーションエラーがある場合は、エラーを表示する
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) == 0 or len(title) > 30:
            raise forms.ValidationError('1文字以上30字以下で入力してください')
        return title
    
    def clean_overall(self):
        overall = self.cleaned_data['overall']
        if len(overall) == 0 or len(overall) > 500:
            raise forms.ValidationError('1文字以上500字以下で入力してください')
        return overall

    def clean_difficulty(self):
        difficulty = self.cleaned_data['difficulty']
        if len(difficulty) == 0 or len(difficulty) > 100:
            raise forms.ValidationError('1文字以上100字以下で入力してください')
        return difficulty

    def clean_kadai(self):
        kadai = self.cleaned_data['kadai']
        if len(kadai) == 0 or len(kadai) > 100:
            raise forms.ValidationError('1文字以上100字以下で入力してください')
        return kadai

    def clean_evaluation(self):
        evaluation = self.cleaned_data['evaluation']
        if len(evaluation) == 0 or len(evaluation) > 100:
            raise forms.ValidationError('1文字以上100字以下で入力してください')
        return evaluation