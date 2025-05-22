from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cvsai.constants import CONTACT_TYPES, SKILL_LEVELS, SL_INTERMEDIATE


class Skill(models.Model):
    """Model representing a skill."""

    name = models.CharField(
        verbose_name=_("name"), max_length=100, unique=True, help_text=_("Skill name")
    )

    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")
        ordering = ['name']

    def __str__(self):
        return self.name


class Resume(models.Model):
    """Model representing a Resume/CV."""

    firstname = models.CharField(
        verbose_name=_("First name"),
        max_length=120,
        help_text=_("First name of the person"),
    )
    lastname = models.CharField(
        verbose_name=_("Last name"),
        max_length=120,
        help_text=_("Last name of the person"),
    )
    title = models.CharField(
        verbose_name=_("Job Title"),
        max_length=300,
        help_text=_("Professional title or position"),
        blank=True,
    )
    bio = models.TextField(
        verbose_name=_("Biography"), help_text=_("Professional biography or summary")
    )
    skills = models.ManyToManyField(
        'Skill',
        verbose_name=_("Skills"),
        through='ResumeSkill',
        blank=True,
        help_text=_("Skills with proficiency levels"),
    )

    created_at = models.DateTimeField(verbose_name=_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated"), auto_now=True)

    class Meta:
        verbose_name = _("Resume")
        verbose_name_plural = _("Resumes")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    @property
    def full_name(self):
        """Return full name."""
        return f"{self.firstname} {self.lastname}"

    def get_absolute_url(self):
        """Return the URL for the resume instance."""
        return reverse('cvsai:cv_detail', args=[str(self.id)])

    def get_download_pdf_url(self):
        """Return the URL for downloading the resume as a PDF."""
        return reverse('cvsai:cv_download_pdf', args=[str(self.id)])


class ResumeSkill(models.Model):
    """Through model for Resume-Skill relationship with level."""

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.CharField(
        verbose_name=_("Skill Level"),
        max_length=20,
        choices=SKILL_LEVELS,
        default=SL_INTERMEDIATE,
    )

    class Meta:
        verbose_name = _("Resume Skill")
        verbose_name_plural = _("Resume Skills")
        unique_together = ['resume', 'skill']
        ordering = ['skill__name']

    def __str__(self):
        return f"{self.resume.full_name} - {self.skill.name} ({self.level})"


class Project(models.Model):
    """Model representing a project."""

    resume = models.ForeignKey(
        Resume,
        verbose_name=_("Resume"),
        on_delete=models.CASCADE,
        related_name='projects',
    )
    title = models.CharField(
        verbose_name=_("Title"), max_length=200, help_text=_("Project title")
    )
    description = models.TextField(
        verbose_name=_("Description"), help_text=_("Project description")
    )
    url = models.URLField(
        verbose_name=_("Project URL"), blank=True, help_text=_("Project URL (optional)")
    )
    start_date = models.DateField(verbose_name=_("Start date"), null=True, blank=True)
    end_date = models.DateField(
        verbose_name=_("End date"),
        null=True,
        blank=True,
        help_text=_("Leave empty if project is ongoing"),
    )

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        """Check if project is ongoing."""
        return self.end_date is None


class Contact(models.Model):
    """Model representing contact information."""

    resume = models.ForeignKey(
        Resume,
        verbose_name=_("Resume"),
        on_delete=models.CASCADE,
        related_name='contacts',
    )
    contact_type = models.CharField(
        verbose_name=_("Contact Type"), max_length=20, choices=CONTACT_TYPES
    )
    value = models.CharField(
        verbose_name=_("Contact Value"),
        max_length=200,
        help_text=("Contact value (email, phone number, URL, etc.)"),
    )

    class Meta:
        unique_together = ['resume', 'contact_type', 'value']
        ordering = ['resume', 'contact_type']

    def __str__(self):
        return f"{self.get_contact_type_display()}: {self.value}"
