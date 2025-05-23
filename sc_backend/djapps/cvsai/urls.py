from django.urls import path

from cvsai.views import (
    ResumeDetailView,
    ResumeListView,
    download_resume_pdf,
    send_cv_email,
)

app_name = 'cvsai'

urlpatterns = [
    path('', ResumeListView.as_view(), name='cv_list'),
    path('cv/<int:pk>/', ResumeDetailView.as_view(), name='cv_detail'),
    path('cv/<int:pk>/download-pdf/', download_resume_pdf, name='cv_download_pdf'),
    path('cv/<int:pk>/send-email/', send_cv_email, name='send_cv_email'),
]
