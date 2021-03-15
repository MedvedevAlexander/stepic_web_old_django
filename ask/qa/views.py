from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.http import require_GET
from .models import Question, Answer
from .forms import AskForm, AnswerForm
from django.core.paginator import Paginator
from django.urls import reverse


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
            question = form.save()
            url = reverse('ask:question', args=[question.pk])
            return HttpResponseRedirect(url)
    else:
        form = AskForm()

    context = {
        'form': form
    }
    return render(request, 'qa/ask.html', context)