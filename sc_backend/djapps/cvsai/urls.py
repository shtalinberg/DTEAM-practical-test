
from django.urls import path

from cvsai.views import ResumeListView

urlpatterns = [
    path('', ResumeListView.as_view(), name='cv_list'),
    path('cv/<int:pk>/', ResumeListView.as_view(), name='cv_detail'),
]