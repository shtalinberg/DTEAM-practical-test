import json

from django.urls import reverse

import pytest
from cvsai.models import Contact, Project, Resume, ResumeSkill, Skill
from cvsai.tests.constants import TEST_EMAIL
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """API client fixture."""
    return APIClient()


@pytest.mark.django_db
class TestResumeAPI:
    """Test cases for Resume API endpoints."""

    def test_list_resumes(self, api_client, sample_resume):
        """Test GET /api/resumes/ - List all resumes."""
        url = reverse('cvsai_api:resume-list-create')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["results"]
        assert len(data) == 1
        assert data[0]['firstname'] == 'Oleksandr'
        assert data[0]['lastname'] == 'Shtalinberg'
        assert data[0]['full_name'] == 'Oleksandr Shtalinberg'
        assert len(data[0]['skills']) == 1
        assert len(data[0]['projects']) == 1
        assert len(data[0]['contacts']) == 1

    def test_retrieve_resume(self, api_client, sample_resume):
        """Test GET /api/resumes/{id}/ - Retrieve specific resume."""
        url = reverse('cvsai_api:resume-detail', kwargs={'pk': sample_resume.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['id'] == sample_resume.pk
        assert data['firstname'] == 'Oleksandr'
        assert data['title'] == 'Python Django Developer'
        assert data['skills'][0]['skill']['name'] == 'Python'
        assert data['projects'][0]['title'] == 'Test Project'
        assert data['contacts'][0]['value'] == TEST_EMAIL

    def test_create_resume(self, api_client, sample_skill):
        """Test POST /api/resumes/ - Create new resume."""
        url = reverse('cvsai_api:resume-list-create')
        payload = {
            'firstname': 'Sergiy',
            'lastname': 'Rebrov',
            'title': 'Frontend Developer',
            'bio': 'Frontend specialist',
            'skills': [
                {'skill_id': sample_skill.id, 'level': 'expert'}
            ],
            'projects': [
                {
                    'title': 'React App',
                    'description': 'Modern React application',
                    'url': 'https://github.com/rebrov/react-app',
                    'start_date': '2023-06-01'
                }
            ],
            'contacts': [
                {'contact_type': 'email', 'value': 'rebrov@example.com'},
                {'contact_type': 'github', 'value': 'https://github.com/rebrov'}
            ]
        }

        response = api_client.post(
            url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data['firstname'] == 'Sergiy'
        assert data['lastname'] == 'Rebrov'
        assert data['full_name'] == 'Sergiy Rebrov'
        assert len(data['skills']) == 1
        assert data['skills'][0]['skill']['name'] == 'Python'
        assert data['skills'][0]['level'] == 'expert'
        assert len(data['projects']) == 1
        assert data['projects'][0]['title'] == 'React App'
        assert len(data['contacts']) == 2

        # Verify data in database
        resume = Resume.objects.get(id=data['id'])
        assert resume.firstname == 'Sergiy'
        assert resume.resumeskill_set.count() == 1
        assert resume.projects.count() == 1
        assert resume.contacts.count() == 2

    def test_update_resume(self, api_client, sample_resume):
        """Test PUT /api/resumes/{id}/ - Update resume."""
        url = reverse('cvsai_api:resume-detail', kwargs={'pk': sample_resume.pk})
        payload = {
            'firstname': 'John Updated',
            'lastname': 'Wick',
            'title': 'Senior Software Developer',
            'bio': 'Updated bio'
        }

        response = api_client.put(
            url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['firstname'] == 'John Updated'
        assert data['title'] == 'Senior Software Developer'
        assert data['bio'] == 'Updated bio'

        # Verify in database
        sample_resume.refresh_from_db()
        assert sample_resume.firstname == 'John Updated'
        assert sample_resume.title == 'Senior Software Developer'

    def test_partial_update_resume(self, api_client, sample_resume):
        """Test PATCH /api/resumes/{id}/ - Partial update resume."""
        url = reverse('cvsai_api:resume-detail', kwargs={'pk': sample_resume.pk})
        payload = {
            'title': 'Lead Developer'
        }

        response = api_client.patch(
            url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['title'] == 'Lead Developer'
        # Verify in database
        sample_resume.refresh_from_db()
        assert sample_resume.title == 'Lead Developer'


    def test_delete_resume(self, api_client, sample_resume):
        """Test DELETE /api/resumes/{id}/ - Delete resume."""
        url = reverse('cvsai_api:resume-detail', kwargs={'pk': sample_resume.pk})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify deletion in database
        assert not Resume.objects.filter(id=sample_resume.pk).exists()

    def test_resume_not_found(self, api_client):
        """Test 404 for non-existent resume."""
        url = reverse('cvsai_api:resume-detail', kwargs={'pk': 9999})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestSkillAPI:
    """Test cases for Skill API endpoints."""

    def test_list_skills(self, api_client, sample_skill):
        """Test GET /api/skills/ - List all skills."""
        url = reverse('cvsai_api:skill-list-create')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["results"]) >= 1
        assert any(skill['name'] == 'Python' for skill in data["results"])

    def test_create_skill(self, api_client):
        """Test POST /api/skills/ - Create new skill."""
        url = reverse('cvsai_api:skill-list-create')
        payload = {'name': 'JavaScript'}

        response = api_client.post(
            url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data['name'] == 'JavaScript'

        # Verify in database
        assert Skill.objects.filter(name='JavaScript').exists()


@pytest.mark.django_db
class TestAPIValidation:
    """Test API validation and error handling."""

    def test_create_resume_invalid_data(self, api_client):
        """Test creating resume with invalid data."""
        url = reverse('cvsai_api:resume-list-create')
        payload = {
            'firstname': '',  # Empty firstname should be invalid
            'lastname': 'Doe'
        }

        response = api_client.post(
            url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

