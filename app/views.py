from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

questions = {
    i: {'id': i, 'title': f'question # {i}'}
    for i in range(5)
}

def index(request):
    print("hello there")
    return render(request, 'index.html', {
        'questions': questions.values(),
    })
# Create your views here.

def login(request):
    print("hello there")
    return render(request, 'login.html', {})


def question(request, qid):
    question = questions.get(qid)
    return render(request, 'question.html', {
        'question': question
    })

def ask(request):
    print("hello there")
    return render(request, 'ask.html', {})
