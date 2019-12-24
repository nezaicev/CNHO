from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View, TemplateView
from django.contrib import messages
from main.models import Teacher
from main.forms import TeacherForm, EmailForm, ArtakiadaContestForm, NRushevaContestForm, MymoskviciContestForm
from main.tasks import nrusheva_tasks, artakiada_tasks, mymoskvici_tasks


class BaseView(TemplateView):
    form = None
    template = None

    def get(self, request, *args, **kwargs):
        context = {'form': self.form}
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        context = {'form': self.form, 'teacher_id': request.session.get('id')}
        bound_form = self.form(request.POST, request.FILES)
        print(bound_form.errors)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            messages.add_message(request, messages.SUCCESS, 'Данные сохранены, на Ваш email будет отправленно информационное письмо, отражающее зарегистрированных участников')
            if request.session.get('contest') == 'nrusheva':
                nrusheva_tasks.delay(new_obj.id)
            if request.session.get('contest') == 'artakiada':
                artakiada_tasks.delay(new_obj.id)
            if request.session.get('contest') == 'mymoskvichi':
                mymoskvici_tasks.delay(new_obj.id)
            return render(request, self.template, context)
        else:
            context={'errors':bound_form.errors}
            return render(request,'error_registration.html',context)

    @classmethod
    def redirect_contest(cls, request):
        try:
            teacher = Teacher.objects.get(pk=request.session.get('id'))
        except:
            teacher = None
        if request.session.get('contest') == 'artakiada':
            context = {'form': ArtakiadaContestForm, 'teacher': teacher, 'email': request.session.get('email')}
            return render(request, 'artakiada.html', context)
        if request.session.get('contest') == 'nrusheva':
            context = {'form': NRushevaContestForm, 'teacher': teacher, 'email': request.session.get('email')}
            return render(request, 'nrusheva.html', context)
        if request.session.get('contest') == 'mymoskvichi':
            context = {'form': MymoskviciContestForm, 'teacher': teacher, 'email': request.session.get('email')}
            return render(request, 'mymoskvichi.html', context)


class Index(BaseView, View):
    template = 'index.html'
    form = EmailForm

    def get(self, request, *args, **kwargs):
        request.session.clear()
        return super().get(request)

    def post(self, request, *args, **kwargs):

        request.session['email'] = request.POST['email']
        request.session['contest'] = request.POST['info']
        request.session['status'] = request.POST['status']

        try:
            request.session['id'] = Teacher.objects.get(email=request.session['email']).id
            return self.redirect_contest(request)
        except:
            context = {'status': request.POST['status'], 'email': request.session.get('email'),
                       'form': TeacherForm, 'contest': request.session.get('contest')}
            return render(request, 'teacher.html', context)


class TeacherView(BaseView, View):
    form = TeacherForm

    def post(self, request, *args, **kwargs):
        bound_form = self.form(request.POST)
        print(bound_form.errors)
        if bound_form.is_valid():
            teacher = bound_form.save()
            request.session['id'] = teacher.id
            return self.redirect_contest(request)
