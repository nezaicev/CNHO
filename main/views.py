import django.core.serializers as to_json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View, TemplateView
from main.models import Teacher
from main.forms import TeacherForm, EmailForm, ArtakiadaContestForm


class BaseView(TemplateView):
    form = None
    template = None

    def get(self, request, *args, **kwargs):
        context = {'form': self.form}
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        context = {'form': self.form, 'teacher_id': request.session.get('id')}
        bound_form = self.form(request.POST)
        if bound_form.is_valid():
            bound_form.save()
        return render(request, self.template, context)

    @classmethod
    def redirect_contest(cls, request):
        try:
            teacher = Teacher.objects.get(pk=request.session.get('id'))
        except:
            teacher = None
        if request.session.get('contest') == 'artakiada':
            context = {'form': ArtakiadaContestForm, 'teacher': teacher, 'email': request.session.get('email')}
            return render(request, 'artakiada.html', context)
        # if request.session.get('contest')=='mymoskvichi':
        #     context={'form':''}
        #     return render(request)
        # if request.session.get('contest')=='nrusheva':
        #     context={'form':''}
        #     return render(request)

    @classmethod
    def finish(cls, request, *args, **kwargs):
        return HttpResponse('ok')


class Index(BaseView, View):
    def get(self, request, *args, **kwargs):
        request.session.clear()
        return super().get(request)


class Status(BaseView, View):
    template = 'choice.html'

    def get(self, request, *args, **kwargs):
        request.session['contest'] = self.kwargs['contest']
        return super().get(request)


class Email(BaseView, View):
    template = 'auth_by_email.html'
    form = EmailForm

    def get(self, request, *args, **kwargs):
        request.session['status'] = self.kwargs['status']
        return super().get(request)

    def post(self, request, *args, **kwargs):
        request.session['email'] = request.POST['email']
        if request.session.get('status') == 'teacher':

            try:
                request.session['id'] = Teacher.objects.get(email=request.POST['email']).id
                return self.redirect_contest(request)

            except:
                context = {'email': request.POST['email'], 'form': TeacherForm}
                return render(request, 'teacher.html', context)
        else:
            try:
                request.session['id'] = Teacher.objects.get(email='user@user.ru').id
            except:
                user = Teacher.objects.create(status=False, fio='user', region='0', school='user', email='user@user.ru',
                                              position='user')
                request.session['id'] = user.id

            return self.redirect_contest(request)


class TeacherView(BaseView, View):
    form = TeacherForm

    def post(self, request, *args, **kwargs):
        bound_form = self.form(request.POST)
        if bound_form.is_valid():
            teacher = bound_form.save()
            request.session['id'] = teacher.id
            # request.session['teacher']=to_json.serialize('json',teacher)
            # context = {'teacher_id': teacher.id}
            return self.redirect_contest(request)
