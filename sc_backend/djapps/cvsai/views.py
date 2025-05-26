import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from cvsai.constants import SUPPORTED_LANGUAGES
from cvsai.forms import SendCVEmailForm
from cvsai.models import Resume
from cvsai.tasks import send_cv_pdf_email
from cvsai.translation_services import translate_cv_content
from cvsai.utils import render_to_pdf


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


@require_POST
def send_cv_email(request, pk):
    """
    View to send CV PDF via email using Celery task.
    """
    resume = get_object_or_404(Resume, pk=pk)

    # Handle AJAX request
    if request.headers.get('Content-Type') == 'application/json':
        try:
            data = json.loads(request.body)
            email = data.get('email')
        except json.JSONDecodeError:
            return JsonResponse(
                {'status': 'error', 'message': 'Invalid JSON data'}, status=400
            )
    else:
        # Handle form submission
        email = request.POST.get('email')

    if not email:
        response_data = {'status': 'error', 'message': 'Email address is required'}
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse(response_data, status=400)
        messages.error(request, response_data['message'])
        return redirect('cvsai:cv_detail', pk=pk)

    # Validate email using form
    form = SendCVEmailForm({'email': email})
    if not form.is_valid():
        response_data = {'status': 'error', 'message': 'Invalid email address'}
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse(response_data, status=400)
        messages.error(request, response_data['message'])
        return redirect('cvsai:cv_detail', pk=pk)

    try:
        # Queue the Celery task
        task = send_cv_pdf_email.delay(resume.id, email)

        response_data = {
            'status': 'success',
            'message': (
                f"CV is being sent to {email}. " "You will be notified when complete."
            ),
            'task_id': task.id,
        }

        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse(response_data)
        messages.success(request, response_data['message'])
        return redirect('cvsai:cv_detail', pk=pk)

    except Exception as exc:
        response_data = {
            'status': 'error',
            'message': f'Failed to queue email task: {str(exc)}',
        }

        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse(response_data, status=500)
        messages.error(request, response_data['message'])
        return redirect('cvsai:cv_detail', pk=pk)


def translate_cv(request, pk):
    """
    Translate CV content to selected language.
    Supports both POST (with language) and GET (show translation page).
    """
    resume = get_object_or_404(Resume, pk=pk)

    if request.method == 'POST':
        # Handle AJAX translation request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            target_language = data.get('language')
        else:
            target_language = request.POST.get('language')
        try:
            if not target_language:
                return JsonResponse(
                    {'error': 'Language parameter is required'}, status=400
                )

            if target_language not in SUPPORTED_LANGUAGES:
                return JsonResponse(
                    {'error': f'Language {target_language} is not supported'},
                    status=400,
                )

            # Perform translation
            translated_content = translate_cv_content(resume, target_language)

            return JsonResponse(
                {
                    'success': True,
                    'translated_content': translated_content,
                    'original_resume_id': resume.id,
                }
            )

        except Exception as exc:
            return JsonResponse(
                {'error': f'Translation failed: {str(exc)}'}, status=500
            )

    else:
        # GET request - show translation interface
        context = {'resume': resume, 'supported_languages': SUPPORTED_LANGUAGES}
        return render(request, 'cvsai/translate_cv.html', context)
