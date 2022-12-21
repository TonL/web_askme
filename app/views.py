from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def question(request): #, question_id: int):
    # return HttpResponse(f'q_id = {question_id}')
    return render(request, 'question.html')

def settings(request):
    return render(request, 'settings.html')

def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')