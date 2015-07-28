from django.shortcuts import render
from django.http import HttpResponse
from english.models import word, item, correction
from django import forms
from django.http import HttpResponseRedirect
from django.db.models import Q
from operator import __or__ as OR
from django.template import loader, Context
from django.db.models.functions import Lower
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from english.forms import correctionform, findentryform, newwordform, lookupform#, approvalform
from django.forms.formsets import formset_factory

def home(request):
    s = "hello world"
    return HttpResponse(s)

def detail(request):

    corrformset = formset_factory(correctionform)
    corrform = corrformset(initial=[{'correction_made': 0, 'correction_author': request.user}])
    return render(request, "detail.html", {'corrform': corrform})


def create(request):
    if request.method == 'POST':
        form = newwordform(request.POST)
        if form.is_valid():
            newword = form.save()
            return HttpResponseRedirect('/entry/' + str(newword.pk))
    form = newwordform()
    return render(request, 'create_word.html', {'form':form})

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
    return render(request, 'findentry.html', {'form': form})

def wordinfo(request, pk):
    cat = item.objects.get(pk=int(pk))
    return render(request, "wordinfo.html", {'cat': cat})


def findentry(request):
    form = findentryform()
    if request.method == 'GET':
        form = findentryform(request.GET)
        if form.is_valid():
            query = form.cleaned_data

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
            word_list = word_list.extra(order_by=['keyword'])
            corrformset = formset_factory(correctionform, extra = len(word_list))
            corrform = corrformset(initial=[{'correction_made': 0, 'correction_author': request.user}])
            for entry in corrform:
                if entry.is_valid():
                    return HttpResponse('ji')
                    validform = entry
                    validform.save()

        if search > 0:
            return render(request, 'findentry.html', {'form': form, 'corrform': corrform, 'word_list': word_list})
            # c = Context({'word_list': word_list}, {'form': form}, {'corrform': corrform})
            # t = loader.get_template("findentry.html")
            # return HttpResponse(t.render(c))

    else:
        form = findentryform()
    corrform = correctionform()



    return render(request, 'findentry.html', {'form': form, 'corrform': corrform})


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered=True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'register.html', {'user_form': user_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/findentry/')
            else:
                return HttpResponse('Your account is disabled.')
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'login.html', {})

# @login_required
# def requesttoedit(request):
#     if request.method == 'POST':
#         corrform = correctionform(request.POST)
#         if corrform.is_valid():
#             corrform.save()
#             return HttpResponseRedirect('/findentry/')
#     corrform = correctionform()
#     return render(request, 'requesttoedit.html', {'corrform':corrform})

@login_required
def requesttoedit(request):
    CorrFormSet = formset_factory(correctionform, extra = len(word_list))
    corrform = CorrFormSet(initial=[{'correction_made': 0, 'correction_author': request.user, 'corrected_word': word} for aword in word_list])
    if request.method == 'POST':
        corrform = CorrFormSet(request.POST)
        if corrform.is_valid():
            corrform.save()
            return HttpResponseRedirect('/findentry/')
    corrform = correctionform()
    return render(request, 'requesttoedit.html', {'corrform':corrform})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/findentry/')


def revision(request):

    word_list = item.objects.all()
    if request.method == 'POST':
        form = approvalform(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            word.update(approved=formdata)

    form = newwordform()
    return render(request, 'revision.html', {'word_list': word_list, 'form': form})


def index(request):
    word_list = item.objects.all()
    return render(request, 'index.html', {'action':'Display all items', 'word_list':word_list})




