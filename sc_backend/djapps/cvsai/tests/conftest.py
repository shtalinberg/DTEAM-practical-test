
import pytest
from cvsai.models import Contact, Project, Resume, ResumeSkill, Skill


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
