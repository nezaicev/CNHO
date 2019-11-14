from django.shortcuts import render
from django.http import HttpResponse
from main.models import Teacher
from main.forms import TeacherForm, EmailForm, MSKCHContestForm, ArtakiadaContestForm


def index(request):
    return render(request, 'index.html')


def check_existence(request, contest):
    request.session['contest'] = contest
    if request.method == 'GET':
        context = {'form': EmailForm}
        return render(request, 'auth_by_email.html', context)

    if request.method == 'POST':
        request.session['email'] = request.POST['email']
        try:
            teacher = Teacher.objects.get(email=request.POST['email']).id
            request.session['id'] = teacher
            context = {'teacher_id': teacher, 'form': MSKCHContestForm}
            return render(request, 'contest.html', context)
        except:
            context = {'email': request.POST['email'], 'form': TeacherForm}
            return render(request, 'choice.html', context)


def registration(request):
    if request.method == 'GET':
        if 'who' in request.GET:
            if request.GET['who'] == 'Педагог':
                context = {'form': TeacherForm, 'email': request.session.get('email')}
                return render(request, 'teacher.html', context)
            else:
                if request.session.get('contest') == 'artakiada':
                    context = {'form': ArtakiadaContestForm }
                    return render(request, 'artakiada.html', context)

                else:
                    context = {'form': MSKCHContestForm}
                    return render(request, 'contest.html', context)


def teacher_registration(request):
    form = TeacherForm
    if request.method == 'POST':
        bound_form = form(request.POST)
        if bound_form.is_valid():
            teacher = bound_form.save()
            request.session['id'] = teacher.id
            context = {'form': MSKCHContestForm, 'teacher_id': teacher.id}
            return render(request, 'contest.html', context)


def contest_registrations(request):
    form = MSKCHContestForm
    if request.method == 'POST':
        bound_form = form(request.POST)
        # print(bound_form)
        if bound_form.is_valid():
            bound_form.save()
            return HttpResponse('ok')
