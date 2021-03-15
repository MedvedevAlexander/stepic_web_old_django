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
    page_num = request.GET.get('page')
    paginator = Paginator(questions, limit)

    # check page range
    if page_num > max(paginator.page_range):
        raise Http404

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

    # check page range
    if page_num > max(paginator.page_range):
        raise Http404

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

    context = {
        'question': question
    }

    return render(request, 'qa/question.html', context)