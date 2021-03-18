from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.http import require_GET
from .models import Question, Answer
from .forms import AskForm, AnswerForm, SignupForm
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login


def test(request, *args, **kwargs):
    return HttpResponse('OK1')


@require_GET
def index(request, *args, **kwargs):
    questions = Question.objects.new()
    limit = 10
    page_num = request.GET.get('page')
    paginator = Paginator(questions, limit)
    p = paginator.get_page(page_num)
    context = {
        'paginator': p
    }

    return render(request, 'qa/index.html', context)


@require_GET
def popular(request, *args, **kwargs):
    questions = Question.objects.popular()
    limit = 10
    page_num = request.GET.get('page')
    paginator = Paginator(questions, limit)
    p = paginator.get_page(page_num)
    context = {
        'paginator': p
    }

    return render(request, 'qa/index.html', context)


def question(request, *args, **kwargs):
    # check data type
    try:
        question_id = int(kwargs['question_id'])
    except ValueError:
        raise Http404
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        #return HttpResponse('200 ok')
        form = AnswerForm(request.POST)
        if form.is_valid():
            form._user = request.user
            answer = form.save()
            url = reverse('ask:question', args=[question_id])
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': question.pk})

    context = {
        'question': question,
        'form': form
    }

    return render(request, 'qa/question.html', context)


def ask(request, *args, **kwargs):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            form._user = request.user
            question = form.save()
            url = reverse('ask:question', args=[question.pk])
            return HttpResponseRedirect(url)
    else:
        form = AskForm()

    context = {
        'form': form
    }
    return render(request, 'qa/ask.html', context)


def signup(request, *args, **kwargs):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(request.POST.get('username'), request.POST.get('email'),
                                            request.POST.get('password'))
            login(request, user)
            url = reverse('ask:main_page')

            return HttpResponseRedirect(url)
    else:
        form = SignupForm()

    context = {
        'form': form
    }
    return render(request, 'qa/signup.html', context)