from django.urls import path

from cvsai import api_views

app_name = 'cvsai_api'

urlpatterns = [
    path('', api_views.api_root, name='api-root'),
    # Resume endpoints
    path(
        'resumes/',
        api_views.ResumeListCreateAPIView.as_view(),
        name='resume-list-create',
    ),
    path(
        'resumes/<int:pk>/',
        api_views.ResumeRetrieveUpdateDestroyAPIView.as_view(),
        name='resume-detail',
    ),
    path('resumes/<int:pk>/pdf/', api_views.resume_pdf_api, name='resume-pdf'),
    # Skill endpoints
    path(
        'skills/', api_views.SkillListCreateAPIView.as_view(), name='skill-list-create'
    ),
]
