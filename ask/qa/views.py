from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.http import require_GET
from .models import Question
from django.core.paginator import Paginator


def test(request, *args, **kwargs):
    return HttpResponse('OK1')


@require_GET
def index(request, *args, **kwargs):
    questions = Question.objects.new()
    limit = 10

    # check data type
    try:
        page = int(request.GET['page'])
    except ValueError:
        raise Http404

    paginator = Paginator(questions, limit)

    # check page range
    if page > max(paginator.page_range):
        raise Http404

    p = paginator.page(page)
    context = {
        'paginator': p
    }

    return render(request, 'qa/index.html', context)


@require_GET
def popular(request, *args, **kwargs):
    questions = Question.objects.popular()
    limit = 10

    # check data type
    try:
        page = int(request.GET['page'])
    except ValueError:
        Http404

    paginator = Paginator(questions, limit)

    # check page range
    if page > max(paginator.page_range):
        raise Http404

    p = paginator.page(page)
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

    context = {
        'question': question
    }

    return render(request, 'qa/question.html', context)