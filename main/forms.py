from django import forms
from django.forms import widgets
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from main.models import Teacher, Artakiada, NRusheva, Mymoskvichi
from main import lists


class TextEditor(forms.Form):
    theme = forms.CharField(widget=forms.TextInput, label='Тема')
    editor = forms.CharField(widget=CKEditorUploadingWidget(), label='Содержание')


class EmailForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['email', 'status', 'info']
        widgets = {
            'email': forms.EmailInput(
                attrs={'class': "form-control col-6", 'oninvalid': "this.setCustomValidity('Укажите Ваш Email')",
                       'required': ''}),
            'status': forms.Select(attrs={'class': 'custom-select col-7',
                                          'required': 'Укажите Ваш статус'},
                                   choices=lists.REG_STATUS),
            'info': forms.HiddenInput(attrs={'name': 'contest', 'id': 'contest'})
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['fio', 'region', 'district', 'city', 'school', 'position', 'age', 'email', 'phone', 'info', 'status']
        widgets = {
            'fio': forms.HiddenInput(attrs={'name': 'fio', 'id': 'fio'}),
            'email': forms.HiddenInput(attrs={'name': 'email', 'id': 'email'}),
            'region': forms.Select(attrs={'onchange': 'regionChanged(this.value)', 'class': 'custom-select',
                                          'placeholder': 'Москва', 'required': ''}, choices=lists.REGIONS),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Населенный пункт',
                                           'type': 'hidden', 'required': '', 'value': 'г. Москва'}),
            'district': forms.Select(attrs={'class': 'custom-select', 'type': 'hidden'}, choices=lists.DISTRICT),
            'school': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Школа №123', 'required': ''}),
            'position': forms.Select(attrs={'class': 'custom-select '}, choices=lists.POSITIONS),
            'age': forms.Select(attrs={'class': 'custom-select'}, choices=lists.AGE_TEACHER),
            'phone': forms.TextInput(attrs={'class': 'form-control col-4'}),
            'info': forms.TextInput(attrs={'class': 'form-control col-1', 'required': ''}),

        }


class BaseContestForm(forms.ModelForm):
    class Meta:
        model = None
        fields = ['fio', 'region', 'city', 'district', 'school', 'level', 'teacher', 'email', 'fio_teacher', 'age',
                  'gender', 'theme', 'theme_extra', 'material', 'author_name', 'format', 'description', 'image',
                  'program']
        widgets = {
            'fio': forms.HiddenInput(attrs={'name': 'fio', 'id': 'fio'}),
            'level': forms.Select(attrs={'class': 'custom-select'}, choices=lists.LEVEL),
            'school': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Школа №123'}),
            'district': forms.Select(attrs={'class': 'custom-select', 'type': 'hidden'}, choices=lists.DISTRICT),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Населенный пункт',
                                           'type': 'hidden', 'required': '', 'value': 'г. Москва'}),
            'region': forms.Select(attrs={'onchange': 'regionChanged(this.value)', 'class': 'custom-select',
                                          'placeholder': 'Москва', 'required': ''}, choices=lists.REGIONS),
            'email': forms.HiddenInput(attrs={'name': 'email', 'id': 'id_email'}),
            'teacher': forms.HiddenInput(attrs={'name': 'teacher', 'id': 'id_teacher'}),
            'fio_teacher': forms.HiddenInput(attrs={'name': 'fio_teacher', 'id': 'fio_teacher'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'type': 'file'}),
            'gender': forms.Select(attrs={'class': 'custom-select'}),
            'age': forms.Select(attrs={'class': 'custom-select'}),
            'theme': forms.Select(attrs={'class': 'custom-select '}),
            'theme_extra': forms.Select(attrs={'class': 'custom-select '}),
            'author_name': forms.TextInput(attrs={'class': 'form-control col-5', 'placeholder': 'Авторское название'}),
            'material': forms.Select(attrs={'class': 'form-control ', 'placeholder': 'Материал (Гуашь)'}),
            'format': forms.Select(attrs={'class': 'custom-select '}),
            'description': forms.Textarea(attrs={'class': 'form-control ', 'rows': '3',
                                                 'placeholder': 'Краткая, сжатая, характеристика содержания работы'}),
            'program': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adobe Flash'}),

        }


class ArtakiadaContestForm(BaseContestForm):
    class Meta(BaseContestForm.Meta):
        model = Artakiada
        exclude = (
            'image', 'material', 'age', 'description', 'author_name', 'gender', 'theme', 'theme_extra', 'format',
            'program')


class NRushevaContestForm(BaseContestForm):
    def clean_image(self):
        data = self.cleaned_data['image']
        if data.size > 20000000:
            raise forms.ValidationError("Файл должен быть меньше 20 Мб.")

        return data

    class Meta(BaseContestForm.Meta):
        model = NRusheva
        exclude = ('theme_extra', 'program')


class MymoskviciContestForm(BaseContestForm):
    class Meta(BaseContestForm.Meta):
        model = Mymoskvichi
        exclude = ('image', 'material', 'description', 'gender', 'format', 'level')
