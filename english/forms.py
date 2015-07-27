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

# class UnknownForm(forms.Form):
#     choices = forms.ModelMultipleChoiceField(
#         choices = queryset_of_valid_choices, # not optional, use .all() if unsure
#         widget  = forms.CheckboxSelectMultiple,
#     )

# if request.method == 'POST':
#     form = UnknownForm(request.POST):
#     if 'delete' in request.POST:
#         for item in form.cleaned_data['choices']:
#             item.delete()
#     if 'mark_read' in request.POST:
#         for item in form.cleaned_data['choices']:
#             item.read = True; 
#             item.save()




class correctionform(forms.ModelForm):
    class Meta:
        model = item
        fields = ['correct_choice']

class approvalform(forms.ModelForm):
    class Meta:
        model = correction
        fields = ['approved']