from django.urls import path

from cvsai.views import ResumeDetailView, ResumeListView

urlpatterns = [
    path('', ResumeListView.as_view(), name='cv_list'),
    path('cv/<int:pk>/', ResumeDetailView.as_view(), name='cv_detail'),
]
