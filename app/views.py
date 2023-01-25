from django.http import HttpResponse
from django.shortcuts import render, reverse, redirect
from django.core.paginator import Paginator
from . import models
from app.forms import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# from app.models import Question, Answer, Tag, LikeQuestion, LikeAnswer, Profile

popular_tags = models.Tag.objects.top()
best_members = models.Profile.objects.top()


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', '1')
    page_obj = paginator.page(page_number)
    return page_obj


def index(request):
    questions = models.Question.objects.new()
    page = paginate(questions, request)
    contex = {'questions': page.object_list, 'page_obj': page, 'best_members': best_members, 'popular_tags': popular_tags}
    return render(request, 'index.html', contex)


def hot(request):
    questions = models.Question.objects.hot()
    page = paginate(questions, request)
    contex = {'questions': page.object_list, 'page_obj': page, 'popular_tags': popular_tags, 'best_members': best_members}
    return render(request, "hot.html", contex)


def question(request, question_id: int):
    question_item = models.Question.objects.get_id(question_id)
    answers = models.Answer.objects.by_question(question_id)

    context = {'question': question_item, 'popular_tags': popular_tags, 'best_members': best_members, 'answers': answers}
    return render(request, 'question.html', context=context)


def tag(request, tag_name):
    questions = models.Question.objects.get_tag(tag_name)
    page = paginate(questions, request)
    context = {'questions': page.object_list, 'page_obj': page, 'popular_tags': popular_tags, 'best_members': best_members, 'tag': tag_name}
    return render(request, "tag.html", context)


def settings(request):
    return render(request, 'settings.html')


def ask(request):
    return render(request, 'ask.html')


def login(request):
    if request.method == 'POST':
        user_form = LoginForm(request.POST)

        if user_form.is_valid():
            user = auth.authenticate(request=request, **user_form.cleaned_data)
            print(user)
            if user:
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="Wrong username or password!")
    else:
        user_form = LoginForm()

    return render(request, 'login.html', {'form': user_form})


def signup(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            if user:
                return redirect(reverse('login'))
            else:
                user_form.add_error(field=None, error="Sign up error!")
    else:
        user_form = RegistrationForm()

    return render(request, 'signup.html', {'form': user_form})

