from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
                  path('', views.index, name='index'),
                  path('choice_contest/<str:contest>/',views.check_existence,name='choice_contest'),
                  path('reg', views.registration, name='registration'),
                  path('teacher_reg', views.teacher_registration, name='teacher_form_registration_url'),
                  path('contest_reg', views.contest_registrations, name='contest_form_registration_url'),

              ] + static(settings.STATIC_URL)
