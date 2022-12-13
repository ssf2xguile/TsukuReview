from django import forms
from .models import Review, Contact

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'year', 'rating', 'grade', 'overall', 'difficulty', 'kadai', 'evaluation']
    
    # バリデーションエラーがある場合は、エラーを表示する
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 2:
            raise forms.ValidationError('タイトルが短すぎます')
        return title
    
    def clean_overall(self):
        overall = self.cleaned_data['overall']
        if len(overall) < 3:
            raise forms.ValidationError('総評が短すぎます')
        return overall

    def clean_difficulty(self):
        difficulty = self.cleaned_data['difficulty']
        if len(difficulty) < 3:
            raise forms.ValidationError('課題の難易度についての言及が短すぎます')
        return difficulty

    def clean_kadai(self):
        kadai = self.cleaned_data['kadai']
        if len(kadai) < 3:
            raise forms.ValidationError('課題や試験についての言及が短すぎます')
        return kadai

    def clean_evaluation(self):
        evaluation = self.cleaned_data['evaluation']
        if len(evaluation) < 2:
            raise forms.ValidationError('課題の評価についての言及が短すぎます')
        return evaluation

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs["class"] = "form-control"
        super().__init__(*args, **kwargs)

    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) < 10:
            raise forms.ValidationError('お問い合わせ内容が短すぎます')
        return message