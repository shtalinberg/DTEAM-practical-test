import os
import tempfile

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from celery import shared_task

from .models import Resume
from .utils import render_to_pdf


@shared_task
def send_cv_pdf_email(resume_id, recipient_email):
    """
    Celery task to send CV PDF via email.

    Args:
        resume_id (int): ID of the resume to send
        recipient_email (str): Email address to send to

    Returns:
        dict: Result of the email sending operation
    """
    # Get the resume
    resume = Resume.objects.filter(id=resume_id).firtst()
    if not resume:
        return {'status': 'error', 'message': f'Resume with ID {resume_id} not found'}
    # Generate PDF
    try:
        # Create a temporary file for the PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            # Use our existing PDF utility
            pdf_response = render_to_pdf(
                'cvsai/resume_pdf.html',
                {
                    'resume': resume,
                },
                f"{resume.full_name}_resume.pdf",
            )

            # Write PDF content to temporary file
            tmp_file.write(pdf_response.content)
            tmp_file_path = tmp_file.name

        # Prepare email
        subject = f'CV: {resume.full_name} - {resume.title}'

        # Email body
        email_body = render_to_string(
            'cvsai/emails/cv_email.txt',
            {'resume': resume, 'recipient_email': recipient_email},
        )

        # Create email message
        email = EmailMessage(
            subject=subject,
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email],
        )

        # Attach PDF
        filename = f"{resume.full_name.replace(' ', '_')}_resume.pdf"
        with open(tmp_file_path, 'rb') as file_obj:
            email.attach(filename, file_obj.read(), 'application/pdf')

        # Send email
        email.send()

        # Clean up temporary file
        os.unlink(tmp_file_path)

        return {
            'status': 'success',
            'message': f'CV sent successfully to {recipient_email}',
            'resume_id': resume_id,
            'recipient': recipient_email,
        }

    except Exception as exc:
        # Clean up temporary file if it exists
        if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)

        return {'status': 'error', 'message': f'Failed to send email: {str(exc)}'}
