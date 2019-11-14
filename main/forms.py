from django import forms
from django.forms import widgets
from main.models import Teacher, Mskch, Artakiada
from main import lists


class EmailForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['email']
        widgets = {'email': forms.EmailInput()}


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['fio', 'region', 'district', 'city', 'school', 'position', 'age', 'email', 'phone']
        widgets = {
            'fio': forms.HiddenInput(attrs={'name': 'fio', 'id': 'fio'}),
            'email': forms.HiddenInput(attrs={'name': 'email', 'id': 'email'}),
            'region': forms.Select(attrs={'onchange': 'regionChanged(this.value)', 'class': 'custom-select',
                                          'placeholder': 'Москва', 'required': ''}, choices=lists.REGIONS),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Населенный пункт',
                                           'type': 'hidden', 'required': '', 'value': 'г. Москва'}),
            'district': forms.Select(attrs={'class': 'custom-select', 'type': 'hidden'}, choices=lists.DISTRICT),
            'school': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Школа №123'}),
            'position': forms.Select(attrs={'class': 'custom-select '}, choices=lists.POSITIONS),
            'age': forms.Select(attrs={'class': 'custom-select'}, choices=lists.AGE_TEACHER),
            'phone': forms.TextInput(attrs={'class': 'form-control col-4'}),

        }


class MSKCHContestForm(forms.ModelForm):
    class Meta:
        model = Mskch
        fields = ['title', 'teacher','fio_teacher']
        widgets = {
            # 'teacher': forms.HiddenInput(attrs={'name': 'teacher', 'id': 'teacher'}),

            'title': forms.TextInput(),
            'teacher': forms.HiddenInput(attrs={'name': 'teacher', 'id': 'teacher'}),
            'fio_teacher':forms.HiddenInput(),

        }


class ArtakiadaContestForm(forms.ModelForm):
    class Meta:
        model = Artakiada
        fields = ['fio','gender','age','title',]
        widgets = {
            'fio': forms.HiddenInput(attrs={'name': 'fio', 'id': 'fio'}),
            'age': forms.Select(attrs={'class': 'custom-select'}),
            'gender':forms.Select(attrs={'class': 'custom-select'}),


        }
