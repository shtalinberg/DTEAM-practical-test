from cvsai.models import Contact, Project, Resume, ResumeSkill, Skill
from rest_framework import serializers


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for Skill model."""

    class Meta:
        model = Skill
        fields = ['id', 'name']


class ResumeSkillSerializer(serializers.ModelSerializer):
    """Serializer for ResumeSkill model."""

    skill = SkillSerializer(read_only=True)
    skill_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ResumeSkill
        fields = ['id', 'skill', 'skill_id', 'level']


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model."""

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'url',
            'start_date',
            'end_date',
            'is_ongoing',
        ]
        read_only_fields = ['is_ongoing']


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact model."""

    class Meta:
        model = Contact
        fields = ['id', 'contact_type', 'value']


class ResumeSerializer(serializers.ModelSerializer):
    """Serializer for Resume model."""

    skills = ResumeSkillSerializer(source='resumeskill_set', many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Resume
        fields = [
            'id',
            'firstname',
            'lastname',
            'title',
            'bio',
            'full_name',
            'skills',
            'projects',
            'contacts',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class ResumeCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating Resume ."""

    skills = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )
    projects = ProjectSerializer(many=True, required=False)
    contacts = ContactSerializer(many=True, required=False)

    class Meta:
        model = Resume
        fields = [
            'id',
            'firstname',
            'lastname',
            'title',
            'bio',
            'skills',
            'projects',
            'contacts',
        ]

    def create(self, validated_data):
        """Create resume with nested relationships."""
        skills_data = validated_data.pop('skills', [])
        projects_data = validated_data.pop('projects', [])
        contacts_data = validated_data.pop('contacts', [])

        # Create resume
        resume = Resume.objects.create(**validated_data)

        # Create skills
        self._create_skills(resume, skills_data)

        # Create projects
        self._create_projects(resume, projects_data)

        # Create contacts
        self._create_contacts(resume, contacts_data)

        return resume

    def update(self, instance, validated_data):
        """Update resume with nested relationships."""
        skills_data = validated_data.pop('skills', None)
        projects_data = validated_data.pop('projects', None)
        contacts_data = validated_data.pop('contacts', None)

        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update skills if provided
        if skills_data is not None:
            instance.resumeskill_set.all().delete()
            self._create_skills(instance, skills_data)

        # Update projects if provided
        if projects_data is not None:
            instance.projects.all().delete()
            self._create_projects(instance, projects_data)

        # Update contacts if provided
        if contacts_data is not None:
            instance.contacts.all().delete()
            self._create_contacts(instance, contacts_data)

        return instance

    def _create_skills(self, resume, skills_data):
        """Helper method to create skills."""
        for skill_data in skills_data:
            skill_id = skill_data.get('skill_id')
            level = skill_data.get('level', 'intermediate')

            if skill_id:
                try:
                    skill = Skill.objects.get(id=skill_id)
                    ResumeSkill.objects.create(resume=resume, skill=skill, level=level)
                except Skill.DoesNotExist:
                    continue

    def _create_projects(self, resume, projects_data):
        """Helper method to create projects."""
        for project_data in projects_data:
            Project.objects.create(resume=resume, **project_data)

    def _create_contacts(self, resume, contacts_data):
        """Helper method to create contacts."""
        for contact_data in contacts_data:
            Contact.objects.create(resume=resume, **contact_data)

    def to_representation(self, instance):
        """Return full representation after create/update."""
        return ResumeSerializer(instance).data
