from django.shortcuts import render
from django.http import HttpResponse
from english.models import word, item
from django import forms
from django.http import HttpResponseRedirect
from django.db.models import Q
from operator import __or__ as OR
from django.template import loader, Context


def home(request):
    s = "hello world"
    return HttpResponse(s)

def detail(request, pk):
    cat = word.objects.get(pk=int(pk))
    return render(request, "detail.html", {'cat': cat})




class newwordform(forms.ModelForm):
    class Meta:
        model = word
        fields = ['theword', 'index', 'category']


def create(request):
    if request.method == 'POST':
        form = newwordform(request.POST)
        if form.is_valid():
            newword = form.save()
            return HttpResponseRedirect('/entry/' + str(newword.pk))
    form = newwordform()
    return render(request, 'create_word.html', {'form':form})

class lookupform(forms.ModelForm):
    class Meta:
        model = word
        fields = ['theword']



def search_for_keywords(keyword):
    posts = word.objects.all()
    post = posts.filter(theword=keyword)
    return posts



def lookup(request):
    if request.method == 'GET':
        form = lookupform(request.GET)
        if form.is_valid():
            query = form.cleaned_data
            field = query['theword']
            if word.objects.filter(theword=field).exists():
                newword = word.objects.get(theword=field)
                return HttpResponseRedirect('/entry/' + str(newword.index))
            return HttpResponse('word does not exist in database')
    return render(request, 'lookup.html', {'form': form})

class findentryform(forms.ModelForm):
    class Meta:
        model = item
        fields = ['file_position', 'kwicl', 'keyword', 'kwicr', 'choice1', 'choice2', 'choice3', 'correct_choice']


def wordinfo(request, pk):
    cat = item.objects.get(pk=int(pk))
    return render(request, "wordinfo.html", {'cat': cat})


def findentry(request):

    if request.method == 'GET':

        form = findentryform(request.GET)
        if form.is_valid():
            query = form.cleaned_data
        page = None
        word_list = None
        qobj = []
        search = 0
        file_position_search = query['file_position']
        kwicl_search = query.__getitem__('kwicl')
        keyword_search = query.__getitem__('keyword')
        kwicr_search = query.__getitem__('kwicr')
        choice1_search = query.__getitem__('choice1')
        choice2_search = query.__getitem__('choice2')
        choice3_search = query.__getitem__('choice3')
        correct_choice_search = query.__getitem__('correct_choice')
        if file_position_search:
            qobj.append(Q(file_position__contains=file_position_search))
            search = 100
        if kwicl_search:
            qobj.append(Q(kwicl__contains=kwicl_search))
            search = 1
        if keyword_search:
            qobj.append(Q(keyword__contains=keyword_search))
            search = 1
        if kwicr_search:
            qobj.append(Q(kwicr__contains=kwicr_search))
            search = 1
        if choice1_search:
            qobj.append(Q(choice1__contains=choice1_search))
            search = 1
        if choice2_search:
            qobj.append(Q(choice2__contains=choice2_search))
            search = 1
        if choice3_search:
            qobj.append(Q(choice3__contains=choice3_search))
            search = 1
        if correct_choice_search:
            qobj.append(Q(correct_choice__contains=correct_choice_search))
            search = 1
        if qobj:
            word_list = item.objects.filter(reduce(OR, qobj))

        if search > 0:
            c = Context({'word_list': word_list}, {'form': form})
            t = loader.get_template("findentry.html")
            return HttpResponse(t.render(c))


    return render(request, 'findentry.html', {'form': form})


