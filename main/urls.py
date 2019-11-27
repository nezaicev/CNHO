from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import Index, Status, Email, TeacherView, BaseView
from .forms import ArtakiadaContestForm, NRushevaContestForm

urlpatterns = [
    path('', Index.as_view(template='index.html'), name='index'),
    path('status/<str:contest>/', Status.as_view(), name='status_url'),
    path('check_existence/<str:status>', Email.as_view(), name='check_existence_url'),
    path('teacher_reg', TeacherView.as_view(), name='teacher_form_registration_url'),
    path('contest_reg/artakiada', BaseView.as_view(template='finish_registration.html', form=ArtakiadaContestForm),
         name='artakiada_form_registration_url'),
    path('contest_reg/nrusheva', BaseView.as_view(template='finish_registration.html', form=NRushevaContestForm),
         name='nrusheva_form_registration_url'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
