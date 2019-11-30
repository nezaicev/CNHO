from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View, TemplateView
from django.contrib import messages
from main.models import Teacher
from main.forms import TeacherForm, EmailForm, ArtakiadaContestForm, NRushevaContestForm, MymoskviciContestForm


class BaseView(TemplateView):
    form = None
    template = None

    def get(self, request, *args, **kwargs):
        context = {'form': self.form}
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        context = {'form': self.form, 'teacher_id': request.session.get('id')}
        bound_form = self.form(request.POST, request.FILES)
        if bound_form.is_valid():
            bound_form.save()
            messages.add_message(request, messages.SUCCESS, 'Ваши данные отправлены')
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
        if request.session.get('contest') == 'nrusheva':
            context = {'form': NRushevaContestForm, 'teacher': teacher, 'email': request.session.get('email')}
            return render(request, 'nrusheva.html', context)
        if request.session.get('contest') == 'mymoskvichi':
            context = {'form': MymoskviciContestForm, 'teacher': teacher, 'email': request.session.get('email')}
            return render(request, 'mymoskvichi.html', context)

    @classmethod
    def finish(cls, request, *args, **kwargs):
        return HttpResponse('ok')


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
            print(request.session.get('status'))
            context = {'status': request.POST['status'], 'email': request.session.get('email'),
                       'form': TeacherForm, 'contest': request.session.get('contest')}
            return render(request, 'teacher.html', context)


#
# class Status(BaseView, View):
#     template = 'choice.html'
#
#     def get(self, request, *args, **kwargs):
#         request.session['contest'] = self.kwargs['contest']
#         return super().get(request)

#
# class Email(BaseView, View):
#     template = 'auth_by_email.html'
#     form = EmailForm
#
#     def get(self, request, *args, **kwargs):
#         request.session['status'] = self.kwargs['status']
#         return super().get(request)
#
#     def post(self, request, *args, **kwargs):
#         request.session['email'] = request.POST['email']
#         if request.session.get('status') == 'teacher':
#
#             try:
#                 request.session['id'] = Teacher.objects.get(email=request.POST['email']).id
#                 return self.redirect_contest(request)
#
#             except:
#                 context = {'email': request.POST['email'], 'form': TeacherForm,
#                            'contest': request.session.get('contest')}
#                 return render(request, 'teacher.html', context)
#         else:
#             try:
#                 request.session['id'] = Teacher.objects.get(email='user@user.ru').id
#             except:
#                 user = Teacher.objects.create(status=False, fio='user', region='0', school='user', email='user@user.ru',
#                                               position='user')
#                 request.session['id'] = user.id
#
#             return self.redirect_contest(request)


class TeacherView(BaseView, View):
    form = TeacherForm

    def post(self, request, *args, **kwargs):
        bound_form = self.form(request.POST)
        print(bound_form.errors)
        if bound_form.is_valid():
            teacher = bound_form.save()
            request.session['id'] = teacher.id
            return self.redirect_contest(request)
