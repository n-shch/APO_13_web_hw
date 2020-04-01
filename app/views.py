from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


QUESTIONS = {
    '1': {'id': 1, 'title': 'I`m your dream', 'text': 'I`m your dream, make you real'},
    '2': {'id': 2, 'title': 'I`m your eyes', 'text': 'I`m your eyes when you must steal'},
    '3': {'id': 3, 'title': 'I`m your pain', 'text': 'I`m your pain when you can`t feel'},
}

tags_list = ['fish',
 'fashion',
  'covid-19',
   'how much does place in cemetery cost',
   ]

tags = {
    i: {'id': tags_list[i]}
    for i in range(4)
}

questions = {
    i: {'id': i, 'title': f'question # {i}'}
    for i in range(10)
}

def index(request):
    contact_list = questions.values()
    CL = list(contact_list)
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
        'questions': page_obj,
    })


def listing(request):
    contact_list = Contact.objects.all()
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'paginator.html', {'page_obj': page_obj})


def tag(request, tid):
    print("hello there")
    return render(request, 'tag.html', {
    'tag' : tid,
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

# that's where u start to do hw
def main(request):
    print("hello there")
    return render(request, 'index.html', {
        'questions': questions.values(),
    })

def hot(request):
    print("hello there")
    return render(request, 'index.html', {
    'questions': questions.values(),
    })

def signup(request):
    print("hello there")
    return render(request, 'signup.html', {})

def ask(request):
    print("hellow world")
    return render(request, 'ask.html', {})