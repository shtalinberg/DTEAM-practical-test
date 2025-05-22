from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.views.generic import DetailView, ListView

from cvsai.models import Resume
from cvsai.utils import render_to_pdf

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


def download_resume_pdf(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    context = {'resume': resume, 'request': request}
    slugify_name = slugify(resume.full_name.replace(' ', '_'))
    filename = f"{slugify_name}_resume.pdf"
    return render_to_pdf('cvsai/resume_pdf.html', context, filename)
