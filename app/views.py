from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.contrib import auth
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .forms import SignupForm
from .models import *
from app import forms, models




context = {
    'best_users': Profile.objects.all(),
    'hot_tags': Tag.objects.all(),
}



def index(request):
    tag_list = Tag.objects.all()[:10]
    latest_question_list = Question.objects.all()
    CL = list(latest_question_list)
    paginator = Paginator(CL, 5)
    page_number = request.GET.get('page')
#
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # В случае, GET параметр не число
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    print("hello there")
    return render(request, 'index.html', {
        'tags': tag_list,
        'questions': page_obj,
    })



def hot(request):
    tag_list = Tag.objects.all()[:10]
    hot_questions = Question.objects.hot()
    CL = list(hot_questions)
    paginator = Paginator(CL, 5)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    print("hello there")
    return render(request, 'index.html', {
        'tags': tag_list,
        'questions': page_obj,
    })


def fresh(request):
    tag_list = Tag.objects.all()[:10]
    fresh_question = Question.objects.get_new()
    CL = list(fresh_question)
    paginator = Paginator(CL, 5)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    print("hello there")
    return render(request, 'index.html', {
        'tags': tag_list,
        'questions': page_obj,
    })




def tag(request, tid):
    tag_list = Tag.objects.all()[:10]
    tag = Tag.objects.get(tag_title=tid)
    latest_question_list = tag.question_set.all()
    CL = list(latest_question_list)
    paginator = Paginator(CL, 5)
    page_number = request.GET.get('page')
#
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # В случае, GET параметр не число
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    print("hello there")
    return render(request, 'tag.html', {
        'tag': tid,
        'questions': page_obj,
        'tags': tag_list,
    })



def login(request):
    if request.method == 'GET':
        form = forms.LoginForm()
    else:
        form = forms.LoginForm(data=request.POST)
        print(form.errors)
        print(form.cleaned_data)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                print(user.username)
                auth.login(request, user)
                print("залогировался")
                return redirect(request.META.get('HTTP_REFERER'))
    ctx = {'form': form}
    return render(request, 'login.html', ctx)



def question(request, qid):
    tag_list_all = Tag.objects.all()[:10]
    question = Question.objects.get(pk = qid)
    comments_list = list(question.comment_set.all())
    CL = list(comments_list)
    paginator = Paginator(CL, 5)
    page_number = request.GET.get('page')
    tag_list = question.tags.all()[:5]
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    return render(request, 'question.html', {
    'question': question,
    'comments': page_obj,
    'question_tags' : tag_list,
    'tags': tag_list_all,
    })



def signup(request):
    if request.method == "GET":
        form = forms.SignupForm()
        rendered_data = {'form': form}
        return render(request, 'signup.html', rendered_data)

    if request.method == "POST":
        form = forms.SignupForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            auth.login(request, user=user)
            return redirect('/')

        rendered_data = {'form': form}
        return render(request, 'signup.html', rendered_data)


@login_required
def log_out(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER'))




@login_required
def ask(request):
    if request.method == 'POST':
        author, created = models.Profile.objects.get_or_create(nickname=request.user.username)
        form = forms.QuestionForm(profile=author, data=request.POST)
        if form.is_valid():
            question = form.save(request.user.profile)
            return redirect(reverse('question', kwargs={'qid': question.pk}))
    else:
        form = forms.QuestionForm(request.POST)
    context['form'] = form
    return render(request, 'ask.html', context)

@login_required
def comment(request):
    if request.method == 'POST':
        author, created = models.Profile.objects.get_or_create(nickname=request.user.username)
        form = forms.CommentForm(profile=author, data=request.POST)
        if form.is_valid():
            comment = form.save(request.user.profile)
            return redirect(reverse('question', kwargs={'qid': question.pk}))
    else:
        form = forms.QuestionForm(request.POST)
    context['form'] = form
    return render(request, 'ask.html', context)



@login_required
def settings(request):
    if request.method == "GET":
        form = forms.SettingsForm()
        rendered_data = {'form': form}
        return render(request, 'settings.html', rendered_data)
    if request.method == "POST":
        form = forms.SettingsForm(data=request.POST,
                                  files=request.FILES,
                                  instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
        rendered_data = {'form': form}
        return render(request, 'settings.html', rendered_data)

