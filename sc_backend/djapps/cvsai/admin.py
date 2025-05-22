from django.contrib import admin

from cvsai.models import Contact, Resume, ResumeSkill, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Admin view for the Skill model."""
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('name',)
    list_per_page = 20
    list_display_links = ('name',)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    """Admin view for the Resume model."""
    list_display = ('firstname', 'lastname', 'created_at')
    search_fields = ('firstname', 'lastname')
    ordering = ('-created_at',)
    list_filter = ('created_at',)
    list_per_page = 20
    list_display_links = ('firstname', 'lastname')
    raw_id_fields = ('skills',)
    autocomplete_fields = ('skills',)

@admin.register(ResumeSkill)
class ResumeSkillAdmin(admin.ModelAdmin):
    """Admin view for the ResumeSkill model."""
    list_display = ('resume', 'skill', 'level')
    search_fields = ('resume__firstname', 'resume__lastname', 'skill__name')
    ordering = ('resume',)
    list_filter = ('resume', 'skill')
    list_per_page = 20
    list_display_links = ('resume', 'skill')
    raw_id_fields = ('resume', 'skill')
    autocomplete_fields = ('resume', 'skill')
    list_editable = ('level',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin view for the Contact model."""
    list_display = ('contact_type', 'value', 'resume')
    search_fields = ('contact_type', 'value', 'resume__firstname', 'resume__lastname')
    ordering = ('resume',)
    list_filter = ('contact_type', 'resume')
    list_per_page = 20
    list_display_links = ('contact_type', 'value')
    raw_id_fields = ('resume',)
    autocomplete_fields = ('resume',)

