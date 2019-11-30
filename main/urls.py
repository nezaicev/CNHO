from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import Index,TeacherView, BaseView
from .forms import ArtakiadaContestForm, NRushevaContestForm, MymoskviciContestForm,EmailForm

urlpatterns = [
    path('', Index.as_view(), name='index'),
    # path('status/<str:contest>/', Status.as_view(), name='status_url'),
    # path('check_existence/<str:status>', Email.as_view(), name='check_existence_url'),
    path('teacher_reg', TeacherView.as_view(), name='teacher_form_registration_url'),
    path('contest_reg/artakiada', BaseView.as_view(template='finish_registration.html', form=ArtakiadaContestForm),
         name='artakiada_form_registration_url'),
    path('contest_reg/nrusheva', BaseView.as_view(template='finish_registration.html', form=NRushevaContestForm),
         name='nrusheva_form_registration_url'),
    path('contest_reg/mymoskvichi', BaseView.as_view(template='finish_registration.html', form=MymoskviciContestForm),
         name='mymoskvichi_form_registration_url'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
