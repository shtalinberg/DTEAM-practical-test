from cvsai.models import Resume, Skill
from cvsai.serializers import (
    ResumeCreateUpdateSerializer,
    ResumeSerializer,
    SkillSerializer,
)
from cvsai.views import download_resume_pdf
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response


class ResumeListCreateAPIView(generics.ListCreateAPIView):
    """
    List all resumes or create a new resume.

    GET /api/resumes/ - List all resumes
    POST /api/resumes/ - Create new resume
    """

    queryset = Resume.objects.all().prefetch_related(
        'resumeskill_set__skill', 'projects', 'contacts'
    )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ResumeCreateUpdateSerializer
        return ResumeSerializer


class ResumeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a resume.

    GET /api/resumes/{id}/ - Retrieve resume
    PUT /api/resumes/{id}/ - Update resume
    PATCH /api/resumes/{id}/ - Partial update resume
    DELETE /api/resumes/{id}/ - Delete resume
    """

    queryset = Resume.objects.all().prefetch_related(
        'resumeskill_set__skill', 'projects', 'contacts'
    )

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ResumeCreateUpdateSerializer
        return ResumeSerializer


class SkillListCreateAPIView(generics.ListCreateAPIView):
    """
    List all skills or create a new skill.

    GET /api/skills/ - List all skills
    POST /api/skills/ - Create new skill
    """

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


@api_view(['GET'])
def resume_pdf_api(request, pk):
    """
    Download resume as PDF via API.

    GET /api/resumes/{id}/pdf/ - Download resume PDF
    """
    return download_resume_pdf(request, pk)


@api_view(['GET'])
def api_root(request):
    """
    API root endpoint with available endpoints.
    """
    return Response(
        {
            'message': 'Welcome to Resume API',
            'endpoints': {
                'resumes': '/api/resumes/',
                'skills': '/api/skills/',
                'resume_detail': '/api/resumes/{id}/',
                'resume_pdf': '/api/resumes/{id}/pdf/',
            },
            'documentation': {
                'create_resume': {
                    'method': 'POST',
                    'url': '/api/resumes/',
                    'example_payload': {
                        'firstname': 'Alex',
                        'lastname': 'Berg',
                        'title': 'Python Django Developer',
                        'bio': 'Experienced python developer - bla bla bla',
                        'skills': [
                            {'skill_id': 1, 'level': 'advanced'},
                            {'skill_id': 2, 'level': 'intermediate'},
                        ],
                        'projects': [
                            {
                                'title': 'Project Name',
                                'description': 'Project description',
                                'url': 'https://github.com/...',
                                'start_date': '2025-01-01',
                                'end_date': '2025-12-31',
                            }
                        ],
                        'contacts': [
                            {'contact_type': 'email', 'value': 'berg@example.com'},
                            {
                                'contact_type': 'github',
                                'value': 'https://github.com/berg',
                            },
                        ],
                    },
                }
            },
        }
    )
