from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def question(request, question_id: int):
    return HttpResponse(f'q_id = {question_id}')
    # return render(request, 'question-base.html')
