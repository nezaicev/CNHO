from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import Index,TeacherView, BaseView
from .forms import ArtakiadaContestForm, NRushevaContestForm, MymoskviciContestForm

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('teacher_reg', TeacherView.as_view(), name='teacher_form_registration_url'),

    path('contest_reg/artakiada', BaseView.as_view(template='finish_registration.html', form=ArtakiadaContestForm),
         name='artakiada_form_registration_url'),

    path('contest_reg/nrusheva', BaseView.as_view(template='finish_registration.html', form=NRushevaContestForm),
         name='nrusheva_form_registration_url'),

    path('contest_reg/mymoskvichi', BaseView.as_view(template='finish_registration.html', form=MymoskviciContestForm),
         name='mymoskvichi_form_registration_url'),
path('contest_reg', BaseView.redirect_contest,
         name='contest_reg'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
