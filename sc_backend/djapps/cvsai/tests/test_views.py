from django.test import Client
from django.urls import reverse

import pytest
from cvsai.models import Contact, Project, Resume, ResumeSkill, Skill


@pytest.fixture
def client():
    """Django test client fixture."""
    return Client()


@pytest.fixture
def sample_skill():
    """Create a sample skill for testing."""
    return Skill.objects.create(name="Python")


@pytest.fixture
def sample_resume(sample_skill):
    """Create a sample resume with related data for testing."""
    resume = Resume.objects.create(
        firstname="Oleksandr",
        lastname="Shtalinberg",
        title="Python Django Developer",
        bio="Experienced developer. Skilled in Python and Django.",
    )

    # Add skill to resume
    ResumeSkill.objects.create(
        resume=resume,
        skill=sample_skill,
        level="advanced"
    )

    # Add project
    Project.objects.create(
        resume=resume,
        title="Test Project",
        description="A test project for testing purposes",
        url="https://github.com/shtalinberg/DTEAM-practical-test",
        start_date="2025-01-01"
    )

    # Add contact
    Contact.objects.create(
        resume=resume,
        contact_type="email",
        value="berg.box@test.com"
    )

    return resume


@pytest.fixture
def multiple_resumes():
    """Create multiple resumes for list view testing."""
    resumes = []
    for i in range(3):
        resume = Resume.objects.create(
            firstname=f"Test{i}",
            lastname=f"User{i}",
            title=f"Developer {i}",
            bio=f"Bio for test user {i}"
        )
        resumes.append(resume)
    return resumes


@pytest.mark.django_db
class TestResumeListView:
    """Test cases for resume list view."""

    def test_list_view_empty(self, client):
        """Test list view with no resumes."""
        url = reverse('cvsai:cv_list')
        response = client.get(url)

        assert response.status_code == 200
        assert 'resumes' in response.context
        assert response.context['resumes'].count() == 0

    def test_list_view_with_resumes(self, client, multiple_resumes):
        """Test list view with multiple resumes."""
        url = reverse('cvsai:cv_list')
        response = client.get(url)

        assert response.status_code == 200
        assert 'resumes' in response.context
        assert response.context['resumes'].count() == 3

        # Check if resumes are in response content
        for resume in multiple_resumes:
            assert resume.firstname.encode() in response.content
            assert resume.lastname.encode() in response.content

    def test_list_view_ordering(self, client, multiple_resumes):
        """Test that resumes are ordered by creation date (newest first)."""
        url = reverse('cvsai:cv_list')
        response = client.get(url)

        resumes = response.context['resumes']
        # Should be ordered by -created_at (newest first)
        assert resumes[0].created_at >= resumes[1].created_at >= resumes[2].created_at

    def test_list_view_template_used(self, client):
        """Test that correct template is used."""
        url = reverse('cvsai:cv_list')
        response = client.get(url)

        assert response.status_code == 200
        assert 'cvsai/resume_list.html' in [t.name for t in response.templates]


@pytest.mark.django_db
class TestResumeDetailView:
    """Test cases for resume detail view."""

    def test_detail_view_existing_resume(self, client, sample_resume):
        """Test detail view with existing resume."""
        url = sample_resume.get_absolute_url()
        response = client.get(url)

        assert response.status_code == 200
        assert 'resume' in response.context
        assert response.context['resume'] == sample_resume

        # Check if resume data is in response
        assert sample_resume.firstname.encode() in response.content
        assert sample_resume.lastname.encode() in response.content
        assert sample_resume.title.encode() in response.content
        assert sample_resume.bio.encode() in response.content

    def test_detail_view_nonexistent_resume(self, client):
        """Test detail view with non-existent resume returns 404."""
        url = reverse('cvsai:cv_detail', kwargs={'pk': 9999})
        response = client.get(url)

        assert response.status_code == 404

    def test_detail_view_includes_skills(self, client, sample_resume):
        """Test that detail view includes resume skills."""
        url = reverse('cvsai:cv_detail', kwargs={'pk': sample_resume.pk})
        response = client.get(url)

        assert response.status_code == 200
        resume = response.context['resume']

        # Check that skills are accessible
        skills = resume.skills.all()
        assert skills.count() == 1
        assert skills[0].name == "Python"

    def test_detail_view_includes_projects(self, client, sample_resume):
        """Test that detail view includes resume projects."""
        url = sample_resume.get_absolute_url()
        response = client.get(url)

        assert response.status_code == 200
        resume = response.context['resume']

        # Check that projects are accessible
        projects = resume.projects.all()
        assert projects.count() == 1
        assert projects[0].title == "Test Project"

    def test_detail_view_includes_contacts(self, client, sample_resume):
        """Test that detail view includes resume contacts."""
        url = sample_resume.get_absolute_url()
        response = client.get(url)

        assert response.status_code == 200
        resume = response.context['resume']

        # Check that contacts are accessible
        contacts = resume.contacts.all()
        assert contacts.count() == 1
        assert contacts[0].value == "berg.box@test.com"

    def test_detail_view_template_used(self, client, sample_resume):
        """Test that correct template is used."""
        url = sample_resume.get_absolute_url()
        response = client.get(url)

        assert response.status_code == 200
        assert 'cvsai/resume_detail.html' in [t.name for t in response.templates]

