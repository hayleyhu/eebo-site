from django.contrib.auth.models import User
from django import forms
from english.models import word, item, correction

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class newwordform(forms.ModelForm):
    class Meta:
        model = word
        fields = ['theword', 'index', 'category']

class lookupform(forms.ModelForm):
    class Meta:
        model = word
        fields = ['theword']

class findentryform(forms.ModelForm):
    class Meta:
        model = item
        fields = ['file_position', 'kwicl', 'keyword', 'kwicr', 'choice1', 'choice2', 'choice3', 'correct_choice']


class correctionform(forms.ModelForm):
    class Meta:
        model = correction
        fields = ['corrected_word', 'correction_made', 'correction_word']

class approvalform(forms.ModelForm):
    class Meta:
        model = correction
        fields = ['approved']