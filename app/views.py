from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models

def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', '1')
    page_obj = paginator.page(page_number)
    return page_obj

def index(request):
    page = paginate(models.QUESTIONS, request)
    contex = {'questions': page.object_list, 'page_obj': page}
    return render(request, 'index.html', contex)

def question(request, question_id: int):
    if question_id >= len(models.QUESTIONS):
        return HttpResponse(status=404)
    question_item = models.QUESTIONS[question_id]
    context = {'question': question_item}
    return render(request, 'question.html', context=context)

def settings(request):
    return render(request, 'settings.html')

def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')