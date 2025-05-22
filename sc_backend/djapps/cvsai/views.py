from django.views.generic import DetailView, ListView

from cvsai.models import Resume

# Create your views here.


class ResumeListView(ListView):
    """Render a list of resumes."""

    model = Resume
    template_name = 'cvsai/resume_list.html'
    context_object_name = 'resumes'

    def get_queryset(self):
        return Resume.objects.all()


class ResumeDetailView(DetailView):
    """View for displaying resume details."""

    model = Resume
    template_name = 'cvsai/resume_detail.html'
    context_object_name = 'resume'

    def get_queryset(self):
        return Resume.objects.all()
